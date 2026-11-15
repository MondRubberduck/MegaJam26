# Leaping Guard → Unreal Engine 5

A buff royal guard on a rider chariot ahead of the player. He turns round, crouches, dives backwards off the chariot at the
player's car (it drives rear-first, behind him) and either belly-flops onto the car roof and bounces off, or misses and tumbles on the road.
Open-work item 5. 6 clips per guard, 30 fps, centimetres, key-posed on top of BP Retarget sources. **v2 (15 Nov, after review).**

| What | Where |
|---|---|
| Animations (this folder) | `Animations/A_Guard2_Leap_<Clip>.fbx` (main) and `Animations/A_Guard1_Leap_<Clip>.fbx` (bonus), skeleton only |
| Skeletons | **Already in Unreal**: `UE_Export/Guards/SK_Guard2.fbx`, `SK_Guard1.fbx`. No new SK here. Bone names, hierarchy and rest matrices are identical (checked, error 0.0) |
| Source | `Worked_Models/Leaping_Guard_Anims.blend` (actions `<Guard>_Leap_<Clip>`) |
| Scripts | `Scripts/leaping_guard/` (`lg_game.py` = the game setup below, `lg_clips.py` the clips, `lg_build.py` rebuilds and saves, `lg_export.py`, `lg_preview.py`, `lg_world.py` world-space checks) |
| Preview | `Worked_Models/Previews/Leaping_Guard_preview.mp4`. Left: game view (camera in front of the car, chariot ahead). Right: side view of the whole jump. Hit, then miss |

## Import

- **Units:** centimetres. UnitScaleFactor 1, so import at scale 1.0. Sample rate 30. Animation Length: *Exported Time*.
- **Skeleton:** `A_Guard2_Leap_*` onto SK_Guard2's skeleton, `A_Guard1_Leap_*` onto SK_Guard1's. No `head` bone (the head is on `neck_02`).
- **Root motion:** off for every clip except `Leap_Land_Car` and `Leap_Land_Road`.
- **Facing (UE mesh space; the FBX import flips Blender Y, so UE Y = −Blender Y):**
  - He starts like the guard `Idle`, facing **+Y**: place the actor with mesh +Y along the chariot's travel direction. The camera sees his back.
  - `Leap_Crouch_In` turns him 180°. From then on he faces **−Y** (the car and the camera) and dives toward −Y.
  - After the turn his left side is −X = **screen right** in the game view.
- **All numbers below are at 1:1 (guard 100 cm tall).** Multiply lengths and speeds by the guard's world scale.

## Sequence

```
Idle (guard Idle, loop) ─► Leap_Crouch_In ─► Leap_Crouch (loop) ─┬─► Leap_Jump ─┬─► Leap_Land_Car   (hit the roof)
                                         ▲  [Leap_Bellow]  ◄────┘              └─► Leap_Land_Road  (missed)
```

- **Idle → Leap_Crouch_In:** `Leap_Crouch_In` f1 = guard `Idle` f1. Switch when Idle wraps (f61 = f1).
- **Leap_Crouch:** `Leap_Jump` and `Leap_Bellow` start on `Leap_Crouch` f1. Switch at the loop end (f37 = f1). `Leap_Bellow` ends on `Leap_Crouch` f1.
- **Leap_Jump → land:** `Leap_Land_*` f1 = `Leap_Jump` f34, the moment the chest touches. No crossfade.
- **Joins:** same pose (gap ≤ 0.5 mm). Velocity is continuous **in world space** when the game follows the arc below: at the takeoff the pelvis
  goes 9.6 → 10.6 cm/f forward and 7.5 → 7.9 cm/f up (Guard2). At the contact the chest stops on the roof in one frame (the impact, on purpose),
  the hips follow within 2–3 frames. Without the arc (clip space only) the Jump has the body nearly still after f11, because the game carries it.

## Game setup: the arc (built into the clips)

