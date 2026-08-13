# Schorisse Build — The Glass-Gable Barn

A site-grounded visual concept for rebuilding the main barn in rural Flanders:
**17.0 × 7.5 m**, a valley-facing glass gable, a thick ICF wall shell with one
continuous Belgian brick exterior, one ground-floor master bedroom and a partial
open mezzanine.

## Visual presentation

**[Open the live concept gallery](https://deniscarriere.github.io/schorisse-build/)**

The mobile-first gallery now foregrounds coordinated model views and plans, with
the earlier photoreal studies retained only for material, atmosphere and real
property context: glass gable, shared tractor lane, cobbled courtyard,
valley-facing living hall and the rear open mezzanine.

The GitHub Pages workflow publishes `index.html`, the optimized images and plans
under `renders/web/`, and the generated model package under `models/`. Original
site references, source photoreal renders and project notes remain repository
assets rather than gallery content.

## Project documents

- [Architectural concept](docs/ARCHITECTURAL-CONCEPT.md)
- [Conceptual floor plans](docs/CONCEPTUAL-FLOOR-PLANS.md)
- [Model-first rendering workflow](docs/MODEL-FIRST-WORKFLOW.md)
- [Valley glass solar-control options](docs/VALLEY-SOLAR-CONTROL-OPTIONS.md)
- [Solar-control image studies and prompt record](renders/solar-control/README.md)
- [Structure and envelope](docs/STRUCTURE-AND-ENVELOPE.md)
- [Feasibility and performance](docs/FEASIBILITY-AND-PERFORMANCE.md)
- [Cost assumptions](docs/COSTS.md)
- [Image constraints and prompt record](renders/site-concepts/README.md)
- [Selected Belgian Brick Lantern concept and exact prompts](renders/belgian-brick-lantern/README.md)
- [Black Barn Lantern ICF concept and exact prompts](renders/black-barn-icf/README.md)
- [Hybrid Flemish Brick + Black Lantern concept and exact prompts](renders/hybrid-barn-icf/README.md)
- [Brick Veil concept set and exact prompts](renders/brick-veil/README.md)
- [Site-reference mapping](uploads/README.md)

## Source assets

- `renders/site-concepts/` — final site-grounded concept PNGs and earlier variants.
- `renders/belgian-brick-lantern/` — selected all-brick front, side and back concept PNGs.
- `renders/black-barn-icf/` — superseded full-black concept PNGs plus the current interior-loft study.
- `renders/hybrid-barn-icf/` — superseded mixed-material concept PNGs.
- `renders/brick-veil/` — developed front, side, back and interior-loft concept PNGs.
- `renders/solar-control/` — Options A–C studies and the selected Option C grass-grid patio concept.
- `renders/concepts/` — broader material explorations.
- `renders/web/` — responsive JPEG derivatives and editable SVG floor plans used by the gallery.
- `uploads/site-reference/` — four original property photographs plus the
  owner-marked bird's-eye orientation record and retained-building brick-pattern
  reference.
- `models/` — authoritative design JSON, semantic GLB, editable OBJ/MTL, STL,
  generated review views, validation report and dependency-free generator.

## Geometry workflow

The building is modeled before it is rendered. `models/design.json` defines the
site axes, fixed 17.0 × 7.5 m outer envelope, thick walls, rooms, openings,
doors, fixtures, stair, mezzanine and fixed cameras. Run:

```sh
python3 models/gen_model.py
python3 models/gen_model.py --check
```

The generated plans and 3D files are downstream artifacts. Structural image
changes require a model update first; non-structural image changes reuse the
approved model and proposed camera as geometry context.

All drawings, renders, dimensions and estimates remain pre-design material. A
measured survey and professional planning, architectural, structural, energy and
cost advice are required before design development or construction.
