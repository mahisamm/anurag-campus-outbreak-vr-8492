"""
Build realistic 3D game assets in Blender 5.3 for Anurag University: Campus Outbreak (FP & Meta Quest 3 VR).
Generates:
  - Anurag-Zombie-Assets.blend
  - zombie_assets.json (compact Three.js BufferGeometry export: p, n, i)
  - Blender-Assets-Showcase.png (studio render for visual verification)
"""
import bpy
import bmesh
import math
import json
import os
from mathutils import Vector, Matrix, Euler

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_mat(name, color, metallic=0.0, roughness=0.5, emission=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if emission is not None and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def add_box(bm, size, center=(0, 0, 0), rot=(0, 0, 0), bevel=0.0):
    ret = bmesh.ops.create_cube(bm, size=1.0)
    verts = ret["verts"]
    mat_s = Matrix.Diagonal((size[0], size[1], size[2], 1.0))
    mat_r = Euler(rot, 'XYZ').to_matrix().to_4x4()
    mat_t = Matrix.Translation(Vector(center))
    bmesh.ops.transform(bm, matrix=mat_t @ mat_r @ mat_s, verts=verts)
    if bevel > 0:
        edges = list({e for v in verts for e in v.link_edges})
        bmesh.ops.bevel(bm, geom=edges, offset=bevel, segments=2, affect='EDGES', clamp_overlap=True)
    return verts


def add_cyl(bm, r1, r2, depth, segs=16, center=(0, 0, 0), rot=(0, 0, 0)):
    ret = bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False, segments=segs,
        radius1=r1, radius2=r2, depth=depth
    )
    verts = ret["verts"]
    mat_r = Euler(rot, 'XYZ').to_matrix().to_4x4()
    mat_t = Matrix.Translation(Vector(center))
    bmesh.ops.transform(bm, matrix=mat_t @ mat_r, verts=verts)
    return verts


def finalize_obj(name, bm, mat, subdiv=0, smooth=True):
    mesh = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    if subdiv > 0:
        mod = obj.modifiers.new("Subsurf", 'SUBSURF')
        mod.levels = subdiv
        mod.render_levels = subdiv
    if smooth:
        for p in obj.data.polygons:
            p.use_smooth = True
    return obj


# ---------------------------------------------------------------------------
# 1. REALISTIC SCULPTED ZOMBIE HEAD (Three.js: +Y up, +Z forward -> Blender: +Z up, -Y forward)
#    Wait: we will export directly with (x, y, z)_blender -> (x, z, -y)_three
#    So in Blender:
#      +X = right
#      +Z = up
#      +Y = forward (which becomes -Z in Three.js, i.e., weapon barrel points +Y in Blender -> -Z in Three.js!)
#    For Zombie Head: in Three.js zombie faces +Z, so in Blender face points -Y (becomes +Z in Three.js)!
# ---------------------------------------------------------------------------
def build_zombie_head(mat):
    bm = bmesh.new()
    # High-res UV sphere for cranial sculpt
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=18, radius=0.118)
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z
        # Elongate skull vertically & slightly front-to-back
        x *= 0.88
        y *= 1.06
        z *= 1.18
        # Narrow jaw & chin (lower half, front is -Y)
        if z < 0.0:
            t = min(1.0, -z / 0.13)
            x *= (1.0 - 0.34 * t)
            if y < 0:
                y -= 0.022 * t * (1.0 - 0.5 * abs(x) / 0.08)
        # Sunken hollow cheeks (necrotic gaunt look)
        if -0.055 < z < 0.015 and abs(x) > 0.032 and y < 0.02:
            cheek = math.exp(-((abs(x) - 0.068) / 0.028) ** 2 - ((z + 0.02) / 0.028) ** 2)
            x *= (1.0 - 0.18 * cheek)
            y += 0.014 * cheek
        # Prominent brow ridge (front is -Y)
        if 0.022 < z < 0.058 and y < -0.05:
            brow = math.exp(-((z - 0.038) / 0.015) ** 2) * max(0.0, 1.0 - abs(x) / 0.085)
            y -= 0.020 * brow
        # Deep sunken eye sockets
        if -0.002 < z < 0.036 and y < -0.04:
            for ex in (-0.036, 0.036):
                d = math.hypot(x - ex, (z - 0.016) * 1.25)
                if d < 0.026:
                    socket = math.cos((d / 0.026) * math.pi * 0.5)
                    y += 0.030 * socket
        # Nasal bridge & decayed nose cavity
        if -0.028 < z < 0.022 and abs(x) < 0.018 and y < -0.06:
            nose = math.exp(-(x / 0.011) ** 2) * math.exp(-((z + 0.004) / 0.02) ** 2)
            y -= 0.016 * nose
        # Snarling open mouth / recessed jaw crease
        if -0.082 < z < -0.042 and abs(x) < 0.042 and y < -0.04:
            mouth = math.exp(-((z + 0.062) / 0.012) ** 2) * math.exp(-(x / 0.032) ** 2)
            y += 0.026 * mouth
        # Subtle organic bone/scar asymmetry
        rip = 0.0035 * math.sin(x * 65.0 + z * 45.0) * math.cos(y * 55.0)
        v.co = Vector((x + rip * 0.6, y + rip, z + rip * 0.5))

    # Add ears
    for side in (-1, 1):
        add_box(bm, (0.018, 0.028, 0.046), center=(side * 0.104, 0.005, 0.005), rot=(0.0, 0.0, side * 0.25), bevel=0.005)

    return finalize_obj("zombie_head", bm, mat, subdiv=1, smooth=True)


