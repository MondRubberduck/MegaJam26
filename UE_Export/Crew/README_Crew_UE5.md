# Cart crew (rider chariots) → Unreal Engine 5   (v2, 15 Nov, after review)

The plain cart crew of stage 3 (the spear chariot and the ramming chariot): the four camel-rider warriors **standing in the rider
chariot**. 13 clips per warrior, 30 fps. Built from BP Retarget results of Nils's prepared mocap (Standing_Bulky = base stance,
Roar_Bulky = taunt spine, Throwing_Bulky = throw spine, second half of Pharao_Explosion = fall), re-animated for slim, cheeky nomads.
The hit is hand-made (Pharao_Flinch is a recoil from the front; this hit comes from behind).

```
Crew/<warrior>/Animations/A_<warrior>_<Clip>.fbx   13 clips per warrior, skeleton only (52 files)
   <warrior> = Peasant_warrior, city_warrior, female_warrior, high_warrior
```

**No new meshes.** Use what is already in Unreal from `Riders/`: `SK_<warrior>` (body), `SK_Spear_<warrior>` (spear on `hand_r`,
Leader Pose) and `Props/SM_Spear` (thrown spear). Source: `Worked_Models/Crew_Anims.blend`. Scripts: `Scripts/crew/` (build:
`crew_build_all.py` → `crew_clips.py`). Preview: `Worked_Models/Previews/Crew_preview.mp4` (left: game view from behind, right: front 3/4).

## What changed in v2 (all clips re-exported, same names)

Base stance raised (soft knees, not a squat; fists just over the front rail), spear-throw wrist fixed (no candy-wrapper), elbow-led
whip in every throw, javelin readable from the game camera, slower `_R` spin-up, new `Cart_Hit`, `high_warrior`'s fall rolls him onto
his front, feet/legs kept out of the chariot, quiver draw in `Spear_Cart_Throw_B`. Event frames changed slightly: taunt lands f10
(was f11), every throw hops at f2 and lands f9 (was f3/f8), hit grabs the rail f8 / looks back f13. Release stays on f13.

## Import

- **Skeleton:** import onto the skeleton that already exists for `Riders/<warrior>/SK_<warrior>`. Do not create a skeleton. 80 bones,
  same names as the riders.
- **Units:** the same metre format as the rider clips (same exporter settings, UnitScaleFactor 100 like the rider clips). Use the import
  settings you used for the rider animations.
- **Frame rate:** 30 fps, Animation Length *Exported Time*. Heads-up: the existing rider clip files (`Riders/*/Animations/*.fbx`)
  declare **24 fps** in their header; if they were imported at the file's rate they play 20 % slow. I did not touch them.
- **Root motion:** off for every clip except `Cart_Fall_Off`.

## Placement in the chariot

- **Facing:** the crew face **+Y in UE mesh space** (−Y in Blender), like the riders = the chariot's travel direction (toward the
  camels / the chariot's shafts). Their left is +X. The player is behind them (mesh −Y).
- **Root:** the `root` bone = the standing spot on the deck, between the feet. It does not move in any clip except `Cart_Fall_Off`
  (measured 0.0 mm on every frame of the other 48 clips).
  - The root is **not at the mesh origin** for `Peasant_warrior` and `high_warrior`: 24 cm in front of it (mesh +Y), as in their rider
    SK. `city_warrior`, `female_warrior`: within 2 mm. Put the **root** on the spot, not the actor origin.
  - Pelvis above the root at `Cart_Ride` f1 (bottom of a bounce = the base pose of every one-shot): Peasant 0.50, city 0.49,
    female 0.50, high 0.46 m (their rest: 0.53–0.56). In the ride loop the pelvis moves within 0.46–0.53 m.
- **Chariot scale (assumption, `[to confirm]`):** animated with the chariot at **2.2 × the warrior's scale** (warrior 1 m tall, the
  chariot mesh is 1 unit long on its own → 2.2 m). Front wall top 0.55 m above the deck (his waist); front wall inner face 0.37 m
  ahead of the root; side walls 0.32–0.37 m to his right (a 5 cm step at 0.20 m) and 0.42–0.54 m to his left; open back.
- **The spot in the chariot mesh's own units** (length 1.0, wheel bottom = road at Z 0, shafts at −X, open back at +X):
  - Blender import axes: deck top Z **0.294**, spot X **+0.21**, Y **−0.02**.
  - **UE axes** (Y flipped by the FBX import): spot X **+0.21**, Y **+0.02**, Z **0.294** = **(21, 2, 29.4) cm in the chariot's local
    space before its actor scale** (×2.2 at the assumed scale: root 0.647 m above the road, 0.46 m behind the front wall top edge,
    0.57 m in front of the open back). Turn the warrior so his mesh +Y points along the chariot's −X (toward the shafts).
