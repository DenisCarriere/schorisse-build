#!/usr/bin/env python3
"""Generate the Glass-Gable Barn massing model (STL + GLB) from the concept
board's dimensions: 17.0 x 7.5 m footprint, eaves 3.2 m, ridge 5.2 m,
glazed gable at the valley end, timber door bay on the courtyard side.

Axes: x = length (0..17, glass gable at x=17), y = up, z = width (0..7.5).
Units: meters.
"""
import json, struct, os

L, W = 17.0, 7.5
EAVES, RIDGE = 3.2, 5.2
T = 0.30          # wall thickness
OH = 0.45         # roof overhang at eaves
GOH = 0.18        # roof overhang at gables
ROOF_T = 0.15

# ---------------------------------------------------------------- geometry --
TRIS = []  # (material, v0, v1, v2) with outward-ish winding

def tri(mat, a, b, c):
    TRIS.append((mat, a, b, c))

def quad(mat, a, b, c, d):
    tri(mat, a, b, c); tri(mat, a, c, d)

def box(mat, x0, x1, y0, y1, z0, z1):
    p = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
         (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    quad(mat, p[0],p[3],p[2],p[1])   # z0 face (normal -z)
    quad(mat, p[4],p[5],p[6],p[7])   # z1 face (+z)
    quad(mat, p[0],p[1],p[5],p[4])   # y0 (-y)
    quad(mat, p[3],p[7],p[6],p[2])   # y1 (+y)
    quad(mat, p[0],p[4],p[7],p[3])   # x0 (-x)
    quad(mat, p[1],p[2],p[6],p[5])   # x1 (+x)

def prism_x(mat, profile_zy, x0, x1):
    """Extrude a convex polygon (z,y) along x. Profile CCW when viewed from +x."""
    n = len(profile_zy)
    front = [(x1, y, z) for z, y in profile_zy]
    back  = [(x0, y, z) for z, y in profile_zy]
    for i in range(1, n-1):                      # end caps (fan)
        tri(mat, front[0], front[i], front[i+1])
        tri(mat, back[0], back[i+1], back[i])
    for i in range(n):                           # sides
        j = (i+1) % n
        quad(mat, back[i], back[j], front[j], front[i])

GABLE = [(0,0), (W,0), (W,EAVES), (W/2,RIDGE), (0,EAVES)]  # CCW from +x

def roof_y(z):
    """Roof underside height at cross-position z (south slope, z<=W/2)."""
    return EAVES + (RIDGE-EAVES) * (z/(W/2))

# Brick envelope
box('brick', 0, L, 0, EAVES, 0, T)            # courtyard long wall (z=0)
box('brick', 0, L, 0, EAVES, W-T, W)          # garden long wall (z=W)
prism_x('brick', GABLE, 0, T)                 # closed gable, x=0

# Glass gable at x=L: inset glazed pentagon + slim dark mullions
INSET = 0.25
GLASS_PENTA = [(INSET,0.02), (W-INSET,0.02), (W-INSET,EAVES-0.10),
               (W/2,RIDGE-0.12), (INSET,EAVES-0.10)]
prism_x('glass', GLASS_PENTA, L-0.06, L-0.01)
# perimeter frame legs
box('dark', L-0.08, L+0.02, 0, EAVES, 0, INSET)              # left jamb
box('dark', L-0.08, L+0.02, 0, EAVES, W-INSET, W)            # right jamb
# transom at 3.0 m + center mullion + slider-edge mullions
box('dark', L-0.04, L+0.03, 2.95, 3.05, INSET, W-INSET)
box('dark', L-0.04, L+0.03, 0, RIDGE-0.20, W/2-0.04, W/2+0.04)
box('dark', L-0.04, L+0.03, 0, 3.0, W/2-1.90, W/2-1.82)
box('dark', L-0.04, L+0.03, 0, 3.0, W/2+1.82, W/2+1.90)

# Roof: two sloped slabs with overhang
z_lo = -OH
y_lo = roof_y(z_lo)
south = [(z_lo,y_lo), (W/2,RIDGE), (W/2,RIDGE+ROOF_T), (z_lo,y_lo+ROOF_T)]
north = [(W-z, y) for z, y in south]   # mirror about z=W/2
north.reverse()
prism_x('roof', south, -GOH, L+GOH)
prism_x('roof', north, -GOH, L+GOH)

# Courtyard side (z=0): dark timber door bay in the old barn-door position
BAY_W = 3.5
box('timber', L/2-BAY_W/2, L/2+BAY_W/2, 0, EAVES-0.15, -0.05, 0.10)
# two fixed windows (from courtyard elevation, 1:100)
box('window', 1.75, 4.00, 0.70, 2.00, -0.03, 0.08)
box('window', 12.50, 14.75, 0.70, 2.00, -0.03, 0.08)

# Flush stone terrace on the lawn side
box('stone', L, L+3.0, 0, 0.06, -0.4, W+0.4)

STL_MATS = {'brick','glass','dark','roof','timber','window','stone'}

# GLB-only site context
box('hedge', L-0.6, L+0.8, 0, 1.15, -2.4, -1.1)
box('hedge', L-0.6, L+0.8, 0, 1.15, W+1.1, W+2.4)
box('ground', -14, L+14, -0.02, 0.0, -12, W+12)

# ------------------------------------------------------------------- export --
def normal(a, b, c):
    ux, uy, uz = b[0]-a[0], b[1]-a[1], b[2]-a[2]
    vx, vy, vz = c[0]-a[0], c[1]-a[1], c[2]-a[2]
    nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    l = (nx*nx+ny*ny+nz*nz) ** .5 or 1.0
    return (nx/l, ny/l, nz/l)

os.makedirs('/Users/denis/Github/schorisse-build/models', exist_ok=True)

# --- binary STL (building only, meters)
stl_tris = [t for t in TRIS if t[0] in STL_MATS]
with open('/Users/denis/Github/schorisse-build/models/barn.stl', 'wb') as f:
    f.write(b'Glass-Gable Barn 17.0x7.5m massing (meters)'.ljust(80, b'\0'))
    f.write(struct.pack('<I', len(stl_tris)))
    for mat, a, b, c in stl_tris:
        n = normal(a, b, c)
        f.write(struct.pack('<12fH', *n, *a, *b, *c, 0))
print('STL:', len(stl_tris), 'triangles')

# --- GLB (glTF 2.0, flat-shaded, one primitive per material)
MATERIALS = {
    'brick':  dict(color=(0x95/255, 0x59/255, 0x3f/255, 1.0), rough=0.95),
    'roof':   dict(color=(0x7a/255, 0x3e/255, 0x27/255, 1.0), rough=0.9),
    'glass':  dict(color=(0x9d/255, 0xb6/255, 0xb8/255, 0.45), rough=0.05, blend=True),
    'dark':   dict(color=(0x26/255, 0x22/255, 0x1c/255, 1.0), rough=0.6),
    'timber': dict(color=(0x42/255, 0x38/255, 0x2d/255, 1.0), rough=0.85),
    'window': dict(color=(0x3c/255, 0x46/255, 0x48/255, 0.85), rough=0.2, blend=True),
    'stone':  dict(color=(0xcf/255, 0xc6/255, 0xb2/255, 1.0), rough=0.9),
    'hedge':  dict(color=(0x46/255, 0x56/255, 0x3a/255, 1.0), rough=1.0),
    'ground': dict(color=(0xa8/255, 0xb7/255, 0x88/255, 1.0), rough=1.0),
}
order = [m for m in MATERIALS if any(t[0] == m for t in TRIS)]
bin_parts, views, accessors, primitives, materials = b'', [], [], [], []

def add_view(data, target):
    global bin_parts
    off = len(bin_parts)
    bin_parts += data + b'\0' * ((4 - len(data) % 4) % 4)
    views.append({'buffer': 0, 'byteOffset': off, 'byteLength': len(data), 'target': target})
    return len(views) - 1

for mi, mat in enumerate(order):
    tris = [t for t in TRIS if t[0] == mat]
    pos, nrm = [], []
    for _, a, b, c in tris:
        n = normal(a, b, c)
        pos += [a, b, c]; nrm += [n, n, n]
    flat = [x for p in pos for x in p]
    pv = add_view(struct.pack('<%df' % len(flat), *flat), 34962)
    accessors.append({'bufferView': pv, 'componentType': 5126, 'count': len(pos),
                      'type': 'VEC3',
                      'min': [min(p[i] for p in pos) for i in range(3)],
                      'max': [max(p[i] for p in pos) for i in range(3)]})
    pa = len(accessors) - 1
    flatn = [x for p in nrm for x in p]
    nv = add_view(struct.pack('<%df' % len(flatn), *flatn), 34962)
    accessors.append({'bufferView': nv, 'componentType': 5126, 'count': len(nrm), 'type': 'VEC3'})
    na = len(accessors) - 1
    idx = list(range(len(pos)))
    iv = add_view(struct.pack('<%dI' % len(idx), *idx), 34963)
    accessors.append({'bufferView': iv, 'componentType': 5125, 'count': len(idx), 'type': 'SCALAR'})
    ia = len(accessors) - 1
    primitives.append({'attributes': {'POSITION': pa, 'NORMAL': na}, 'indices': ia, 'material': mi})
    m = MATERIALS[mat]
    entry = {'name': mat, 'doubleSided': True,
             'pbrMetallicRoughness': {'baseColorFactor': list(m['color']),
                                      'metallicFactor': 0.0,
                                      'roughnessFactor': m['rough']}}
    if m.get('blend'):
        entry['alphaMode'] = 'BLEND'
    materials.append(entry)

gltf = {
    'asset': {'version': '2.0', 'generator': 'schorisse-build gen_model.py'},
    'scene': 0,
    'scenes': [{'nodes': [0]}],
    # center the barn on the origin so viewers orbit its middle
    'nodes': [{'mesh': 0, 'translation': [-L/2, 0, -W/2]}],
    'meshes': [{'primitives': primitives}],
    'materials': materials,
    'accessors': accessors,
    'bufferViews': views,
    'buffers': [{'byteLength': len(bin_parts)}],
}
js = json.dumps(gltf, separators=(',', ':')).encode()
js += b' ' * ((4 - len(js) % 4) % 4)
glb = (b'glTF' + struct.pack('<II', 2, 12 + 8 + len(js) + 8 + len(bin_parts))
       + struct.pack('<I', len(js)) + b'JSON' + js
       + struct.pack('<I', len(bin_parts)) + b'BIN\0' + bin_parts)
open('/Users/denis/Github/schorisse-build/models/barn.glb', 'wb').write(glb)
print('GLB:', len(glb), 'bytes,', len(TRIS), 'triangles,', len(order), 'materials')