# ---------------------------------------------------------------------------
# 2. TACTICAL ENERGY RIOT SHIELD (Left Hand)
#    In Blender: faces +Y (forward away from player), tall along +Z, wide along X
# ---------------------------------------------------------------------------
def build_riot_shield(mat):
    bm = bmesh.new()
    # Curved shield body using grid strips
    cols = 10
    rows = 12
    w = 0.44
    h = 0.72
    thick = 0.024
    curve_r = 0.58

    def shield_pt(u, v, off):
        # u in [-1,1], v in [-1,1]
        # Taper slightly at bottom like a tactical ballistic shield
        taper = 1.0 - 0.16 * max(0.0, -v) - 0.08 * max(0.0, v) ** 2
        ang = u * (w * 0.5 * taper) / curve_r
        r = curve_r + off
        x = r * math.sin(ang)
        y = (r * math.cos(ang) - curve_r) + 0.05
        z = v * (h * 0.5)
        return Vector((x, y, z))

    front_grid = []
    back_grid = []
    for r_i in range(rows + 1):
        v = -1.0 + 2.0 * (r_i / rows)
        f_row, b_row = [], []
        for c_i in range(cols + 1):
            u = -1.0 + 2.0 * (c_i / cols)
            f_row.append(bm.verts.new(shield_pt(u, v, thick * 0.5)))
            b_row.append(bm.verts.new(shield_pt(u, v, -thick * 0.5)))
        front_grid.append(f_row)
        back_grid.append(b_row)

    for r_i in range(rows):
        for c_i in range(cols):
            # Front face
            bm.faces.new((front_grid[r_i][c_i], front_grid[r_i][c_i + 1],
                          front_grid[r_i + 1][c_i + 1], front_grid[r_i + 1][c_i]))
            # Back face
            bm.faces.new((back_grid[r_i][c_i], back_grid[r_i + 1][c_i],
                          back_grid[r_i + 1][c_i + 1], back_grid[r_i][c_i + 1]))

    # Stitch border edges
    for c_i in range(cols):
        bm.faces.new((front_grid[0][c_i], back_grid[0][c_i], back_grid[0][c_i + 1], front_grid[0][c_i + 1]))
        bm.faces.new((front_grid[rows][c_i], front_grid[rows][c_i + 1], back_grid[rows][c_i + 1], back_grid[rows][c_i]))
    for r_i in range(rows):
        bm.faces.new((front_grid[r_i][0], front_grid[r_i + 1][0], back_grid[r_i + 1][0], back_grid[r_i][0]))
        bm.faces.new((front_grid[r_i][cols], back_grid[r_i][cols], back_grid[r_i + 1][cols], front_grid[r_i + 1][cols]))

    # Raised ballistic visor frame (upper third)
    add_box(bm, (0.28, 0.025, 0.025), center=(0, 0.068, 0.24), bevel=0.004)
    add_box(bm, (0.28, 0.025, 0.025), center=(0, 0.068, 0.11), bevel=0.004)
    add_box(bm, (0.026, 0.025, 0.14), center=(-0.13, 0.062, 0.175), bevel=0.004)
    add_box(bm, (0.026, 0.025, 0.14), center=(0.13, 0.062, 0.175), bevel=0.004)
    # Central reinforced rib
    add_box(bm, (0.048, 0.022, 0.34), center=(0, 0.068, -0.10), bevel=0.005)
    # Rear ergonomic handle bar
    add_cyl(bm, 0.014, 0.014, 0.16, segs=12, center=(0, -0.015, 0.0), rot=(0, 0, 0))
    add_box(bm, (0.024, 0.055, 0.024), center=(0, 0.015, 0.075), bevel=0.003)
    add_box(bm, (0.024, 0.055, 0.024), center=(0, 0.015, -0.075), bevel=0.003)

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return finalize_obj("riot_shield", bm, mat, subdiv=0, smooth=True)


