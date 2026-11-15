# Passenger → Unreal Engine 5 (v3, 15 Nov: review fixes; car clips rebuilt on a control rig, car review round 2)

The captive girl (mesh `female_warrior`, UE5-mannequin skeleton **with** a `head` bone). She is carried tied up on an enemy camel,
jumps into the player's car when its rider dies, then rides shotgun hanging out of her window and throws cans (**matcha latte** cans).
13 clips.

- **Source file:** `Worked_Models/Passenger_Anims_v3.blend` (armature `Rider_female_warrior`, actions `Passenger_<Clip>`; v2 kept as `v2_Passenger_*`,
  the previous car clips as `car_v3_Passenger_*`, the first control-rig car clips as `r1_Passenger_*`). The **car clips** (`Seat_*`, `Jump_Land` after f11) are keyed on the Rig Bridge control rig
  `Passenger_Armature_rig` (actions `CTRL_Passenger_<Clip>`, mounted on `Passenger_Socket` by `Passenger_Mount`) and baked onto `Rider_female_warrior`.
- **Scripts:** `Scripts/passenger/` (camel clips and the jump: `build_v3.py`, `export_v3.py`, `c3_checks.py`); `Scripts/passenger_car/` (car clips:
  `pc_build_rig.py`, `pc_build_all.py`, `pc_check.py` = the arm checks, `pc_export.py`; see its `README.md`)
- **Preview:** `Worked_Models/Previews/Passenger_preview.mp4`; car clips: `Worked_Models/Previews/Passenger_Car_preview.mp4`
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
| In the car | `Car_Final`'s **`Passenger_Socket`** | **0.6** (same as the driver) | **cancel the socket's roll: see "Socket orientation" below** | `Jump_Land`, `Seat_*` |
| Flying | free actor, yaw = the car's yaw | blend from 1.5 × camel scale to 0.6 × car scale | – | `Jump_Air` |

- **Camel:** she is slung over the camel's back **behind the rider like a sack, on her stomach**: hips on the ridge, pelvis ≈ (0, +33, 0) cm
  from the socket (× 1.5 ≈ 50 cm behind the saddle), torso and head hanging down the camel's left flank (screen left, seen from behind),
  legs down the right flank, hands cuffed behind her back. Fitted on `Rig_Cmel_High` (belly ~0.5 cm into the blanket). Per-camel Z offset
  on the socket (cm, camel actor at scale 1): **`Rig_Cmel_High` 0, `Rig_Camel_mid` +1.5, `Rig_Camel_low` −1.5** (without it she sinks
  ~2 cm into the mid camel and floats ~1 cm over the low one).
- **Car:** base pose (= `Seat_Idle` f1) = "sitting in the window", the mirror of the driver: pelvis ≈ (−6, +1, +22) cm from the socket,
  chest out over her door (screen left), right forearm laid across the door top with the hand hanging outside, left hand on the door top
  in front of her, head beside the roof at the driver's height (head bone 0.42 m above the car origin in `Car_Final` vs the driver's
  0.44 m), face turned 3/4 to the game camera. In `Seat_Throw_R` and `Seat_Cheer` she sits up on the sill: head and shoulders above the
  roof line, chest just below it.
- **Socket orientation (the rule, every car clip and `Jump_Land`):** `Passenger_Socket`'s rest is rolled **−98° about the car's long
  axis** in the car rig (`Driver_Socket` is not rotated), and her clips are authored in the **car's axes** at the socket's position. So:
  1. `AttachToComponent(CarMesh, Passenger_Socket)` with Location = *SnapToTarget*, Rotation = *SnapToTarget*, Scale = *KeepRelative*
     (relative scale 0.6);
  2. right after attaching, **`SetWorldRotation(CarMesh.GetComponentRotation())`** on her mesh/actor once. That stores the relative
     rotation that cancels the socket's roll, so she then follows the car exactly like the driver does at `Driver_Socket`.
  Do **not** attach with "no rotation offset" (she would lie ~98° on her side). `import_manifest.json` (`passenger.in_car`) still says
  "no rotation offset"; this rule replaces it. Check once with a Preview Asset: she sits upright in her window facing the hood, mirror of the driver.
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
| Jump_Land | no | 34 | car | Arrives outside her window feet first, legs over the sill, grabs the roof edge, `in_seat` **11** (thump onto the seat, head stays out of the window). f1–11 unchanged; new tail: her left hand lets go of the roof edge at once and drops forward onto the door top (elbow down, f12–19), "ta-da" with her right arm out of the window (f15–20), settles exactly into `Seat_Idle` f1 |
| Seat_Idle | **yes** | 61 (60 + closing key) | car | Leaning out of her window: breathes into the wind, slides her left hand forward along the door top and turns her chest to glance back at the enemies (f18–40, face into the wind), back to the camera with a head tilt, three taps on the door (f41–51) |
| Seat_Throw_L | no | 36 | car | Right hand: snatches the can from behind her shoulder, cocks it beside her face (outside, face stays visible), whips it out of her window; the left hand stays braced on the door top and slides forward. `can_show` **5**, `release` **15** (peak hand speed; the hand keeps travelling through f18, then eases out) |
| Seat_Throw_R | no | 44 | car | Draws the can, sits up on the sill turned to the roof; her left arm aims over the roof at the target while the right hand cocks the can behind her head; on the whip the left hand pulls in and grabs the A-pillar, the can goes up and over the roof to screen right, she points after it, then swings the arm back behind her head into the window. `can_show` **5**, `release` **18** (peak hand speed; hand 18 cm above the roof) |
| Seat_Flinch | no | 28 | car | `hit` **1**: recoils and cowers in her window (shoulders up, head ducked, forearms up in front of her face, hands clear of it), peeks out, leans back out |
| Seat_Cheer | no | 36 | car | Dips, pops up onto her sill holding the A-pillar, three fist pumps high above the roof line, both arms up with a little shake (f22–26), back into the window |

