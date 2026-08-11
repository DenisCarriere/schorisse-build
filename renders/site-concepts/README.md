# Site-grounded concepts

These studies use the real site photographs in `uploads/site-reference/` rather
than an invented rural backdrop. They are pre-design visualizations, not survey,
planning, structural or construction documents.

## Fixed geometry

- Footprint: 17.0 × 7.5 m.
- Eaves: 3.2 m.
- Ridge: 5.2 m.
- Symmetric roof rise: 2.0 m over a 3.75 m half-span.
- Implied roof pitch: approximately 28.1°, not the 45° stated in an early prompt.

## Fixed site context

- Photo 1: retain the full shared tractor lane, pasture gate, left hedge, right
  boundary screen and clear working width. Nothing may project into the lane.
- Photo 2: retain the neighboring/retained brick building, narrow paved passage,
  left hedge, ground levels, drains and tree positions.
- Photo 3: use the recognizable Schorisse valley, fields, tree clusters and
  right-hand hedge as the real living-room outlook.
- Photo 4: retain the complete cobbled courtyard, curbs, clipped hedges,
  hydrangeas, mature canopy and every non-target building mass.
- Dry grass may become naturally green. Temporary debris, people, shadows and
  the portable toilet need not remain.

## Program and loft

The side elevation is intentionally zoned rather than evenly fenestrated:

1. Rear/private zone: two ground-floor bedrooms with residential windows.
2. Middle transition: bath/technical core, side entrance and a tall stair marker.
3. Front/valley zone: a larger side window and the full glazed living-room gable.

The optional loft is a partial open mezzanine over the rear 7–8.5 m. Its floor is
conceptually around +2.40–2.45 m, while the front 8.5–10 m remains a double-height
living hall. The stair rises near the ridge at the transition. Because the roof is
shallow, only an estimated 10–18 m² will have comfortable standing headroom after
allowing for the roof structure and insulation; low edges become storage, shelving
and seating. A measured survey and architect/engineer review must verify the inner
roof profile, room heights, structure, stair, fire safety and permitting.
The board's current cost range remains a ground-floor base case; the loft, stair
and rooflights need a separate allowance once their measured design is resolved.

## Final concept images

| File | Reference role | Purpose |
|---|---|---|
| `site-glass-gable-modern-brick-loft.png` | Photo 2 edit target | Modern glass living-room gable within the retained hedge/building context |
| `site-shared-tractor-laneway-zoned-modern-brick.png` | Photo 1 edit target | Program-aware lane elevation while preserving tractor clearance |
| `site-cobbled-courtyard-modern-brick-loft.png` | Photo 4 edit target | Bedrooms, recessed side entrance and flush loft rooflights over preserved cobbles |
| `site-interior-real-valley.png` | Original interior + Photo 3 composite | Living room with the actual valley outlook |
| `site-interior-open-loft-reverse.png` | New view from interior references | Reverse view of the stair, rear mezzanine and double-height front room |

Earlier variants remain beside the final files for comparison. The separate
`renders/concepts/` directory contains four broader material directions plus
courtyard/interior studies made before the site photographs were supplied.

## Prompt set

All final images used the built-in image-generation/editing workflow. Exterior
edits used the relevant site photograph as the authoritative edit target; the
original context controlled crop, camera, horizon, topography, occlusion, retained
buildings, hedges, trees, access and hardscape.

Reusable geometry lock:

```text
Preserve one barn volume exactly 17.0 m long × 7.5 m wide, eaves exactly
3.2 m and ridge exactly 5.2 m, with a symmetric 2.0 m roof rise. Keep the
building inside its existing footprint. No annex, canopy, dormer, raised roof,
second-storey wall or projection into retained access and landscape.
```

Reusable material direction:

```text
Use true contemporary long-format fired-clay masonry: slender individual bricks
in warm umber, deep red-brown and occasional charcoal, visible staggered joints,
dark recessed mineral mortar and precise deep reveals. Pair it with thin dark
terracotta tiles, dark-bronze frames and smoked-oak entrance joinery. It must read
as masonry, not timber siding.
```

Per-image prompt deltas:

- Glass gable: edit only the target barn in Photo 2; retain both side boundaries;
  use a roughly 7.0 m glazed field, 3.0 m transom, triangular clerestory and central
  sliding doors; show a double-height living room with the loft only deep at rear.
- Tractor lane: retain the full working route; rear bedroom windows nearest the
  closed end, a tall stair window at the middle transition, and a larger living
  window toward the valley; no entrance or opening projection on this facade.
- Cobbled courtyard: change only the target barn; keep every cobble, curb, hedge,
  hydrangea and tree; use a recessed smoked-oak side entrance, bedroom windows, a
  stair marker and two small flush rooflights over the rear loft.
- Valley interior: preserve the original one-point room geometry and composite the
  recognizable landscape from Photo 3 through the glass with plausible exposure.
- Open loft: generate a reverse interior view from near the glass gable; keep the
  front double-height, place the loft over the rear private core, bring the stair
  up near the ridge and show honest low-eaves storage rather than a full floor.

No image prompt requested text, labels, logos, people or watermarks.