- **f1–f11:** the actor stays on the chariot (root on the deck). The push-off accelerates the body into the takeoff in the clip.
- **f11 → f34 (23 frames, 0.77 s):** the game moves the actor (the root) on a parabola from the takeoff point P0 (the root on the deck) to the
  contact point P1, arriving exactly at f34:
  `root(t) = P0 + (P1 − P0)·t/23 + Up · (g/2)·t·(23 − t)`, with `t = frame − 11` and **g = 0.907 cm/frame² (816 cm/s²)**.
  That puts the apex **60 cm above the straight line**, at about f22 (= `dive_peak`).
  **Compute the arc in car space** (P1 is a point on the moving car).
- **Speeds the clips are built for:** horizontal **12.6 cm/f (378 cm/s)** = 290 cm takeoff-to-contact; vertical **+10.0 cm/f** at the takeoff and
  **−10.9 cm/f** at the roof (deck 10.8 cm above the roof). Other distances change only the horizontal speed (distance / 23). With g and the
  23 frames fixed, the vertical speeds stay the same (± height difference / 23).
- **Clearance:** this arc clears the chariot's back rail (checked on the skinned mesh); a much flatter arc does not.
- **Hit or miss:** aim at the roof contact point. If the car is under him at f34, play `Leap_Land_Car`. If the player evaded, **hold `Leap_Jump`
  on f34 and continue the same parabola** (same g) until the root reaches the road (≈ 4 more frames), then play `Leap_Land_Road`. It is built
  for arriving at −14 cm/f down and 12.6 cm/f forward. Aiming a fresh 23-frame arc at the road also works (−13.3 cm/f).

## Clips

Events are 1-based frame numbers.

| Clip | Loop | Frames | What happens | Events |
|---|---|---|---|---|
| `Leap_Crouch_In` | no | 21 (0.7 s) | Head and chest lead the turn to his left, a hop-turn with the arms still crossed (feet up 8 cm, stance narrows to ±20 cm). Lands tall, absorbs over f12–f16 (pelvis 47 → 39 cm) with a small rebound; the arms open with breakdowns into a wrestler crouch. | feet leave **6**, land **12** |
| `Leap_Crouch` | **yes** (f37 = f1) | 37 | High wrestler crouch, fists forward, elbows out, glaring at the car. Visible life above the chariot's back rail: side-to-side rock with hip rotation (±11°) and chest counter-twist, a fist pound into the palm, a snort head-toss, a feint lunge at the car, shoulder rolls, glances, a small right-foot paw. Head moves 18–23 cm, pelvis 8–10 cm. | fist_pound **8**, snort **16**, feint **24**, paw_scrape **32** |
| `Leap_Bellow` (optional) | no | 40 | Rears up into a double-biceps bellow at the car with a 9 Hz shake on chest, head and shoulders, a head-and-chest jut at the loudest moment and a second pump, then sinks back. | roar start **10**, loudest **13**, pump **19**, roar end **24** |
| `Leap_Jump` | no | 34 (1.1 s) | Sinks 14 cm and swings the arms back (held f4–f6), then a constant-acceleration push (f6–f11): the arms whip forward and up (hands fastest f9–f11, still travelling after the takeoff), legs straight at f11, toes-hips-fists along the launch. Knees tuck over the back rail (f12–f16), then a superman dive: body banked ~20°, right fist forward, left arm wide (a V), legs split, head up so the face looks at the camera. Ends nose-down, arms spread above the chest, legs lifted: **the chest touches at the root on f34.** | **takeoff 11**, **dive_peak 22** |
| `Leap_Land_Car` | no | 50 | f1 chest on the roof, f2–f4 hips and legs slap down (heels kick up), arms splat flat: squash. f5 banana rebound, off the roof f6, one barrel roll in the air off his left side (screen right), belly-flop on the road at f25, rolls onto his back over 8 frames, still. | **impact 1**, squash 3, leaves_roof **6** (Guard1 7), clear_of_car **10** (Guard1 8), **hits_road 25**, **still 45** |
| `Leap_Land_Road` | no | 50 | f1 chest on the road, splat, the legs whip up as he slides, swing round (head to screen right), 1.5 barrel rolls toward the camera travelling 1.3 m (f10–f31), ends on his back. | **impact 1**, squash 3, rolls 10–31, **still 44** |

