#!/usr/bin/env python3
"""Generate coordinated Schorisse model assets from ``models/design.json``.

No third-party package is required. The JSON file is authoritative; this script
emits a semantic GLB, editable OBJ/MTL, STL, SVG plans, fixed-camera SVG model
views, and a validation report. Units are metres.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"
WEB_DIR = ROOT / "renders" / "web"
GEN_DIR = MODEL_DIR / "generated"
EPS = 1e-8


def load_spec(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class Scene:
    def __init__(self) -> None:
        self.elements: list[dict] = []

    def add(self, name: str, material: str, triangles: list[tuple], category: str, **meta) -> None:
        if triangles:
            self.elements.append({
                "name": name, "material": material, "triangles": triangles,
                "category": category, "meta": meta,
            })

    def box(self, name, material, x0, x1, y0, y1, z0, z1, category="building", **meta):
        if min(x1 - x0, y1 - y0, z1 - z0) <= EPS:
            return
        p = [
            (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
        ]
        faces = [
            (0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
            (3, 7, 6, 2), (0, 4, 7, 3), (1, 2, 6, 5),
        ]
        tris = []
        for a, b, c, d in faces:
            tris.extend(((p[a], p[b], p[c]), (p[a], p[c], p[d])))
        self.add(name, material, tris, category, **meta)

    def prism_x(self, name, material, profile_zy, x0, x1, category="building", **meta):
        """Extrude a convex (z,y) polygon along x."""
        front = [(x1, y, z) for z, y in profile_zy]
        back = [(x0, y, z) for z, y in profile_zy]
        tris = []
        for i in range(1, len(profile_zy) - 1):
            tris.extend(((front[0], front[i], front[i + 1]), (back[0], back[i + 1], back[i])))
        for i in range(len(profile_zy)):
            j = (i + 1) % len(profile_zy)
            tris.extend(((back[i], back[j], front[j]), (back[i], front[j], front[i])))
        self.add(name, material, tris, category, **meta)

    def beam(self, name, material, start, end, thickness=.045, category="building", **meta):
        """Create a square-section beam between two arbitrary 3D points."""
        dx, dy, dz = (end[i] - start[i] for i in range(3))
        length = math.sqrt(dx * dx + dy * dy + dz * dz)
        if length <= EPS:
            return
        direction = (dx / length, dy / length, dz / length)
        reference = (0.0, 1.0, 0.0) if abs(direction[1]) < .92 else (1.0, 0.0, 0.0)
        ux = direction[1] * reference[2] - direction[2] * reference[1]
        uy = direction[2] * reference[0] - direction[0] * reference[2]
        uz = direction[0] * reference[1] - direction[1] * reference[0]
        ulen = math.sqrt(ux * ux + uy * uy + uz * uz)
        u = (ux / ulen, uy / ulen, uz / ulen)
        v = (direction[1] * u[2] - direction[2] * u[1],
             direction[2] * u[0] - direction[0] * u[2],
             direction[0] * u[1] - direction[1] * u[0])
        half = thickness / 2

        def corner(point, su, sv):
            return tuple(point[i] + half * (su * u[i] + sv * v[i]) for i in range(3))

        p = [corner(start, -1, -1), corner(start, 1, -1), corner(start, 1, 1), corner(start, -1, 1),
             corner(end, -1, -1), corner(end, 1, -1), corner(end, 1, 1), corner(end, -1, 1)]
        faces = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
                 (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
        tris = []
        for a, b, c, d in faces:
            tris.extend(((p[a], p[b], p[c]), (p[a], p[c], p[d])))
        self.add(name, material, tris, category, **meta)

    def vertices(self):
        for element in self.elements:
            for tri in element["triangles"]:
                yield from tri


MATERIALS = {
    "brick": {"color": (0.52, 0.25, 0.15, 1.0), "rough": 0.92},
    "roof": {"color": (0.055, 0.06, 0.065, 1.0), "rough": 0.85},
    "glass": {"color": (0.35, 0.68, 0.78, 0.36), "rough": 0.08, "blend": True},
    "frame": {"color": (0.035, 0.04, 0.045, 1.0), "rough": 0.48},
    "oak": {"color": (0.34, 0.20, 0.11, 1.0), "rough": 0.75},
    "partition": {"color": (0.82, 0.79, 0.71, 1.0), "rough": 0.94},
    "floor": {"color": (0.69, 0.64, 0.55, 1.0), "rough": 0.90},
    "stair": {"color": (0.43, 0.27, 0.15, 1.0), "rough": 0.72},
    "guard": {"color": (0.07, 0.075, 0.08, 1.0), "rough": 0.50},
    "cabinet": {"color": (0.26, 0.22, 0.18, 1.0), "rough": 0.78},
    "furniture": {"color": (0.66, 0.58, 0.47, 1.0), "rough": 0.90},
    "sanitary": {"color": (0.88, 0.89, 0.86, 1.0), "rough": 0.45},
    "mezzanine": {"color": (0.48, 0.34, 0.22, 1.0), "rough": 0.75},
    "site": {"color": (0.28, 0.42, 0.20, 1.0), "rough": 1.0},
    "cobble": {"color": (0.43, 0.40, 0.35, 1.0), "rough": 1.0},
}


def gable_profile(spec):
    env = spec["envelope"]
    return [(0, 0), (env["width"], 0), (env["width"], env["eaves_height"]),
            (env["width"] / 2, env["ridge_height"]), (0, env["eaves_height"])]


def add_sloped_bar_x(scene, name, material, x0, x1, start_zy, end_zy,
                     thickness=.055, category="opening_frame", **meta):
    """Extrude a constant-depth bar along a line in the z/y plane."""
    z0, y0 = start_zy
    z1, y1 = end_zy
    dz, dy = z1 - z0, y1 - y0
    length = math.hypot(dz, dy)
    if length <= EPS:
        return
    nz, ny = -dy / length * thickness / 2, dz / length * thickness / 2
    profile = [
        (z0 + nz, y0 + ny), (z1 + nz, y1 + ny),
        (z1 - nz, y1 - ny), (z0 - nz, y0 - ny),
    ]
    scene.prism_x(name, material, profile, x0, x1, category, **meta)


def add_segmented_wall(scene, name, host, openings, spec):
    """Create a thick long wall with actual voids, split around each opening."""
    env = spec["envelope"]
    L, W, H, T = env["length"], env["width"], env["eaves_height"], env["external_wall_build_up"]
    intervals = sorted((o["x"][0], o["x"][1], o["y"][0], o["y"][1], o) for o in openings)
    cursor = 0.0
    z0, z1 = (0, T) if host == "tractor_lane_z0" else (W - T, W)
    wall_category = "lane_wall_structure" if host == "tractor_lane_z0" else "courtyard_wall_structure"
    for index, (x0, x1, y0, y1, opening) in enumerate(intervals):
        if x0 > cursor:
            scene.box(f"{name}_pier_{index}", "brick", cursor, x0, 0, H, z0, z1, wall_category)
        if y0 > 0:
            scene.box(f"{name}_{opening['id']}_sill", "brick", x0, x1, 0, y0, z0, z1, wall_category)
        if y1 < H:
            scene.box(f"{name}_{opening['id']}_head", "brick", x0, x1, y1, H, z0, z1, wall_category)
        depth0, depth1 = ((0.03, T - 0.03) if host == "tractor_lane_z0" else (W - T + 0.03, W - 0.03))
        material = "oak" if opening["type"] == "door" else "glass"
        scene.box(opening["id"], material, x0 + 0.04, x1 - 0.04, y0 + 0.02, y1 - 0.04,
                  depth0, depth1, "courtyard_wall" if host == "courtyard_zW" else "lane_wall",
                  opening=opening["id"])
        frame_t = 0.055
        scene.box(f"{opening['id']}_frame_left", "frame", x0, x0 + frame_t, y0, y1, depth0, depth1, "opening_frame")
        scene.box(f"{opening['id']}_frame_right", "frame", x1 - frame_t, x1, y0, y1, depth0, depth1, "opening_frame")
        scene.box(f"{opening['id']}_frame_head", "frame", x0, x1, y1 - frame_t, y1, depth0, depth1, "opening_frame")
        if opening["type"] != "door":
            scene.box(f"{opening['id']}_frame_sill", "frame", x0, x1, y0, y0 + frame_t, depth0, depth1, "opening_frame")
        else:
            # Thin smoked-oak linings make the courtyard entrance legible without
            # changing the one-metre structural opening or continuous brick wall.
            scene.box(f"{opening['id']}_oak_reveal_left", "oak", x0 + frame_t, x0 + frame_t + .02,
                      y0, y1 - frame_t, depth0, depth1, "entrance_detail")
            scene.box(f"{opening['id']}_oak_reveal_right", "oak", x1 - frame_t - .02, x1 - frame_t,
                      y0, y1 - frame_t, depth0, depth1, "entrance_detail")
            scene.box(f"{opening['id']}_oak_reveal_head", "oak", x0 + frame_t, x1 - frame_t,
                      y1 - frame_t - .02, y1 - frame_t, depth0, depth1, "entrance_detail")
        cursor = x1
    if cursor < L:
        scene.box(f"{name}_pier_end", "brick", cursor, L, 0, H, z0, z1, wall_category)


def add_valley_gable(scene, spec, opening):
    env = spec["envelope"]
    W, H, R, T = env["width"], env["eaves_height"], env["ridge_height"], env["external_wall_build_up"]
    inset = opening["side_inset"]
    profile = [(inset, opening["base"]), (W - inset, opening["base"]),
               (W - inset, H - 0.08), (W / 2, R - opening["head_inset"]), (inset, H - 0.08)]
    scene.prism_x("front_glass_gable", "glass", profile, 0.03, 0.07, "front_glazing")
    scene.box("front_left_brick_return", "brick", 0, T, 0, H, 0, inset, "wall")
    scene.box("front_right_brick_return", "brick", 0, T, 0, H, W - inset, W, "wall")
    scene.box("front_base_frame", "frame", 0.02, 0.10, opening["base"], opening["base"] + .075,
              inset, W - inset, "opening_frame")
    scene.box("front_left_jamb", "frame", 0.02, 0.10, opening["base"], H - .08,
              inset - .04, inset + .04, "opening_frame")
    scene.box("front_right_jamb", "frame", 0.02, 0.10, opening["base"], H - .08,
              W - inset - .04, W - inset + .04, "opening_frame")
    add_sloped_bar_x(scene, "front_left_slope_frame", "frame", 0.02, 0.10,
                     (inset, H - .08), (W / 2, R - opening["head_inset"]), .075)
    add_sloped_bar_x(scene, "front_right_slope_frame", "frame", 0.02, 0.10,
                     (W - inset, H - .08), (W / 2, R - opening["head_inset"]), .075)
    scene.box("front_center_mullion", "frame", 0.02, 0.10, 0, R - .18, W / 2 - .045, W / 2 + .045, "opening_frame")
    scene.box("front_transom", "frame", 0.02, 0.10, 2.94, 3.04, inset, W - inset, "opening_frame")
    scene.box("front_slider_mullion_left", "frame", 0.02, 0.10, 0, 3.0, W / 2 - 1.86, W / 2 - 1.78, "opening_frame")
    scene.box("front_slider_mullion_right", "frame", 0.02, 0.10, 0, 3.0, W / 2 + 1.78, W / 2 + 1.86, "opening_frame")


def add_rear_gable(scene, spec, opening):
    env = spec["envelope"]
    L, W, H, R, T = env["length"], env["width"], env["eaves_height"], env["ridge_height"], env["external_wall_build_up"]
    z0, z1 = opening["base_z"]
    apex_y, apex_z = opening["apex_y"], opening["apex_z"]
    # Build around a true triangular void: solid ground floor plus two gable cheeks.
    scene.box("rear_gable_ground_solid", "brick", L - T, L, 0, opening["base_y"], 0, W, "wall")
    left_profile = [(0, opening["base_y"]), (z0, opening["base_y"]),
                    (apex_z, apex_y), (W / 2, R), (0, H)]
    right_profile = [(apex_z, apex_y), (z1, opening["base_y"]),
                     (W, opening["base_y"]), (W, H), (W / 2, R)]
    scene.prism_x("rear_gable_left_cheek", "brick", left_profile, L - T, L, "wall")
    scene.prism_x("rear_gable_right_cheek", "brick", right_profile, L - T, L, "wall")
    glass_profile = [(z0, opening["base_y"]), (z1, opening["base_y"]), (apex_z, apex_y)]
    scene.prism_x("rear_loft_window", "glass", glass_profile, L - T + .01, L - T + .05, "rear_glazing")
    scene.box("rear_loft_base_frame", "frame", L - T, L - T + .08, opening["base_y"], opening["base_y"] + .07, z0, z1, "opening_frame")
    add_sloped_bar_x(scene, "rear_loft_left_slope_frame", "frame", L - T, L - T + .08,
                     (z0, opening["base_y"]), (apex_z, apex_y), .07)
    add_sloped_bar_x(scene, "rear_loft_right_slope_frame", "frame", L - T, L - T + .08,
                     (z1, opening["base_y"]), (apex_z, apex_y), .07)
    scene.box("rear_loft_center_mullion", "frame", L - T, L - T + .08, opening["base_y"], apex_y, apex_z - .035, apex_z + .035, "opening_frame")


def add_partition_x(scene, name, x, z0, z1, openings, spec, height=None):
    T = .12
    H = height or spec["levels"]["mezzanine_finished_floor"]
    cursor = z0
    for op in sorted(openings, key=lambda item: item["z"][0]):
        a, b = op["z"]
        if a > cursor:
            scene.box(f"{name}_{cursor:.2f}", "partition", x - T / 2, x + T / 2, 0, H, cursor, a, "partition")
        scene.box(f"{op['id']}_head", "partition", x - T / 2, x + T / 2,
                  spec["levels"]["internal_door_height"], H, a, b, "partition")
        cursor = b
    if cursor < z1:
        scene.box(f"{name}_end", "partition", x - T / 2, x + T / 2, 0, H, cursor, z1, "partition")


def add_partition_z(scene, name, z, x0, x1, openings, spec, height=None):
    T = .12
    H = height or spec["levels"]["mezzanine_finished_floor"]
    cursor = x0
    for op in sorted(openings, key=lambda item: item["x"][0]):
        a, b = op["x"]
        if a > cursor:
            scene.box(f"{name}_{cursor:.2f}", "partition", cursor, a, 0, H, z - T / 2, z + T / 2, "partition")
        scene.box(f"{op['id']}_head", "partition", a, b, spec["levels"]["internal_door_height"], H,
                  z - T / 2, z + T / 2, "partition")
        cursor = b
    if cursor < x1:
        scene.box(f"{name}_end", "partition", cursor, x1, 0, H, z - T / 2, z + T / 2, "partition")


def add_stair(scene, spec):
    s = spec["stair"]
    riser, going = s["riser"], s["going"]
    x0, x1 = s["lower_flight_x"]
    ux0, ux1 = s["upper_flight_x"]
    z_land0, z_land1 = s["half_landing_z"]
    lower_z0, lower_z1 = s["lower_flight_z"]
    upper_z0, upper_z1 = s["upper_flight_z"]
    half_y = s["lower_risers"] * riser
    top_y = s["risers_total"] * riser

    scene.box("stair_half_landing", "stair", x0, ux1, half_y - .16, half_y, z_land0, z_land1, "stair")
    scene.box("stair_top_landing", "stair", ux0, ux1, top_y - .18, top_y,
              s["top_landing_z"][0], s["top_landing_z"][1], "stair")

    # Lower flight climbs toward the lane (decreasing z).
    for i in range(s["lower_risers"] - 1):
        y0 = i * riser
        za = lower_z1 - (i + 1) * going
        zb = lower_z1 - i * going
        scene.box(f"stair_lower_tread_{i + 1:02d}", "stair", x0, x1, y0, y0 + riser, za, zb, "stair")

    # Upper flight returns toward the ridge/courtyard (increasing z).
    for i in range(s["upper_risers"] - 1):
        y0 = half_y + i * riser
        za = upper_z0 + i * going
        zb = upper_z0 + (i + 1) * going
        scene.box(f"stair_upper_tread_{i + 1:02d}", "stair", ux0, ux1, y0, y0 + riser, za, zb, "stair")

    # Slim guard posts at landings make the U-turn legible without blocking views.
    for index, (x, z, y0) in enumerate(((x0, z_land1, half_y), (ux1, z_land1, half_y),
                                        (ux0, s["top_landing_z"][1], top_y))):
        scene.box(f"stair_guard_post_{index + 1}", "guard", x - .022, x + .022, y0, y0 + s["guard_height"],
                  z - .022, z + .022, "guard")

    # Handrails follow the actual rise direction of both flights. Their end
    # points are semantic geometry so a downstream renderer cannot invent a
    # straight stair or detach the two runs.
    rail_h = .9
    lower_start_z = lower_z1 - going / 2
    lower_end_z = lower_z0 + going / 2
    lower_end_y = (s["lower_risers"] - 1) * riser
    upper_start_z = upper_z0 + going / 2
    upper_end_z = upper_z1 - going / 2
    upper_end_y = half_y + (s["upper_risers"] - 1) * riser
    for side, x in (("outer", x0 + .04), ("inner", x1 - .04)):
        scene.beam(f"stair_lower_{side}_handrail", "guard",
                   (x, rail_h, lower_start_z), (x, lower_end_y + rail_h, lower_end_z),
                   .04, "guard")
    for side, x in (("inner", ux0 + .04), ("outer", ux1 - .04)):
        scene.beam(f"stair_upper_{side}_handrail", "guard",
                   (x, half_y + rail_h, upper_start_z), (x, upper_end_y + rail_h, upper_end_z),
                   .04, "guard")
    add_guard_line(scene, "stair_half_landing_guard",
                   (x0, z_land0), (ux1, z_land0), half_y, s["guard_height"])


def add_mezzanine(scene, spec):
    m = spec["mezzanine"]
    floor_y = spec["levels"]["mezzanine_finished_floor"]
    t = spec["levels"]["mezzanine_structure"]
    x0, x1 = m["x"]
    z0, z1 = m["z"]
    sx0, sx1 = m["stair_opening_x"]
    sz0, sz1 = m["stair_opening_z"]
    # Four rectangles around the stair opening.
    scene.box("mezzanine_front_strip", "mezzanine", x0, sx0, floor_y - t, floor_y, z0, z1, "mezzanine")
    scene.box("mezzanine_rear_strip", "mezzanine", sx1, x1, floor_y - t, floor_y, z0, z1, "mezzanine")
    scene.box("mezzanine_lane_strip", "mezzanine", sx0, sx1, floor_y - t, floor_y, z0, sz0, "mezzanine")
    scene.box("mezzanine_courtyard_strip", "mezzanine", sx0, sx1, floor_y - t, floor_y, sz1, z1, "mezzanine")
    guard_h = spec["stair"]["guard_height"]
    add_guard_line(scene, "mezzanine_front_guard", (x0, z0), (x0, z1), floor_y, guard_h)
    # The x=sx1 guard stops at the top-landing depth, leaving a 1.10 m clear
    # exit onto the mezzanine instead of trapping the upper flight behind rail.
    add_guard_line(scene, "stair_opening_guard_rear", (sx1, sz0), (sx1, spec["stair"]["top_landing_z"][0]), floor_y, guard_h)
    add_guard_line(scene, "stair_opening_guard_courtyard", (sx0, sz1), (sx1, sz1), floor_y, guard_h)


def add_guard_line(scene, name, start_xz, end_xz, base_y, height):
    """Model a readable 1 m guard as posts plus top rail, not a solid black slab."""
    x0, z0 = start_xz; x1, z1 = end_xz
    length = math.hypot(x1 - x0, z1 - z0)
    count = max(2, math.ceil(length / .9) + 1)
    for index in range(count):
        t = index / (count - 1)
        x = x0 + (x1 - x0) * t; z = z0 + (z1 - z0) * t
        scene.box(f"{name}_post_{index + 1:02d}", "guard", x - .018, x + .018, base_y, base_y + height,
                  z - .018, z + .018, "guard")
    rail = .045
    if abs(x1 - x0) < EPS:
        scene.box(f"{name}_top_rail", "guard", x0 - rail / 2, x0 + rail / 2,
                  base_y + height - rail, base_y + height, min(z0, z1), max(z0, z1), "guard")
    else:
        scene.box(f"{name}_top_rail", "guard", min(x0, x1), max(x0, x1),
                  base_y + height - rail, base_y + height, z0 - rail / 2, z0 + rail / 2, "guard")


def add_roof(scene, spec):
    env = spec["envelope"]
    L, W, H, R = env["length"], env["width"], env["eaves_height"], env["ridge_height"]
    oh, goh, t = env["eaves_overhang"], env["gable_overhang"], env["roof_build_up"]
    slope = (R - H) / (W / 2)
    z0 = -oh
    low_y = H + slope * z0
    lane = [(z0, low_y), (W / 2, R), (W / 2, R + t), (z0, low_y + t)]
    courtyard = [(W - z, y) for z, y in lane]
    courtyard.reverse()
    scene.prism_x("roof_lane_slope", "roof", lane, -goh, L + goh, "roof")
    scene.prism_x("roof_courtyard_slope", "roof", courtyard, -goh, L + goh, "roof")


def add_furniture(scene, spec):
    for item in spec["furniture_and_fixtures"]:
        x0, x1 = item["x"]
        z0, z1 = item["z"]
        material = {"cabinet": "cabinet", "sanitary": "sanitary", "shower": "sanitary"}.get(item["kind"], "furniture")
        scene.box(item["id"], material, x0, x1, 0.02, item["height"], z0, z1, "furniture", fixture=item["kind"])


def add_internal_doors(scene, spec):
    """Add semantic door leaves/panels using the operation declared in JSON."""
    height = spec["levels"]["internal_door_height"] - .04
    partitions = {partition["id"]: partition for partition in spec["interior_partitions"]}
    for door in spec["interior_doors"]:
        partition = partitions[door["host"]]
        axis = partition["axis"]
        coordinate = partition["coordinate"]
        if "hinged" in door["operation"] and axis == "x":
            hinge = door["z"][0]
            scene.box(door["id"], "oak", coordinate + .02, coordinate + door["clear_width"],
                      .02, height, hinge - .025, hinge + .025, "internal_door",
                      operation=door["operation"], state="shown_open_90_degrees")
        elif "pocket" in door["operation"]:
            a, b = door["z"] if axis == "x" else door["x"]
            if door.get("pocket_direction") == "toward_lower_coordinate":
                a, b = a - door["clear_width"], a
            else:
                a, b = b, b + door["clear_width"]
            if axis == "x":
                scene.box(door["id"], "oak", coordinate - .025, coordinate + .025,
                          .02, height, a, b, "internal_door",
                          operation=door["operation"], state="retracted_in_pocket")
            else:
                scene.box(door["id"], "oak", a, b, .02, height,
                          coordinate - .025, coordinate + .025, "internal_door",
                          operation=door["operation"], state="retracted_in_pocket")
        elif "sliding" in door["operation"] and axis == "z":
            a, b = door["x"]
            middle = (a + b) / 2
            scene.box(f"{door['id']}_panel_1", "oak", a, middle + .04, .02, height,
                      coordinate - .035, coordinate, "internal_door",
                      operation=door["operation"], state="shown_closed")
            scene.box(f"{door['id']}_panel_2", "oak", middle - .04, b, .02, height,
                      coordinate, coordinate + .035, "internal_door",
                      operation=door["operation"], state="shown_closed")


def build_scene(spec):
    scene = Scene()
    env = spec["envelope"]
    L, W = env["length"], env["width"]
    ext = spec["exterior_openings"]
    by_host = {}
    for opening in ext:
        by_host.setdefault(opening["host"], []).append(opening)

    # Site context is diagrammatic, never survey geometry.
    scene.box("tractor_lane_context", "site", -2, L + 2, -.04, 0, -3.0, -.35, "site")
    scene.box("courtyard_cobbles_context", "cobble", -2, L + 3, -.035, 0, W + .35, W + 4.2, "site")
    scene.box("ground_floor_slab", "floor", .42, L - .42, -.08, 0, .42, W - .42, "floor")

    add_segmented_wall(scene, "tractor_lane_wall", "tractor_lane_z0", by_host["tractor_lane_z0"], spec)
    add_segmented_wall(scene, "courtyard_wall", "courtyard_zW", by_host["courtyard_zW"], spec)
    add_valley_gable(scene, spec, by_host["valley_gable_x0"][0])
    add_rear_gable(scene, spec, by_host["rear_gable_xL"][0])

    doors = {door["id"]: door for door in spec["interior_doors"]}
    for partition in spec["interior_partitions"]:
        partition_doors = [doors[door_id] for door_id in partition["door_ids"]]
        a, b = partition["span"]
        if partition["axis"] == "x":
            add_partition_x(scene, partition["id"], partition["coordinate"], a, b,
                            partition_doors, spec)
        else:
            add_partition_z(scene, partition["id"], partition["coordinate"], a, b,
                            partition_doors, spec)

    add_stair(scene, spec)
    add_mezzanine(scene, spec)
    add_furniture(scene, spec)
    add_internal_doors(scene, spec)
    add_roof(scene, spec)
    return scene


def normal(a, b, c):
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    vx, vy, vz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
    length = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return nx / length, ny / length, nz / length


def export_stl(scene, path):
    elements = [e for e in scene.elements if e["category"] != "site"]
    triangles = [(e, tri) for e in elements for tri in e["triangles"]]
    with path.open("wb") as handle:
        handle.write(b"Schorisse coordinated model - metres".ljust(80, b"\0"))
        handle.write(struct.pack("<I", len(triangles)))
        for _, (a, b, c) in triangles:
            handle.write(struct.pack("<12fH", *normal(a, b, c), *a, *b, *c, 0))


def export_obj(scene, obj_path, mtl_path):
    with mtl_path.open("w", encoding="utf-8") as mtl:
        for name, material in MATERIALS.items():
            r, g, b, a = material["color"]
            mtl.write(f"newmtl {name}\nKd {r:.4f} {g:.4f} {b:.4f}\nd {a:.4f}\nNs 10\n\n")
    with obj_path.open("w", encoding="utf-8") as obj:
        obj.write(f"# Generated from design.json; metres\nmtllib {mtl_path.name}\n")
        index = 1
        for element in scene.elements:
            obj.write(f"\no {element['name']}\nusemtl {element['material']}\n")
            for tri in element["triangles"]:
                for x, y, z in tri:
                    obj.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
                obj.write(f"f {index} {index + 1} {index + 2}\n")
                index += 3


def add_buffer_view(gltf, blob, data, target):
    offset = len(blob)
    blob.extend(data)
    blob.extend(b"\0" * ((4 - len(data) % 4) % 4))
    gltf["bufferViews"].append({"buffer": 0, "byteOffset": offset, "byteLength": len(data), "target": target})
    return len(gltf["bufferViews"]) - 1


def export_glb(scene, path, spec):
    used = [m for m in MATERIALS if any(e["material"] == m for e in scene.elements)]
    materials = []
    for name in used:
        item = MATERIALS[name]
        entry = {
            "name": name,
            "doubleSided": True,
            "pbrMetallicRoughness": {
                "baseColorFactor": list(item["color"]),
                "metallicFactor": 0.0,
                "roughnessFactor": item["rough"],
            },
        }
        if item.get("blend"):
            entry["alphaMode"] = "BLEND"
        materials.append(entry)
    mat_index = {name: i for i, name in enumerate(used)}
    gltf = {
        "asset": {"version": "2.0", "generator": "schorisse-build gen_model.py"},
        "scene": 0,
        "scenes": [{"nodes": []}],
        "nodes": [], "meshes": [], "materials": materials,
        "accessors": [], "bufferViews": [], "buffers": [],
        "extras": {
            "source": "models/design.json",
            "model_revision": spec["model_revision"],
            "units": "metres",
            "axes": spec["axes"],
            "photoreal_approved": spec["approval"]["geometry_approved_for_photoreal"],
        },
    }
    blob = bytearray()
    for element in scene.elements:
        positions, normals = [], []
        for a, b, c in element["triangles"]:
            n = normal(a, b, c)
            positions.extend((a, b, c))
            normals.extend((n, n, n))
        flat_pos = [number for point in positions for number in point]
        flat_nrm = [number for point in normals for number in point]
        pos_view = add_buffer_view(gltf, blob, struct.pack(f"<{len(flat_pos)}f", *flat_pos), 34962)
        gltf["accessors"].append({
            "bufferView": pos_view, "componentType": 5126, "count": len(positions), "type": "VEC3",
            "min": [min(p[i] for p in positions) for i in range(3)],
            "max": [max(p[i] for p in positions) for i in range(3)],
        })
        pos_accessor = len(gltf["accessors"]) - 1
        nrm_view = add_buffer_view(gltf, blob, struct.pack(f"<{len(flat_nrm)}f", *flat_nrm), 34962)
        gltf["accessors"].append({"bufferView": nrm_view, "componentType": 5126, "count": len(normals), "type": "VEC3"})
        nrm_accessor = len(gltf["accessors"]) - 1
        indices = list(range(len(positions)))
        idx_view = add_buffer_view(gltf, blob, struct.pack(f"<{len(indices)}I", *indices), 34963)
        gltf["accessors"].append({"bufferView": idx_view, "componentType": 5125, "count": len(indices), "type": "SCALAR"})
        idx_accessor = len(gltf["accessors"]) - 1
        gltf["meshes"].append({
            "name": element["name"],
            "primitives": [{
                "attributes": {"POSITION": pos_accessor, "NORMAL": nrm_accessor},
                "indices": idx_accessor, "material": mat_index[element["material"]],
            }],
            "extras": {"category": element["category"], **element["meta"]},
        })
        gltf["nodes"].append({"name": element["name"], "mesh": len(gltf["meshes"]) - 1})
        gltf["scenes"][0]["nodes"].append(len(gltf["nodes"]) - 1)
    gltf["buffers"] = [{"byteLength": len(blob)}]
    js = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
    js += b" " * ((4 - len(js) % 4) % 4)
    payload = (b"glTF" + struct.pack("<II", 2, 12 + 8 + len(js) + 8 + len(blob))
               + struct.pack("<I", len(js)) + b"JSON" + js
               + struct.pack("<I", len(blob)) + b"BIN\0" + bytes(blob))
    path.write_bytes(payload)


def validate(spec, scene):
    checks = []

    def check(name, ok, detail):
        checks.append({"name": name, "status": "pass" if ok else "fail", "detail": detail})

    env = spec["envelope"]
    check("external envelope", env["length"] == 17.0 and env["width"] == 7.5,
          f"{env['length']:.2f} x {env['width']:.2f} m")
    check("thick external walls", .35 <= env["external_wall_build_up"] <= .45,
          f"{env['external_wall_build_up']:.2f} m build-up")
    shell_categories = {"wall", "lane_wall_structure", "courtyard_wall_structure"}
    shell_vertices = [point for element in scene.elements if element["category"] in shell_categories
                      for tri in element["triangles"] for point in tri]
    shell_bounds = tuple((min(p[i] for p in shell_vertices), max(p[i] for p in shell_vertices)) for i in range(3))
    expected_bounds = ((0.0, env["length"]), (0.0, env["ridge_height"]), (0.0, env["width"]))
    bounds_ok = all(abs(shell_bounds[i][j] - expected_bounds[i][j]) < .001 for i in range(3) for j in range(2))
    check("modeled shell bounds", bounds_ok,
          f"x={shell_bounds[0][0]:.2f}..{shell_bounds[0][1]:.2f}; "
          f"y={shell_bounds[1][0]:.2f}..{shell_bounds[1][1]:.2f}; "
          f"z={shell_bounds[2][0]:.2f}..{shell_bounds[2][1]:.2f} m")
    hosts = {opening["id"]: opening["host"] for opening in spec["exterior_openings"]}
    check("courtyard entry host", hosts.get("courtyard_entry") == "courtyard_zW",
          f"courtyard_entry host = {hosts.get('courtyard_entry')}")
    check("valley glass gable host", hosts.get("front_glass_gable") == "valley_gable_x0",
          f"front_glass_gable host = {hosts.get('front_glass_gable')}")
    check("rear loft window host", hosts.get("rear_loft_window") == "rear_gable_xL",
          f"rear_loft_window host = {hosts.get('rear_loft_window')}")
    for host in ("tractor_lane_z0", "courtyard_zW"):
        ops = sorted((o for o in spec["exterior_openings"] if o["host"] == host), key=lambda o: o["x"][0])
        clear = all(ops[i]["x"][1] <= ops[i + 1]["x"][0] for i in range(len(ops) - 1))
        inside = all(0 <= o["x"][0] < o["x"][1] <= env["length"] and 0 <= o["y"][0] < o["y"][1] <= env["eaves_height"] for o in ops)
        check(f"{host} opening bounds", clear and inside, f"{len(ops)} non-overlapping openings inside wall")
    door_by_id = {door["id"]: door for door in spec["interior_doors"]}
    partition_ids = {partition["id"] for partition in spec["interior_partitions"]}
    door_hosts_ok = all(door["host"] in partition_ids for door in spec["interior_doors"])
    check("interior door hosts", door_hosts_ok,
          "every interior door is assigned to a named partition")
    partition_doors_ok = True
    partition_details = []
    for partition in spec["interior_partitions"]:
        span0, span1 = partition["span"]
        openings = sorted((door_by_id[door_id] for door_id in partition["door_ids"]),
                          key=lambda door: door["z"][0] if partition["axis"] == "x" else door["x"][0])
        extents = [door["z"] if partition["axis"] == "x" else door["x"] for door in openings]
        inside = all(span0 <= a < b <= span1 for a, b in extents)
        separate = all(extents[i][1] <= extents[i + 1][0] for i in range(len(extents) - 1))
        partition_doors_ok &= inside and separate
        partition_details.append(f"{partition['id']}:{len(extents)}")
    check("partition door bounds", partition_doors_ok,
          "; ".join(partition_details))
    pocket_depth_ok = True
    pocket_details = []
    for door in (item for item in spec["interior_doors"] if "pocket" in item["operation"]):
        partition = next(item for item in spec["interior_partitions"] if item["id"] == door["host"])
        a, b = door["z"] if partition["axis"] == "x" else door["x"]
        available = a - partition["span"][0] if door.get("pocket_direction") == "toward_lower_coordinate" else partition["span"][1] - b
        ok = available + .001 >= door["clear_width"]
        pocket_depth_ok &= ok
        pocket_details.append(f"{door['id']} {available:.2f}/{door['clear_width']:.2f} m")
    check("pocket door cavities", pocket_depth_ok, "; ".join(pocket_details))
    m = spec["mezzanine"]
    stair = spec["stair"]
    stacked = m["stair_opening_x"] == stair["x"] and m["stair_opening_z"] == stair["z"]
    check("stair opening stacks", stacked, "ground stair and mezzanine void use identical x/z extents")
    riser_total = stair["risers_total"] * stair["riser"]
    check("stair reaches mezzanine", abs(riser_total - spec["levels"]["mezzanine_finished_floor"]) < .001,
          f"{stair['risers_total']} x {stair['riser']:.3f} = {riser_total:.3f} m")
    comfort = 2 * stair["riser"] + stair["going"]
    check("stair comfort rule", .60 <= comfort <= .64, f"2R+G = {comfort:.3f} m")
    check("stair clear width", stair["flight_clear_width"] >= .90, f"{stair['flight_clear_width']:.2f} m")
    check("landing depth", stair["landing_depth"] >= stair["flight_clear_width"],
          f"{stair['landing_depth']:.2f} m landing vs {stair['flight_clear_width']:.2f} m flight")
    lower_run = stair["lower_flight_z"][1] - stair["lower_flight_z"][0]
    upper_run = stair["upper_flight_z"][1] - stair["upper_flight_z"][0]
    run_ok = (abs(lower_run - (stair["lower_risers"] - 1) * stair["going"]) < .001 and
              abs(upper_run - (stair["upper_risers"] - 1) * stair["going"]) < .001)
    check("stair runs match tread count", run_ok,
          f"lower {lower_run:.3f} m; upper {upper_run:.3f} m at {stair['going']:.3f} m going")
    half_height = stair["lower_risers"] * stair["riser"]
    landing_inner_edge = stair["half_landing_z"][0]
    roof_inside = (env["eaves_height"] +
                   (env["ridge_height"] - env["eaves_height"]) * (landing_inner_edge / (env["width"] / 2)) -
                   env["roof_build_up"])
    headroom = roof_inside - half_height
    check("half-landing headroom", headroom >= stair["minimum_target_headroom"],
          f"{headroom:.3f} m at the lowest landing edge under assumed roof build-up")
    stair_inside = (env["external_wall_build_up"] <= stair["x"][0] < stair["x"][1] <= env["length"] - env["external_wall_build_up"] and
                    env["external_wall_build_up"] <= stair["z"][0] < stair["z"][1] <= env["width"] - env["external_wall_build_up"])
    check("stair footprint inside shell", stair_inside,
          f"x={stair['x'][0]:.2f}..{stair['x'][1]:.2f}; z={stair['z'][0]:.2f}..{stair['z'][1]:.2f} m")
    exit_width = stair["top_landing_z"][1] - stair["top_landing_z"][0]
    check("top landing exits to mezzanine", exit_width >= stair["flight_clear_width"],
          f"{exit_width:.2f} m clear exit beyond shortened opening guard")
    check("mezzanine stays over rear", m["x"][0] == 7.9 and m["x"][1] <= env["length"] - env["external_wall_build_up"],
          f"x={m['x'][0]:.2f}..{m['x'][1]:.2f}; front {m['x'][0]:.2f} m remains double-height")
    interior_limits_ok = True
    offending = []
    for item in spec["furniture_and_fixtures"]:
        if not (env["external_wall_build_up"] <= item["x"][0] < item["x"][1] <= env["length"] - env["external_wall_build_up"] and
                env["external_wall_build_up"] <= item["z"][0] < item["z"][1] <= env["width"] - env["external_wall_build_up"] and
                0 < item["height"] <= env["eaves_height"]):
            interior_limits_ok = False
            offending.append(item["id"])
    check("fixture bounds inside shell", interior_limits_ok,
          "all fixtures inside clear envelope" if interior_limits_ok else f"outside: {', '.join(offending)}")
    fixtures = {item["id"]: item for item in spec["furniture_and_fixtures"]}
    sanitary_brief = spec["sanitary_brief"]
    modeled_wc_ids = sorted(item["id"] for item in spec["furniture_and_fixtures"]
                            if item["id"].endswith("_wc"))
    required_wc_ids = sorted(sanitary_brief["toilet_fixture_ids"])
    single_toilet_ok = (sanitary_brief["total_toilets"] == 1 and
                        not sanitary_brief["ensuite_has_toilet"] and
                        modeled_wc_ids == required_wc_ids == ["powder_wc"])
    check("single-toilet sanitary brief", single_toilet_ok,
          f"modeled WC fixtures: {', '.join(modeled_wc_ids)}; ensuite WC: "
          f"{'yes' if sanitary_brief['ensuite_has_toilet'] else 'no'}")

    def gap(a, b, axis):
        index = 0 if axis == "x" else 1
        key = "x" if axis == "x" else "z"
        return b[key][0] - a[key][1]
    kitchen_aisle = gap(fixtures["kitchen_wall_run"], fixtures["kitchen_island"], "z")
    check("kitchen working aisle", kitchen_aisle >= 1.0,
          f"{kitchen_aisle:.2f} m clear between wall run and island")
    dining_transition = gap(fixtures["dining_table"], fixtures["kitchen_island"], "x")
    check("dining to kitchen transition", dining_transition >= 1.0,
          f"{dining_transition:.2f} m clear between dining table and island")
    threshold_clear = min(item["x"][0] for item in fixtures.values()) - env["external_wall_build_up"]
    check("valley threshold clear", threshold_clear >= 1.1,
          f"{threshold_clear:.2f} m clear before first furniture")
    courtyard_route = env["width"] - env["external_wall_build_up"] - max(
        fixtures["living_sofa"]["z"][1], fixtures["dining_table"]["z"][1], fixtures["kitchen_island"]["z"][1])
    check("courtyard-side circulation", courtyard_route >= 1.2,
          f"{courtyard_route:.2f} m clear route along courtyard side")
    master = next(zone for zone in spec["longitudinal_zones"] if zone["id"] == "master_bedroom")
    master_door = door_by_id["master_door"]
    master_fixtures = [item for item in spec["furniture_and_fixtures"]
                       if item["id"] in {"master_bed", "master_wardrobe_lane", "master_wardrobe_courtyard"}]
    swing_x0, swing_x1 = master_door["coordinate"], master_door["coordinate"] + master_door["clear_width"]
    swing_z0, swing_z1 = master_door["z"]
    master_swing_clear = all(item["x"][1] <= swing_x0 or item["x"][0] >= swing_x1 or
                             item["z"][1] <= swing_z0 or item["z"][0] >= swing_z1
                             for item in master_fixtures)
    check("master door swing clear", master_swing_clear,
          f"{master_door['clear_width']:.2f} m leaf zone clear of bed and wardrobes")
    scene_names = {e["name"] for e in scene.elements}
    for required in ("front_glass_gable", "courtyard_entry", "rear_loft_window", "stair_half_landing", "stair_top_landing"):
        check(f"semantic element {required}", required in scene_names, "present as named 3D element")
    check("semantic element mezzanine_front_guard",
          any(name.startswith("mezzanine_front_guard_") for name in scene_names),
          "present as named posts and top rail")
    check("semantic stair handrails",
          all(name in scene_names for name in ("stair_lower_outer_handrail", "stair_lower_inner_handrail",
                                               "stair_upper_inner_handrail", "stair_upper_outer_handrail")),
          "both flights have explicit inner and outer rails")
    check("semantic sloped gable frames",
          all(name in scene_names for name in ("front_left_slope_frame", "front_right_slope_frame",
                                               "rear_loft_left_slope_frame", "rear_loft_right_slope_frame")),
          "front and rear triangular glazing perimeters are modeled")
    internal_door_geometry_ok = all(door["id"] in scene_names or
                                    all(f"{door['id']}_panel_{index}" in scene_names for index in (1, 2))
                                    for door in spec["interior_doors"])
    check("semantic internal doors", internal_door_geometry_ok,
          "hinged, pocket and sliding door elements are present in the 3D model")
    passed = all(item["status"] == "pass" for item in checks)
    return {
        "model_revision": spec["model_revision"],
        "source": "models/design.json",
        "status": "pass" if passed else "fail",
        "photoreal_gate": "open" if passed and spec["approval"]["geometry_approved_for_photoreal"] else "blocked_pending_geometry_approval",
        "checks": checks,
        "semantic_elements": len(scene.elements),
        "triangles": sum(len(e["triangles"]) for e in scene.elements),
    }


def svg_header(title, subtitle, spec):
    revision = spec["model_revision"].split("-", 1)[0]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="850" viewBox="0 0 1400 850" role="img" aria-label="{html.escape(title)}">
<rect width="1400" height="850" fill="#f4f0e7"/>
<text x="70" y="58" font-family="Arial,sans-serif" font-size="12" font-weight="700" letter-spacing="2" fill="#b4522e">MODEL-GENERATED · REV {html.escape(revision)}</text>
<text x="70" y="98" font-family="Arial,sans-serif" font-size="32" font-weight="700" fill="#1d1b18">{html.escape(title)}</text>
<text x="70" y="126" font-family="Arial,sans-serif" font-size="14" fill="#686158">{html.escape(subtitle)}</text>
'''


def export_ground_plan(spec, path):
    env = spec["envelope"]
    L, W, T = env["length"], env["width"], env["external_wall_build_up"]
    sx, sy = 58, 58
    ox, oy = 205, 190
    mx, mz = lambda x: ox + x * sx, lambda z: oy + z * sy
    out = [svg_header("Ground floor — approved layout", "Valley glass at left · cobbled courtyard and entrance below · master/mezzanine at right", spec)]
    # Site labels and dimensions.
    out.append(f'<text x="{mx(L/2):.1f}" y="170" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#9a472a">SHARED TRACTOR LANE</text>')
    out.append(f'<text x="{mx(L/2):.1f}" y="650" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#9a472a">COBBLED COURTYARD · SIDE ENTRANCE</text>')
    out.append(f'<text x="{mx(0)-15:.1f}" y="160" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#4f4a43">VALLEY GLASS</text>')
    out.append(f'<text x="{mx(L)+5:.1f}" y="160" text-anchor="end" font-family="Arial" font-size="11" font-weight="700" fill="#4f4a43">BEDROOM / MEZZANINE GABLE</text>')
    # Shell and floors.
    out.append(f'<rect x="{mx(0)}" y="{mz(0)}" width="{L*sx}" height="{W*sy}" fill="#211f1b"/>')
    colors = {"open_living": "#e2e7de", "service_core": "#dedbd2", "master_bedroom": "#e8ded1"}
    for zone in spec["longitudinal_zones"][:3]:
        x0, x1 = zone["x"]; z0, z1 = zone["z"]
        out.append(f'<rect x="{mx(x0)}" y="{mz(z0)}" width="{(x1-x0)*sx}" height="{(z1-z0)*sy}" fill="{colors[zone["id"]]}"/>')
    # Room overlays; wall and door geometry is drawn later from the same spec.
    room_label_positions = []
    room_labels = {
        "ensuite": "ENSUITE",
        "laundry_plant": "LAUNDRY / PLANT",
        "powder_room": "POWDER",
        "entry_gallery": "ENTRY GALLERY",
    }
    for room in spec["rooms"]:
        x0, x1 = room["x"]; z0, z1 = room["z"]
        out.append(f'<rect x="{mx(x0)}" y="{mz(z0)}" width="{(x1-x0)*sx}" height="{(z1-z0)*sy}" fill="#f7f3ea" fill-opacity=".34"/>')
        room_label_positions.append((room, room_labels[room["id"]]))
    # Exterior openings.
    for opening in spec["exterior_openings"]:
        host, color = opening["host"], "#2f6f81"
        if host == "tractor_lane_z0":
            out.append(f'<line x1="{mx(opening["x"][0])}" x2="{mx(opening["x"][1])}" y1="{mz(0)}" y2="{mz(0)}" stroke="{color}" stroke-width="15"/>')
        elif host == "courtyard_zW":
            out.append(f'<line x1="{mx(opening["x"][0])}" x2="{mx(opening["x"][1])}" y1="{mz(W)}" y2="{mz(W)}" stroke="{color}" stroke-width="15"/>')
            if opening["type"] == "door":
                hx, hy = mx(opening["x"][1]), mz(W - T)
                leaf = (opening["x"][1] - opening["x"][0]) * sx
                out.append(f'<path d="M{hx:.1f} {hy:.1f}v-{leaf:.1f}A{leaf:.1f} {leaf:.1f} 0 0 1 {hx-leaf:.1f} {hy:.1f}" fill="none" stroke="#a64d2d" stroke-width="3"/>')
        elif host == "valley_gable_x0":
            out.append(f'<line x1="{mx(0)}" x2="{mx(0)}" y1="{mz(T)}" y2="{mz(W-T)}" stroke="#315f9f" stroke-width="18"/>')
    # Interior wall lines with actual openings.
    wall = '#514c44'; wall_w = 5
    def line(x1, z1, x2, z2, stroke=wall, width=wall_w, dash=''):
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
        out.append(f'<line x1="{mx(x1):.1f}" y1="{mz(z1):.1f}" x2="{mx(x2):.1f}" y2="{mz(z2):.1f}" stroke="{stroke}" stroke-width="{width}"{dash_attr}/>')
    doors_by_id = {door["id"]: door for door in spec["interior_doors"]}
    for partition in spec["interior_partitions"]:
        openings = sorted((doors_by_id[door_id] for door_id in partition["door_ids"]),
                          key=lambda door: door["z"][0] if partition["axis"] == "x" else door["x"][0])
        cursor = partition["span"][0]
        for door in openings:
            a, b = door["z"] if partition["axis"] == "x" else door["x"]
            if a > cursor:
                if partition["axis"] == "x":
                    line(partition["coordinate"], cursor, partition["coordinate"], a)
                else:
                    line(cursor, partition["coordinate"], a, partition["coordinate"])
            cursor = b
        if cursor < partition["span"][1]:
            if partition["axis"] == "x":
                line(partition["coordinate"], cursor, partition["coordinate"], partition["span"][1])
            else:
                line(cursor, partition["coordinate"], partition["span"][1], partition["coordinate"])
    # Ensuite pocket symbol.
    line(12.43, 2.52, 12.43, 3.38, '#a64d2d', 2)
    line(12.57, 2.52, 12.57, 3.38, '#a64d2d', 2)
    # Master door swings into the bedroom against a blank wall.
    master_door = doors_by_id["master_door"]
    master_leaf = (master_door["z"][1] - master_door["z"][0]) * sy
    hx, hy = mx(master_door["coordinate"]), mz(master_door["z"][0])
    out.append(f'<path d="M{hx:.1f} {hy:.1f}h{master_leaf:.1f}A{master_leaf:.1f} {master_leaf:.1f} 0 0 1 {hx:.1f} {mz(master_door["z"][1]):.1f}" fill="none" stroke="#a64d2d" stroke-width="3"/>')
    # Powder pocket door and laundry sliding pair.
    line(10.67, 5.72, 11.39, 5.72, '#a64d2d', 2)
    line(9.92, 5.88, 10.64, 5.88, '#a64d2d', 2, '5 3')
    line(11.62, 5.72, 12.08, 5.72, '#a64d2d', 2)
    line(11.88, 5.88, 12.34, 5.88, '#a64d2d', 2)
    # Stair footprint and direction.
    s = spec["stair"]
    x0, x1 = s["lower_flight_x"]; ux0, ux1 = s["upper_flight_x"]
    lz0, lz1 = s["lower_flight_z"]; uz0, uz1 = s["upper_flight_z"]
    out.append(f'<rect x="{mx(x0)}" y="{mz(lz0)}" width="{(x1-x0)*sx}" height="{(lz1-lz0)*sy}" fill="#c8bdad" stroke="#514c44" stroke-width="3"/>')
    out.append(f'<rect x="{mx(ux0)}" y="{mz(uz0)}" width="{(ux1-ux0)*sx}" height="{(uz1-uz0)*sy}" fill="#d7cfc2" stroke="#514c44" stroke-width="3"/>')
    z0, z1 = s["half_landing_z"]
    out.append(f'<rect x="{mx(x0)}" y="{mz(z0)}" width="{(ux1-x0)*sx}" height="{(z1-z0)*sy}" fill="#a69a88" stroke="#514c44" stroke-width="3"/>')
    for i in range(s["lower_risers"] + 1):
        z = lz1 - i * s["going"]
        out.append(f'<line x1="{mx(x0)}" x2="{mx(x1)}" y1="{mz(z)}" y2="{mz(z)}" stroke="#514c44" stroke-width="2"/>')
    for i in range(s["upper_risers"] + 1):
        z = uz0 + i * s["going"]
        out.append(f'<line x1="{mx(ux0)}" x2="{mx(ux1)}" y1="{mz(z)}" y2="{mz(z)}" stroke="#514c44" stroke-width="2"/>')
    out.append(f'<path d="M{mx((x0+x1)/2):.1f} {mz(lz1):.1f}V{mz(lz0):.1f}" stroke="#b4522e" stroke-width="4" marker-end="url(#none)"/><text x="{mx((x0+x1)/2):.1f}" y="{mz((lz0+lz1)/2):.1f}" text-anchor="middle" font-family="Arial" font-size="10" font-weight="700" fill="#9a472a" transform="rotate(-90 {mx((x0+x1)/2):.1f} {mz((lz0+lz1)/2):.1f})">UP 6 RISERS TO LANE LANDING</text>')
    out.append(f'<text x="{mx((ux0+ux1)/2):.1f}" y="{mz((uz0+uz1)/2):.1f}" text-anchor="middle" font-family="Arial" font-size="10" font-weight="700" fill="#9a472a" transform="rotate(90 {mx((ux0+ux1)/2):.1f} {mz((uz0+uz1)/2):.1f})">TURN 180° · UP 8 TO MEZZANINE</text>')
    # Fixture/furniture footprints. Titles retain exact semantic IDs; only
    # selected small-room fixtures receive visible labels below.
    fixture_labels = {
        "italian_shower": "ITALIAN SHOWER",
        "ensuite_vanity": "VANITY",
        "powder_wc": "WC",
        "powder_basin": "BASIN",
        "laundry_bank": "LAUNDRY",
        "entry_coats": "COATS",
    }
    for item in spec["furniture_and_fixtures"]:
        x0, x1 = item["x"]; z0, z1 = item["z"]
        fill = "#625b51" if item["kind"] == "cabinet" else "#d0c0aa"
        out.append(f'<rect x="{mx(x0)}" y="{mz(z0)}" width="{(x1-x0)*sx}" height="{(z1-z0)*sy}" rx="3" fill="{fill}" stroke="#514c44" stroke-width="2"><title>{html.escape(item["id"])}</title></rect>')
        if item["id"] in fixture_labels:
            out.append(f'<text x="{mx((x0+x1)/2):.1f}" y="{mz((z0+z1)/2)+3:.1f}" text-anchor="middle" font-family="Arial" font-size="6.8" font-weight="700" fill="#f4f0e7">{fixture_labels[item["id"]]}</text>')
    # Major labels and camera translation.
    labels = [(4.0, 5.0, "OPEN LIVING"), (4.2, 1.65, "KITCHEN"), (14.45, 4.9, "MASTER BEDROOM")]
    for x, z, label in labels:
        out.append(f'<text x="{mx(x):.1f}" y="{mz(z):.1f}" text-anchor="middle" font-family="Arial" font-size="16" font-weight="700" fill="#211f1b">{label}</text>')
    # Compact service-room labels sit in reserved clear bands.
    for room, label in room_label_positions:
        x0, x1 = room["x"]; z0, z1 = room["z"]
        cx = mx((x0 + x1) / 2)
        cy = mz(z0) + 12 if room["id"] != "entry_gallery" else mz(z1) - 22
        out.append(f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" font-family="Arial" font-size="7.2" font-weight="700" fill="#4f4a43">{html.escape(label)}</text>')
    entry = next(o for o in spec["exterior_openings"] if o["id"] == "courtyard_entry")
    out.append(f'<text x="{mx(sum(entry["x"])/2):.1f}" y="{mz(W)+18:.1f}" text-anchor="middle" font-family="Arial" font-size="10" font-weight="700" fill="#4f4a43">SIDE ENTRANCE</text>')
    out.append(f'<text x="70" y="730" font-family="Arial" font-size="13" fill="#4f4a43">17.0 × 7.5 m external · 420 mm placeholder ICF/insulation/cavity/brick build-up</text>')
    out.append(f'<text x="70" y="754" font-family="Arial" font-size="13" fill="#4f4a43">All rooms, openings, furniture and stair geometry are generated from models/design.json.</text>')
    out.append(f'<rect x="740" y="700" width="590" height="82" rx="8" fill="#211f1b"/><text x="762" y="729" font-family="Arial" font-size="11" font-weight="700" fill="#fff">CAMERA AT VALLEY GLASS LOOKING INWARD</text><text x="762" y="757" font-family="Arial" font-size="13" fill="#fff">Viewer left: lane + kitchen + stair</text><text x="1052" y="757" font-family="Arial" font-size="13" fill="#fff">Viewer right: courtyard + entrance</text>')
    out.append('<text x="70" y="825" font-family="Arial" font-size="12" fill="#686158">Geometry-review model only. Measured survey, architect, engineer, fire and code review remain required.</text></svg>')
    path.write_text("\n".join(out), encoding="utf-8")


def export_mezzanine_plan(spec, path):
    env = spec["envelope"]
    L, W = env["length"], env["width"]
    sx, sy, ox, oy = 58, 58, 205, 190
    mx, mz = lambda x: ox + x * sx, lambda z: oy + z * sy
    m, s = spec["mezzanine"], spec["stair"]
    out = [svg_header("Upper mezzanine — stair and void coordinated", "One open room over the rear zone · no plumbing · valley living remains double-height", spec)]
    out.append(f'<rect x="{mx(0)}" y="{mz(0)}" width="{L*sx}" height="{W*sy}" fill="#211f1b"/>')
    out.append(f'<rect x="{mx(m["x"][0])}" y="{mz(m["z"][0])}" width="{(m["x"][1]-m["x"][0])*sx}" height="{(m["z"][1]-m["z"][0])*sy}" fill="#eee6d8"/>')
    out.append(f'<rect x="{mx(.42)}" y="{mz(.42)}" width="{(m["x"][0]-.42)*sx}" height="{(W-.84)*sy}" fill="#e2e7de" stroke="#9b968d" stroke-width="3" stroke-dasharray="12 10"/>')
    sx0, sx1 = m["stair_opening_x"]; sz0, sz1 = m["stair_opening_z"]
    out.append(f'<rect x="{mx(sx0)}" y="{mz(sz0)}" width="{(sx1-sx0)*sx}" height="{(sz1-sz0)*sy}" fill="#f4f0e7" stroke="#514c44" stroke-width="4"/>')
    # Show the stair below as a coordinated dashed underlay and the upper run solid.
    lx0, lx1 = s["lower_flight_x"]; lz0, lz1 = s["lower_flight_z"]
    ux0, ux1 = s["upper_flight_x"]; uz0, uz1 = s["upper_flight_z"]
    out.append(f'<rect x="{mx(lx0)}" y="{mz(lz0)}" width="{(lx1-lx0)*sx}" height="{(lz1-lz0)*sy}" fill="#d7cfc2" fill-opacity=".35" stroke="#777168" stroke-width="2" stroke-dasharray="7 5"/>')
    out.append(f'<rect x="{mx(ux0)}" y="{mz(uz0)}" width="{(ux1-ux0)*sx}" height="{(uz1-uz0)*sy}" fill="#d7cfc2" stroke="#514c44" stroke-width="3"/>')
    for i in range(s["upper_risers"]):
        z = uz0 + i * s["going"]
        out.append(f'<line x1="{mx(ux0)}" x2="{mx(ux1)}" y1="{mz(z)}" y2="{mz(z)}" stroke="#514c44" stroke-width="1.5"/>')
    hz0, hz1 = s["half_landing_z"]
    out.append(f'<rect x="{mx(lx0)}" y="{mz(hz0)}" width="{(ux1-lx0)*sx}" height="{(hz1-hz0)*sy}" fill="#c8bdad" fill-opacity=".65" stroke="#777168" stroke-width="2" stroke-dasharray="7 5"/>')
    top0, top1 = s["top_landing_z"]
    out.append(f'<rect x="{mx(s["upper_flight_x"][0])}" y="{mz(top0)}" width="{(s["upper_flight_x"][1]-s["upper_flight_x"][0])*sx}" height="{(top1-top0)*sy}" fill="#d7cfc2" stroke="#514c44" stroke-width="3"/>')
    out.append(f'<line x1="{mx(m["front_guard_x"])}" x2="{mx(m["front_guard_x"])}" y1="{mz(.42)}" y2="{mz(W-.42)}" stroke="#211f1b" stroke-width="8"/>')
    out.append(f'<text x="{mx(3.9)}" y="{mz(3.7)}" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="#4f4a43">OPEN TO BELOW</text>')
    out.append(f'<text x="{mx(14.2)}" y="{mz(3.7)}" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="#4f4a43">ONE OPEN MEZZANINE ROOM</text>')
    out.append(f'<text x="{mx(14.2)}" y="{mz(4.05)}" text-anchor="middle" font-family="Arial" font-size="13" fill="#686158">library · lounge · project space · no plumbing</text>')
    out.append(f'<text x="{mx(sx1)+12:.1f}" y="{mz(top1)+3:.1f}" font-family="Arial" font-size="9" font-weight="700" fill="#9a472a">PROTECTED TOP LANDING</text>')
    out.append(f'<text x="{mx(L/2)}" y="170" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#9a472a">SHARED TRACTOR LANE · TALL STAIR WINDOW AT HALF-LANDING</text>')
    out.append(f'<text x="{mx(L/2)}" y="650" text-anchor="middle" font-family="Arial" font-size="11" font-weight="700" fill="#9a472a">COURTYARD · SIDE ENTRANCE BELOW</text>')
    out.append(f'<text x="70" y="760" font-family="Arial" font-size="13" fill="#4f4a43">Mezzanine x={m["x"][0]:.2f}..{m["x"][1]:.2f} m · floor +{spec["levels"]["mezzanine_finished_floor"]:.2f} m · exact stair opening stacks with ground floor</text>')
    out.append(f'<text x="70" y="790" font-family="Arial" font-size="13" fill="#4f4a43">Dog-leg stair: {s["lower_risers"]} lower + {s["upper_risers"]} upper risers · {s["riser"]*1000:.0f} mm rise · {s["going"]*1000:.0f} mm going · 2R+G={(2*s["riser"]+s["going"])*1000:.0f} mm</text>')
    out.append('<text x="70" y="825" font-family="Arial" font-size="12" fill="#686158">Headroom bands require a measured roof section; model checks only the assumed lane landing condition.</text></svg>')
    path.write_text("\n".join(out), encoding="utf-8")


def camera_basis(eye, target):
    f = [target[i] - eye[i] for i in range(3)]
    fl = math.sqrt(sum(v * v for v in f)); f = [v / fl for v in f]
    up_world = [0.0, 1.0, 0.0]
    r = [f[1] * up_world[2] - f[2] * up_world[1], f[2] * up_world[0] - f[0] * up_world[2], f[0] * up_world[1] - f[1] * up_world[0]]
    rl = math.sqrt(sum(v * v for v in r)); r = [v / rl for v in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    return r, u, f


def project(point, eye, basis, width=1400, height=850, focal=950):
    r, u, f = basis
    rel = [point[i] - eye[i] for i in range(3)]
    cx, cy, cz = sum(rel[i] * r[i] for i in range(3)), sum(rel[i] * u[i] for i in range(3)), sum(rel[i] * f[i] for i in range(3))
    if cz <= .05:
        return None
    return width / 2 + focal * cx / cz, height / 2 - focal * cy / cz, cz


def export_camera_svg(scene, spec, camera, path):
    eye, target = camera["eye"], camera["target"]
    basis = camera_basis(eye, target)
    omitted = set(camera["omit_categories"])
    polygons = []
    for element in scene.elements:
        if element["category"] in omitted:
            continue
        for tri in element["triangles"]:
            points = [project(p, eye, basis, focal=camera.get("focal", 650)) for p in tri]
            if any(p is None for p in points):
                continue
            depth = sum(p[2] for p in points) / 3
            coords = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in points)
            color = MATERIALS[element["material"]]["color"]
            rgb = tuple(round(c * 255) for c in color[:3])
            opacity = color[3]
            polygons.append((depth, f'<polygon points="{coords}" fill="rgb{rgb}" fill-opacity="{opacity:.2f}" stroke="#282722" stroke-opacity=".22" stroke-width=".55"><title>{html.escape(element["name"])}</title></polygon>'))
    polygons.sort(reverse=True)
    title = camera["id"].replace("_", " ").title()
    out = [svg_header(title, camera["purpose"], spec)]
    out.extend(poly for _, poly in polygons)
    out.append(f'<rect x="70" y="735" width="1260" height="66" rx="8" fill="#211f1b" fill-opacity=".92"/><text x="92" y="760" font-family="Arial" font-size="12" font-weight="700" fill="#fff">FIXED CAMERA: {html.escape(camera["id"])}</text><text x="92" y="784" font-family="Arial" font-size="13" fill="#fff">Generated from models/design.json · use this exact geometry and angle as the photoreal structural reference</text>')
    out.append('</svg>')
    path.write_text("\n".join(out), encoding="utf-8")


def write_handoff(spec, report):
    s = spec["stair"]
    gate = "open" if spec["approval"]["geometry_approved_for_photoreal"] else "blocked"
    content = f"""# Model-first design handoff

