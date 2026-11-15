# For an agent: load everything into Unreal Engine 5

**One step:** run `ue_import.py` inside the UE5 editor of the target project (Python Editor Script Plugin enabled):

```
UnrealEditor-Cmd.exe "<Project>.uproject" -run=pythonscript -script="<abs path>/UE_Export/ue_import.py"
```

You can also run it from the editor (Output Log → Python) with `py "<abs path>/UE_Export/ue_import.py"`.
It reads `import_manifest.json` from its own folder. Don't move the FBX files relative to it.

## What it does

1. **Meshes:** imports the 16 skeletal meshes, each creating its own skeleton.
   - The 4 `SK_Spear_<warrior>` meshes and `SK_BeerCan_Driver` are imported onto their owner's skeleton.
   - It also imports 2 static meshes, `SM_Spear` and `SM_BeerCan`.
2. **Animations:** imports 178 animations, each onto its asset's skeleton.
   - 30 fps for riders and camels, 24 fps for cars and the driver; length set to Exported Time.
   - Root motion off.
3. **Metadata:** tags every AnimSequence with metadata: `MegaJam.Clip`, `MegaJam.Loop`, `MegaJam.Fps`, `MegaJam.Frames`,
   `MegaJam.Events` (JSON, 1-based frames), `MegaJam.SyncGroup`, `MegaJam.Direction`, `MegaJam.Set`.
4. **Report:** writes `import_report.json` next to the script. Check `summary.errors == 0`.
   - `animations[*].ue_num_frames` / `ue_length_s` let you confirm the lengths against `expected_frames`.
   - Length in seconds = (frames − 1) / fps.

**Safe to re-run:** existing assets are skipped. Set the env var `MEGAJAM_FORCE=1` to re-import, or `MEGAJAM_ONLY=car,rider,camel,driver`
to limit groups. `MEGAJAM_ROOT=/Game/Somewhere` changes the target folder (default `/Game/MegaJam`).

## Content layout after import

```
/Game/MegaJam/Cars/<Car_Final|Car_Base|Car_High>/SK_*, Animations/A_<car>_<clip>
/Game/MegaJam/Riders/<warrior>/SK_<warrior>, SK_Spear_<warrior>, Animations/A_<warrior>_<clip>
/Game/MegaJam/Riders/Props/SM_Spear
/Game/MegaJam/Camels/<Camel_Low|Camel_Mid|Camel_High>/SK_*, Animations/A_<camel>_Run
/Game/MegaJam/Driver/SK_Driver, SK_BeerCan_Driver, Props/SM_BeerCan, Animations/A_Driver_<clip>
```

## Facts you need for setup (all also in `import_manifest.json` → `conventions`)

- **Car facing:** cars face +Y in mesh space and **always drive backwards**. Rotate the car mesh component **Yaw 90** so
  the tail points along the actor's +X; verify against the arrow.
- **Car L/R:** car `_L` / `_R` = the direction the car's path bends, seen in the direction of travel.
- **Car sockets:** cars have bones `Driver_Socket` and `Passenger_Socket` to attach characters to.
- **Driver:** attach `SK_Driver` to `Car_Final`'s `Driver_Socket` at **relative scale 0.6**. Play `Idle_*` with `Car_Idle` and
  `Drive_*`, throws and taunts with `Car_Drive`; all loops are 48 frames @24fps.
  - Every driver one-shot starts and ends on frame 1 of `Drive_A`; blend in and out of that loop.
  - The clips are authored in `Car_Final`. In the other cars move the driver on the socket (car mesh units, X toward his window, Y toward the
    tail, Z up; flip Y for Unreal): `Car_Base` (+0.012, +0.012, −0.027), `Car_High` (0, +0.012, −0.045).
  - The beer can: `SK_BeerCan_Driver` with Leader Pose = the driver mesh. Show it from the `can_show` event (frame 4)
    of a throw; at the `release` event hide it and spawn `SM_BeerCan`.
  - Release frames: `Throw_Window_A` 12, `Throw_Window_B` 14, `Throw_Roof_A` 15, `Throw_Roof_B` 17.
  - `Throw_Window_*` go to screen right; `Throw_Roof_*` go over the roof to screen left.
  - Sound-hook events (frame lists): `door_slap` (Drive_A), `door_bang` (Taunt_A, Taunt_C), `roof_slap`, `head_clonk`,
    `lands`.
- **Car blend space:** car `Drive`, `Turn_L/R`, `Turn_L/R_Max` share length, wheel spin and road bumps. Use them as a 1D
  steering blend space (sync group `Steer`).
- **Rider directions:** rider `_B` / `_L` / `_R` = where the player is relative to the rider (behind / left / right).
  For `Damage_*` / `Death_*` it is where the hit comes from.
- **Rider sets:** rider clips come in two sets: unarmed and `Spear_*`. `Damage_*` / `Death_*` are shared.
- **Spear:** add `SK_Spear_<warrior>` as a second SkeletalMeshComponent.
  - Set its **Leader Pose Component** to the warrior mesh so it follows `hand_r`.
  - Hide it for unarmed riders.
  - For `Spear_Throw_*`, hide it at the `release` event (frame 13) and spawn `SM_Spear` as the projectile from the
    spear's transform. `SM_Spear`'s shaft runs along its local Z; the origin is the grip.
- **Event frames** (1-based, in the manifest and the metadata):
  - Throws: `release` 13.
  - Rider deaths: `lands_on_road` 31; detach with KeepWorld at frame 1 or hide after landing.
  - Rider damage: `hit` 3.
  - Car Ram*: `impact` 9.
  - Car Death_Flip: `roof_lands` 28.
- **Attaching riders:**
  - Riders attach to the camel bone `ORG-Sitting_Root` at **relative scale 1.5**.
  - That bone points up, so create a Skeleton Socket on it with a **90° rotation** so the rider sits upright facing the
    camel's head. Verify with a Preview Asset.
  - Optional socket yaw: Camel_Low −6.7°, Camel_Mid −4.8°, Camel_High −1.8°.
- **Sync:** rider `Ride*` loops and camel `Run` loops are all 18 frames @30fps (sync group `CamelStride`). Start
  them together.
- **Looping:** in every loop the last key repeats the first. Loop on the full length; don't trim.

Human-readable details: `Cars/README_Cars_UE5.md`, `Riders/README_Riders_UE5.md`, `Driver/README_Driver_UE5.md`.
**Testing:** all FBX contents were checked by re-importing them in Blender. This script was dry-run against a mock
`unreal` module, **not yet run in a real UE editor**, so read `import_report.json` warnings on the first run.