```json
{"fps": 30, "skeletons": {"Guard2": "SK_Guard2", "Guard1": "SK_Guard1"}, "files": "Animations/A_<Guard>_Leap_<Clip>.fbx",
 "arc": {"from_frame": 11, "to_frame": 34, "gravity_cm_per_frame2": 0.907, "apex_above_line_cm": 60, "space": "car",
         "built_for": {"horizontal_cm_per_frame": 12.6, "launch_up_cm_per_frame": 10.0, "arrive_roof_cm_per_frame": -10.9, "arrive_road_cm_per_frame": -14.0},
         "note": "all values at 1:1 (guard 100 cm), multiply by the guard's world scale"},
 "clips": [
  {"name": "Leap_Crouch_In", "frames": 21, "loop": false, "root_motion": false, "events": {"feet_leave": 6, "feet_land": 12}},
  {"name": "Leap_Crouch",    "frames": 37, "loop": true,  "root_motion": false, "events": {"fist_pound": 8, "snort": 16, "feint": 24, "paw_scrape": 32}},
  {"name": "Leap_Bellow",    "frames": 40, "loop": false, "root_motion": false, "events": {"roar_start": 10, "roar_peak": 13, "pump": 19, "roar_end": 24}, "optional": true},
  {"name": "Leap_Jump",      "frames": 34, "loop": false, "root_motion": false, "events": {"takeoff": 11, "dive_peak": 22, "contact": 34}},
  {"name": "Leap_Land_Car",  "frames": 50, "loop": false, "root_motion": true,  "space": "car until hits_road, then road",
   "events": {"impact": 1, "squash": 3, "leaves_roof": 6, "clear_of_car": 10, "hits_road": 25, "still": 45}},
  {"name": "Leap_Land_Road", "frames": 50, "loop": false, "root_motion": true,  "space": "road", "events": {"impact": 1, "squash": 3, "still": 44}}]}
```

## Root, per clip (measured)

- **Leap_Crouch_In, Leap_Crouch, Leap_Bellow, Leap_Jump:** `root` stays at its rest pose in every frame (like the guard Idle). Planted soles
  (skinned mesh) are within 0.2 cm of the deck (Guard1: toes 2.3 cm into it on the takeoff frame f11).
- **Leap_Jump body, relative to the root (Guard2):** f11 pelvis 50 cm up, 27 cm toward the car. f11–f34 the pelvis drifts in a straight
  line (2.0 cm/f back, 1.6 cm/f down), so its world path stays a parabola. f34: the chest's lowest point is exactly at the root, at root height.
- **Leap_Land_Car** (UE mesh space, Guard2; Guard1 ≈ ×0.96):
  - f1–f5: the root slides on toward the car's front (−Y) from 92 % of the arrival speed and sticks: −7.5, −10.3, −11.3, −11.8 cm at f2–f5.
  - Then it bounces up 21 cm and off to his left (−X), falls 53.9 cm to the road (f25) and stops. **End: X −124.9, Y −44.0, Z −53.9 cm**
    (Guard1: −119.6, −42.1, −53.9).
- **Leap_Land_Road:** the root slides and rolls straight on: **Y −201.9 cm** at the end (Guard1 −193.3), Z 0 (the road at root height).
- **Spaces:** play `Leap_Land_Car` **attached to the car** (car space) from f1 to `hits_road` (f25), then detach (keep world): he lies on the road
  and the car drives on. Play `Leap_Land_Road` in road space from f1: he is left behind by the car.

## Contact point convention (Leap_Land_Car)

- The root at `Leap_Jump` f34 = `Leap_Land_Car` f1 is **the contact point on top of the roof**: the chest touches it on that frame.
- **Car_Final** (car units = its Blender metres, as in `Passenger_Anims.blend`): on the roof centre line, **0.10 from the car's origin toward
  the rear bumper**, on the roof top (0.431 up), 2 cm ahead of the flat roof's middle. The flat roof runs from 0.27 behind to 0.03 ahead of
  the origin (with a 2.6 cm higher lip at the front); the slide (9.4 car cm at scale 0.8) ends 0.6 cm behind the origin. Keep the contact
  point between 0.05 and 0.15 behind the origin.
