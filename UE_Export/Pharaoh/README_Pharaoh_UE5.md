# Pharaoh → Unreal Engine 5

The end boss on top of his chariot: 7 clips (30 fps), all authored **on his throne**. Retargeted from Nils's prepared clips with
BP Retarget, then reworked by scripts (v2, after review on 15 Nov).

- **Source file:** `Worked_Models/Pharaoh_Anims.blend` (actions `Pharaoh_<Clip>`; the raw BPR retargets are kept as `RTH_*`)
- **Preview:** `Worked_Models/Previews/Pharaoh_preview.mp4` (left: front 3/4, right: from behind; in the deaths the right view follows him)
- **Scripts:** `Scripts/pharaoh/` (`build_all.sh` rebuilds everything; `ph_clips.py` holds every clip)

```
Pharaoh/SK_Pharaoh.fbx                   skeleton + mesh, textures embedded, 100 cm tall
Pharaoh/Animations/A_Pharaoh_<Clip>.fbx  one clip per file (skeleton only)
```

## Format

- **Centimetres, 30 fps.** FBX unit scale 1 (cm): import with no conversion. In Blender the character is 1 m tall.
- **Skeleton:** UE5-mannequin names, 67 bones. There is **no `head` bone**: the head is weighted to `neck_02`.
- **Facing:** Blender −Y, like the other characters in `UE_Export`. In the game, turn the actor so he **faces the player**:
  the cast and the taunts go forward, `Death_R` flies to the player's screen right, `Death_L` to screen left.

## Placing him on the throne (read this)

Every clip is authored with the throne mesh (`Vehicles/Pharao_Chariot/Pharao_Throne/tripo_convert_ac75…fbx`) at **1:1**.
Both are 100 cm tall in their source files.

- **Actor origin = the throne's pivot** (bottom centre of the throne mesh). Put the pharaoh actor at the throne's pivot, with the
  throne's rotation and the **same scale as the throne actor**.