- **Events and frame counts match `import_manifest.json`** (Throw_L 5/15, Throw_R 5/18, Cheer 36 frames, Jump_Land in_seat 11).

- **Loops:** last frame == first frame (keyed). Captive loops are 54 frames = 3 camel strides: start them in phase with the camel's run
  (clip frame 1 = camel frame 1, like the riders' `Ride`). `Seat_Idle` is 2.0 s.
- **Blending:** every car one-shot starts and ends exactly on `Seat_Idle` f1 (< 4 mm); `Jump_Land` ends on it. Between captive loops
  crossfade 0.25 s (they share the hips-on-the-ridge drape). Enter `Jump_Start` from `Captive_Idle` (exact match), or crossfade 0.25 s
  from another captive loop.
- **Projectile directions at release (car space, Blender axes, flip Y for Unreal):** Throw_L (−0.39, +0.86, −0.34) = out of her window
  and into the screen toward the enemies (hand 0.08 m/frame); Throw_R (+0.94, −0.15, +0.29) = up and across the roof to screen right
  (hand 0.11 m/frame, 18 cm above the roof). Speeds at scale 0.6; give the can your own arc.

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
3. At the end of `Jump_Air` **attach** her to `Passenger_Socket` at 0.6 (no position offset; rotation as in "Socket orientation" above) and
   play **`Jump_Land`**, then **`Seat_Idle`**.

## The can (matcha latte, never beer)

1. Add `SK_Can_Passenger` as a second Skeletal Mesh Component with **Leader Pose** = her mesh (it follows `hand_r`; the can sits in her
   right fist, ~6 cm from the wrist). Hidden by default.
2. Show it on `can_show`, hide it on `release` and spawn **`SM_Can_Passenger`** (static mesh, cm, same plain can) as the projectile there.

## Notes

- **Neck:** the head is aimed with a clamped look: head + neck at most ~68° yaw / 48° swing from the chest, spread over neck_01/neck_02/head.
  Bigger looks are done by turning the torso.
- **Contacts:** belly resting on the camel's back (auto-placed per frame); the thighs press into the saddle blanket where she folds over the
  ridge; no overlap with `city_warrior`; ≤ 3 mm with `Peasant_warrior` / `high_warrior` (one frame each). Car (car clips, every frame,
  `Car_Final` at rest): arm/hand/head bone segments and skinned vertices tested against `Cae_Base3`; arm and hand skin stays within 1 cm of
  the car surfaces it touches (forearms and hands on the door top, left hand on the A-pillar in `Seat_Throw_R`; worst 0.9 cm), one-frame
  1.0 cm graze of the right forearm on the door at `Seat_Flinch` f2. The head never touches the car. Her belly/chest rests on the door top
  and her thighs touch the door's inner trim (up to ~3 cm, hidden inside the door). Feet rest on the footwell floor.
- **Arms (car clips, measured every frame; `Jump_Land` from f12):** bone lengths kept (≤ 0.02 mm, scale 1), elbows bend only on the
  natural hinge (≤ 1.8° off) between 34° and 144° (no jackknifed or straight-locked elbows), elbows never point at the sky (car-up component
  ≤ 0.30), wrist bend and twist ≤ 57° (forearm twist bones carry most of it), head within 74° of the chest, no hand or forearm through her
  head or torso (one 2-polygon graze of the right forearm past her turban at `Seat_Throw_R` f30). `Jump_Land`: the twist bones blend smoothly from the approved landing into the rig's values over f12–19 (no re-twist at
  `in_seat`). Fast rotations (> 40°/frame, all deliberate): Throw_L f4–5 (snatch), f7–8 (cock), f15–16 (whip); Throw_R f4–6 (draw),
  f17–19 (whip), f30–31 (arm swings back), left arm f6, f17, f34; Flinch f3–4 (hit); Cheer f7–8, f13, f16–17, f20–22 (pumps, both
  arms up); Jump_Land f13 (left hand lets go of the roof); `Seat_Idle` has none.
- **Other cars:** authored in `Car_Final` only. `Car_Base` / `Car_High` may need a per-car seat offset like the driver's
  (see `Driver/README_Driver_UE5.md`); not measured for her yet.
- **Hands:** mitten hands, fingers kept near their rest shape.
- **Testing:** checked in Blender (re-imported FBX), not inside UE.
