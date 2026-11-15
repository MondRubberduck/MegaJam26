# Royal Guards → Unreal Engine 5

The heavy guards on the pharaoh's chariot deck. Each guard has 6 clips at 30 fps. They are BP Retarget results of Nils's mocap, then re-animated by hand (v2, after review).
`Throw` was redone in v3 (15 Nov): a heavy two-handed overhead heave of a **big log**, which comes with its own prop files (see "Throw: the log").
v3.1 (same day, after review): the hands now hold the log from **underneath** (palms under it), the lift is slow and heavy, and the log leaves the hands **rising**. The clip is now **78 frames** with new events (grab f9, release f58).

- **Guard2** (royal_guard_2) is the main guard Nils picked.
- **Guard1** (royal_guard_1) is the bonus guard. It has the same clips on its own skeleton.

| What | Where |
|---|---|
| Source | `Worked_Models/Guards_Anims_v3.blend` = v2 + the v3 `Throw` and the log (mesh `Wood_Mesh`; objects `Wood_<Guard>_InHand` / `_Deck` / `_Thrown` for viewing). Armatures `Guard2`, `Guard1`, actions `<Guard>_<Clip>`; `RAW_<Guard>_<Src>` = untouched retargets |
| Scripts | `Scripts/guards/` (`rebuild_guards.py` rebuilds all clips from the RAW actions; `make_guards.py` also re-runs BP Retarget; `make_throw_wood2.py` rebuilds the v3.1 `Throw` + log on v3 (builder `build_throw_wood2.py`), export with `export_throw_wood.py`) |
| Preview | `Worked_Models/Previews/Guards_preview.mp4`: front 3/4 on the left, from behind on the right. Guard2 first, then Guard1. **Both guards' Throw segments there are outdated** (old rock throw). `Guards_Throw_Wood_preview.mp4`: the v3.1 log Throw, game view left, side right; there the flying log is aimed at the camera (preview only) |
| Lineup | `Guards/Guards_lineup.png`: the guards beside the seated pharaoh on his throne. Left half 1.0x, right half 1.2x |

