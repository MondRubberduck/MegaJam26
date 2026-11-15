# For an agent: load everything into Unreal Engine 5

**One step:** run `ue_import.py` inside the UE5 editor of the target project (Python Editor Script Plugin enabled):

```
UnrealEditor-Cmd.exe "<Project>.uproject" -run=pythonscript -script="<abs path>/UE_Export/ue_import.py"
```

You can also run it from the editor (Output Log → Python) with `py "<abs path>/UE_Export/ue_import.py"`.
It reads `import_manifest.json` from its own folder. Don't move the FBX files relative to it.

## What it does

1. **Meshes:** imports the 23 skeletal meshes, each creating its own skeleton.
   - The 4 `SK_Spear_<warrior>` meshes, `SK_BeerCan_Driver`, `SK_Can_Passenger` and the guards' `SK_Wood_Guard2` / `SK_Wood_Guard1` are imported onto their owner's skeleton.
   - It also imports 4 static meshes, `SM_Spear`, `SM_BeerCan`, `SM_Can_Passenger` and `SM_Wood`.
2. **Animations:** imports 210 animations, each onto its asset's skeleton.
   - 30 fps for riders, camels, the passenger, the pharaoh and the guards; 24 fps for cars and the driver. Length set to Exported Time.
   - Root motion off.
   - **Units (new on 15 Nov):** the passenger, the pharaoh and the guards are **centimetre** FBX files:
     UnitScaleFactor 1, so there is **no factor 100 on the root bone**. Their manifest entries carry `"units": "cm"`.
     Cars, riders, camels and the driver are still the older metre files, unchanged. Import everything at uniform scale 1.0.
3. **Metadata:** tags every AnimSequence with metadata: `MegaJam.Clip`, `MegaJam.Loop`, `MegaJam.Fps`, `MegaJam.Frames`,
   `MegaJam.Events` (JSON, 1-based frames), `MegaJam.SyncGroup`, `MegaJam.Direction`, `MegaJam.Set`.
4. **Report:** writes `import_report.json` next to the script. Check `summary.errors == 0`.
   - `animations[*].ue_num_frames` / `ue_length_s` let you confirm the lengths against `expected_frames`.
   - Length in seconds = (frames − 1) / fps.

**Safe to re-run:** existing assets are skipped. Set the env var `MEGAJAM_FORCE=1` to re-import, or `MEGAJAM_ONLY=car,rider,camel,driver`
to limit groups (the new groups are `passenger`, `pharaoh` and `guards`, e.g. `MEGAJAM_ONLY=passenger,pharaoh,guards`). `MEGAJAM_ROOT=/Game/Somewhere` changes the target folder (default `/Game/MegaJam`).

## Content layout after import

