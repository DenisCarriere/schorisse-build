# Conceptual Floor Plans

- Status: **parametric geometry review — not permit-ready**
- Revision: **06 — one powder-room toilet**
- External envelope: **17.0 × 7.5 m**
- Levels: ground floor and partial open mezzanine
- Sleeping brief: **one ground-floor master bedroom**
- Geometry source: [`../models/design.json`](../models/design.json)

The drawings are generated from the same specification as the GLB, OBJ and STL
models. They are no longer hand-edited illustrations. A change to any wall,
door, window, room, stair, mezzanine or roof must begin in `models/design.json`,
then regenerate every downstream asset with `python3 models/gen_model.py`.

These remain concept drawings. A measured survey, architect, structural
engineer and building-services designer must replace every assumed dimension
before planning or construction.

## Site orientation fixed by the owner

The marked bird's-eye image resolves the axes:

- **blue / x=0:** valley-facing full glass gable and double-height living room;
- **yellow / x=17:** master bedroom with the open mezzanine above;
- **upper red / z=0:** shared tractor-lane wall;
- **lower red / z=7.5:** cobbled courtyard wall;
- **green:** the entrance in the courtyard wall near the yellow/private end.

When a camera stands at the blue glass gable and looks inward, the tractor-lane
wall, kitchen and stair are on the **viewer's left**. The courtyard wall and
green entrance are on the **viewer's right**. Earlier selected interiors with
the entrance on the left are superseded and must not guide future renders.

## Generated review assets

- [Ground-floor plan](../renders/web/plan-ground-floor.svg)
- [Upper-mezzanine plan](../renders/web/plan-mezzanine.svg)
- [Bird's-eye model view](../models/generated/birdseye-orientation.svg)
- [Interior-from-valley model view](../models/generated/interior-from-valley.svg)
- [Interior-toward-valley model view](../models/generated/interior-toward-valley.svg)
- [Courtyard cutaway](../models/generated/courtyard-cutaway.svg)
- [Validation report](../models/generated/model-report.json)

## Dimensional basis

| Item | Revision 06 assumption |
|---|---:|
| External envelope | 17.0 × 7.5 m |
| Placeholder external wall build-up | 420 mm |
| Approximate internal clear shell | 16.16 × 6.66 m |
| Front open-living zone | 7.48 m internal length |
| Central service and stair zone | 4.60 m external length |
| Rear master zone | 4.08 m internal length |
| Mezzanine floor | +2.45 m |
| Mezzanine extent | x=7.90–16.58 m |

The external dimensions now resolve to the outer shell faces, not wall
centre-lines. The 420 mm wall is a placeholder for the ICF, insulation, cavity,
brick and internal finish. The actual system will move every internal face.

## Ground-floor sequence

1. Enter from the retained cobbled courtyard through the green smoked-oak door.
2. The 1.0 m leaf swings inward toward the yellow/private end and parks beside
   the service wall, clear of the stair and main route.
3. The gallery gives direct access rearward to the master bedroom, inward to the
   separate powder room and laundry cupboard, and forward to the living hall.
4. A clear courtyard-side route continues to an operable panel in the blue
   valley glass gable.

The kitchen stays on the tractor-lane wall. The stair is beside that same wall,
so its tall exterior window genuinely lights the half-landing. The living room
occupies the courtyard half of the open zone. No entrance or projecting element
is added to the tractor lane.

## Master suite and services

The yellow/private end contains one ground-floor master bedroom. Two modest
lane-side windows and one courtyard-side window provide daylight and potential
cross-ventilation; the rear ground-floor gable stays solid behind the bed.

The private ensuite occupies approximately 2.15 × 3.82 m in the service zone and
contains:

- an approximately 1.20 × 1.85 m threshold-free Italian shower;
- a vanity;
- linen/storage;
- a pocket entrance from the master side.

There is deliberately no toilet in the ensuite. The separate powder room
contains the home's only WC and one compact hand-washing basin. A pocket door
slides into the extended entry-screen wall, so no leaf
sweeps across either fixture or the gallery. The laundry/plant cupboard uses
sliding panels to avoid another swing conflict. Final fixture offsets, plumbing,
ventilation, waterproofing and acoustic performance require professional design.

## Dog-leg stair

The stair is now explicit geometry rather than a symbolic arrow:

- two parallel 1.0 m clear flights against the tractor-lane wall;
- 14 risers to the +2.45 m mezzanine, split **6 lower + 8 upper** so the
  lane-side half-landing remains below the lowest roof edge;
- 175 mm riser and 270 mm going;
- 2R+G = 620 mm;
- 1.10 m-deep half-landing and top landing;
- lower flight rises toward the lane-side half-landing and tall window;
- 180-degree turn, then the upper flight returns toward the ridge/courtyard;
- protected top landing connects within the rear mezzanine;
- exact stair void is shared by the ground-floor and mezzanine geometry;
- modeled worst-edge half-landing headroom is approximately **2.19 m** under
  the assumed roof build-up;
- the opening guard stops before the full 1.10 m top landing, leaving an actual
  exit onto the mezzanine rather than trapping the upper flight behind rail.

The last figure is not code certification. The surveyed roof profile, floor and
roof build-ups, nosings, handrails, guards, escape and fire strategy must be
resolved in a coordinated architectural section.

## Open kitchen, dining and living

The blue/valley end remains fully double-height.

- low kitchen run and sink beneath the large lane-facing picture window;
- approximately 2.75 × 1.0 m island with at least a 1.0 m working aisle;
- dining table offset toward the valley side, with at least a 1.0 m transition
  beside the island;
- living furniture kept low and away from the glass doors;
- one courtyard-side living window;
- full-height clear glass gable framing the valley, with a furniture-free
  threshold zone;
- a continuous courtyard-side route comfortably wider than 1.2 m.

The model includes scaled placeholders for these elements so later interior
renders cannot invent room zones or place furniture through the stair and walls.

## Upper mezzanine

The yellow rear/service zone supports one open room. There is no upstairs
bathroom, toilet, sink, kitchenette, wet bar, bedroom wall or corridor.

- x=7.90–16.58 m, leaving the front 7.90 m open to the ridge;
- one continuous guard along the double-height living void;
- guarded stair opening and proper top landing;
- broad triangular window in the yellow/rear gable;
- future low-eaves storage, library, lounge and project-table uses;
- no plumbing.

The whole deck is not equivalent to full standing area. Headroom bands require
a surveyed roof section before usable floor area can be claimed.

## Validation and professional checks

`python3 models/gen_model.py --check` currently validates the envelope, wall
thickness and modeled shell bounds, site-side placement of the
blue/green/yellow elements, opening overlaps, stair/mezzanine stacking,
rise/going, flight and landing widths, worst-edge half-landing headroom,
top-landing egress, fixture bounds, explicit handrails and required semantic
model elements. It also checks the scaled kitchen aisle, dining transition,
valley threshold and courtyard-side circulation route.

It cannot replace:

1. measured site, building and roof survey;
2. architect-led room, door, accessibility and code coordination;
3. structural design of ICF, roof, mezzanine and openings;
4. fire and escape design for the connected living/mezzanine volume;
5. ventilation, drainage, heating, electrical and plant design;
6. planning, change-of-use, EPB and local/heritage review.

See [the model-first rendering workflow](MODEL-FIRST-WORKFLOW.md) before making
any further photoreal image.
