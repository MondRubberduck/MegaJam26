# Passenger → Unreal Engine 5 (v3, 15 Nov: review fixes)

The captive girl (mesh `female_warrior`, UE5-mannequin skeleton **with** a `head` bone). She is carried tied up on an enemy camel,
jumps into the player's car when its rider dies, then rides shotgun hanging out of her window and throws cans (**matcha latte** cans).
13 clips.

- **Source file:** `Worked_Models/Passenger_Anims_v2.blend` (armature `Rider_female_warrior`, actions `Passenger_<Clip>`; v2 kept as `v2_Passenger_*`)
- **Scripts:** `Scripts/passenger/` (`build_v3.py` rebuilds every clip, `export_v3.py` writes this folder, `c3_checks.py` = the checks below)
- **Preview:** `Worked_Models/Previews/Passenger_preview.mp4`
- **Format (15 Nov brief):** centimetres, **30 fps**, one clip per FBX. Re-import check (`verify_cm`): mesh 1.0 m tall, armature scale 0.01,
  80 bones, root rest scale 1, every clip 30 fps with matching frame counts, joints identical to the source (error 0.0 mm).

```
Passenger/SK_Passenger.fbx                 skeleton + mesh (textures embedded), 80 bones, 1 m tall at scale 1
Passenger/SK_Can_Passenger.fbx             the can, skinned 100% to hand_r (use with Leader Pose)
Passenger/SM_Can_Passenger.fbx             the same can as a static mesh (the projectile), origin at its centre
Passenger/Animations/A_Passenger_*.fbx     the clips below
```

## Root and placement

- **The `root` bone is at identity on every frame of every clip** (no rotation, no translation). The pelvis carries all body placement.
  Root motion / Force Root Lock make no difference; leave root motion off.
- Offsets below are in clip centimetres before the actor scale, Blender axes (X = her left on the camel / toward the driver in the car,
  Y = toward the camel's tail / the car's tail, Z = up). **Flip Y for Unreal.**

| Where | Socket | Relative scale | Rotation offset | Clips |
|---|---|---|---|---|
| On the camel | the camel's **`ORG-Sitting_Root`** (the riders' socket) | **1.5** (same as the riders) | none (use the same optional squaring yaw as the rider on that camel) | `Captive_*`, `Jump_Start` |
| In the car | `Car_Final`'s **`Passenger_Socket`** | **0.6** (same as the driver) | none | `Jump_Land`, `Seat_*` |
| Flying | free actor, yaw = the car's yaw | blend from 1.5 × camel scale to 0.6 × car scale | – | `Jump_Air` |

- **Camel:** she is slung over the camel's back **behind the rider like a sack, on her stomach**: hips on the ridge, pelvis ≈ (0, +33, 0) cm
  from the socket (× 1.5 ≈ 50 cm behind the saddle), torso and head hanging down the camel's left flank (screen left, seen from behind),
  legs down the right flank, hands cuffed behind her back. Fitted on `Rig_Cmel_High` (belly ~0.5 cm into the blanket). Per-camel Z offset
  on the socket (cm, camel actor at scale 1): **`Rig_Cmel_High` 0, `Rig_Camel_mid` +1.5, `Rig_Camel_low` −1.5** (without it she sinks
  ~2 cm into the mid camel and floats ~1 cm over the low one).
- **Car:** base pose = "sitting in the window", the mirror of the driver: pelvis ≈ (−7, 0, +29) cm from the socket (on the door-side
  bolster), chest leaning out of her window (screen left), head beside the roof at the driver's height (head bone 0.46 m above the car
  origin in `Car_Final` vs the driver's 0.44 m), face toward the game camera. The cabin is too low for her to sit upright under the roof
  at this scale, so every car clip keeps her head out in the window opening.
- **The camel's gallop** reaches her through the socket; her loops add a passive flop timed to the run (2 bounces per stride).

## Clips