```
Guards/SK_Guard2.fbx                  skeleton + mesh, textures embedded
Guards/SK_Guard1.fbx                  bonus guard: same bone names, different proportions
Guards/Animations/A_Guard2_<Clip>.fbx one clip per file (skeleton only)
Guards/Animations/A_Guard1_<Clip>.fbx
Guards/SK_Wood_Guard2.fbx             the log in Guard2's hands: skinned 100 % to hand_r on Guard2's skeleton (Leader Pose prop)
Guards/SK_Wood_Guard1.fbx             the same for Guard1
Guards/Props/SM_Wood.fbx              the log as a static mesh (the projectile), cm, origin = centre of the grip, long axis = local X
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
- **Log props:** import `SK_Wood_Guard2.fbx` as a skeletal mesh using SK_Guard2's skeleton (same 67 bones and rest pose), `SK_Wood_Guard1.fbx` with SK_Guard1's.
  Import `Props/SM_Wood.fbx` as a static mesh. Same units as above (scale 1.0, no conversion). Textures are embedded.
  - On each skeleton add a socket **`Wood` on `hand_r`** (values in "Throw: the log"). The thrown log spawns there.
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
  - **Hands:** up to 68 cm in front of the root (Beat), 47 cm to the side (Guard1: 49 cm), 45 cm behind, and 109 cm high (Roar).
  - **The log (Throw):** 114 cm long. In the hands it sweeps up to 63 cm to each side, 52 cm behind and 42 cm in front of the root, and up to 129 cm high (Guard1: 63, 53, 40, 130 cm). On the deck it lies across, 25 cm in front of the root (Guard1: 24 cm). The left foot stomps 13 cm forward.
  - Place the guards so they do not hit each other or the pharaoh.

## Clips

Events are 1-based frame numbers.

| Clip | Loop | Frames | What happens | Events |
|---|---|---|---|---|
| `Idle` | **yes** (f61 = f1) | 61 | Arms crossed, wide stance. The knees dip twice per loop with the deck, the weight sways, and he holds a glare left and then right. One chest puff with a shoulder roll. | – |
| `Taunt_Roar` | no | 62 | Unfolds his arms and stomps the left foot forward (real step, knee up). He lunges his whole body at the player with both feet planted, then holds a double-biceps **ROAR** with chest heaves and tremble. He rocks back, steps the left foot home and settles. | stomp lands **f9**, loudest pose **f16** (0.5 s), roar held to f30 |
| `Taunt_Beat` | no | 92 | Barbarian beat-down: punch, two hammer fists, then a big **right-fist** smash. The fist lands on the deck and stays there f62–f64, the left arm flung up behind. He holds low, then stands back up. | hits **f14, f34, f46, f62** (f62 = the smash, fist on the deck) |
| `Throw` | no | 78 | **Two-handed log heave.** Dives into a deep squat; palms on the near side of a big log lying across the deck, fingers hooked under it (grab f9). Strains with a body shake and one failed pull: the log comes up 5 cm and thumps back (f12–f16); the head comes up to the camera. Slow, heavy lift with his hands under the log, swinging it round his knees. A hip pop rolls it onto his palms at collarbone height (rack, f34). Presses it overhead with a stall at the forehead (f41–f43). Leans back with the log above and behind his head, tilted, with the left knee up. Holds this wind-up with a tremble (f51–f55). Stomps forward (f57) and heaves it over the top. **Release f58 above his head, rising about 12° toward the player**, hands at full speed. The arms keep going through toward the camera into a deep bow (torso about 47°, right heel up). Holds a breath, steps back, crosses his arms. Both hands stay on the log from grab to release. | grab **f9**, stomp f57, **release f58**; the log rides on `hand_r` (`SK_Wood_<Guard>`); can blend out from ~f70 |
| `Hit` | no | 26 | A heavy hit to the chest. Pelvis knocked back 6 cm, knees buckle 7.5 cm, chest arches back, head snaps back, arms burst out of the cross and fly out and back. Short moving hold, an angry head shake and a chest puff, then the arms fold back. | impact **f1**, recoil peak **f3** |
| `Fall_Off` | no | 64 | Blast impact pose (chest caves, arms flung forward, head whips), then thrown off the deck **backwards**. Back flip, lands on his back at f16, tumbles, slows to a stop by about f49 and ends lying face-down. Does not return to Idle. | leaves the deck **f4**, lands **f16**, still from **~f49** |

```json
{"fps": 30, "skeletons": {"Guard2": "SK_Guard2", "Guard1": "SK_Guard1"}, "files": "Animations/A_<Guard>_<Clip>.fbx",
 "clips": [
  {"name": "Idle",       "frames": 61, "loop": true,  "root_motion": false, "events": {}},
  {"name": "Taunt_Roar", "frames": 62, "loop": false, "root_motion": false, "events": {"stomp": 9, "roar_peak": 16, "roar_end": 30}},
  {"name": "Taunt_Beat", "frames": 92, "loop": false, "root_motion": false, "events": {"hit": [14, 34, 46, 62], "smash": 62}},
  {"name": "Throw",      "frames": 78, "loop": false, "root_motion": false, "events": {"grab": 9, "stomp": 57, "release": 58, "blend_out_from": 70},
   "hand": "hand_r", "prop_in_hand": {"Guard2": "SK_Wood_Guard2", "Guard1": "SK_Wood_Guard1"}, "projectile": "SM_Wood",
   "projectile_socket": {"bone": "hand_r", "name": "Wood"}, "deck_prop": "SM_Wood"},
  {"name": "Hit",        "frames": 26, "loop": false, "root_motion": false, "events": {"impact": 1}},
  {"name": "Fall_Off",   "frames": 64, "loop": false, "root_motion": true,  "events": {"leaves_ground": 4, "lands": 16, "still": 49}}]}
