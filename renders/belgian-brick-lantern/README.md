# Belgian Brick Lantern — selected exterior direction

Status: **selected material record; Rev 09 solar geometry remains under review**

The current selected non-structural brick refinement is
`rev09-lane-brick-pattern-study.png`. It keeps the coordinated model geometry
unchanged and translates the retained-building reference into two quiet flush
soldier-course bands with slim blue-stone window heads/sills.

## Approved model-first geometry

The owner's marked bird's-eye view supersedes all earlier attempts to infer the
plan orientation from ground photographs. `models/design.json` is now the only
geometry authority:

- valley glass gable at x=0;
- rear master-bedroom/mezzanine gable at x=17;
- shared tractor lane at z=0;
- cobbled courtyard and entrance at z=7.5;
- from the valley glass looking inward, lane/kitchen/stair are image-left and the
  courtyard/entrance are image-right.

Every earlier PNG in this folder predates the approved parametric model and may
guide only Belgian brick, black frames, oak, lighting and atmosphere. The new
`rev09-lane-brick-pattern-study.png` reuses the approved Rev 08 lane geometry
without altering walls or openings. Rev 09 adds pending solar-control and patio
geometry, so `geometry_approved_for_photoreal` remains false until that model is
reviewed.

See [`../../docs/MODEL-FIRST-WORKFLOW.md`](../../docs/MODEL-FIRST-WORKFLOW.md).

This is the selected development of Option B. It keeps the complete ICF wall
shell but uses one consistent exterior wall finish:

- all exterior walls: warm Belgian/Flemish fired-clay facing brick;
- no fibre cement, timber wall cladding or material transition;
- all windows and the glass gable: deep matte-black aluminium liners and frames;
- roof: black gently curved hollow ceramic Flemish tiles, not standing-seam metal;
- rear loft: one broad triangular black-framed gable window above the master and
  service core;
- courtyard entrance: smoked oak door and vertical timber-lined recess within a
  deep matte-black portal; brick remains continuous outside the entrance recess;
- exterior lighting: shielded warm pier and eaves lights with no projection into
  the shared tractor lane;
- interior openings: rear loft gable, lane-facing kitchen window and stair window
  aligned with the exterior elevations;
- glass: clear and unobstructed;
- existing tractor lane, gate, hedges, neighbour, cobbles and trees: retained.

The roof language is comparable to a black glazed Vlaamse Pan 401. That current
Belgian product is described as a hollow ceramic tile and is listed for a minimum
22° pitch with the referenced underlay, making it a plausible visual precedent
for the concept's approximately 28° roof. Final product selection and detailing
remain for the architect and roofer:
<https://www.wienerberger.be/Dak/productzoeker/vlaamse-pan-401-zwart-geglazuurd.html>

## Window structure — shared tractor lane

The side elevation is deliberately driven by the plan. From the pasture gate at
the far/rear end toward the valley-facing glass gable at the near/front end:

1. two separate horizontal master-bedroom windows;
2. one tall narrow stair window at the transition;
3. one larger horizontal kitchen picture window;
4. the full-height glass front gable, partly hidden by the retained boundary screen.

There is no entrance on the tractor-lane elevation and no evenly spaced decorative
window row.

## Generation method

Generated with Codex's built-in ImageGen image-edit mode. The previous hybrid
images were edit targets, the matching property photographs were site truth, and
the approved new front image became the material-identity reference for the side
and rear.

## Exact prompts

### Rev 09 full-width courtyard at 6:30–7:00 PM

Generated with Codex's built-in ImageGen edit mode as a lighting-only revision
of `rev09-courtyard-full-width-study.png`. The darker blue-hour version remains
available as an alternate; this brighter early-evening image is the website
presentation selection.

> Use case: lighting-weather
> Asset type: revised website photoreal — full-width courtyard side entrance.
> Image 1 is the EDIT TARGET and is the absolute authority for all geometry, camera, composition, materials, landscaping and objects.
>
> Primary request: change ONLY the time of day and exposure from deep blue hour to a bright Belgian summer early evening at approximately 6:30–7:00 PM. It must still clearly read as daytime: pale blue sky, sunlit green foliage, fully readable warm Belgian brick, roof tiles, hedges, hydrangeas, cobbles, neighbouring structures and right-side gate. Use soft warm low-angle sunlight with realistic late-day shadows and a natural documentary exposure. The scene should be much lighter than Image 1, with no dark crushed foreground or navy night sky.
>
> Keep all exterior lighting switched on and visibly effective despite the daylight: restrained warm 2700K brick-grazing pools along the wall, a discreet warm entrance-soffit light, a small hedge/path accent, and subtle warm interior light behind both windows. The fixtures and glow must remain credible and delicate—visible because evening is approaching, never overpowering the daylight or turning the scene into night.
>
> LOCK EVERYTHING ELSE EXACTLY: same straight-on full-width 4:3 camera and crop; complete 17.0 m courtyard elevation; exact roof silhouette and black Belgian tiles; continuous modern Belgian brick with two restrained soldier-course bands; exactly one living-room window on the left, exactly one single smoked-oak entrance door in its deep matte-black portal immediately left of the retained centre-right tree, and exactly one master-bedroom window on the right; exact window/door size and position; black surrounds; every cobble; central approach; clipped hedge blocks and gaps; hydrangeas; both mature tree trunks and entire canopy; neighbouring buildings and gate. Do not move, resize, add, remove, mirror or reinterpret any architectural or landscape element.
>
> Avoid: dusk or night darkness, navy/cobalt night sky, dramatic sunset orange, artificial HDR, overexposure, changed brick pattern, extra or missing doors/windows/lights, double door, door hidden behind tree, triangular loft window, canopy, porch, new paving, people, vehicles, signs, text, logo or watermark. Premium believable Belgian architectural photography, not glossy CGI.