# ---------------------------------------------------------------------------
# 3. LIGHTSABER HILT (Blade extends along +Z in Blender -> +Y in Three.js)
# ---------------------------------------------------------------------------
def build_lightsaber_hilt(mat):
    bm = bmesh.new()
    # Main cylindrical grip
    add_cyl(bm, 0.017, 0.017, 0.22, segs=18, center=(0, 0, 0.0))
    # Fluted grip ribs around lower grip
    for i in range(6):
        ang = i * (math.pi * 2 / 6)
        add_box(bm, (0.005, 0.006, 0.095), center=(math.cos(ang) * 0.0185, math.sin(ang) * 0.0185, -0.045), rot=(0, 0, ang), bevel=0.001)
    # Pommel cap with ring
    add_cyl(bm, 0.021, 0.018, 0.026, segs=18, center=(0, 0, -0.118))
    # Activation switch box
    add_box(bm, (0.014, 0.024, 0.042), center=(0, 0.016, 0.025), bevel=0.002)
    # Choke neck
    add_cyl(bm, 0.013, 0.015, 0.032, segs=18, center=(0, 0, 0.115))
    # Flared emitter shroud
    add_cyl(bm, 0.018, 0.025, 0.038, segs=20, center=(0, 0, 0.145))
    # Emitter fins
    for i in range(4):
        ang = i * (math.pi * 0.5)
        add_box(bm, (0.004, 0.012, 0.044), center=(math.cos(ang) * 0.022, math.sin(ang) * 0.022, 0.148), rot=(0, 0, ang), bevel=0.001)

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return finalize_obj("lightsaber_hilt", bm, mat, subdiv=0, smooth=True)


# ---------------------------------------------------------------------------
# 4. TACTICAL 9MM PISTOL (Barrel points +Y in Blender -> -Z in Three.js)
# ---------------------------------------------------------------------------
def build_pistol(mat):
    bm = bmesh.new()
    # Ergonomic angled grip (centered near palm origin)
    add_box(bm, (0.030, 0.046, 0.115), center=(0, -0.012, -0.040), rot=(-0.22, 0, 0), bevel=0.004)
    # Magazine baseplate
    add_box(bm, (0.032, 0.052, 0.014), center=(0, -0.026, -0.098), rot=(-0.22, 0, 0), bevel=0.002)
    # Lower frame & rail
    add_box(bm, (0.029, 0.175, 0.024), center=(0, 0.058, 0.024), bevel=0.003)
    # Upper slide
    add_box(bm, (0.031, 0.190, 0.034), center=(0, 0.056, 0.052), bevel=0.004)
    # Barrel protruding slightly
    add_cyl(bm, 0.0085, 0.0085, 0.045, segs=14, center=(0, 0.155, 0.054), rot=(math.pi * 0.5, 0, 0))
    # Trigger guard
    add_box(bm, (0.014, 0.052, 0.006), center=(0, 0.036, -0.016), bevel=0.001)
    add_box(bm, (0.014, 0.006, 0.034), center=(0, 0.060, 0.001), bevel=0.001)
    # Trigger
    add_box(bm, (0.006, 0.008, 0.022), center=(0, 0.030, 0.002), rot=(0.35, 0, 0))
    # Front & rear iron sights
    add_box(bm, (0.006, 0.010, 0.009), center=(0, 0.142, 0.072), bevel=0.001)
    add_box(bm, (0.020, 0.010, 0.009), center=(0, -0.028, 0.072), bevel=0.001)

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return finalize_obj("pistol", bm, mat, subdiv=0, smooth=True)


