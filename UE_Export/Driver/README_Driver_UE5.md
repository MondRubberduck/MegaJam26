# Driver → Unreal Engine 5

The driver for `Car_Final`: 13 clips (24 fps, same as the cars), a beer can for his hand, and a static can for the
projectile. **Automatic import:** `../ue_import.py` (see `../AGENT_README.md`).

- **Source file:** `Worked_Models/Car_Driver_Anims_v4.blend`
- **Format:** unchanged from the 00:50 delivery on 15 Nov (metres, 24 fps, same file and bone names), so the same re-import works.
- **Preview:** `Worked_Models/Previews/Car_Driver_preview.mp4`

```
Driver/SK_Driver.fbx              UE5-mannequin skeleton (same bone names as the warriors), 1 m tall
Driver/SK_BeerCan_Driver.fbx      can skinned to hand_l (use with Leader Pose)
Driver/Props/SM_BeerCan.fbx       static can for the thrown projectile
Driver/Animations/A_Driver_*.fbx  the clips below
```

## Attaching

- **Socket:** attach the driver to the car bone **`Driver_Socket`** at **relative scale 0.6**.
  - He's deliberately oversized: his torso hangs out of the window in every clip.
- **Orientation:** the socket's rest axes match the car's, so the driver should face the bonnet with zero offset.
  Check once with a Preview Asset on that socket and rotate the socket if UE disagrees.
- **Car body motion:** he rides along with all of the car's lean and bounce through the socket.
- **Per-car seat offset:** the clips are authored in `Car_Final`. The other two cars sit lower around their `Driver_Socket`, so without an
  offset his right arm cuts through their roof edge and his hands float above the wheel and door. Move the driver by this much on the
  socket, in the car mesh's own units before any actor scale (X = toward his window, Y = toward the tail, Z = up; flip Y for Unreal):

  | Car | X | Y | Z |
  |---|---|---|---|
  | `Car_Final` | 0 | 0 | 0 |
  | `Car_Base` | +0.012 | +0.012 | −0.027 |
  | `Car_High` | 0 | +0.012 | −0.045 |

  With these, arm-through-car crossings drop from 184 to 3 (`Car_Base`) and from 65 to 8 (`Car_High`) out of 780 tested arm segments;
  `Car_Final` has 12, all single frames while a hand travels between the wheel and the roof.

## Directions (game camera at the car's nose)

- **Screen right** = the driver's window side.
- **Into the screen** = toward the car's tail = where the car is driving (it always drives backwards).
- **Screen left** = the far side of the car, across the roof.

## Clips

| Clip | Type | Frames | What happens |
|---|---|---|---|
| Idle_A | loop | 49 | Slumped over the door, arm dangling like a pendulum, nodding to the music; sways with the idling car |
| Idle_B | loop | 49 | Bored: a long stare into the camera, then a huge yawn and stretch |
| Drive_A | loop | 49 | **The reference pose**: torso out of the window, propped on the door, right hand on the wheel, glaring where he drives. Slaps the door twice (frames 27, 32) |
| Drive_B | loop | 49 | Hauled up with a hand on the roof: free arm surfing the wind, a whoop, a grin at the camera |
| Damage_A | one-shot | 30 | Side hit: squashed, floats up, slammed down as the car lands (frame 12), clonks his head on the roof edge (frame 16), dizzy |
| Damage_B | one-shot | 30 | Front or rear hit: jolted back, the hand is yanked off the wheel, then he flops over the door like a wet towel with both arms dangling when the car lands (frame 11), springs back up |
| Throw_Window_A | one-shot | 32 | Grabs a can from inside, cocks it by his ear, whips it out to screen right. **Release frame 12** |
| Throw_Window_B | one-shot | 36 | Hauls himself up on the roof, big overhand hurl to screen right, folds over the door, fist pump. **Release frame 14** |
| Throw_Roof_A | one-shot | 36 | Sits up in the window, turns to the roof, braces a hand on it and lobs the can over to screen left. **Release frame 15** |
| Throw_Roof_B | one-shot | 40 | Sky-hook: swings the can from low outside up over his head and across the roof, right forearm braced on the roof; then two fist pumps with the left while the right hand slaps the roof (frames 26, 32). **Release frame 17** |
| Taunt_A | one-shot | 48 | At screen right: leans out shaking his fist, then hammers the door twice (frames 30, 36) |
| Taunt_B | one-shot | 48 | Twists round to face ahead: punches a fist at the sky, then two big "come on then!" sweeps |
| Taunt_C | one-shot | 48 | Party: pounds the door to the beat (frames 8, 16, 24, 32, 40), head-banging, slapping the wheel |

- **Blending:** every one-shot starts and ends exactly on frame 1 of `Drive_A`, so a short blend in and out of the
  loop is enough.
- **Loop sync:** the loops are 48 frames like the car's loops. Play `Idle_*` with `Car_Idle` and everything else with
  `Car_Drive` (one sync group).
- **Damage pairing:** `Damage_A` is timed to `Car_Damage_L` / `Car_Damage_R`, `Damage_B` to
  `Car_Damage_Front` / `Car_Damage_Rear`. Start them on the same frame as the car's clip.
- **Roof throws:** both go over the roof to the far side of the car (screen left). The projectile's real direction is
  whatever the game gives `SM_BeerCan`.
- **Event frames** are also in `../import_manifest.json` and in each clip's `MegaJam.Events` metadata (handy for
  sounds: `door_slap`, `door_bang`, `roof_slap`, `head_clonk`, `lands`).

## The can

1. Add `SK_BeerCan_Driver` as a second Skeletal Mesh Component with **Leader Pose** = the driver mesh. It follows
   `hand_l`.
2. Show it from **frame 4** of a throw clip (the `can_show` event: his hand comes back up from inside the car).
3. Hide it on the release frame and spawn `SM_BeerCan` there with the can's transform. The can's axis is its local Z;
   the origin is the grip.

## Editing the animation (Blender)

The clips are keyed on a control rig (Rigify + Rig Bridge), with a few hand-timed keys per control instead of a key
on every frame:

- **Control-rig actions:** `CTRL_Driver_<clip>` on `Armature_rig`. Change poses or timing there.
- **Export skeleton:** `Driver_Armature` holds the baked `Driver_<clip>` actions that the FBX files come from.
- **After editing:** run `Scripts/driver_v3/rebake.py` in Blender (re-samples the rig onto the export skeleton), then
  `Scripts/driver_v3/export_driver.py`.
- **Regenerating from code:** `Scripts/driver_v3/build_all.py` rebuilds every clip from `mj_clips.py`. It overwrites
  hand edits to the `CTRL_Driver_*` actions.

## Notes

- **Right arm (fixed 15 Nov):** the elbow now bends the way his body allows (it pointed at the front of his chest before), his palm lies
  on the wheel rim instead of passing through the wheel, and his right hand no longer punches toward the windscreen in `Throw_Roof_B`:
  it rests on the roof. Between the wheel and the roof the hand travels out through the window.
- **Left drift:** if the car hides him, `Drive_B` already sits further out and higher (hand on the roof).
- **Clipping:** he's far too big for the cabin on purpose, so his hips and legs pass through the door.
- **Hands:** his hands are mittens (the fingers are one fused piece), so the clips keep the fingers near their rest
  shape.
- **Testing:** checked in Blender (every FBX re-imported, poses match the source to within 0.01 mm, the can sits in
  his hand), not inside UE.