### Rev 09 full-width courtyard entrance study

The owner's new full-width photograph was used as the site-and-camera truth,
`models/generated/courtyard-full-width.svg` was the opening-position authority,
the selected lane study supplied the brick language, and the earlier courtyard
concept supplied only its black/oak entrance detail and blue-hour atmosphere.
Generated with Codex's built-in ImageGen edit mode in two passes; the second
pass made the single entrance completely readable beside the retained tree.

> Use case: precise-object-edit
> Asset type: final full-width courtyard side-entrance concept.
> Image 1 is the EDIT TARGET. Image 2 is authoritative SITE TRUTH. Image 3 is the MODEL AUTHORITY.
>
> Make one targeted correction to Image 1: make the proposed side entrance exactly ONE single smoked-oak entrance door inside a deep matte-black rectangular portal and narrow timber-lined recess. The whole door leaf must be fully readable immediately LEFT of the large retained centre-right tree trunk, aligned with the existing central cobbled approach through the hedge opening. The retained tree may overlap only a tiny edge of the portal; it must not split or hide the door leaf. Use one vertical matte-black pull and one discreet warm soffit light. The entrance remains right of the building midpoint, consistent with Image 3.
>
> LOCK EVERYTHING ELSE from Image 1 exactly: same straight-on full-width 4:3 camera; entire 17.0 m long courtyard wall visible; same 7.5 m building width, 3.2 m eaves, 5.2 m ridge and black Belgian tile roof; same continuous modern Belgian brick with two restrained flush soldier-course bands; same deep black surrounds; exactly one living-room window left of the entrance and one master-bedroom window right of it; same blue-hour brightness, warm brick grazing lights and interior glow. Preserve every site element from Images 1 and 2: full cobbled forecourt, clipped hedge blocks and their gaps, hydrangeas, both mature tree trunks and complete overhead canopy, neighbouring structures and right-side gate. Do not crop or move the building.
>
> Avoid: double doors, a second door, door behind the tree, extra windows, missing windows, rear gable or triangular loft window in this long-wall elevation, canopy, porch, new paving, removed hedges, removed trees, grass-grid patio, people, vehicles, signage, text, logo or watermark. Premium believable Belgian architectural photography, not glossy CGI.

### Rev 09 restrained brick-pattern refinement

> Use case: precise-object-edit. Asset type: architectural material refinement. Image 1 is the EDIT TARGET and controls all geometry, camera, lighting, site, landscape and openings. Image 2 is MATERIAL REFERENCE ONLY.
>
> Make one targeted masonry refinement to Image 1. On the NEW BARN ONLY, make exactly two subtle continuous horizontal accent bands clearly readable along the entire 17 m long brick wall. Each band is a single course of the same warm red-brown brick laid vertically as a flush soldier course, matching the material language in Image 2. Put the lower band at the common conventional-window sill datum and the upper band at the common conventional-window head datum. The courses must be real vertical bricks, flush with the field brick, never gray stone and never projecting ledges. Where the bands meet openings, resolve them neatly into the jambs.
>
> Keep restrained thin Belgian blue-stone sills and flat lintels only at conventional rectangular windows, but make them slimmer and calmer than in Image 1. No large gray arches, no wedge lintels, no pyramid blocks, no decorative corner blocks, no stone bands. The triangular loft window retains only its continuous black frame and a neat brick edge; no blue stone around the triangle.
>
> LOCK EVERYTHING ELSE EXACTLY from Image 1: same portrait composition, 17.0 m building length, roof and gable, triangular loft window, exact four lane-wall windows and rear-gable windows, no doors on the lane wall, black frames, black tiled roof, hedge, gate, screen, grass tracks, trees, lights, dusk brightness and warm interior glow. Do not add or remove openings or objects. No mixed cladding, render, columns, signs, people, vehicles, text, logos or watermark. Highly realistic Belgian architectural photography.

Generated with Codex's built-in ImageGen edit mode. Image 1 was the preceding
model-locked lane study and Image 2 was
[`../../uploads/site-reference/existing-brick-pattern-reference.jpg`](../../uploads/site-reference/existing-brick-pattern-reference.jpg).

### Front glass gable

> Use case: precise-object-edit. Asset type: photoreal architectural concept — FRONT glass-gable view. Image 1 is the EDIT TARGET and controls the exact camera, crop, building footprint, 7.5 m gable width, 3.2 m eaves, 5.2 m ridge, approximately 28-degree roof pitch, full-height glass geometry, lawn grade, mature hedge, paved passage, drains, trees and neighbouring brick building. Image 2 is authoritative SITE TRUTH. Image 3 is a MATERIAL reference for warm Belgian/Flemish red-brown brick and deep black window liners.
>
> Change the target barn into one materially consistent Belgian brick building. Replace every strip of black fibre-cement wall cladding around the glass gable and on any visible return with refined contemporary Belgian/Flemish fired-clay facing brick over the continuous thick ICF shell. Use warm red-brown, umber and occasional darker fired units, traditional horizontal running bond, slender real bricks, subtly irregular coloration and fine recessed mineral mortar. No cladding transition and no black wall panels anywhere.
>
> Keep the approximately 7.0 m-wide floor-to-ridge living-room glass gable exactly clear and unobstructed, with its horizontal transom around 3.0 m, triangular clerestory, central lift-slide doors and warm double-height living room behind it. Give the entire glazed field a pronounced deep matte-black aluminium perimeter liner plus slim black mullions, honestly expressing the 35–45 cm ICF wall depth. Black is an accent only at windows, flashings, gutters and downpipes.
>
> Replace the standing-seam metal roof with a distinctly Belgian black roof of small individual gently curved hollow ceramic clay tiles, comparable in character to a black glazed Flemish pantile. Show believable overlapping tile courses, a traditional black tiled ridge and precise dark eaves; absolutely no metal seams or large panels. Preserve the exact roof shape and height.
>
> Keep the healthy natural green grass and every fixed site element. Warm natural Belgian late-afternoon daylight, accurate brick scale and mortar, believable black ceramic tile texture, clear glazing reflections and grounded shadows, premium documentary architectural photography rather than glossy CGI.
>
> Change only the target barn materials and detailing. No black fibre cement, timber siding or mixed wall finish. No brick screens, perforated brick, fins, shutters, curtains, columns or planting across the glass. No annex, terrace expansion, canopy, dormer, raised roof, altered footprint, cars, people, signage, text, logos or watermark.

