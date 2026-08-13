# Model-first design handoff

Status: **geometry review pending; photoreal generation gate is blocked**

The owner's bird's-eye markup is the orientation authority:

[`uploads/site-reference/birdseye-orientation-markup.png`](uploads/site-reference/birdseye-orientation-markup.png)

- **x=0:** valley-facing full glass gable and double-height living room;
- **x=17:** ground-floor master bedroom with open mezzanine above;
- **z=0:** shared tractor-lane wall;
- **z=7.5:** cobbled courtyard wall with the entrance near the rear/service transition.

From a camera at the valley glass gable looking inward, the lane, kitchen and
stair appear on the **left**; the courtyard and entrance appear on the
**right**.

## Source of truth

1. [`models/design.json`](models/design.json) — dimensions, axes, rooms,
   openings, doors, stair, mezzanine, fixtures and fixed cameras.
2. [`models/gen_model.py`](models/gen_model.py) — deterministic generator and
   validator.
3. Generated geometry and drawings are downstream outputs; do not edit them by
   hand.

Run:

```sh
python3 models/gen_model.py
python3 models/gen_model.py --check
```

## Stair geometry encoded

- type: two-flight dog-leg / U-turn stair against the tractor-lane wall;
- floor-to-floor: 2.45 m;
- 14 risers at 175 mm: 6 lower + 8 upper;
- going: 270 mm; 2R+G = 620 mm;
- clear flight width: 1.00 m;
- half-landing at the tall lane window, then 180-degree return;
- protected top landing connects inside the rear mezzanine;
- assumed half-landing headroom: 2.194 m at the lowest landing edge under assumed roof build-up.

This is coherent concept geometry, not a code or permit certification. A
measured survey and architect must verify the roof section, stair headroom,
guards, fire strategy, structure and all wall build-ups.

## Sanitary brief encoded

- one WC in the home, located in the separate powder room with a hand basin;
- no WC in the master ensuite;
- master ensuite contains the threshold-free Italian shower and vanity.

Any future plan or render showing a second toilet conflicts with
`models/design.json` and must be corrected.

## Rendering gate

For every future photoreal concept:

1. Decide whether the request changes geometry.
2. **Structural change:** update `design.json`, regenerate, validate, review the
   fixed-camera model view, then render.
3. **Non-structural change:** keep `design.json` unchanged and pass the existing
   fixed-camera model view for the proposed angle as the structural reference.
4. Every image prompt must say that model geometry, opening count/positions,
   stair topology, room boundaries, camera and perspective are locked.
5. A photoreal image never becomes geometry authority. If it conflicts with the
   model, reject or regenerate it.

The explicit gate is currently:

```json
"geometry_approved_for_photoreal": false
```

Revision 08-rear-window-review is awaiting owner approval; 07-photoreal-approved remains the last approved photoreal authority. Do not generate revised photoreal concepts until the regenerated model views and plans are approved.