- **Room each clip needs** (metres at warrior scale 1:1, around the root, max over the four warriors, skinned mesh incl. hands):

| Clip | left | right | forward | back | top |
|---|---|---|---|---|---|
| Cart_Ride / Spear_Cart_Ride | 0.46 | 0.35 | 0.36 | 0.59 | 0.98 |
| Cart_Taunt_B / _L / _R | 0.60 | 0.54 | 0.60 | 0.57 | 1.12 |
| Cart_Throw_* / Spear_Cart_Throw_* | 0.57 | 0.61 | 0.66 | 0.61 | 1.17 |
| Cart_Hit | 0.46 | 0.37 | 0.50 | 0.57 | 0.98 |
| Cart_Fall_Off | 0.42 | 1.04 | 0.31 | **3.78** | 1.22 |

  Arms, rock and spear reach over the walls; the feet stay inside the tub. `high_warrior`'s back blades (part of his mesh, rigid on
  `spine_05`) stick out 0.6 m behind him in every clip ("back" 0.59 in the ride is the blades).

## Directions

`_B` = player behind (the usual camera view, required). `_L` / `_R` = player on screen left / right (= the crew's left / right).
Taunts and throws turn toward the player.

## Clips

Events are 1-based frame numbers. Every one-shot except `Cart_Fall_Off` starts **and** ends exactly on `Cart_Ride` frame 1 (the
`Spear_` ones on `Spear_Cart_Ride` frame 1): measured gap 0.000 mm on all joints. Crossfade 0.1–0.2 s or none.

| Clip | Loop | Frames | What happens | Events |
|---|---|---|---|---|
| `Cart_Ride` | **yes** (f37 = f1) | 37 | Standing tall, knees soft, both fists forward just above the front rail on the reins (no reins prop). Four deck bumps per loop (f1 = bottom of one): hips dip ~2.3 cm, chest folds a frame later; weight rocks side to side; glance back over the right shoulder (f6–20), quick look left (f25–35); "hyah!" rein snap f19–26 (spread over 3 frames). | – |
| `Spear_Cart_Ride` | **yes** (f37 = f1) | 37 | Same body; spear upright in the right fist, reins in the left fist; the snap becomes a spear pump. | – |
| `Cart_Taunt_B` / `_L` / `_R` | no | 54 | Crouch, **hop-turn** to the player, lands f10, absorbs, then springs **up on the balls of his feet** into the ROAR: arms in a big V, chest out, chin out, trembling (the loudest pose is also the tallest: head +4–5 cm above the ride). Two chest pounds, hops back, reins. | hop f4, lands f10, **loudest f13**, pounds f24 / f28, hop back f35, lands f43 |
| `Cart_Throw_B` / `_L` / `_R` | no | 40 | Rock from the belt (right hip) f3, hop-turn (f2–9, fists pulled in while he spins) into a coil (left arm aims at the player), **elbow leads** (f10–12), the arm snaps straight f12–14, **release f13** at the top of the arc ~25 cm to his right of the head (reads clear of the head from the game camera), follow-through down over the front leg, fist pump, hops back, reins. `_R` spins 150° (v1: 190° in 5 frames). | rock in hand **f3**, hop f2, lands f9, **release f13** (`hand_r`), hop back f26, lands f34 |
| `Spear_Cart_Throw_B` / `_L` / `_R` | no | 46 | Javelin: the shaft rises with the forearm, turns with the body in the hop, is held cocked **tip-up ~40° and across the screen** (f7–11, readable from behind), flattens onto the player over f11–13, **release f13**. `_B` then leans out to the quiver (his right-front once he faces the player) and draws a new spear straight up out of it (f23–26); `_L`/`_R` get the spare spear back in the fist as they land from the hop back (f36). | hop f2, lands f9, **release f13** (`hand_r`); spear back in hand **f23** (`_B`) / **f36** (`_L`, `_R`); hop back f28, lands f36 |
| `Cart_Hit` | no | 28 | Smacked in the back from behind: hips shoved forward, back arched, head snapped back, arms flung back and out (left a frame after the right), knees buckle as he lurches into the front rail with **both fists on the rail top**, then twists to glare back over his right shoulder and shakes his fist behind his head **at the player**; back to the reins. | impact **f1**, fists on rail **f8**, looks back f13, fist shake f14–19 |
| `Cart_Fall_Off` | no | 64 | Blasted off **backwards** out of the open back (toward the player): over the back edge, lands on the road, tumbles, slides, lies still. Does not return to the ride. **Travel on the root.** `high_warrior` rolls onto his side in the air and onto his **front** on the road, so his back blades point up (they cannot lie under him); during the tumble (f23–29) the blades make him bounce ~15 cm. | impact f1, leaves the deck **f4**, over the back edge **f8**, lands on the road **f17**, still from **f56** |

### Throws: the projectile

- **Rock (unarmed throws):** show/attach a rock on `hand_r` at **f3** (about 7 cm along the hand bone); release at **f13**. No rock
  mesh is exported (`[to confirm]` rock or pot).
- **Spear:** `SK_Spear_<warrior>` (Leader Pose). At **f13** hide it and spawn `SM_Spear` from its current transform (aimed at the player,
  ~20° up). Show the SK spear again at **f23** (`_B`) or **f36** (`_L`, `_R`).
- **Release point** (`hand_r` head at f13, relative to the root, UE mesh space, cm at 1:1, range over the four warriors):
  - `Cart_Throw_B`: X +19..+20, Y −30..−34 (toward the player), Z 81–85. `_L`: X +28..+32, Y +19..+20. `_R`: X −28..−33, Y −18..−19.
  - `Spear_Cart_Throw_B`: X +18..+20, Y −26..−30, Z 86–90. `_L`: X +24..+28, Y +18..+20. `_R`: X −24..−29, Y −17..−19.
- **Hand speed:** fastest arriving at f13 (rock 27–32 cm/frame, spear 28–32), and still moving toward the player for 2–3 frames after
  the release (rock about 11, 2–3, 0 cm/frame; spear 13–15, 4–6, 0), total speed decaying 15–18, 11–15, 5–9 cm/frame. The wind-up
  is slower than the whip in every clip (hands ≤ 27 cm/frame before f11 in `_B`/`_R`, ≤ 16 in `_L`).

### Cart_Fall_Off root motion

- **Travel:** `root` carries it: **2.89–3.07 m backwards** (mesh −Y, toward the player), 0.41–0.44 m to his right (mesh −X), and
  **0.647 m down** (deck to road at the 2.2× chariot scale), the drop between f8 and f17. After landing the body rests on the road
  (lowest vertex 0–2 mm above it).
- If your chariot scale differs, the drop is wrong by `0.294 × (chariot/warrior scale) − 0.647` m: detach at f4 and let your own drop
  take over, or ignore root Z.
- **Using it:** detach him from the chariot (`KeepWorld`) at f1–f4 and play with root motion; the chariot drives on.

## Machine-readable clip list

```json
{"fps": 30, "skeleton_from": "Riders/<warrior>/SK_<warrior>", "file": "Crew/<warrior>/Animations/A_<warrior>_<clip>.fbx",
 "clips": [
  {"clip": "Cart_Ride", "frames": 37, "loop": true, "root_motion": false, "events": {}},
  {"clip": "Spear_Cart_Ride", "frames": 37, "loop": true, "root_motion": false, "events": {}, "show_spear": true},
  {"clip": "Cart_Taunt_B", "frames": 54, "loop": false, "root_motion": false, "events": {"hop_off": 4, "land": 10, "loudest": 13, "pound": [24, 28], "hop_back": 35, "land_back": 43}},
  {"clip": "Cart_Taunt_L", "frames": 54, "loop": false, "root_motion": false, "events": {"hop_off": 4, "land": 10, "loudest": 13, "pound": [24, 28], "hop_back": 35, "land_back": 43}},
  {"clip": "Cart_Taunt_R", "frames": 54, "loop": false, "root_motion": false, "events": {"hop_off": 4, "land": 10, "loudest": 13, "pound": [24, 28], "hop_back": 35, "land_back": 43}},
  {"clip": "Cart_Throw_B", "frames": 40, "loop": false, "root_motion": false, "events": {"rock_show": 3, "release": 13, "release_bone": "hand_r", "hop_back": 26, "land_back": 34}},
  {"clip": "Cart_Throw_L", "frames": 40, "loop": false, "root_motion": false, "events": {"rock_show": 3, "release": 13, "release_bone": "hand_r", "hop_back": 26, "land_back": 34}},
  {"clip": "Cart_Throw_R", "frames": 40, "loop": false, "root_motion": false, "events": {"rock_show": 3, "release": 13, "release_bone": "hand_r", "hop_back": 26, "land_back": 34}},
  {"clip": "Spear_Cart_Throw_B", "frames": 46, "loop": false, "root_motion": false, "events": {"release": 13, "release_bone": "hand_r", "spear_hide": 13, "spear_show": 23, "hop_back": 28, "land_back": 36}, "show_spear": true},
  {"clip": "Spear_Cart_Throw_L", "frames": 46, "loop": false, "root_motion": false, "events": {"release": 13, "release_bone": "hand_r", "spear_hide": 13, "spear_show": 36, "hop_back": 28, "land_back": 36}, "show_spear": true},
  {"clip": "Spear_Cart_Throw_R", "frames": 46, "loop": false, "root_motion": false, "events": {"release": 13, "release_bone": "hand_r", "spear_hide": 13, "spear_show": 36, "hop_back": 28, "land_back": 36}, "show_spear": true},
  {"clip": "Cart_Hit", "frames": 28, "loop": false, "root_motion": false, "events": {"impact": 1, "on_rail": 8, "look_back": 13, "fist_shake": [14, 19]}},
  {"clip": "Cart_Fall_Off", "frames": 64, "loop": false, "root_motion": true, "events": {"impact": 1, "leaves_deck": 4, "over_back_edge": 8, "lands_on_road": 17, "still_from": 56}}
 ]}
```

## Checks done (in Blender, not inside UE)

- **Re-import** (`crew_verify.py`: each FBX into an emptied scene, against the already-imported `Riders/<warrior>/Animations/A_<warrior>_Ride.fbx`):
  same armature object scale (1.0), same 80 bone names, root rest identical (difference 0.0), every clip 30 fps (the rider reference
  reports 24), frame counts as authored, re-imported joints vs the .blend: max **0.0065 mm** (every 3rd frame + the last, all 52 clips).
  Bone offsets vs the rider SK bind pose: max 0.0002 mm.
  - The pelvis "rest" of an animation-only FBX re-imports as its own first frame (no BindPose in these files; the rider clips behave the
    same: their pelvis rest is 0.40–0.44 off their own SK rest). So crew vs rider pelvis rests differ (0.34–0.38 in matrix terms); the
    pelvis rest equals each file's own frame 1 to 2e-7. UE uses the curves on the existing skeleton.
- **Stance:** pelvis 0.46–0.53 m in the ride (rest 0.53–0.56; v1 squatted at 0.39–0.48). Knee bend of the straighter leg 4–35° (by
  warrior) at the top of a bounce, 47–60° at the bottom of the deepest dip (f1; v1: 55–96°). Pelvis bob 2.3 cm, head bob 2.6–2.7 cm.
  Fists 0.54–0.70 m high, 7–18 cm behind the front wall's inner face.
- **Wrist:** the spear hand's roll about the shaft is solved over the whole clip (no spinning); forearm twist bones carry 2/3 and 1/3
  of the hand roll. Hand twist vs forearm: ≤ 78° in the rides, ≤ 84° in the throws (female 96°, only at the release frames f12–14),
  bend ≤ 62° (female 71°). Close-ups show no pinched wrist.
- **Head:** face within **62°** of the chest (`spine_05`), measured in the chest's own frame, in every clip; 3D angle incl. nod ≤ 74°.
- **Arms:** single-frame rotations > 40° (against the chest) only in deliberate snaps: the rock whip (f11–12, ≤ 42°), the spear fist
  at the release f12–13 (the wrist snap as the javelin flattens onto the player: 45–65°, city/female `_R` 74–78°) and as the empty
  hand relaxes f15–17 (≤ 47°), the hit impact f2 (≤ 49°), the roar into the first pound (f22, 41°).
- **Joins:** no hand or hip reversal at the starts; the throws melt into the ride's own last frames (hips 2 mm/frame against 3 mm/frame
  of the ride: invisible). `Cart_Hit` and `Cart_Fall_Off` reverse at f1 by design (impact).
