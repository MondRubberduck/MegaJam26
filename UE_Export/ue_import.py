"""
MegaJam UE5 importer - imports every mesh and animation listed in import_manifest.json (same folder as this file).

Run inside Unreal Editor 5.x with the "Python Editor Script Plugin" enabled:
  * Editor menu:   Tools > Execute Python Script...  -> pick this file
  * Output Log:    py "C:/path/to/UE_Export/ue_import.py"
  * Headless:      UnrealEditor-Cmd.exe "<Project>.uproject" -run=pythonscript -script="C:/path/to/UE_Export/ue_import.py"

Optional environment variables (set before launching the editor/commandlet):
  MEGAJAM_ROOT   content folder to import into (default from the manifest: /Game/MegaJam)
  MEGAJAM_ONLY   comma list of groups to import: car,rider,camel   (meshes of those groups + their animations)
  MEGAJAM_FORCE  "1" = re-import assets that already exist (default: skip existing, so re-running is safe)

Order: skeletal meshes (each creates its skeleton) -> meshes that share a skeleton (spears) -> static meshes -> animations.
Writes import_report.json next to this file (what was created, skipped, failed, frame counts, warnings).
Every animation gets asset metadata tags: MegaJam.Clip, MegaJam.Loop, MegaJam.Fps, MegaJam.Frames, MegaJam.Events (JSON,
1-based frames), MegaJam.SyncGroup, MegaJam.Direction, MegaJam.Set.
"""
import os, json, traceback
import unreal

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = json.load(open(os.path.join(HERE, "import_manifest.json"), encoding="utf-8"))
ROOT_OVERRIDE = os.environ.get("MEGAJAM_ROOT", "").rstrip("/")
ONLY = {g.strip() for g in os.environ.get("MEGAJAM_ONLY", "").split(",") if g.strip()}
FORCE = os.environ.get("MEGAJAM_FORCE", "") == "1"

TOOLS = unreal.AssetToolsHelpers.get_asset_tools()
EAL = unreal.EditorAssetLibrary
report = {"root": ROOT_OVERRIDE or MAN["unreal_root"], "assets": {}, "animations": {}, "skipped": [], "errors": [], "warnings": []}


def log(msg): unreal.log("[MegaJam] " + msg)
def dest_of(path): return path.replace(MAN["unreal_root"], ROOT_OVERRIDE, 1) if ROOT_OVERRIDE else path
def group_of_asset(a):
    if a["kind"] == "static_mesh" or a["dest"].split("/")[3:4] == ["Riders"]: return "rider"
    return {"Cars": "car", "Camels": "camel"}.get(a["dest"].split("/")[3], "other")
def wanted(group): return not ONLY or group in ONLY


def setp(obj, name, value, quiet=False):
    try:
        obj.set_editor_property(name, value); return True
    except Exception as e:
        if not quiet: report["warnings"].append("%s.%s: %s" % (type(obj).__name__, name, e))
        return False


def make_task(fbx_rel, dest, name, ui):
    t = unreal.AssetImportTask()
    t.set_editor_property("filename", os.path.join(HERE, fbx_rel).replace("\\", "/"))
    t.set_editor_property("destination_path", dest)
    t.set_editor_property("destination_name", name)
    t.set_editor_property("automated", True)
    t.set_editor_property("replace_existing", True)
    t.set_editor_property("save", True)
    t.set_editor_property("options", ui)
    return t


def common_data(d):
    setp(d, "import_uniform_scale", 1.0)
    setp(d, "convert_scene", True)
    setp(d, "force_front_x_axis", False)


