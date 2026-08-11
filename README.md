# Schorisse Build — The Glass-Gable Barn

Concept study for the demolition and rebuild of the main barn as a contemporary
low volume in rural Flanders, Belgium: **17.0 × 7.5 m (127.5 m²)**, same footprint
and silhouette as the existing barn, with a fully glazed gable facing the valley
and an optional partial open loft inside the rear roof volume. Side wing, hedges,
shared tractor lane and cobbled courtyard are retained.

**[View the concept board](index.html)** — open `index.html` in a browser
(or serve the repo with any static file server).

## The board

1. **Reading the site** — site photos, pacing the 17 m length, Flanders planning note
2. **Site plan** — what stays, what changes
3. **The glass gable** — valley elevation 1:75 and build-up (portal frame, triple glazing, lift-slide doors, clerestory)
4. **Plan & long elevation** — 2-bed living/rental fit-out at 1:100
5. **Early massing views** — diagrammatic front, side and interior envelope studies
6. **Three ways to use 127.5 m²** — own home / long-term rental / hobby shell, with VAT treatment
7. **Cost estimate** — rural Flanders 2026, ~€2,200–3,000/m² excl. VAT
8. **Certification** — LEED Silver/Gold vs. Passivhaus premiums over the E30 base build
9. **3D massing model** — interactive shell generated from the fixed envelope
10. **Site-grounded concept + open loft** — real-site photoreal studies, program-aware elevations and mezzanine strategy

Interactive bits: the "Drawings" controls toggle dimension annotations and switch
between one and two sliding doors; each render card has a copy-prompt button; and
every image is a drag-and-drop slot (drops persist in the browser via localStorage).

## Renders

`renders/` holds the three original photorealistic views (front, side, interior).
`renders/site-concepts/` adds site-anchored studies generated from the four real
property photographs: the glass gable beside the retained building, the shared
tractor lane, the preserved cobbled courtyard, the actual valley outlook, and a
partial open-loft interior. The final material direction uses contemporary
long-format red-brown brick, dark-bronze frames and thin dark terracotta tiles.

See [`renders/site-concepts/README.md`](renders/site-concepts/README.md) for the
fixed-site constraints, image-reference roles, loft assumptions and prompt set.

## 3D model

`models/` holds a starter massing model generated from the concept dimensions
(section 09 of the board shows it in an interactive viewer):

- `barn.stl` — building shell for **SketchUp Free** (import with units set to meters)
- `barn.glb` — coloured glTF scene for Blender / three.js / AR

Regenerate from source dimensions with [`models/gen_model.py`](models/gen_model.py).

## Site photos

The four real site photographs are preserved under `uploads/site-reference/`:
shared tractor lane, future glass-gable end, outward valley view, and the rear
cobbled courtyard. See [`uploads/README.md`](uploads/README.md) for the mapping
and the permanent elements that concepts must retain.

---

Pre-design estimate, not a quotation. Design source: claude.ai/design project
"Barn Concept Board".
