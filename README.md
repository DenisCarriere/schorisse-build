# Schorisse Build — The Glass-Gable Barn

Concept study for the demolition and rebuild of the main barn as a single-storey
contemporary volume in rural Flanders, Belgium: **17.0 × 7.5 m (127.5 m²)**, same
footprint and silhouette as the existing barn, with a fully glazed gable facing
the valley. Side wing, hedges and cobbled courtyard are retained.

**[View the concept board](index.html)** — open `index.html` in a browser
(or serve the repo with any static file server).

## The board

1. **Reading the site** — site photos, pacing the 17 m length, Flanders planning note
2. **Site plan** — what stays, what changes
3. **The glass gable** — valley elevation 1:75 and build-up (portal frame, triple glazing, lift-slide doors, clerestory)
4. **Plan & long elevation** — 2-bed living/rental fit-out at 1:100
5. **Concept views** — front, side and interior illustrations plus photoreal renders
6. **Three ways to use 127.5 m²** — own home / long-term rental / hobby shell, with VAT treatment
7. **Cost estimate** — rural Flanders 2026, ~€2,200–3,000/m² excl. VAT
8. **Certification** — LEED Silver/Gold vs. Passivhaus premiums over the E30 base build

Interactive bits: the "Drawings" controls toggle dimension annotations and switch
between one and two sliding doors; each render card has a copy-prompt button; and
every image is a drag-and-drop slot (drops persist in the browser via localStorage).

## Renders

`renders/` holds three photorealistic views (front, side, interior) generated with
`gpt-image-2`, using the board's SVG concept views as structure references and the
prompts shown on the board. Regenerate or replace them by dropping any image onto
the matching slot.

## 3D model

`models/` holds a starter massing model generated from the concept dimensions
(section 09 of the board shows it in an interactive viewer):

- `barn.stl` — building shell for **SketchUp Free** (import with units set to meters)
- `barn.glb` — coloured glTF scene for Blender / three.js / AR

Regenerate from source dimensions with `gen_model.py` (see git history).

## Site photos

The original site photos are not in the repo — see [`uploads/README.md`](uploads/README.md)
for the expected filenames, or drag them onto the slots in section 01.

---

Pre-design estimate, not a quotation. Design source: claude.ai/design project
"Barn Concept Board".
