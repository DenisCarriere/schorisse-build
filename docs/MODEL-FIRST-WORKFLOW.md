# Model-first rendering workflow

The parametric geometry package is the structural source of truth. Photoreal
images are presentation outputs, never a place to invent or correct structure.

## Change classification

| Request | Classification | Required action |
|---|---|---|
| Brick tone, furniture fabric, daylight, fixture finish, planting colour | Non-structural | Reuse the approved model and matching fixed camera |
| New camera angle with unchanged building | Non-structural | Generate a new model camera view first; do not change geometry |
| Add, remove or relocate a fixed sanitary or kitchen fixture | Coordinated layout change | Edit `models/design.json`, regenerate and review the plan/model before rendering |
| Move/add/remove a wall, door, window, stair, floor, roof, mezzanine or room | Structural | Edit `models/design.json`, regenerate and approve before ImageGen |
| Unclear impact | Structural by default | Resolve it in the model first |

## Required sequence

1. Edit only `models/design.json` for geometry.
2. Run `python3 models/gen_model.py`.
3. Run `python3 models/gen_model.py --check`; all validations must pass.
4. Review `models/generated/birdseye-orientation.svg`,
   both generated interior directions (`interior-from-valley.svg` and
   `interior-toward-valley.svg`), both generated plans, and the GLB/OBJ model.
5. Confirm that `geometry_approved_for_photoreal` is true. Any structural edit
   must set it back to false until the regenerated geometry is approved.
6. For the selected camera, supply the generated model view plus relevant site
   photograph(s) to ImageGen. State explicitly that geometry is locked.
7. Compare the result to the model: reject any changed opening, stair, floor,
   roof, room boundary or mirrored orientation.

## Prompt contract

Each downstream photoreal prompt must identify inputs by role:

- Image 1: geometry and camera authority generated from `design.json`;
- Image 2: site truth for fixed landscaping, neighbour and paving;
- Image 3: material/lighting reference, when needed.

It must contain this constraint:

> Preserve Image 1's envelope, wall thickness, roof form, camera, perspective,
> every wall, opening, stair flight, landing, mezzanine edge and room boundary.
> Change only the requested non-structural design layer. Do not mirror, move,
> add, delete or reinterpret structural elements.

## Output roles

- `barn.glb`: preferred semantic review handoff;
- `barn.obj` + `barn.mtl`: editable/importable mesh fallback;
- `barn.stl`: geometry-only coordination mesh;
- generated SVG views: exact image-generation references and review evidence;
- generated plans: website drawings derived from the same specification.