### Shared tractor-lane side — base correction

> Use case: precise-object-edit. Asset type: photoreal architectural concept — LEFT SIDE / shared tractor-lane elevation. Image 1 is the EDIT TARGET and controls the portrait camera, crop, building wall line and dimensions. Image 2 is authoritative SITE TRUTH: preserve the exact full lane width, twin compacted tractor tracks, pasture gate, tall hedge on the left, neighbour boundary screen on the right, mature trees, terrain and every working clearance. Image 3 is the APPROVED DESIGN IDENTITY: match its warm Belgian/Flemish brick, deep matte-black window framing, black tiled roof and photographic realism.
>
> Change the target barn into one materially consistent Belgian brick building. Replace ALL black fibre-cement wall areas and the current brick section with one continuous refined warm red-brown Belgian/Flemish facing brick veneer over the thick ICF shell, from the far pasture end to the near living end. Use one brick family, one running bond and one recessed mortar treatment everywhere. No material transition, black wall strip, timber siding or fibre cement anywhere.
>
> CORRECT THE WINDOW STRUCTURE TO MATCH THE INTERIOR PLAN. The camera looks along the full 17 m side; FAR / LEFT at the pasture gate is the rear private zone and NEAR / RIGHT behind the retained black neighbour screen is the front valley living zone. Show exactly this program-driven sequence, not an evenly spaced decorative row:
> 1. FAR REAR BEDROOM ZONE: exactly TWO separate, generous residential horizontal bedroom windows at normal ground-floor height, each approximately 1.5–1.8 m wide by 1.1–1.3 m high, with clear glazing. They must be clearly readable as two bedroom windows, not tiny slots.
> 2. MIDDLE TRANSITION: exactly ONE tall narrow vertical stair window, approximately 0.65–0.8 m wide by 2.1–2.4 m high, placed between the bedroom and kitchen windows.
> 3. NEAR FRONT LIVING ZONE: exactly ONE larger black-framed kitchen picture window, approximately 2.4–2.8 m wide by 1.6–1.8 m high, naturally partly hidden by the retained neighbour screen.
> No other windows, no entrance, and no door on this tractor-lane elevation. Do not reverse the order. Do not turn all openings into the same shape.
>
> Every opening has a pronounced deep matte-black aluminium perimeter liner, black head/sill flashing and slim black frame, expressing the 35–45 cm ICF wall depth. Set the glazing toward the inner face so each reveal casts a substantial realistic shadow. Glass stays clear and completely unobstructed; no shutters, brick screens, fins or louvers.
>
> Replace the standing-seam roof with the same black Belgian roof as Image 3: small individual gently curved hollow ceramic clay pantiles in believable overlapping courses, black traditional ridge tiles, black gutters and downpipes. No standing seams and no large metal panels. Keep only two small flush dark rooflights above the FAR REAR loft zone if visible; none over the living zone. Preserve exact 3.2 m eaves, 5.2 m ridge and approximately 28-degree pitch.
>
> Revive the grass to believable mixed green but preserve the compacted twin wheel tracks, natural grade, lane width and gate. Natural Belgian daylight, accurate brick scale, black tiled roof texture, clear reflections and grounded shadows, premium documentary architectural photography.
>
> Change only the target barn. No mixed exterior materials. No projection into the lane, paving, planting, steps, lights, furniture, cars, people, annex, canopy, dormer, balcony, raised roof, signage, text, logos or watermark.

### Shared tractor-lane side — glass-gable correction

> Use case: precise-object-edit. Image 1 is the EDIT TARGET. Image 2 is the authoritative design reference for the FRONT full-height glass gable. Image 3 is site truth.
>
> Make exactly one architectural correction: the NEAR / RIGHT END GABLE in Image 1 is the front valley living-room gable and must use the same full-height black-framed glass composition shown in Image 2, not the current brick gable with a single rectangular upper window. Replace the visible near/right end-gable field with clear floor-to-ridge glazing: deep matte-black perimeter frame, horizontal transom around 3.0 m, triangular clerestory following the roof, and slim black vertical mullions. The retained black neighbour boundary screen naturally hides much of the lower glass from this oblique side viewpoint, but the visible upper triangular glass and side edge must make the full glazed gable unmistakable. Keep brick only as the consistent deep perimeter return around that glass. No brick panel spanning the gable face and no rectangular window within it.
>
> LOCK EVERYTHING ELSE FROM IMAGE 1. Preserve the portrait camera, exact wall line, footprint, lane, gate, hedges, boundary screen, trees, green twin tractor tracks, all-brick long wall, black curved Belgian ceramic roof tiles, gutters, downpipes, rooflights, lighting and shadows. Preserve exactly the four program-driven openings on the LONG SIDE WALL in their current positions and shapes: two separate horizontal bedroom windows at far/left, one tall narrow stair window in the middle, and one larger horizontal kitchen picture window near/right. Do not add, delete, resize, reorder or restyle those four long-wall openings. No entrance on the lane.
>
> All glazing retains deep matte-black aluminium liners and remains clear and unobstructed. No mixed wall materials, black cladding, screens across windows, fins, shutters, extra openings, annex, canopy, dormer, people, vehicles, signage, text, logos or watermark. Premium photoreal Belgian architectural photography.

