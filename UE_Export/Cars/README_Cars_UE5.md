# Cars → Unreal Engine 5

Three cars, 22 in-place clips each, exported from `Worked_Models/Car_Game_Anims.blend`.
Preview of every clip: `Worked_Models/Previews/Car_Game_Anims_preview.mp4`.

```
Cars/
  Car_Final/  SK_Car_Final.fbx            skeletal mesh (body + 4 tyres, textures embedded)
              Animations/A_Car_Final_*.fbx 22 clips, one file each
  Car_Base/   (same layout)
  Car_High/   (same layout)
```

Each car has its own copy of the clips, baked to its own wheel positions. Import each car with its own skeleton
and nothing needs retargeting.

## Import (per car)

1. **Mesh:** import `SK_Car_X.fbx` with Skeletal Mesh on and Import Animations off. Leave the uniform scale at 1.0
   (the scale is already baked; Car_Final is about 105 cm long). Materials and textures come along: the textures
   are embedded in the FBX.
2. **Clips:** select all 22 `A_Car_X_*.fbx` files at once and pick `SK_Car_X_Skeleton` as the skeleton. Leave
   Import Mesh off and Animation Length on *Exported Time*. Each file becomes one AnimSequence with the file's name.
3. **Materials:** base colour and normal maps hook up automatically. If roughness or metallic aren't connected,
   plug in the imported `*_roughness` / `*_metallic` textures by hand.

The skeleton root is `Root`. If UE shows an extra root bone called `Armature` above it, that's harmless.

## Orientation and pivot

- **Nose direction:** the nose points along **+Y** in UE, like the mannequin.
- **Rotate the mesh:** the car **drives backwards**, so in the Blueprint rotate the Mesh component until the
  **tail** points along the actor's forward arrow (+X). That should be **Yaw = 90**; check it against the arrow.
- **Pivot:** the actor origin sits at ground level between the axles. Car_Final and Car_High tyres reach 2.2 cm
  below the origin (Car_Base 0.3 cm). Nudge the mesh up if the tyres sink into your road.

## No root motion

**The game moves the car; the clips never translate it horizontally.** Leave *Enable Root Motion* off.
The `Root` bone still carries a few baked effects on purpose:

- `Drift_*` and `Turn_*`: a yaw (slip angle) and, on `_Max`, the tip onto two wheels.
- `Damage_*`, `Ram*`: the short tip/hop from the hit.
- `Death_Flip`, `Dead`: the vertical launch and the upside-down pose.

If the game should own the drift angle itself, ask and I'll zero it out of the clips.

## Clips (24 fps)

| Clip | Type | Frames | Notes |
|---|---|---|---|
| Idle | loop | 49 | Engine rumble, rev roll |
| Drive | loop | 49 | Cruising rear-first, road bumps |
| Boost | loop | 49 | Tail rears up, stretch, thrust pulses |
| Brake | loop | 49 | Weight on the tail, ABS shudder |
| Turn_L / Turn_R | loop | 49 | Lean, steer, slight slip |
| Turn_L_Max / Turn_R_Max | loop | 49 | Up on two wheels |
| Drift_L / Drift_R | loop | 49 | ~37° slide, counter-steer |
| Ram | one-shot | 32 | Tail-first ram, impact on frame 9 |
| Ram_L / Ram_R | one-shot | 30 | Side swipe, impact on frame 9 |
| Jump_Start | one-shot | 12 | Crouch, tail kicks up; ends in the Jump_Air pose |
| Jump_Air | loop | 25 | Wheels dangling |
| Jump_Land | one-shot | 22 | Tail lands first, big squash |
| Damage_Front / _Rear / _L / _R | one-shot | 30 | Hit on that side of the car |
| Death_Flip | one-shot | 64 | 1.5 barrel rolls, lands on the roof; ends where Dead starts |
| Dead | loop | 49 | Upside down, lazy wheels, twitch |

- **Left / Right** = the direction the car's *path* bends, seen in the direction of travel. `Ram_L` hits a target
  on that left side.
- **Loop frames:** in every loop the last frame equals the first, the normal setup for UE looping. Don't trim it.

## Anim Blueprint tips

- **Steering:** make a *Blend Space 1D* on steering (-1…1): `Turn_R_Max, Turn_R, Drive, Turn_L, Turn_L_Max`.
  These five share the same length, wheel spin and road bumps, so they blend without fighting. Keep them on
  one sync group.
- **States:** Idle / Drive (the blend space) / Boost / Brake / Drift_L / Drift_R, with blends of about 0.15–0.2 s.
- **Jump:** `Jump_Start` → `Jump_Air` (loop while airborne) → `Jump_Land` on landing. Use "time remaining" for
  Start→Air.
- **Hits and rams:** play `Damage_*` and `Ram*` as **Montages** in a slot on top of the state machine
  (blend in 0.05 s, out 0.2 s) so they work in any driving state.
- **Death:** `Death_Flip`, then hold `Dead`.
- **Wheel spin:** the spin is baked (about 37° per frame while driving). For exact speed matching, add the spin
  on the `*_Tire` bones with a *Transform (Modify) Bone* node driven by speed.

## Riders / passengers

`Driver_Socket` and `Passenger_Socket` are bones. Attach a character with
`AttachToComponent(CarMesh, SnapToTarget, "Driver_Socket")`. Any bone name works as a socket; add a Skeleton
Socket on that bone if you want an offset you can tweak. The sockets ride along with all the body squash and lean.

## Known small things

- **Upside-down height:** clips are tuned to Car_Final's size. Upside down, Car_Base floats about 1 cm and
  Car_High's taller wing sinks about 2 cm into the road.
- **Squash on child bones:** the body squash uses non-uniform scale. Bones under `Chase` inherit it with a tiny
  approximation (FBX and UE can't do shear). It isn't visible.
- **Testing:** checked in Blender, not inside UE. Re-importing every file showed the right bone count, no extra
  `_end` bones and embedded textures. The raw curves match the source animation key for key.

## Re-exporting / changes

- Source file: `Worked_Models/Car_Game_Anims.blend`.
- Generator: `Scripts/car_game_clips/car_loops.py`. The `EXAG` knob controls exaggeration (1.1 now).
- Exporter: `Scripts/car_game_clips/X02_export.py`. Change something, rebuild, re-export: about a minute.