| Clip | Loop | Frames | Placement | What happens / events (1-based frames) |
|---|---|---|---|---|
| Captive_Idle | **yes** | 55 (54 + closing key) | camel | Hangs limp over the camel, flopping with the gallop; one weary lift of the head toward the player (f13–42) |
| Captive_Distress | **yes** | 55 | camel | Fights: flutter kicks, two thrashing bursts (f4–19, f31–46), wriggles against the cuffs, head tosses |
| Captive_Beg | **yes** | 55 | camel | Arches her chest up, rolled toward the player behind, face to the camera; one plead per camel stride (both legs kick, "please" nods) |
| Captive_Beg_L | **yes** | 55 | camel | Pleading to screen left: torso swung out wide over the left flank, head far left and low, looking left |
| Captive_Beg_R | **yes** | 55 | camel | Pleading to screen right: cranes up high over her own back near the rider, chest rolled to the camera, looking right |
| Jump_Start | no | 37 | camel | Starts exactly on `Captive_Idle` f1. Kicks, swings up onto the camel's rump into a crouch facing the player, strains, `cuffs_snap` **20** (arms fly wide), deep crouch with arms swung back, leaps up and toward the camera. `leave_camel` **35** (airborne; the clip runs 2 more frames) |
| Jump_Air | no | 21 | flying | In place, 0.7 s: front somersault (tucked) with a quarter twist, opening into a seated pike with her feet toward the car (her front faces the car's +X = toward the driver), arms up |
| Jump_Land | no | 34 | car | Arrives outside her window feet first, legs over the sill, grabs the roof edge, `in_seat` **11** (thump onto the seat, head stays out of the window), "ta-da" with her right arm out of the window (f15–20), settles into the base pose = `Seat_Idle` f1 |
| Seat_Idle | **yes** | 61 (60 + closing key) | car | Hanging out of her window: glances back at the enemies (turning her torso), smiles at the camera with a head tilt, faces into the wind, drums on the door |
| Seat_Throw_L | no | 36 | car | Right hand: can from the door pocket, cocked by her ear (hold), 3-frame whip out of her window. `can_show` **5**, `release` **15** (peak hand speed) |
| Seat_Throw_R | no | 44 | car | Hauls herself up onto the sill, winds up, whips the can up and over the roof. `can_show` **5**, `release` **18** (peak hand speed) |
| Seat_Flinch | no | 28 | car | `hit` **1**: yanked inside, ducks with her arms over her head, peeks out, leans back out |
| Seat_Cheer | no | 36 | car | Dips, rises up in the window, three fist pumps high above the roof line, both fists up and held (f23–30) with a little shake |

- **Loops:** last frame == first frame (keyed). Captive loops are 54 frames = 3 camel strides: start them in phase with the camel's run
  (clip frame 1 = camel frame 1, like the riders' `Ride`). `Seat_Idle` is 2.0 s.
- **Blending:** every car one-shot starts and ends exactly on `Seat_Idle` f1 (< 4 mm); `Jump_Land` ends on it. Between captive loops
  crossfade 0.25 s (they share the hips-on-the-ridge drape). Enter `Jump_Start` from `Captive_Idle` (exact match), or crossfade 0.25 s
  from another captive loop.
- **Projectile directions at release (car space, Blender axes, flip Y for Unreal):** Throw_L (−0.73, +0.68, −0.09) = out of her window
  and into the screen toward the enemies; Throw_R (+0.69, +0.52, +0.51) = up and over the roof to screen right / into the screen.
  Hand speed at release ≈ 0.09–0.11 m/frame at scale 0.6.

## The jump sequence (game logic)

1. The rider dies → (blend to `Captive_Idle`, then) play **`Jump_Start`** (still on the camel socket, scale 1.5).
2. On `leave_camel` (f35) or at the end of the clip, **detach** her and play **`Jump_Air`** (0.7 s) while the game flies her to the car.
   Crossfade **2–3 frames** at this switch and at the next one; the poses at both joins are identical (0.0 cm) and the motion runs
   straight through them (the clips were built from shared keys).
   - actor **yaw = the car's yaw** (she already faces the camera at the end of `Jump_Start`, because the camel runs facing away);
   - in `Jump_Air` her pelvis sits **50 cm above the root** (× her current scale), no horizontal offset;
   - **path:** start the root at the pelvis world location on the last `Jump_Start` frame (`GetBoneLocation("pelvis")`) minus
     50 cm × S_camel straight down. On that frame the pelvis is at (+10, +80, +70) cm × 1.5 from the camel socket (behind the rump, in
     the air). End the root at Passenger_Socket + car rotation × (S_car × (−78, −4, +12) cm) in **Unreal** axes: that puts her pelvis
     where frame 1 of `Jump_Land` has it, (−78, −4, +62) cm × S_car from the socket (Unreal axes), outside her window;
   - **scale:** blend from S_camel = 1.5 × camel actor scale to S_car = 0.6 × car actor scale over the flight (if the car actor is
     2.5 × the camel actor, as in my preview staging, they are equal and nothing needs blending);
   - add an arc (~1 m up at mid-flight) so the somersault reads.
3. At the end of `Jump_Air` **attach** her to `Passenger_Socket` at 0.6 (no offset) and play **`Jump_Land`**, then **`Seat_Idle`**.

## The can (matcha latte, never beer)

1. Add `SK_Can_Passenger` as a second Skeletal Mesh Component with **Leader Pose** = her mesh (it follows `hand_r`; the can sits in her
   right fist, ~6 cm from the wrist). Hidden by default.
2. Show it on `can_show`, hide it on `release` and spawn **`SM_Can_Passenger`** (static mesh, cm, same plain can) as the projectile there.

## Notes

- **Neck:** the head is aimed with a clamped look: head + neck at most ~68° yaw / 48° swing from the chest, spread over neck_01/neck_02/head.
  Bigger looks are done by turning the torso.
- **Contacts:** belly resting on the camel's back (auto-placed per frame); the thighs press into the saddle blanket where she folds over the
  ridge; no overlap with `city_warrior`; ≤ 3 mm with `Peasant_warrior` / `high_warrior` (one frame each). Car: her skeleton segments
  (arms, legs, spine, neck) ray-cast against `Cae_Base3` every frame: none in `Seat_Idle` and `Seat_Throw_L`; her right thigh lies on the
  door armrest while she sits up on the sill (`Seat_Throw_R`, `Seat_Cheer`); fingertips on the roof edge in `Jump_Land` (grabbing it).
  Feet rest on the footwell floor.
- **Other cars:** authored in `Car_Final` only. `Car_Base` / `Car_High` may need a per-car seat offset like the driver's
  (see `Driver/README_Driver_UE5.md`); not measured for her yet.
- **Hands:** mitten hands, fingers kept near their rest shape.
- **Testing:** checked in Blender (re-imported FBX), not inside UE.