### Cobbled rear courtyard

> Use case: precise-object-edit. Asset type: photoreal architectural concept — REAR / cobbled courtyard and side entrance. Image 1 is the EDIT TARGET and controls the renovated building footprint, openings and portrait composition. Image 2 is authoritative SITE TRUTH: preserve the exact foreground cobble driveway and parking geometry, curbs, clipped hedge forms, hydrangeas, mature trees and canopy, dappled shadows, access gaps and all non-target structures. Image 3 is the APPROVED DESIGN IDENTITY: match its consistent warm Belgian/Flemish brick, pronounced matte-black window framing and black curved ceramic roof tiles.
>
> Make the entire visible exterior wall finish one continuous Belgian/Flemish fired-clay facing brick veneer over the thick ICF shell. Use the same warm red-brown and umber brick family, traditional running bond, occasional darker fired units and fine recessed mortar as Image 3 across the rear gable, long wall and every entrance return. Remove any black fibre-cement, black wall panel, timber siding or material transition. The entrance remains recessed, but its jambs and head are brick; use only a warm smoked-oak door inside a pronounced matte-black frame.
>
> This is the quiet rear bedroom/service end, not another living facade. Keep the rear gable mostly solid with exactly two generous clear black-framed bedroom windows at ground-floor level. Preserve the visible long-wall residential/service openings and recessed side entrance in a room-driven arrangement. Give every window and the entrance a deep, prominent matte-black aluminium perimeter liner plus black sill/head flashing, expressing the 35–45 cm ICF wall depth. Glazing stays clear and unobstructed. No brick screens, perforated masonry, shutters, fins or louvers.
>
> Replace the standing-seam metal roof with the same traditional black Belgian ceramic roof as Image 3: small individual gently curved hollow clay pantiles in regular overlapping courses, black ridge tiles, black gutters and downpipes. Keep exactly two small flush dark rooflights over the rear partial loft. No standing seams, large metal sheets, dormers or raised roof. Preserve the exact 17.0 x 7.5 m single volume, 3.2 m eaves, 5.2 m ridge and approximately 28-degree roof pitch.
>
> Preserve every existing cobble and its irregular patina, drainage fall and curb edge. Preserve all clipped hedges, hydrangeas, mature trees and approach openings. Only a narrow flush accessible threshold may meet the entrance. Natural warm Belgian late-afternoon light, accurate brick and tile scale, clear reflections, oak grain and tree-filtered grounded shadows, premium documentary architectural photography rather than glossy CGI.
>
> Change only the target barn materials and detailing. No mixed wall finish, black cladding, glass rear gable, projecting canopy, porch, terrace, new paving, gravel, deck, annex, balcony, cars, people, outdoor furniture, signage, text, logos or watermark.

### Rear triangular loft-window revision

> Use case: precise-object-edit. Asset type: photoreal architectural concept — REAR courtyard view with loft gable window. Image 1 is the EDIT TARGET and controls the exact renovated building, portrait camera, crop, perspective, all-brick material, roof, openings, entrance and lighting. Image 2 is the FRONT glass-gable design reference only, showing the approved deep matte-black perimeter frame and slim mullion language. Image 3 is authoritative SITE TRUTH for the cobbled courtyard, curbs, clipped hedges, hydrangeas, mature trees, dappled shadows and every non-target structure.
>
> Make one architectural change only: open the currently solid UPPER TRIANGULAR FIELD of the visible rear gable with one generous wide triangular loft window. This is a loft window above the ground-floor bedroom zone, not a second full-height glass wall. Center it symmetrically in the rear gable. Place its horizontal base approximately at 2.9–3.1 m, just above the loft floor/eaves zone; make the glazed base approximately 4.5–5.0 m wide and taper it cleanly to an apex below the 5.2 m ridge. Leave a substantial continuous Belgian-brick perimeter around the glass at both sloping sides, base and ridge so the gable still reads as brick and the thick ICF shell remains structurally plausible.
>
> Use a deep pronounced matte-black aluminium perimeter liner matching Image 2, with one slim central vertical mullion and at most one restrained horizontal transom at the base. The glass is clear and unobstructed, with realistic reflections and a subtle warm view into the compact rear loft reading/lounge. No balcony, Juliet rail, external guard, projecting frame, shutter, screen, fins or brick veil. The window must light the loft and visually relieve the hard gable wall while remaining clearly smaller and quieter than the full front living-room glass gable.
>
> LOCK EVERYTHING ELSE FROM IMAGE 1. Preserve the two existing ground-floor black-framed bedroom windows in the rear gable exactly where they are. Preserve the long-wall windows, deeply recessed smoked-oak side entrance, continuous Belgian/Flemish brick on every exterior wall, black hollow ceramic Flemish roof tiles, black ridge/gutters/downpipes, two flush rear-loft rooflights, exact 17.0 x 7.5 m footprint, 3.2 m eaves, 5.2 m ridge and approximately 28-degree roof. Do not alter the roof shape, raise the ridge or add a dormer.
>
> Preserve every cobble, curb, hedge, hydrangea, mature tree, canopy opening, access route, shadow and non-target building from Images 1 and 3. Premium documentary Belgian architectural photography with accurate brick, mortar, black aluminium, ceramic tile and glass texture; natural warm late-afternoon light, not glossy CGI.
>
> No mixed wall finish, fibre cement, standing-seam roof, full-height rear glazing, glass at bedroom level, annex, canopy, porch, terrace, new paving, cars, people, outdoor furniture, signage, text, logos or watermark.