- **Clipping against the chariot** (`crew_check.py`, skinned meshes, every frame of all 52 clips; deck floor contact excluded):
  body vs chariot ≤ 11 mm everywhere (worst: `high_warrior` spear throws, a blade edge 9 mm / a finger 11 mm for 1–2 frames; every
  other clip 0). Spear vs chariot: the new spear passes through the quiver while being drawn (`Spear_Cart_Throw_B` f23–27, intended);
  the spear tip touches the front-right rail for 1 frame in `_L` (f4) and the right wall top in `_R` (f5). Spear vs his own body: none,
  except `high_warrior`, the spear butt against his right foot f37–39 as he lands from the hop back.

## Known limitations

- `high_warrior`'s back blades stick 0.6 m out behind him: during the hop-turns they sweep over the quiver and side-wall tops (no
  longer through them by more than 9 mm, he leans into the spins so they tilt up), and they dominate his silhouette from the game
  camera. A shorter blade mesh would help; the SK was not re-exported.
- `_L` / `_R` spear throws: the spare spear appears in the fist at f36 (no reach to the quiver).
- Not tested inside Unreal; the preview's game camera is an approximation (behind and above at about 3.6 m).

## To confirm

- **Chariot scale** in the game (animated at chariot = 2.2 × warrior). The fall's root drop (0.647 m) assumes it.
- **Who rides where:** one warrior per chariot, standing in the middle of the tub (the clips use the whole tub). Spear chariot = `Spear_` set, ramming chariot = unarmed set?
- **Rock or pot** for the unarmed throw (animated as a rock from the belt).
