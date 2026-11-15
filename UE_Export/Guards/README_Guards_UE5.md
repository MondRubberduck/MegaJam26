# Royal Guards → Unreal Engine 5

The heavy guards on the pharaoh's chariot deck. Each guard has 6 clips at 30 fps. They are BP Retarget results of Nils's mocap, then re-animated by hand (v2, after review).

- **Guard2** (royal_guard_2) is the main guard Nils picked.
- **Guard1** (royal_guard_1) is the bonus guard. It has the same clips on its own skeleton.

| What | Where |
|---|---|
| Source | `Worked_Models/Guards_Anims_v2.blend` (armatures `Guard2`, `Guard1`, actions `<Guard>_<Clip>`; `RAW_<Guard>_<Src>` = untouched retargets) |
| Scripts | `Scripts/guards/` (`rebuild_guards.py` rebuilds all clips from the RAW actions; `make_guards.py` also re-runs BP Retarget) |
| Preview | `Worked_Models/Previews/Guards_preview.mp4`: front 3/4 on the left, from behind on the right. Guard2 first, then Guard1 |
| Lineup | `Guards/Guards_lineup.png`: the guards beside the seated pharaoh on his throne. Left half 1.0x, right half 1.2x |

```
Guards/SK_Guard2.fbx                  skeleton + mesh, textures embedded
Guards/SK_Guard1.fbx                  bonus guard: same bone names, different proportions
Guards/Animations/A_Guard2_<Clip>.fbx one clip per file (skeleton only)
Guards/Animations/A_Guard1_<Clip>.fbx
```

## Import (manual: the guards are NOT in `UE_Export/import_manifest.json` / `ue_import.py` yet; the lead agent must add them)

- **Units:** centimetres. The FBX has UnitScaleFactor 1, so import at uniform scale 1.0 with no unit conversion. 30 fps.
- **Skeletons:** import `SK_Guard2.fbx` and `SK_Guard1.fbx` as two skeletal meshes, each creating its **own** skeleton.
  - The bone names match but the proportions differ, so do not share one skeleton.
  - The skeleton has 67 UE5-mannequin bones. There is **no `head` bone** (the head is weighted to `neck_02`).
  - The FBX armature object is called `Armature`.
- **Animations:** import `A_Guard2_*` onto SK_Guard2's skeleton and `A_Guard1_*` onto SK_Guard1's.
  - Animation Length: *Exported Time*. Sample rate: 30.
  - *Enable Root Motion* off for every clip except `Fall_Off` (see below).
- **Facing:** the guards face **+Y in UE mesh space** (−Y in Blender), like the mannequin. Their left side is +X.
  - The Building agent turns the actor to face the player camera. Taunts and throws go forward, at the player.
- **Root:** the `root` bone sits on the deck between the feet and stays at identity in every clip except `Fall_Off`.
  - In the base pose the pelvis is 51 cm above root (Guard1: 49 cm).
- **Blending:** every one-shot except `Fall_Off` starts **and** ends exactly on Idle frame 1 (measured gap 0.0 mm). Use a 0.1–0.2 s crossfade, or none.

## Scale (read this, it matters next to the pharaoh)

- Both guards are **100 cm** in the files, the same as the pharaoh.
- Place them at the **same actor scale as the throne/pharaoh actor**, then add an extra **×1.25** (proposed, **[to confirm]** with Nils).
- At 1:1 a standing guard (94 cm top of head) is no taller than the seated pharaoh (97 cm). At ×1.2 the guards reach 113 cm (`Guards_lineup.png`, right half). At ×1.25 they reach about 118 cm and tower over him.
- **Room per guard**, measured on Guard2 at 1:1 from the Idle feet; multiply by your scale:
  - **Feet:** up to 19 cm forward (Roar stomp), 4 cm back, 8 cm to the side.
  - **Pelvis:** travels 32 cm forward in the Roar lunge.
  - **Hands:** up to 68 cm in front of the root (Beat), 47 cm to the side (Guard1: 49 cm), 45 cm behind, and 109 cm high (Roar, Throw).
  - Place the guards so they do not hit each other or the pharaoh.

## Clips

Events are 1-based frame numbers.