### Front integrated-lighting revision

> Use case: precise-object-edit
> Asset type: photoreal architectural concept — selected Belgian Brick Lantern FRONT glass-gable elevation with integrated exterior lighting.
> Input images: Image 1 is the edit target and controls the exact building, camera, crop, perspective, site, neighbouring building, hedge, lawn, black tiled roof, continuous Belgian brick and full unobstructed front glass gable.
>
> Primary request: add a restrained, credible exterior lighting scheme to the TARGET BARN so the architecture is prepared for night use. Add one slim matte-black shielded downlight high on each of the two brick gable piers flanking the front glass wall, mounted flush or nearly flush to the brick and casting soft warm pools down the brick and threshold. Add a very subtle warm concealed linear glow within the deep black perimeter reveal at the base of the glass gable, not a bright outline. The fixtures must look permanent, minimal, weatherproof and architecturally integrated.
>
> Lighting/mood: preserve the existing natural late-afternoon/early-evening sky, green lawn, visible landscape and realistic daylight. The new lights are switched on but subtle, warm 2700K, demonstrating evening use without converting the image into darkness or overpowering the glass. Preserve the warm occupied interior.
>
> LOCK EVERYTHING ELSE: exact 17.0 x 7.5 m envelope, 3.2 m eaves, 5.2 m ridge, approximately 28-degree roof; continuous Belgian/Flemish brick on all exterior walls; black hollow ceramic Flemish roof tiles; deep matte-black glass frame; clear unobstructed glazing; same furniture, hedge, neighbour building, paved path, terrain, grass, trees, camera and composition. Do not alter window mullions, add doors, change the roof, extend the footprint or add landscaping.
>
> Avoid: wall lanterns with historic ornament, bright spotlights, uplights that cause glare, exposed cables, bollards, posts, projecting fixtures, signage, people, cars, terrace furniture, new paving, mixed wall finishes, fibre cement, text, logo or watermark.

### Shared-lane integrated-lighting revision

> Use case: precise-object-edit
> Asset type: photoreal architectural concept — selected Belgian Brick Lantern SHARED TRACTOR-LANE elevation with integrated exterior lighting.
> Input images: Image 1 is the edit target and controls the exact portrait camera, crop, perspective, lane, gate, hedge, neighbour screen, roof, continuous Belgian brick, front glass gable and every existing opening.
>
> Primary request: add a restrained, tractor-safe exterior lighting scheme along the target barn's long brick wall. Install three very low-profile matte-black shielded downlights directly beneath the eaves, aligned respectively with the rear bedroom-window zone, the tall stair window, and the larger kitchen picture window. They should project only a few centimetres and cast soft narrow warm washes down the brick, enough to define the path and openings after dark without lighting the neighbour or pasture. Keep the lane completely unobstructed: no ground fixtures, bollards, posts or projecting arms.
>
> Lighting/mood: preserve the existing blue-sky late-afternoon scene, green lane and readable landscape. Switch the new fixtures on with a subtle 2700K glow; deepen the light only slightly toward early evening so both the building and lighting effect remain clear and photorealistic. Add a quiet warm occupied glow behind the front glass gable and larger kitchen window, with realistic reflections.
>
> CRITICAL WINDOW LOCK: from the rear gate toward the glass front, preserve exactly two small black-framed bedroom windows, then one tall narrow black-framed stair window, then one larger horizontal black-framed kitchen picture window, then the full glass front gable. Do not move, resize, delete, duplicate or replace any opening. Do not turn the tall stair window into a door.
>
> LOCK EVERYTHING ELSE: exact 17.0 x 7.5 m envelope, 3.2 m eaves, 5.2 m ridge, approximately 28-degree black hollow ceramic Flemish roof; continuous Belgian/Flemish brick on all walls; same gutter/downpipe; same tractor wheel tracks, grass, hedge, gate, fence/screen, trees, camera and composition.
>
> Avoid: entrance doors on this lane, wall lanterns with historic ornament, glaring spotlights, exposed cables, bollards, posts, path pavers, gravel, vehicles, people, new landscaping, mixed wall finishes, fibre cement, text, logo or watermark.

### Timber-lined courtyard entrance revision

This entrance-material study is retained as a prompt record but is superseded
by Revision 04 for the rear-gable opening schedule: the ground floor of the
rear/private gable is solid behind the master bed.