# ---------------------------------------------------------------------------
# 5. PULSE ASSAULT RIFLE (Barrel points +Y in Blender -> -Z in Three.js)
# ---------------------------------------------------------------------------
def build_assault_rifle(mat):
    bm = bmesh.new()
    # Grip
    add_box(bm, (0.032, 0.046, 0.115), center=(0, -0.015, -0.045), rot=(-0.25, 0, 0), bevel=0.004)
    # Main receiver
    add_box(bm, (0.044, 0.250, 0.066), center=(0, 0.060, 0.036), bevel=0.005)
    # Ventilated tactical handguard
    add_box(bm, (0.042, 0.230, 0.052), center=(0, 0.295, 0.040), bevel=0.006)
    # Barrel + muzzle brake
    add_cyl(bm, 0.011, 0.011, 0.14, segs=14, center=(0, 0.455, 0.042), rot=(math.pi * 0.5, 0, 0))
    add_cyl(bm, 0.015, 0.014, 0.038, segs=12, center=(0, 0.525, 0.042), rot=(math.pi * 0.5, 0, 0))
    # Curved magazine
    add_box(bm, (0.026, 0.056, 0.155), center=(0, 0.120, -0.062), rot=(0.18, 0, 0), bevel=0.004)
    # Tactical stock
    add_box(bm, (0.032, 0.195, 0.042), center=(0, -0.155, 0.034), bevel=0.004)
    add_box(bm, (0.036, 0.030, 0.115), center=(0, -0.245, 0.005), bevel=0.005)
    # Top Picatinny rail + holographic optic sight
    add_box(bm, (0.024, 0.34, 0.012), center=(0, 0.145, 0.074), bevel=0.002)
    add_box(bm, (0.034, 0.068, 0.040), center=(0, 0.065, 0.098), bevel=0.004)

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return finalize_obj("assault_rifle", bm, mat, subdiv=0, smooth=True)


# ---------------------------------------------------------------------------
# 6. COMBAT SHOTGUN (Barrel points +Y in Blender -> -Z in Three.js)
# ---------------------------------------------------------------------------
def build_shotgun(mat):
    bm = bmesh.new()
    # Angled stock/grip
    add_box(bm, (0.038, 0.24, 0.054), center=(0, -0.13, -0.008), rot=(-0.18, 0, 0), bevel=0.006)
    add_box(bm, (0.040, 0.032, 0.115), center=(0, -0.245, -0.032), bevel=0.006)
    # Heavy receiver
    add_box(bm, (0.046, 0.20, 0.062), center=(0, 0.06, 0.034), bevel=0.005)
    # Top long barrel
    add_cyl(bm, 0.014, 0.014, 0.44, segs=16, center=(0, 0.36, 0.050), rot=(math.pi * 0.5, 0, 0))
    # Under-barrel shell tube
    add_cyl(bm, 0.012, 0.012, 0.38, segs=14, center=(0, 0.33, 0.022), rot=(math.pi * 0.5, 0, 0))
    # Ribbed pump forend
    add_cyl(bm, 0.022, 0.022, 0.16, segs=14, center=(0, 0.29, 0.022), rot=(math.pi * 0.5, 0, 0))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return finalize_obj("shotgun", bm, mat, subdiv=0, smooth=True)


# ---------------------------------------------------------------------------
# 7. IRON CONSTRUCTION ROD (Campus ground pickup melee weapon; extends along +Z)
# ---------------------------------------------------------------------------
def build_iron_rod(mat):
    bm = bmesh.new()
    # Main ribbed rebar shaft (0.95m long)
    segs = 12
    steps = 16
    prev_ring = None
    for i in range(steps + 1):
        t = i / steps
        z = -0.15 + t * 0.96
        # Slight realistic bend near the striking end
        bend_y = 0.0 if t < 0.72 else ((t - 0.72) / 0.28) ** 2 * 0.085
        r = 0.0135 + (0.0022 if i % 2 == 0 else 0.0)
        ring = []
        for s in range(segs):
            a = s * (math.pi * 2 / segs)
            ring.append(bm.verts.new((math.cos(a) * r, bend_y + math.sin(a) * r, z)))
        if prev_ring:
            for s in range(segs):
                sn = (s + 1) % segs
                bm.faces.new((prev_ring[s], prev_ring[sn], ring[sn], ring[s]))
        prev_ring = ring
    # Wrapped tape grip at handle
    add_cyl(bm, 0.017, 0.016, 0.19, segs=14, center=(0, 0, -0.02))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return finalize_obj("iron_rod", bm, mat, subdiv=0, smooth=True)


