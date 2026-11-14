# UE5 export: overview

| Folder | What | Notes |
|---|---|---|
| `Cars/` | 3 cars, 22 in-place clips each (24 fps) | `Cars/README_Cars_UE5.md` |
| `Riders/` | 4 camel-rider warriors, 24 clips each (directions + spear set, 30 fps), spears | `Riders/README_Riders_UE5.md` |
| `Camels/` | 3 camels, 18-frame gallop loop (30 fps) | The rider README covers the `ORG-Sitting_Root` socket |

**Files:** one skeletal mesh per asset (`SK_*.fbx`, textures embedded) and one FBX per animation (`A_*.fbx`).
In UE, import the mesh first, then select all of its `A_*` files and pick that mesh's skeleton.

**Animation:** no clip uses root motion; the game moves everything.

**Automatic import:** an agent (or you) can load everything in one go with `ue_import.py` + `import_manifest.json`.
See `AGENT_README.md`.