- The `root` bone's rest position is **3.7 cm toward his back** of the actor origin (and 0.2 cm to his left), at floor height.
- Seated (every clip's first frame = `Sit_Idle` frame 1), measured **from the actor origin**:
  - pelvis bone **53.8 cm up** and **4.7 cm toward his back** (that is 0.95 cm toward his back of the `root` bone);
  - seat top 44 cm up; ankles 22 cm up, feet on the throne's lower step (step top 14 cm).
  - All values are for a 100 cm pharaoh: scale them with the actor.
- **In-place clips:** `root` never moves except in the two deaths. Standing up in `Taunt_Flex` moves the pelvis (about 25 cm forward
  onto the step, pelvis up to 68 cm), not the root.

## Clips

| Clip | Type | Frames | What happens | Events (1-based frames) |
|---|---|---|---|---|
| `Sit_Idle` | **loop: yes** | 151 (150 + last = first) | Bored, arrogant king: chin on his right fist (elbow on the armrest), left hand on the left armrest. Lifts his head off the fist and looks down his nose to his left, sits up, sinks back onto the fist and re-settles, drums his left fingers on the armrest, sighs. Breathes throughout | head up/turn f13–f33 (moving hold to f61), "hmph" f53, back on the fist f63–f85, re-settle f81–f96, finger taps f99 / f105 / f111 / f119, sigh f119–f147 |
| `Cast` | one-shot | 32 (1.07 s) | Sits up, gathers, leans back hunched with the fists at his chest and **trembles** (charge), then **whips** both arms up into a V with open palms toward the player, chest thrown forward. **Peaks on the last frame** | gather f1–f8, charge f8–f19, whip f19–f30 (arms arrive f30, small overshoot), **peak = f32: spawn the spell here** |
| `Cast_End` | one-shot | 16 (0.53 s) | Back from the `Cast` peak to the idle: arms drop forward and outward, left hand lands on the armrest first, the right fist reaches the chin last and the head dips onto it, torso sinks back with a small overshoot | starts = `Cast` f32 exactly, left hand lands f11, fist on chin f14, **ends = `Sit_Idle` f1** |
| `Taunt_Flex` | one-shot | 114 (3.8 s) | Lurches forward, rises off the throne with both fists thrown overhead, double-biceps pose, arms spread, a crouching "most muscular" crab, then sits back down and settles | standing f19, double biceps f34–f49, crab f70–f87, starts sitting f88, seat contact ~f109 |
| `Flinch` | one-shot | 44 (1.47 s) | Disgust or hit reaction, **nose in the air**: head snaps away to his left with the chin up (face stays visible), leans back, right hand up palm-out ("ugh, stop!"), left hand grips the armrest; a shiver, two "shoo" pushes, back to the idle | recoil peak f5–f6, shiver f12–f19, shoo f16 / f20, return f27–f42 (fist on chin last, f42), settled f44 |
| `Death_R` | one-shot | 61 (2 s) | Blown off the throne: launched up and **to the player's screen right**, cartwheels in a spread-eagle X past the apex, flails (windmilling arms, kicking legs) and falls **beside** the chariot, still spinning. **Travel is on `root`** | blast f1, clear of the throne ~f5, spread-eagle f10–f30, apex ~f23, passes throne-base height ~f45, last frame f61 (still falling) |
| `Death_L` | one-shot | 61 (2 s) | The same to the player's **screen left** (mirrored arc and spin) | as `Death_R` |

- **Blending:** every one-shot starts exactly on `Sit_Idle` frame 1. `Cast_End`, `Taunt_Flex` and `Flinch` also end exactly on it:
  blend in and out with a short crossfade (0.1–0.2 s). **`Cast` ends at its peak:** play `Cast_End` straight after it (its first frame
  is `Cast`'s last frame), or hold the peak and then play `Cast_End`.
- **Death root motion:** `root` travels in his own frame (side = toward his left for `Death_R`, toward his right for `Death_L`;
  back = opposite to his facing). Values from the start, in metres (×100 for cm), ballistic arc:

  | Frame | Side | Back | Up |
  |---|---|---|---|
  | f7 | 0.13 | 0.09 | +0.80 |
  | f13 | 0.57 | 0.40 | +1.42 |
  | f25 | 1.52 | 1.07 | +1.84 (apex ~f23) |
  | f31 | 2.00 | 1.40 | +1.62 |
  | f46 | 3.19 | 2.23 | −0.14 |
  | f61 | 4.37 | 3.06 | −3.64 |

  - Keep **Enable Root Motion off** (the default) so he visibly flies away while the actor stays on the chariot.
  - **Bounds:** he ends up to 6.5 m from the actor origin. Keep **Create Physics Asset** on at import (the bounds then follow the bodies)
    or raise the mesh's **Bounds Scale**, otherwise Unreal can cull him while he flies.
  - At frame 61 he is still falling, 3.6 m below the throne base. Hide or despawn him there, or hand over to an effect or ragdoll.
  - Pick `Death_R` or `Death_L` so he falls on the open side (both clear the chariot body sideways from about f35 when it is
    about 4 m wide; checked with the chariot body at an assumed 4× scale).

## Notes

- **Where each clip comes from:**
  - `Sit_Idle`: the chin-on-fist pose of `Pharao_SitIdle` (an almost static pose), fitted to the throne, with the motion added by hand.
  - `Cast` and `Cast_End`: key poses after `Pharao_Flex` (arms up, fists while charging, Flex's fist shape) with an added gather, charge,
    whip and return.
  - `Taunt_Flex`: `Pharao_Flex` frames 16–100, with the double-biceps hold shortened. The stand-up and sit-down are added; the feet stay
    planted on the step.
  - `Flinch`: re-posed after `Pharao_Flinch` (lean back, head turned away, hand raised palm-out), seated.
  - `Death_R` / `Death_L`: the blast arch from the second half of `Pharao_Explosion` (frames 148–153), then an added spread-eagle,
    flailing and a ballistic cartwheel arc.
- **Not delivered:** `Stand_Idle` (`Taunt_Flex` gets up and sits back down by itself) and a single `Death` (replaced by `Death_R` / `Death_L`).
- **Throne contact:** every frame was checked against the throne mesh: at most 1.3 cm of contact compression (butt on the seat, heel
  strap on the step). The right elbow rests on the armrest (about 1 cm gap).
- **Hands:** his hands are mittens; fingers stay near their rest shape (fists at 60% of the source curl, open palms in the cast).
- **Testing:** checked in Blender, not inside UE. Every FBX was re-imported: cm file, 100 cm tall, 67 bones, root scale 1, 30 fps,
  frame counts match, joint positions match the .blend exactly.