> Use case: precise-object-edit
> Asset type: photoreal architectural concept — selected Belgian Brick Lantern REAR courtyard with a welcoming identifiable side entrance.
> Input images: Image 1 is the edit target and controls the exact portrait camera, crop, perspective, building envelope, Belgian brick, roof, broad triangular rear loft window, ground-floor windows, courtyard cobbles, curbs, hedges, hydrangeas, mature trees and lighting.
>
> Primary request: restyle only the existing entrance on the long courtyard-facing wall so it is unmistakably the home's entrance and feels welcoming. Keep the doorway in exactly its current location. Form a deep matte-black rectangular portal approximately 1.5–1.7 m wide, recessed within the thick ICF wall. Line the entire inside of that recess—both side returns, soffit, and the wall panel immediately around the door—with refined vertical smoked-oak boards. Use one full-height smoked-oak pivot or hinged door within the timber lining, a long slim matte-black pull handle, and a narrow black shadow gap around the door. Add one concealed warm 2700K downlight in the timber soffit, softly illuminating the oak face and existing cobble threshold. The portal may extend visually to the eaves line but must remain a recess, not an exterior wall-cladding field.
>
> Entrance hierarchy: the oak-lined opening should read clearly from across the courtyard as the primary entrance, warmer and more generous than the adjacent black-framed windows, yet restrained and contemporary. Keep the hedge opening and path exactly where they are. No canopy is needed.
>
> LOCK EVERYTHING ELSE: preserve the broad upper triangular black-framed loft window, the existing ground-floor opening arrangement in this superseded image, every long-wall window, continuous Belgian/Flemish brick everywhere outside the entrance recess, black hollow ceramic Flemish roof tiles, two flush rooflights, gutters/downpipes, exact 17.0 x 7.5 m footprint, 3.2 m eaves, 5.2 m ridge and approximately 28-degree roof. Preserve all cobbles, curbs, hedge geometry, hydrangeas, mature trees, access routes, shadows and camera composition.
>
> Lighting/mood: retain natural late-afternoon documentary photography. Let the entrance light be visibly warm but subtle; add no other lighting changes.
>
> Avoid: timber or fibre-cement cladding across the exterior walls, mixed wall fields, projecting porch, projecting canopy, steps that alter accessibility, new paving, terrace, signage, house numbers, sidelights that widen the structural opening, glass door, historic lantern, people, cars, furniture, text, logo or watermark.

#### Final rooflight correction

> Use case: precise-object-edit
> Asset type: photoreal architectural concept correction — rear courtyard entrance concept.
> Input images: Image 1 is the EDIT TARGET and must remain unchanged except for one rooflight correction. Image 2 is the approved previous rear reference confirming that the selected roof has exactly two flush rooflights total on the visible roof plane.
>
> Primary request: remove only the unintended extra far-left rooflight from Image 1—the rooflight highest/leftmost and partially nearest the foliage. Reconstruct continuous matching black curved ceramic Flemish roof tiles beneath it. Keep exactly the two rooflights nearer the rear gable, in their current positions and sizes.
>
> LOCK EVERYTHING ELSE FROM IMAGE 1 PIXEL-CLOSE: preserve the clearly identifiable smoked-oak entrance door, deep matte-black portal, vertical timber-lined recess, concealed warm soffit light, black pull handle, all Belgian brick, every window including the broad rear triangular loft window, roof shape, ridge, gutters, downpipes, hedges, hydrangeas, cobbles, curbs, trees, shadows, sky, camera, crop, perspective and color. Do not move or redesign the entrance. Do not add or remove any other opening.
>
> Avoid: any third rooflight, roof patch, mismatched tiles, dormer, canopy, new fixtures, new landscaping, people, cars, text, logo or watermark.

### Interior opening-alignment revision

This earlier straight-stair study is retained as a prompt record but is
superseded by the Revision 02 switchback-stair concepts below.

Its left/right camera translation is also superseded by Revision 05: from the
front glass gable looking rearward, the shared tractor lane is on the viewer's
left and the courtyard is on the viewer's right.

> Use case: precise-object-edit
> Asset type: photoreal architectural concept — selected Belgian Brick Lantern OPEN LIVING HALL AND REAR LOFT, with interior openings aligned to the approved exterior elevations.
> Input images: Image 1 is the EDIT TARGET and strictly controls the wide landscape camera, front-to-rear viewpoint, room proportions, open living/kitchen layout, rear mezzanine, stair, materials, furniture, timber portal frames and lighting. Image 2 is the authoritative SHARED-LANE ELEVATION reference for the left exterior wall opening order and proportions. Image 3 is the authoritative REAR GABLE reference for the broad upper triangular loft window. Do not copy their outdoor cameras into Image 1.
>
> Primary request: revise only the exterior-wall openings visible from inside so the interior and exterior describe the same building.
>
> REAR LOFT GABLE WINDOW: replace the solid triangular upper rear wall behind the loft furniture with the same broad, black-framed triangular gable window shown in Image 3. Its base sits just above the loft floor/guard line, it tapers below the ridge, and a substantial plastered ICF reveal remains around both sloping sides and ridge. Use one slim central vertical mullion and a restrained base transom. Through it show softly focused courtyard tree canopy and blue sky with realistic reflections. The loft reading table and chairs remain visible in front of the glass.
>
> LEFT SHARED-LANE WALL ALIGNMENT: Image 2 orders the openings from the rear toward the front as bedroom pair, tall stair window, larger kitchen picture window, then front glass gable. In Image 1 the camera stands near the front glass gable and looks toward the rear, so:
> - insert the larger black-framed horizontal kitchen picture window into the left plastered wall in the foreground, directly above/behind the kitchen worktop and sink; give it a deep ICF reveal and a view of the retained lane hedge;
> - insert one tall narrow black-framed stair window beside the stair landing on that same left wall, partially visible behind the stair and extending vertically to light the stair;
> - do NOT put the two rear bedroom windows into the open hall because they belong inside the enclosed rooms beneath the loft, behind their doors.
>
> Preserve the front glass gable behind the camera; do not create another front wall. Keep the right wall restrained because it faces the neighbouring house/courtyard and is not the shared-lane elevation.
>
> LOCK EVERYTHING ELSE FROM IMAGE 1: exact 17.0 x 7.5 m envelope, 3.2 m eaves, 5.2 m ridge, approximately 28-degree roof; compact rear mezzanine rather than full second storey; same stair position; same kitchen island, dining table, sofa, fireplace, bedroom/service doors, black balustrade, two rooflights, oak structural frames, pale mineral-plastered ICF interior, polished floor, furniture, camera, composition and warm natural light. The thick external walls and deep window reveals must remain evident.
>
> Style/medium: premium photoreal Belgian architectural interior photography, coherent natural daylight and warm 2700K interior lights, accurate plaster, oak, black aluminium and glass textures, not glossy CGI.
>
> Avoid: blank rear gable, missing side windows, random extra windows, bedroom windows opening into the living room, moving the stair, changing the loft depth, full-height rear glazing down to the bedrooms, balcony, dormer, altered roof, exposed brick inside, black exterior cladding inside, mixed wall finishes, people, text, logo or watermark.

