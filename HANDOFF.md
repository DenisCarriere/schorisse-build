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

The full-width courtyard photograph is the site-and-camera authority for the
side entrance elevation:

[`uploads/site-reference/photo-5-courtyard-full-width.jpg`](uploads/site-reference/photo-5-courtyard-full-width.jpg)

Its complete 17 m wall, clipped hedge geometry, central cobbled approach,
hydrangeas, mature tree trunks and canopy must be retained in that camera. Use
[`models/generated/courtyard-full-width.svg`](models/generated/courtyard-full-width.svg)
for the proposed window and entrance positions.

Photo 1 is the site-and-camera authority for the shared tractor lane:

[`uploads/site-reference/photo-1-shared-laneway.jpg`](uploads/site-reference/photo-1-shared-laneway.jpg)

The camera stands at the **valley/pasture end** and looks back along the lane
toward the rear gate. The full-height valley glass is therefore nearest and
must be visible. Along the lane, the opening order recedes as kitchen picture
window, tall stair window, then the two master-bedroom windows. The private
mezzanine gable is at the far opposite end. Use
[`models/generated/tractor-lane-photo1-oblique.svg`](models/generated/tractor-lane-photo1-oblique.svg)
as the proposed geometry authority; never mirror this camera.

For the rearward interior from the valley living hall, the entrance is not in
the transverse service/master wall. It is hosted on the **courtyard side wall
at z=7.5 m**, spanning x=10.7–11.7 m, and opens into the entry gallery. In the
selected interior composition it must appear on the receding viewer-right wall,
strongly foreshortened. Use
[`models/generated/interior-from-valley-entry.svg`](models/generated/interior-from-valley-entry.svg)
as the entrance-plane authority. A front-facing exterior door in the transverse
wall is structurally incorrect; front-facing oak doors under the mezzanine are
internal only.

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

## Selected solar-control development

Option C from [`models/solar-control-options.json`](models/solar-control-options.json)
is integrated in the Rev 09 review model: a 1.25 m valley roof visor, nine
operable fins confined above the 3.0 m transom, clear ground-floor glazing and a
compact grass-filled cellular-grid patio with exactly two chairs and one coffee
table. The grid sits on an unbound open-graded base with no impermeable slab;
the final product and infiltration build-up require municipal acceptance. Rev 08
remains the last approved baseline; the photoreal gate remains closed until the
Rev 09 fixed-camera geometry is reviewed and approved.

## Selected non-structural masonry direction

The continuous warm Belgian brick veneer now uses a restrained version of the
retained property's masonry rhythm: two flush soldier courses in the same brick
at the conventional-window sill and head datums on both long elevations, plus
slim Belgian blue-stone heads and sills at rectangular windows only. All deep
jambs and glass surrounds remain matte black. The valley glass and triangular
loft glass receive no stone or brick bands across their glazing. This is a
material-only refinement and does not change `models/design.json` geometry.

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

Revision 09-solar-c-patio-review is awaiting owner approval; 08-photoreal-approved remains the last approved photoreal geometry authority. Do not treat Rev 09 structural additions as final photoreal authority until its regenerated views are approved. Non-structural material studies may reuse the last approved fixed-camera geometry.