- Checked against Car_Final's mesh: the chest/shoulders touch at f1; the belly, hips and thighs press in by at most 1.3 cm at f2–f5 (squash).
  Nothing else touches the car (the heels kick up over the rear spoiler).
- **Road under Land_Car:** 53.9 cm below the roof = Car_Final's roof (0.431) / 0.8. Another scale or car: snap him to the road at `hits_road`.

## Scale and chariot (proposed, [to confirm])

- **Guard:** actor scale = **0.8 × the car actor's scale**. Car_Final: 1.054 long, 0.614 wide, 0.473 high (car units).
  At 0.8 he stands 0.75 (1.25 × the driver, who is 0.6 tall at 0.6 on `Driver_Socket`) and is about car-length in the dive.
  The Guards README proposes 1.25 × the pharaoh/throne actor for the same SK_Guard2: both hold if the throne actor = 0.64 × the car. Nils decides.
- **Chariot (Rider_Chariot mesh):** **2.2 × the guard's scale** (the crew README's chariot assumption; 1.76 × the car at guard 0.8).
  The deck is then 64.7 cm above the road (1:1 guard cm), 10.8 cm above Car_Final's roof.
- **Standing spot:** root at chariot-local **X 0.142, Y −0.02** (chariot units, X toward the open back), 0.068 behind the crew's spot.
  The Idle's right sandal then clears the raised board on the deck, and the back rail (55 cm high) is 75 cm ahead of the root.
- **Room he needs** (1:1, around the root): Leap clips: feet ±25 cm sideways, hips 20 cm back in the load, arms 35 cm out, the dive clears
  everything above the deck rail on the arc. The delivered **Idle** stands wider: sandal edges ±36 cm; on this chariot its right sandal and
  left thigh brush the deck's side features (a few faces). A flat deck at least 75 cm wide (1:1) around the root avoids it.

## Sources and method

- **Start pose:** frame 1 of the delivered guard `Idle` (not changed).
- **Pharao_Explosion, second half:** BP Retarget results stored as `RAW_<Guard>_Explosion` (from `Guards_Anims_v2.blend`); a 20–40 % limb-flail layer on the road part of both landings.
- **Roar_Bulky:** `RAW_<Guard>_Roar` adds the chest/neck tremble of `Leap_Bellow` (plus a keyed 9 Hz shake).
- **Throwing_Bulky:** pose reference for the crouch (posed by hand, not sampled). Everything else is key-posed (Hermite keys, IK legs and arms).

## Checks done (in Blender, not in UE)

- **verify_cm (scratch export):** armature scale 0.01 (cm file), height 1.00 m, 67 bones, root rest scale 1; all 6 clips × 2 guards at 30 fps,
  frame counts match, joint error 0.0. **Every frame** of all 12 delivered files re-imported: ≤ 2e-6 m from the .blend (root travel included).
- **Skeleton:** re-imported SK from this export = delivered `SK_Guard2.fbx` / `SK_Guard1.fbx` (names, parents, rest matrices: error 0.0).
- **World space** (`lg_world.py`, the arc above, chariot 2.2×, Car_Final): no stall at takeoff (largest frame-to-frame pelvis speed change
  over the jump = the roof impact); the body clears the chariot after the takeoff; car contact only at the impact (Jump f34 – Land_Car f5).
- **Head:** face within 56° of the chest (spine_05) in every clip. **Loop:** `Leap_Crouch` f37 = f1, seam velocity change 0.4 cm/f.
- **Rotation per frame over 40°** (body bones) only in deliberate snaps: Land_Car f3 arm slap (43°), Crouch_In f10 left wrist (42°);
  Guard1 also Jump f11 thighs (44°, push-off), f13 calf (47°, tuck) and Land_Car f8 forearm (48°).

## To confirm

- **Scale:** guard 0.8 × car; chariot 2.2 × guard; standing spot on the deck (see above).
- **Other cars:** only Car_Final's roof was checked. Car_Base / Car_High: the contact height and the 53.9 cm drop differ.
- **End of Land_Car:** he ends lying on the road beside the car. Despawn when off screen, or earlier?
- **Which guard:** Guard2 (main) or Guard1. Both sets are delivered.
- **Bellow:** is the optional `Leap_Bellow` telegraph wanted before the jump?