### Revision 02 switchback stair — overall living hall

This stair-focused study is retained as a prompt record but is superseded by
the plan-aligned entrance studies below. Its long rear corridor and repeated
door row did not reflect the compact Revision 02 entry/service core.

> Use case: precise-object-edit. Asset type: photoreal architectural concept for the Belgian Brick Lantern interior — living hall looking rearward toward the master/service core and mezzanine.
>
> Image 1 is the edit target and controls the wide camera, front-to-rear viewpoint, 17.0 × 7.5 m barn proportions, approximately 28-degree roof, 3.2 m eaves, 5.2 m ridge, oak portal frames, pale mineral-plastered thick ICF walls, polished floor, kitchen, dining, living furniture, stove, rear triangular loft window, side windows, lighting and restrained Belgian character. Image 2 is the authoritative Revision 02 ground-floor plan. Image 3 is the authoritative Revision 02 mezzanine plan.
>
> Replace the single straight stair with one compact U-shaped switchback stair. It must visibly contain two parallel flights and a full half-landing at the tall shared-lane window. The lower flight begins at ground level at the living/service transition, rises toward the lane-side half-landing, turns 180 degrees, and the upper flight returns toward the room centre/ridge to a roughly 1.1 m upper landing. Use realistic smoked-oak treads and risers, slim matte-black steel handrails, continuous guards around the opening and a safe connection to the open mezzanine. Do not show one straight floor-to-loft run.
>
> Keep the mezzanine only over the rear master/service zone. The front living hall remains open to the ridge. Show low sloping eaves, low fitted storage, restrained seated furniture, a narrow central standing band and an unobstructed broad triangular rear gable window. Below it, imply a short entry gallery, flush smoked-oak service doors, coat storage and laundry/plant joinery. Keep the ground-floor route clear.
>
> Preserve the large picture window above the kitchen worktop and the tall stair window at the half-landing, both with deep 35–45 cm plastered ICF reveals. Premium photoreal Belgian interior photography, 24–28 mm lens, warm natural daylight, subtle 2700K lamps and real plaster, oak, steel, glass and fabric texture. No exposed interior brick, full second floor, loft above the front living room, raised ridge/eaves, dormer, floating stair, hotel balcony, people, text, logo or watermark.

### Revision 02 switchback stair — three-quarter detail

> Use case: precise-object-edit. Asset type: photoreal architectural interior concept — detailed three-quarter view of the Revision 02 switchback stair and mezzanine transition.
>
> Image 1 is the authoritative completed Belgian Brick Lantern interior identity. Images 2 and 3 are the authoritative Revision 02 ground-floor and mezzanine plans.
>
> Create a complementary ground-floor eye-level photograph from the front open living zone, looking diagonally toward the stair, shared-lane wall and rear mezzanine. The compact U-shaped stair is the main subject and must be unambiguously buildable: one lower smoked-oak flight rises from the living/service transition toward a full rectangular half-landing directly against the tall black-framed lane window; it turns exactly 180 degrees; one upper flight runs back parallel toward the ridge and arrives at a roughly 1.1 m upper landing connected to the rear mezzanine. Both flights must be readable, separated by a slim central stringer or guard, with realistic risers/goings, continuous black handrails and proper guard returns.
>
> Show the mezzanine only behind the stair over the master/service core. The foreground living hall stays open to the roof. Keep the broad rear triangular window clear, the eaves visibly low, and use low storage/library joinery with restrained seated furniture. Below, retain a calm entry gallery with flush smoked-oak doors and integrated storage rather than a second open room. Preserve the kitchen picture window and clear circulation.
>
> Wide 3:2, eye-level 28 mm editorial architectural photograph. Warm off-white mineral plaster, deep ICF reveals, oak structure and stair, matte-black steel, polished mineral floor, Belgian daylight and subtle warm lighting. Exactly one U-shaped stair and two connected parallel flights. No straight stair, extra stair, floating stair, blocked landing, full second floor, loft over the front living room, raised roof, dormer, exposed interior brick, people, text, logo or watermark.

### Revision 03 entrance alignment — overall living hall

This prompt record is superseded by Revision 04 below. It incorrectly mirrored
the glass-gable camera, putting the shared lane on the photograph's left and
the courtyard on its right.