| Clip | Loop | Frames | What happens | Events |
|---|---|---|---|---|
| `Idle` | **yes** (f61 = f1) | 61 | Arms crossed, wide stance. The knees dip twice per loop with the deck, the weight sways, and he holds a glare left and then right. One chest puff with a shoulder roll. | – |
| `Taunt_Roar` | no | 62 | Unfolds his arms and stomps the left foot forward (real step, knee up). He lunges his whole body at the player with both feet planted, then holds a double-biceps **ROAR** with chest heaves and tremble. He rocks back, steps the left foot home and settles. | stomp lands **f9**, loudest pose **f16** (0.5 s), roar held to f30 |
| `Taunt_Beat` | no | 92 | Barbarian beat-down: punch, two hammer fists, then a big **right-fist** smash. The fist lands on the deck and stays there f62–f64, the left arm flung up behind. He holds low, then stands back up. | hits **f14, f34, f46, f62** (f62 = the smash, fist on the deck) |
| `Throw` | no | 64 | Bends down and grabs a rock from the deck with **both hands** at f12. He lifts it to his chest and lets go with the left hand (~f22). Pitcher's leg kick, the rock cocked high behind his head, the left arm aiming at the player. Overhand whip; release to the **right of his face** at f38 with the hand still travelling forward. Follow-through across to the left knee, hands on knees, arms crossed again. | grab **f12**, **release f38**, **right hand** (`hand_r`); can blend out from ~f46 |
| `Hit` | no | 26 | A heavy hit to the chest. Pelvis knocked back 6 cm, knees buckle 7.5 cm, chest arches back, head snaps back, arms burst out of the cross and fly out and back. Short moving hold, an angry head shake and a chest puff, then the arms fold back. | impact **f1**, recoil peak **f3** |
| `Fall_Off` | no | 64 | Blast impact pose (chest caves, arms flung forward, head whips), then thrown off the deck **backwards**. Back flip, lands on his back at f16, tumbles, slows to a stop by about f49 and ends lying face-down. Does not return to Idle. | leaves the deck **f4**, lands **f16**, still from **~f49** |

```json
{"fps": 30, "skeletons": {"Guard2": "SK_Guard2", "Guard1": "SK_Guard1"}, "files": "Animations/A_<Guard>_<Clip>.fbx",
 "clips": [
  {"name": "Idle",       "frames": 61, "loop": true,  "root_motion": false, "events": {}},
  {"name": "Taunt_Roar", "frames": 62, "loop": false, "root_motion": false, "events": {"stomp": 9, "roar_peak": 16, "roar_end": 30}},
  {"name": "Taunt_Beat", "frames": 92, "loop": false, "root_motion": false, "events": {"hit": [14, 34, 46, 62], "smash": 62}},
  {"name": "Throw",      "frames": 64, "loop": false, "root_motion": false, "events": {"grab": 12, "release": 38, "blend_out_from": 46}, "hand": "hand_r"},
  {"name": "Hit",        "frames": 26, "loop": false, "root_motion": false, "events": {"impact": 1}},
  {"name": "Fall_Off",   "frames": 64, "loop": false, "root_motion": true,  "events": {"leaves_ground": 4, "lands": 16, "still": 49}}]}
```

### Throw: the projectile

- **The rock:** spawn or show it at **f12** between the hands (a socket on `hand_r` about 6 cm out along the bone works; both fists sit on it until ~f22). It is carried by `hand_r` until the release.
- **Release:** **f38** from `hand_r`. The hand is then about 27 cm to his right, 24 cm in front of the root and 92 cm up (Guard2; UE mesh space X −27, Y +24, Z 92 cm at 1:1; Guard1: X −28, Y +20, Z 93).
- **Hand speed:** into the release about 28 cm per frame forward and 7 cm per frame down. Aim the projectile straight at the player.
- **Follow-through:** after the release the hand keeps moving forward (16 cm, then 5 cm per frame) while it sweeps down across his body.

### Fall_Off root motion

- **Travel:** `root` carries the travel: **4.37 m backwards** (away from the player, −Y in UE mesh space) and 0.65 m to his right. Guard1: 4.15 m and 0.62 m.
- **Root path:** smoothed, Z = 0. The pelvis carries the height and peaks 91 cm above root at about f9.
- **Deck contact:** nothing goes below the deck (checked on the skinned mesh). He lands at the height he started on.
- **Using it:** use root motion, or detach the guard from the deck and let the clip carry him. To drop him onto the road, also lower the actor (deck height is **[to confirm]**).

## Checks done (in Blender, not inside UE)

- **Re-import:** every FBX was re-imported: armature scale 0.01 (cm file), height 1.00 m, 67 bones, root rest scale 1, 30 fps, frame counts match, joint error under 0.01 mm. `Fall_Off` is included, so the root travel survives.
- **Feet:** planted feet do not move; each relocation is a real step with a lift. Soles sit on the deck. Heel cuffs graze at most 7 mm into the deck in the deepest knee bends.
- **Arms:** single-frame arm rotations above 35° happen only in the deliberate snaps: the Throw whip (f37–f38), the Hit burst (f2–f4), the Fall_Off blast (f2–f3) and the Beat smash (f60–f62).
- **Idle loop:** no seam (frame-to-frame steps are the same size across the loop point).

## To confirm

- **The thrown object:** animated as a rock grabbed from the deck with both hands and thrown with the right hand. A spear held from the start would need a different grab.
- **Scale:** ×1.25 on top of the throne/pharaoh actor scale (proposed).
- **Deck height and size:** should `Fall_Off` drop below deck level onto the road? How many guards stand on the deck, and which mesh goes where?
