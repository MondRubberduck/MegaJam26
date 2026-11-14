# Camel riders → Unreal Engine 5 (v2: directions + spear set)

Four warriors with **24 rider clips each**, a spear per warrior, and the three camels with their run loop.
Source file: `Worked_Models/Camel_Riders.blend`. Preview: `Worked_Models/Previews/Camel_Riders_v2_preview.mp4`.

```
Riders/<warrior>/SK_<warrior>.fbx                  Peasant_warrior, city_warrior, female_warrior, high_warrior
Riders/<warrior>/SK_Spear_<warrior>.fbx            spear skinned to that warrior's hand_r (use with Leader Pose)
Riders/<warrior>/Animations/A_<warrior>_<Clip>.fbx the 24 clips below
Riders/Props/SM_Spear.fbx                          static spear for the thrown projectile
Camels/<camel>/SK_<camel>.fbx + Animations/A_<camel>_Run.fbx
```

**Automatic import:** `../ue_import.py` (see `../AGENT_README.md`).

**Frame rate:** everything is **30 fps**. Import each warrior with its own skeleton (mesh first, then select all
its `A_*` files and pick that skeleton). Import `SK_Spear_<warrior>` onto the **same** skeleton.

## Directions

Riders show up all around the player, so every attack and taunt comes in three versions:

| Suffix | Player is… | Rider turns… |
|---|---|---|
| `_B` | behind the camel (the usual camera view) | around over his right shoulder |
| `_L` | on the rider's left | to his left |
| `_R` | on the rider's right | to his right |

`Damage_*` and `Death_*` use the same suffixes for where the **hit comes from**. `Death_L` is hit from the left,
so he flies off the camel's right side.

## Clips

**Unarmed set** (free right hand: fist shaking, rock throws, thigh slaps)

| Clip | Frames | What happens |
|---|---|---|
| Ride | loop 19 | Bouncing with the saddle, reins forward, whooping fist swirl |
| Ride_Look_L / _R | loop 19 | Riding while glaring at the player, shaking a fist |
| Taunt_B | 54 | Double "nyah-nyah" (thumb on nose, fingers wiggling, head waggling), then a belly laugh with thigh slaps |
| Taunt_L / _R | 54 | The chicken: hands in armpits, elbows flapping, head pecking; then points at you and laughs |
| Throw_B / _L / _R | 36 | 1.5-turn windmill rock throw, **release frame 13**, then a cheeky "gotcha" fist pump |
| Damage_B / _L / _R | 30 | Shoved away from the hit, head whips, arms fling, butt pops up; then a dizzy head wobble |
| Death_B | 54 | Knocked backwards over the camel's rear; lands behind it on frame 31; spread-eagled |
| Death_L / _R | 54 | Launched off the opposite side, rolling like a log in the air; lands beside the camel; spread-eagled |

**Spear set** (spear in the right hand; no thigh slaps, no free-hand gags)

| Clip | Frames | What happens |
|---|---|---|
| Spear_Ride | loop 19 | Spear held out to the side and pumped twice per stride ("whoop whoop") |
| Spear_Ride_Look_L / _R | loop 19 | Spear lowered two-handed and jabbing toward the player |
| Spear_Taunt_B | 54 | War cry with the spear shaken overhead in both hands, then chest pounding with the spear raised |
| Spear_Taunt_L / _R | 54 | Jabs the spear at you while beckoning "come here", then stamps the spear butt three times and cackles |
| Spear_Throw_B / _L / _R | 36 | Javelin: aims with the free hand, hurls on **frame 13**, then an "oops, it's gone" shrug |

`Damage_*` and `Death_*` work for both sets (drop or hide the spear on death).

Which rider is armed is up to the game: any warrior can play either set. (The stray pole on `Peasant_warrior`'s back,
meant to be a scarf, has been removed from his export.)

## The spear in UE (no socket math)

1. Add a second **Skeletal Mesh Component** to the rider Blueprint with `SK_Spear_<warrior>`.
2. Set its **Leader Pose Component** to the warrior's mesh. The spear now follows `hand_r` in every clip.
3. **Unarmed riders:** hide the spear. **Spear throws:** hide it on frame 13 and spawn `SM_Spear` as the projectile
   from the spear's current transform. In `SM_Spear` the shaft runs along its Z axis and the origin is the grip
   point.

## Scale, socket and sync (unchanged from v1)

- **Scale:** the warriors are 1 m tall; the clips are animated for the rider at **1.5× relative to the camel**.
- **Socket:** attach to the camel bone **`ORG-Sitting_Root`**.
  - The bone points straight up, so make a Skeleton Socket on it with a **90° rotation**. Use a warrior as Preview
    Asset and rotate until he sits upright, facing the camel's head.
  - Optional yaw to square the riders up: Low −6.7°, Mid −4.8°, High −1.8°.
- **Sync:** all `Ride*` loops are **18 frames = one camel stride** (`A_Camel_*_Run` is also 18 frames at 30 fps).
  Start rider and camel together (or in one Sync Group) at the same play rate.
- **Root motion:** none anywhere.

## Anim Blueprint tips

- **Base loop:** a `Ride` / `Ride_Look_L` / `Ride_Look_R` blend picked by where the player is (or the `Spear_` versions).
- **One-shots:** Taunts, Throws and Damage play as **Montages** on an upper-body slot (*Layered blend per bone* from
  `spine_01`), so the legs stay locked to the stride. They also work full-body.
- **Deaths:** full body.
  - **Simple:** keep him attached and hide him right after landing (frame 31 for `Death_B`, about the same for the side
    deaths).
  - **Nicer:** detach him (`KeepWorld`) on frame 1 so the camel runs out of frame while he falls.

## Changes to the warrior meshes (exported copies only)

The originals in `Generated_Mesh/Characters` are untouched. In the exported files:

- The back blades (`high_warrior`) are skinned rigidly to `spine_05`; the stray back pole on `Peasant_warrior` was deleted.
- Cloak flaps that hung far from the arm bones now follow the upper back, so raised arms don't tear the cloth.

## Re-exporting / changes

- Generator: `Scripts/camel_riders/rider_clips2.py`, on top of `rider_clips.py` (bounce layer, base pose, `Death_B`).
- Base pose: `rider_pose_ride.json`. Solver: `rider_rig.py` (includes the `grip_r` control that aims the spear).
- Build: `R25_build_v2.py`. Export: `X14_export_v2.py`. Spear prop: `S02_spear.py`.
- Checked in Blender (re-imported every file: curves match the source, spears sit in the fist), not inside UE.