# ---------------------------------------------------------------------------
# 8. FALLEN TREE BRANCH (Campus ground pickup melee weapon; extends along +Z)
# ---------------------------------------------------------------------------
def build_fallen_branch(mat):
    bm = bmesh.new()
    segs = 10
    steps = 14
    prev_ring = None
    for i in range(steps + 1):
        t = i / steps
        z = -0.14 + t * 0.92
        cx = 0.026 * math.sin(t * 4.2)
        cy = 0.022 * math.cos(t * 3.1) - 0.022
        r = 0.020 * (1.0 - 0.35 * t) + 0.005 * math.sin(t * 11.0)
        ring = []
        for s in range(segs):
            a = s * (math.pi * 2 / segs)
            bark = r * (1.0 + 0.14 * math.sin(a * 3.0 + t * 9.0))
            ring.append(bm.verts.new((cx + math.cos(a) * bark, cy + math.sin(a) * bark, z)))
        if prev_ring:
            for s in range(segs):
                sn = (s + 1) % segs
                bm.faces.new((prev_ring[s], prev_ring[sn], ring[sn], ring[s]))
        prev_ring = ring
    # Two forked natural wooden stubs/twigs near the striking end
    add_cyl(bm, 0.012, 0.005, 0.22, segs=8, center=(0.055, 0.02, 0.56), rot=(0.25, 0.58, 0.2))
    add_cyl(bm, 0.010, 0.004, 0.16, segs=8, center=(-0.042, -0.025, 0.38), rot=(-0.3, -0.52, -0.1))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return finalize_obj("fallen_branch", bm, mat, subdiv=0, smooth=True)