> Use case: precise-object-edit. Asset type: corrected photoreal architectural website concept for the Belgian Brick Lantern interior.
>
> Image 1 is the edit target and controls the wide front-to-rear camera, Belgian Brick Lantern interior identity, furniture, pale mineral-plastered thick ICF walls, smoked oak, black metal, polished mineral floor, kitchen, dining, living area, roof volume, rear-only open mezzanine and triangular rear gable window. Images 2 and 3 are the authoritative Revision 02 ground-floor and mezzanine plans and override Image 1 wherever the entrance, service core, stair or windows conflict.
>
> The camera stands in the front double-height living hall at the valley glass gable and looks toward the rear/private gable. The left side of the photograph is the continuous shared-tractor-lane exterior wall; the right side is the continuous courtyard exterior wall. Place the compact U-shaped stair against the left lane wall at the living/service transition. Show its lower flight from the living/core boundary to the full half-landing at the tall lane window, the 180-degree turn and upper return to the guarded ridge landing.
>
> The horizontal kitchen picture window and tall stair window are openings through the same continuous exterior wall plane, with deep 35–45 cm plastered ICF reveals. The tall slot directly touches the half-landing and looks outside to the hedge and lane; it is never an internal window.
>
> Put one smoked-oak exterior entrance in the right courtyard-side wall. Its leaf swings inward into a short approximately 1.2 m gallery beside coat storage and a shoe bench. From the living room show no more than two discreet internal openings: one flush or pocket service opening for the powder/laundry area and one solid master-bedroom door farther rearward. The ensuite remains private and invisible. Remove the invented axial corridor, far-end exterior opening and repeated door row.
>
> Preserve the 17.0 × 7.5 m external envelope, approximately 3.2 m eaves, 5.2 m ridge, approximately 28.1-degree roof, selected material palette, rear triangular loft glazing, double-height front living hall and rear-only mezzanine. Premium photoreal editorial Belgian interior photography, 24–28 mm lens, real material grain, restrained daylight and subtle 2700K lighting. No entrance below a stair flight, centered freestanding stair, internalized window, long hallway, extra doors, full second floor, exposed interior brick, people, text, logo or watermark.

### Revision 03 entrance alignment — closer relationship view

This prompt record is superseded by Revision 04 below for the same mirrored
orientation error.

> Use case: photorealistic-natural with authoritative architectural references. Asset type: complementary photoreal website concept explaining the Belgian Brick Lantern entrance and U-stair relationship.
>
> Use the selected Revision 03 overall interior as the authoritative identity and spatial reference, with the Revision 02 ground-floor and mezzanine plans controlling geometry. Create a closer ground-floor eye-level photograph from the front living area looking diagonally toward the service-core transition. Give the stair and entrance equal visual importance and retain enough of the kitchen and living floor to establish orientation.
>
> On the left, keep the horizontal kitchen picture window and tall half-landing window in the same continuous shared-lane exterior ICF wall. The tall window directly touches the stair landing and clearly looks outdoors. Show one compact U-stair against this wall, with its lower flight, 180-degree turn, parallel upper return, guards and rear mezzanine connection readable.
>
> On the right, show exactly one smoked-oak exterior entrance in the courtyard-side wall. Its leaf swings inward into the short entry gallery beside integrated coat storage and a shoe bench. Show no more than two internal openings: the powder/laundry service opening and the master door. There is no axial hallway, far-end exterior opening or visible ensuite door.
>
> Wide 3:2, eye-level 26–28 mm premium Belgian interior photograph. Preserve the fixed 17.0 × 7.5 m envelope, shallow roof geometry, thick wall reveals, rear-only mezzanine, mineral plaster, oak, matte-black guards and polished mineral floor. No repeated door row, internal window, freestanding stair, entrance beneath a flight, additional opening, person, text, logo or watermark.

### Revision 04 plan/render reconciliation — superseded

This was the prior attempted reconciliation. The owner's bird's-eye markup and
Revision 05 model prove that Revision 04 itself was mirrored; the bullets below
are retained only as a historical prompt record and are **not instructions**:

- camera at the valley/full-glass gable, looking toward the rear/private gable;
- viewer left is the courtyard wall, with the living side window and one oak
  exterior entrance;
- viewer right is the shared tractor-lane wall, with the kitchen picture
  window, tall stair window and U-stair;
- the two stair flights run laterally across the building width and turn at the
  right-hand lane-wall half-landing;
- the service core is screened, with no false axial exterior doorway;
- the mezzanine begins at the 9.1 m transverse division and remains over the
  rear/core zone only;
- the rear ground-floor gable remains solid behind the master bed, while the
  broad triangular window serves only the open loft;
- the reverse valley-facing view puts kitchen/dining left and living/clear
  courtyard route right.

The selected detail is a deterministic crop of the selected overall interior,
not a separately generated room. It therefore cannot introduce a second door,
move a window or reverse the stair.

## Output files

| View | Source output |
|---|---|
| Selected Revision 04 front with plan-visible interior | `belgian-brick-front-lighting.png` |
| Selected Revision 04 shared lane with four plan openings and no door | `belgian-brick-side-lighting.png` |
| Selected Revision 04 courtyard/rear with solid master gable | `belgian-brick-back-oak-entrance.png` |
| Selected Revision 04 valley-facing living hall | `belgian-brick-interior-valley-plan-reconciled.png` |
| Selected Revision 04 rearward plan-reconciled living hall | `belgian-brick-interior-plan-reconciled.png` |
| Selected Revision 04 deterministic core detail crop | `belgian-brick-interior-plan-reconciled-detail.png` |
| Superseded mirrored Revision 03 living hall | `belgian-brick-interior-entry-aligned.png` |
| Superseded separately generated Revision 03 detail | `belgian-brick-interior-entry-stair-detail.png` |
| Superseded Revision 02 living hall with invented corridor | `belgian-brick-interior-u-stair.png` |
| Superseded Revision 02 stair detail with repeated door row | `belgian-brick-interior-stair-detail.png` |
| Superseded aligned straight-stair interior | `belgian-brick-interior-aligned-windows.png` |
| Superseded unlit front | `belgian-brick-front-site.png` |
| Superseded unlit shared lane | `belgian-brick-side-tractor-lane.png` |
| Superseded rear before entrance revision | `belgian-brick-back-loft-window.png` |
| Superseded closed rear study | `belgian-brick-back-courtyard.png` |