Status: **geometry approved; photoreal generation gate is {gate}**

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
- floor-to-floor: {spec['levels']['mezzanine_finished_floor']:.2f} m;
- {s['risers_total']} risers at {s['riser']*1000:.0f} mm: {s['lower_risers']} lower + {s['upper_risers']} upper;
- going: {s['going']*1000:.0f} mm; 2R+G = {(2*s['riser']+s['going'])*1000:.0f} mm;
- clear flight width: {s['flight_clear_width']:.2f} m;
- half-landing at the tall lane window, then 180-degree return;
- protected top landing connects inside the rear mezzanine;
- assumed half-landing headroom: {next(c['detail'] for c in report['checks'] if c['name'] == 'half-landing headroom')}.

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
"geometry_approved_for_photoreal": true
```

The owner approved this geometry on {spec['approval']['approved_on']}. Future
structural changes must close the gate again until their regenerated model views
and plans are approved.
"""
    (ROOT / "HANDOFF.md").write_text(content, encoding="utf-8")


def write_workflow_doc(spec):
    content = """# Model-first rendering workflow

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
"""
    (ROOT / "docs" / "MODEL-FIRST-WORKFLOW.md").write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate generated files are current; do not keep rewrites")
    args = parser.parse_args()
    MODEL_DIR.mkdir(exist_ok=True); WEB_DIR.mkdir(parents=True, exist_ok=True); GEN_DIR.mkdir(parents=True, exist_ok=True)
    spec = load_spec(MODEL_DIR / "design.json")
    scene = build_scene(spec)
    report = validate(spec, scene)
    if report["status"] != "pass":
        for item in report["checks"]:
            if item["status"] == "fail":
                print(f"FAIL: {item['name']}: {item['detail']}")
        raise SystemExit(1)

    targets = [
        MODEL_DIR / "barn.glb", MODEL_DIR / "barn.obj", MODEL_DIR / "barn.mtl", MODEL_DIR / "barn.stl",
        WEB_DIR / "plan-ground-floor.svg", WEB_DIR / "plan-mezzanine.svg",
        *[GEN_DIR / f"{camera['id'].replace('_', '-')}.svg" for camera in spec["reference_cameras"]],
        GEN_DIR / "model-report.json", ROOT / "HANDOFF.md", ROOT / "docs" / "MODEL-FIRST-WORKFLOW.md",
    ]
    before = {path: path.read_bytes() if path.exists() else None for path in targets}
    export_glb(scene, MODEL_DIR / "barn.glb", spec)
    export_obj(scene, MODEL_DIR / "barn.obj", MODEL_DIR / "barn.mtl")
    export_stl(scene, MODEL_DIR / "barn.stl")
    export_ground_plan(spec, WEB_DIR / "plan-ground-floor.svg")
    export_mezzanine_plan(spec, WEB_DIR / "plan-mezzanine.svg")
    for camera in spec["reference_cameras"]:
        export_camera_svg(scene, spec, camera, GEN_DIR / f"{camera['id'].replace('_', '-')}.svg")
    (GEN_DIR / "model-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_handoff(spec, report)
    write_workflow_doc(spec)
    if args.check:
        changed = [str(path.relative_to(ROOT)) for path in targets if before[path] != path.read_bytes()]
        if changed:
            print("Generated files were stale:")
            print("\n".join(f"  {path}" for path in changed))
            raise SystemExit(1)
    print(f"PASS: {len(report['checks'])} checks; {report['semantic_elements']} semantic elements; {report['triangles']} triangles")
    print(f"Photoreal gate: {report['photoreal_gate']}")


if __name__ == "__main__":
    main()