def export_obj_to_three_json(obj):
    """Evaluate modifiers, triangulate, and export (x, z, -y) for Three.js."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    mesh = eval_obj.to_mesh()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()

    positions = []
    normals = []
    indices = []

    for v in mesh.vertices:
        # Blender (x, y, z) -> Three.js (x, z, -y)
        positions.extend([round(v.co.x, 4), round(v.co.z, 4), round(-v.co.y, 4)])
        normals.extend([round(v.normal.x, 4), round(v.normal.z, 4), round(-v.normal.y, 4)])

    for p in mesh.polygons:
        if len(p.vertices) == 3:
            indices.extend([p.vertices[0], p.vertices[1], p.vertices[2]])

    eval_obj.to_mesh_clear()
    return {"p": positions, "n": normals, "i": indices}


def main():
    clear_scene()

    mat_zombie = make_mat("ZombieSkin", (0.28, 0.44, 0.22), metallic=0.02, roughness=0.65)
    mat_shield = make_mat("TacticalShield", (0.10, 0.14, 0.19), metallic=0.72, roughness=0.28)
    mat_hilt = make_mat("SaberHilt", (0.68, 0.72, 0.78), metallic=0.88, roughness=0.22)
    mat_gun = make_mat("GunMetal", (0.14, 0.16, 0.19), metallic=0.78, roughness=0.32)
    mat_rod = make_mat("RebarIron", (0.34, 0.27, 0.24), metallic=0.68, roughness=0.58)
    mat_wood = make_mat("BranchWood", (0.28, 0.19, 0.11), metallic=0.0, roughness=0.88)

    assets = {
        "zombie_head": build_zombie_head(mat_zombie),
        "riot_shield": build_riot_shield(mat_shield),
        "lightsaber_hilt": build_lightsaber_hilt(mat_hilt),
        "pistol": build_pistol(mat_gun),
        "assault_rifle": build_assault_rifle(mat_gun),
        "shotgun": build_shotgun(mat_gun),
        "iron_rod": build_iron_rod(mat_rod),
        "fallen_branch": build_fallen_branch(mat_wood),
    }

    # Export all assets at local origin BEFORE positioning them for the studio showcase render
    exported = {}
    for key, obj in assets.items():
        data = export_obj_to_three_json(obj)
        exported[key] = data
        print(f"Exported {key}: {len(data['p']) // 3} verts, {len(data['i']) // 3} tris")

    json_path = os.path.join(OUT_DIR, "zombie_assets.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(exported, f, separators=(",", ":"))
    print("Saved:", json_path, f"({os.path.getsize(json_path)} bytes)")

    # Arrange assets cleanly on a studio stage for visual verification render
    layout = {
        "zombie_head": ((-1.05, 0.0, 0.45), (0, 0, 0.2), 1.9),
        "riot_shield": ((-0.45, 0.0, 0.48), (0, 0, 2.75), 0.95),
        "lightsaber_hilt": ((0.05, 0.0, 0.32), (0.1, 0, 0), 1.35),
        "pistol": ((0.42, 0.0, 0.42), (0, 0, -1.35), 1.5),
        "assault_rifle": ((0.95, 0.0, 0.44), (0, 0, -1.45), 1.05),
        "shotgun": ((0.95, 0.0, 0.16), (0, 0, -1.45), 1.0),
        "iron_rod": ((-0.95, 0.0, 0.14), (0, 1.35, 0.1), 0.85),
        "fallen_branch": ((-0.05, 0.0, 0.10), (0, 1.48, -0.1), 0.85),
    }
    for key, (loc, rot, sc) in layout.items():
        o = assets[key]
        o.location = loc
        o.rotation_euler = rot
        o.scale = (sc, sc, sc)

    # Add glowing cyan saber blade in showcase only
    bm_b = bmesh.new()
    add_cyl(bm_b, 0.011, 0.008, 0.85, segs=14, center=(0, 0, 0.58))
    mat_blade = make_mat("SaberBlade", (0.15, 0.92, 1.0), emission=(0.15, 0.92, 1.0), emission_strength=6.0)
    blade = finalize_obj("showcase_blade", bm_b, mat_blade)
    blade.location = (0.05, 0.0, 0.32)
    blade.rotation_euler = (0.1, 0, 0)
    blade.scale = (1.35, 1.35, 1.35)

    # Studio floor
    bm_fl = bmesh.new()
    add_box(bm_fl, (8.0, 6.0, 0.05), center=(0, 0, -0.025))
    mat_floor = make_mat("StudioFloor", (0.08, 0.11, 0.15), roughness=0.45)
    finalize_obj("StudioFloor", bm_fl, mat_floor, smooth=False)

    # Lighting
    for name, loc, energy, color in [
        ("KeyLight", (-2.2, -3.2, 3.0), 260, (1.0, 0.96, 0.90)),
        ("FillLight", (2.8, -2.0, 1.8), 110, (0.65, 0.85, 1.0)),
        ("RimLight", (0.0, 2.8, 2.4), 180, (0.35, 0.95, 0.85)),
    ]:
        ldata = bpy.data.lights.new(name=name, type='AREA')
        ldata.energy = energy
        ldata.size = 2.0
        ldata.color = color
        lobj = bpy.data.objects.new(name, ldata)
        lobj.location = loc
        direction = Vector((0, 0, 0.35)) - lobj.location
        lobj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        bpy.context.collection.objects.link(lobj)

    # Camera
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = 42
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    cam_obj.location = (0.0, -3.15, 0.92)
    cam_obj.rotation_euler = (Vector((0.0, 0.0, 0.36)) - cam_obj.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # World background
    world = bpy.data.worlds.new("StudioWorld")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.04, 0.07, 0.10, 1.0)
        bg.inputs["Strength"].default_value = 0.6
    bpy.context.scene.world = world

    # Save .blend file
    blend_path = os.path.join(OUT_DIR, "Anurag-Zombie-Assets.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("Saved:", blend_path)

    # Render showcase PNG
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.image_settings.file_format = 'PNG'
    render_path = os.path.join(OUT_DIR, "Blender-Assets-Showcase.png")
    scene.render.filepath = render_path
    bpy.ops.render.render(write_still=True)
    print("Rendered:", render_path)


if __name__ == "__main__":
    main()