def skeletal_ui(skeleton=None):
    ui = unreal.FbxImportUI()
    setp(ui, "automated_import_should_detect_type", False, quiet=True)
    setp(ui, "import_mesh", True); setp(ui, "import_as_skeletal", True); setp(ui, "import_animations", False)
    setp(ui, "import_materials", True); setp(ui, "import_textures", True); setp(ui, "create_physics_asset", False)
    setp(ui, "mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
    if skeleton is not None: setp(ui, "skeleton", skeleton)
    d = ui.get_editor_property("skeletal_mesh_import_data")
    common_data(d)
    setp(d, "import_morph_targets", False, quiet=True)
    setp(d, "normal_import_method", unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS, quiet=True)
    return ui


def static_ui():
    ui = unreal.FbxImportUI()
    setp(ui, "automated_import_should_detect_type", False, quiet=True)
    setp(ui, "import_mesh", True); setp(ui, "import_as_skeletal", False); setp(ui, "import_animations", False)
    setp(ui, "import_materials", True); setp(ui, "import_textures", True)
    setp(ui, "mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)
    d = ui.get_editor_property("static_mesh_import_data")
    common_data(d)
    setp(d, "combine_meshes", True, quiet=True)
    return ui


def anim_ui(skeleton, fps):
    ui = unreal.FbxImportUI()
    setp(ui, "automated_import_should_detect_type", False, quiet=True)
    setp(ui, "import_mesh", False); setp(ui, "import_as_skeletal", True); setp(ui, "import_animations", True)
    setp(ui, "import_materials", False); setp(ui, "import_textures", False)
    setp(ui, "mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    setp(ui, "skeleton", skeleton)
    d = ui.get_editor_property("anim_sequence_import_data")
    common_data(d)
    setp(d, "animation_length", unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    setp(d, "import_bone_tracks", True, quiet=True)
    setp(d, "remove_redundant_keys", False, quiet=True)
    setp(d, "use_default_sample_rate", False, quiet=True)
    setp(d, "custom_sample_rate", int(fps), quiet=True)
    setp(d, "snap_to_closest_frame_boundary", True, quiet=True)
    return ui


def run(task):
    TOOLS.import_asset_tasks([task])
    return [str(p) for p in (task.get_editor_property("imported_object_paths") or [])]


def load_of_class(paths, cls):
    for p in paths:
        a = unreal.load_asset(p)
        if a is not None and isinstance(a, cls): return a
    return None


# ------------------------------------------------------------------ meshes
skeletons = {}          # asset id -> USkeleton
order = sorted(MAN["assets"], key=lambda a: (a["kind"] != "skeletal_mesh", a.get("skeleton_of") is not None))
for a in order:
    if not wanted(group_of_asset(a)): continue
    dest = dest_of(a["dest"]); name = a["asset_name"]; path = dest + "/" + name
    try:
        if EAL.does_asset_exist(path) and not FORCE:
            report["skipped"].append(path)
            if a["kind"] == "skeletal_mesh":
                skeletons[a["id"]] = unreal.load_asset(path).get_editor_property("skeleton")
            continue
        if a["kind"] == "static_mesh":
            paths = run(make_task(a["fbx"], dest, name, static_ui()))
            report["assets"][a["id"]] = {"path": path, "imported": paths}
            continue
        skel = skeletons.get(a["skeleton_of"]) if a.get("skeleton_of") else None
        if a.get("skeleton_of") and skel is None:
            raise RuntimeError("skeleton of '%s' not available (import it first)" % a["skeleton_of"])
        paths = run(make_task(a["fbx"], dest, name, skeletal_ui(skel)))
        mesh = load_of_class(paths, unreal.SkeletalMesh) or unreal.load_asset(path)
        if mesh is None: raise RuntimeError("no SkeletalMesh created from " + a["fbx"])
        skeletons[a["id"]] = mesh.get_editor_property("skeleton")
        report["assets"][a["id"]] = {"path": mesh.get_path_name(), "skeleton": skeletons[a["id"]].get_path_name(), "imported": paths}
        log("mesh %s -> %s" % (a["fbx"], path))
    except Exception as e:
        report["errors"].append({"fbx": a["fbx"], "error": str(e), "trace": traceback.format_exc(limit=2)})

# ------------------------------------------------------------------ animations
for x in MAN["animations"]:
    if not wanted(x["group"]): continue
    dest = dest_of(x["dest"]); name = x["asset_name"]; path = dest + "/" + name
    try:
        if EAL.does_asset_exist(path) and not FORCE:
            report["skipped"].append(path); continue
        skel = skeletons.get(x["skeleton_of"])
        if skel is None: raise RuntimeError("skeleton of '%s' missing - its mesh failed or was filtered out" % x["skeleton_of"])
        paths = run(make_task(x["fbx"], dest, name, anim_ui(skel, x["fps"])))
        anim = load_of_class(paths, unreal.AnimSequence) or unreal.load_asset(path)
        if anim is None: raise RuntimeError("no AnimSequence created from " + x["fbx"])
        setp(anim, "enable_root_motion", False, quiet=True)
        setp(anim, "force_root_lock", False, quiet=True)
        for tag, val in (("MegaJam.Clip", x["clip"]), ("MegaJam.Loop", str(bool(x.get("loop"))).lower()), ("MegaJam.Fps", str(x["fps"])),
                         ("MegaJam.Frames", str(x.get("frames", ""))), ("MegaJam.Events", json.dumps(x.get("events", {}))),
                         ("MegaJam.SyncGroup", x.get("sync_group", "")), ("MegaJam.Direction", x.get("direction", "")), ("MegaJam.Set", x.get("set", ""))):
            try: EAL.set_metadata_tag(anim, tag, val)
            except Exception as e: report["warnings"].append("metadata %s: %s" % (tag, e))
        EAL.save_loaded_asset(anim)
        info = {"path": anim.get_path_name(), "expected_frames": x.get("frames")}
        try: info["ue_num_frames"] = unreal.AnimationLibrary.get_num_frames(anim)
        except Exception: pass
        try: info["ue_length_s"] = round(anim.get_editor_property("sequence_length"), 4)
        except Exception:
            try: info["ue_length_s"] = round(unreal.AnimationLibrary.get_sequence_length(anim), 4)
            except Exception: pass
        report["animations"][name] = info
    except Exception as e:
        report["errors"].append({"fbx": x["fbx"], "error": str(e), "trace": traceback.format_exc(limit=2)})

try: EAL.save_directory(report["root"], only_if_is_dirty=True, recursive=True)
except Exception as e: report["warnings"].append("save_directory: %s" % e)
report["summary"] = {"meshes": len(report["assets"]), "animations": len(report["animations"]), "skipped": len(report["skipped"]),
                     "errors": len(report["errors"]), "warnings": len(report["warnings"])}
with open(os.path.join(HERE, "import_report.json"), "w", encoding="utf-8") as f: json.dump(report, f, indent=1)
log("done: %s  (report: import_report.json)" % report["summary"])