```

### Throw: the log

- **The prop:** a rough-hewn log, 114 × 17.5 × 17 cm, 42 vertices, small painted wood texture (embedded). No letters or logos.
  - `SK_Wood_<Guard>.fbx`: the log in that guard's right hand, every vertex 100 % on `hand_r`.
  - `Props/SM_Wood.fbx`: the same log as a static mesh. Origin = centre of the grip (the middle of the log), **long axis = local X**, the hands' side = local +Z.
- **Setup per guard:**
  - `SK_Wood_<Guard>`: a second Skeletal Mesh Component under the guard's mesh. Set **Leader Pose Component = the guard's mesh** and **Use Bounds From Leader Pose Component = true**. Without that, its bounds stay at the rest-pose hand, so the log can be culled or lose its shadow when it is overhead. Hidden by default.
  - **Deck log:** an `SM_Wood` attached to the guard's mesh component at the deck transform below. Hidden by default.
  - **Socket `Wood` on `hand_r`** in each skeleton, with this relative transform (cm, degrees):

    | Guard | Location | Rotation (Pitch, Yaw, Roll) | X axis | Z axis |
    |---|---|---|---|---|
    | Guard2 | (14.63, −9.21, −1.45) | (36.48, −14.97, −7.32) | (0.7768, −0.2077, 0.5945) | (−0.6025, 0.0292, 0.7976) |
    | Guard1 | (14.68, −6.77, −6.26) | (15.05, −4.45, −0.92) | (0.9628, −0.0749, 0.2597) | (−0.2601, 0.0042, 0.9656) |

    These values come from the FBX bone frame (bones exported with primary axis Y and no axis correction; Unreal mirrors Y). They were checked only in Blender.
    **Check them once in the Skeleton editor:** put `SM_Wood` on the socket as a preview asset and `SK_Wood_<Guard>` on as a preview mesh, then play `A_<Guard>_Throw`. From f9 to f57 the two logs must overlap exactly. If they do not, spawn with the component-space check values under "Release" instead.
- **Montage start (f1):** show the deck log. It is the default, because a 114 cm log popping out of nothing at his feet would be very visible.
- **Grab, f9:** hide the deck log and show `SK_Wood_<Guard>`. Both are in the same place (within 0.1 mm), so the swap does not show. Both palms are on the near side of the log with the fingers hooked under it. From here to the release the log is exactly where the hands hold it (the left hand is locked to it too).
- **Release, f58:** hide `SK_Wood_<Guard>` and spawn `SM_Wood` at `Mesh->GetSocketTransform("Wood", RTS_World)`. Read the socket when the notify fires, not from a stored value.
  - That is where the in-hand log is on that tick, so there is no hitch if the notify is handled a tick late or the montage is played at another rate or blended.
  - The socket transform already includes the actor and component scale. Spawn with it as it is and do not scale it again.
  - Check values: the in-hand log at f58 relative to the guard's mesh component (Unreal axes, cm, at scale 1):

    | Guard | Location (cm) | Rotator (Pitch, Yaw, Roll) | Log X axis (long axis) | Log Z axis |
    |---|---|---|---|---|
    | Guard2 | (0.0, −2.0, 113.9) | (−6.86, 3.40, 124.63) | (0.9911, 0.0589, −0.1194) | (−0.1166, 0.8173, −0.5642) |
    | Guard1 | (0.0, −1.9, 109.1) | (−11.65, 4.86, 122.29) | (0.9759, 0.0830, −0.2019) | (−0.1791, 0.8332, −0.5232) |

    If the rotator convention is in doubt, build the rotation from the two axes (`FRotationMatrix::MakeFromXZ(X, Z)`).
- **Launch:** the log leaves the palms above his head, **rising**.
  - Guard2: (2.7, +548.6, +108.4) cm/s in component space, 5.6 m/s, 11° up. Guard1: (0, +531.1, +129.2) cm/s, 5.5 m/s, 14° up.
  - Spin about its own long axis: about 350°/s (Guard1 345°/s).
  - These are at actor scale 1: **multiply the velocity by the actor scale** (×1.25 gives about 7 m/s).
  - Aim, speed and gravity are game-side. Aim at the player and keep it rising for its first frames. The preview aims it at the camera at about 16° up, with gravity 4.9 m/s².
- **Hand speed:** the hands are fastest at the release (about 20 cm per frame, f57–f58). Afterwards they keep travelling at 14, 13 and 12 cm per frame, then ease into the bow (10 down to 2 cm per frame by f69).
- **Deck log transform** (relative to the mesh component, at scale 1): location (0, +25.0, 8.8) cm (Guard1 (0, +23.9, 8.8)), rotator (0, 0, −90) [X axis (1, 0, 0), Z axis (0, −1, 0)].

### Fall_Off root motion

- **Travel:** `root` carries the travel: **4.37 m backwards** (away from the player, −Y in UE mesh space) and 0.65 m to his right. Guard1: 4.15 m and 0.62 m.
- **Root path:** smoothed, Z = 0. The pelvis carries the height and peaks 91 cm above root at about f9.
- **Deck contact:** nothing goes below the deck (checked on the skinned mesh). He lands at the height he started on.
- **Using it:** use root motion, or detach the guard from the deck and let the clip carry him. To drop him onto the road, also lower the actor (deck height is **[to confirm]**).

## Checks done (in Blender, not inside UE)

- **Re-import:** every FBX was re-imported: armature scale 0.01 (cm file), height 1.00 m, 67 bones, root rest scale 1, 30 fps, frame counts match, joint error under 0.01 mm. `Fall_Off` is included, so the root travel survives. The v3.1 `Throw` files were compared on every frame (78 frames, joint error at most 0.002 mm).
- **Feet:** planted feet do not move; each relocation is a real step with a lift. Soles sit on the deck. Heel cuffs graze at most 7 mm into the deck in the deepest knee bends.
- **Arms:** single-frame arm rotations above 35° happen only in the deliberate snaps: the Hit burst (f2–f4), the Fall_Off blast (f2–f3) and the Beat smash (f60–f62).
  - In the v3.1 Throw these are: the arms flung out of the cross into the dive (f4–f7, up to 47°), the clean pop (f32–f34, up to 48° on Guard1), and the release whip (f57–f58, up to 46°).
  - After the release no arm step is over 25° until the arms cross again (f75–f76, 32°).
- **Throw (v3.1):**
  - **Grip:** both hands are locked to the log from f9 to f58 (0.0 mm grip error). The palms are on the near side of the log on the deck. From lift-off the palms are under it while it is below the shoulders (palm normal 45° or more up from f24, fully up at the rack). Overhead it rests on the palms.
  - **Wrists:** wrist angle at most 87° (Guard1 95°) in the held wind-up, counting the hands' 25–30° rest bend. Forearm twist at most 50° (Guard1 73°), spread over the twist bones.
  - **Speeds (log centre, cm per frame):** lift peak 4.3; press peak 8.3 with a stall of 1.8–3.4 at the forehead; clean pop 14; heave 21.5 at the release, the fastest move of the clip.
  - **Contacts:** the log only grazes the body: the left forearm by up to 11 mm while it lies against the log, the thigh and forearm by up to 21 mm (Guard1 upper arm 25 mm) for one frame each while the log rolls up the body in the clean. The thumbs and fingers stay on the surface (up to 3 mm in). On the deck the log's lowest corner dips up to 5 mm as the hands roll it at lift-off (f20).
  - **Head and body:** the head stays within 60° of the chest and at least 4.4 cm from the log. No body bone turns more than 30° in a frame.
  - **Feet:** the stomp is a real step with the sole on the deck. The right heel lifts 5 cm (Guard1 4 cm) in the follow-through with the toe planted. Heel cuffs graze at most 7 mm into the deck.
  - **Ends:** starts and ends exactly on Idle f1.
- **Log props (re-imported):** `SK_Wood_<Guard>` has the same 67 bone names and rest pose as `SK_<Guard>` (0 error).
  - Skinned with the clip's `hand_r` on every frame from f9 to f57, it matches the .blend log within 0.002 mm.
  - `SM_Wood` placed with the release and deck transforms above lands within 0.1 mm of the in-hand log. The socket values rebuild the grip within 0.1 mm.
  - `SM_Wood` is a cm file with its long axis along X.
- **Idle loop:** no seam (frame-to-frame steps are the same size across the loop point).

## To confirm

- **The deck log:** it is now shown by default from the montage start to the grab. Open question: does a pile of logs stay on the deck between throws, or does each throw bring its own log?
- **The log's flight:** aim, speed, gravity and spin are game-side; the numbers above are what the hands give it (11–14° up at 5.5 m/s, at scale 1).
- **Scale:** ×1.25 on top of the throne/pharaoh actor scale (proposed).
- **Deck height and size:** should `Fall_Off` drop below deck level onto the road? How many guards stand on the deck, and which mesh goes where?