```
/Game/MegaJam/Cars/<Car_Final|Car_Base|Car_High>/SK_*, Animations/A_<car>_<clip>
/Game/MegaJam/Riders/<warrior>/SK_<warrior>, SK_Spear_<warrior>, Animations/A_<warrior>_<clip>
/Game/MegaJam/Riders/Props/SM_Spear
/Game/MegaJam/Camels/<Camel_Low|Camel_Mid|Camel_High>/SK_*, Animations/A_<camel>_Run
/Game/MegaJam/Driver/SK_Driver, SK_BeerCan_Driver, Props/SM_BeerCan, Animations/A_Driver_<clip>
/Game/MegaJam/Passenger/SK_Passenger, SK_Can_Passenger, Props/SM_Can_Passenger, Animations/A_Passenger_<clip>
/Game/MegaJam/Pharaoh/SK_Pharaoh, Animations/A_Pharaoh_<clip>
/Game/MegaJam/Guards/SK_Guard2, SK_Guard1, SK_Wood_Guard2, SK_Wood_Guard1, Props/SM_Wood, Animations/A_Guard2_<clip>, A_Guard1_<clip>
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
- **Passenger** (13 clips, 30 fps, cm; `female_warrior` mesh on its own skeleton, replaces the stand-in on rider clips). The root bone stays at identity in every clip.
  - **On the camel** (`Captive_Idle`, `Captive_Distress`, `Captive_Beg`, `Captive_Beg_L`, `Captive_Beg_R`, all 55-frame loops = 3 camel strides; and `Jump_Start`):
    attach to the camel bone `ORG-Sitting_Root` at **relative scale 1.5**, the same socket and yaw as the riders. She lies slung across the camel's back behind the
    rider, head on screen left. Per-camel Z offset (cm, camel at scale 1): High 0, Mid +1.5, Low −1.5. `_L` / `_R` = she begs toward the player on screen left / right.
  - **In the car** (`Seat_Idle` 61-frame loop, `Seat_Throw_L`, `Seat_Throw_R`, `Seat_Flinch`, `Seat_Cheer`, and `Jump_Land`): attach to `Car_Final`'s
    `Passenger_Socket` at **relative scale 0.6**, the same as the driver. She faces the hood and leans out of her window on screen left. Every car one-shot starts
    and ends on `Seat_Idle` frame 1. Authored in `Car_Final` only; no seat offsets measured for `Car_Base` / `Car_High` yet.
  - **The jump:** `Jump_Start` on the camel (`cuffs_snap` 20, `leave_camel` 35) → detach and fly her while `Jump_Air` plays (21 f, in place; yaw = the car's yaw;
    blend her scale from 1.5 × camel scale to 0.6 × car scale) → attach to `Passenger_Socket` and play `Jump_Land` (`in_seat` 11) → `Seat_Idle`. The clips join
    pose for pose; crossfade 2–3 frames at each switch. Exact flight start and end points: `Passenger/README_Passenger_UE5.md`.
  - **Throws** (right hand): show `SK_Can_Passenger` (Leader Pose = her mesh) from `can_show` 5 to `release` (`Seat_Throw_L` 15, `Seat_Throw_R` 18), then spawn
    `SM_Can_Passenger`. `Seat_Throw_L` goes out of her window to screen left, `Seat_Throw_R` over the roof to screen right. `Seat_Flinch`: `hit` 1.
- **Pharaoh** (7 clips, 30 fps, cm):
  - Give `SK_Pharaoh` the throne actor's location, rotation and the **same scale**: throne and pharaoh are both authored 1:1 at 1 m.
    The root is at the throne pivot; he faces mesh +Y like the mannequin, so turn the actor to face the player.
  - Base pose = `Sit_Idle` frame 1 (151-frame loop). Every one-shot starts on it; `Cast_End`, `Taunt_Flex` and `Flinch` also end on it.
  - `Cast` (32 f) then `Cast_End` (16 f): spawn the spell at `spell_peak` = frame 32, the last frame of `Cast`.
  - `Flinch` (44 f) doubles as his hit reaction. `Taunt_Flex` (114 f): he stands up, flexes and sits back down.
  - `Death_R` / `Death_L` (61 f): he is blasted off and cartwheels to screen right / screen left. The flight is **on the root bone**:
    keep root motion off, raise the mesh's Bounds Scale so he is not culled, and hide or despawn him at the end (he is still falling, about 3.6 m below the throne).
- **Guards** (`Guard2` = royal_guard_2, the main one; `Guard1` = royal_guard_1, a bonus): 6 clips each, 30 fps, cm, **each mesh has its own skeleton**.
  - Root on the chariot deck between the feet; face the player. Proposed scale: the pharaoh/throne actor scale ×1.25, so they tower over
    the seated pharaoh (`Guards/Guards_lineup.png`). That scale is still to be confirmed by Nils.
  - `Idle` 61-frame loop = base pose; `Taunt_Roar`, `Taunt_Beat`, `Throw` and `Hit` start and end on its frame 1.
  - `Throw` (**new on 15 Nov, 78 f**; already imported? re-import with `MEGAJAM_ONLY=guards MEGAJAM_FORCE=1`): a two-handed overhead heave of a **big log**.
    - Per guard: `SK_Wood_<Guard>` as a second Skeletal Mesh Component with **Leader Pose = the guard mesh** and **Use Bounds From Leader Pose Component = true**, hidden by default.
      Add a skeleton socket **`Wood` on `hand_r`** (exact values per guard in `Guards/README_Guards_UE5.md`, "Throw: the log").
    - Montage start: show an `SM_Wood` on the deck (deck transform in the guards README). `grab` 9: hide it and show `SK_Wood_<Guard>`.
    - `release` 58: hide `SK_Wood_<Guard>` and spawn `SM_Wood` at `GetSocketTransform("Wood", RTS_World)`, read when the notify fires. It leaves rising toward the player;
      launch velocity and spin are in the guards README (multiply the velocity by the actor scale). Also `stomp` 57; blend out from about frame 70.
  - `Taunt_Roar`: `stomp` 9, `loudest_pose` 16. `Taunt_Beat`: `hits` 14/34/46, `deck_smash` 62. `Hit`: `impact` 1.
  - `Fall_Off` (64 f): blasted off backwards, **4.4 m of travel on the root bone**, ends lying face-down at deck height (`still` from 49); no return to Idle.

Human-readable details: `Cars/README_Cars_UE5.md`, `Riders/README_Riders_UE5.md`, `Driver/README_Driver_UE5.md`,
`Passenger/README_Passenger_UE5.md`, `Pharaoh/README_Pharaoh_UE5.md`, `Guards/README_Guards_UE5.md`.
**Testing:** all FBX contents were checked by re-importing them in Blender. This script was dry-run against a mock
`unreal` module, **not yet run in a real UE editor**, so read `import_report.json` warnings on the first run.
