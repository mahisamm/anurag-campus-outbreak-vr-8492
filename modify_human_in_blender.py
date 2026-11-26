"""
Imports the downloaded CC0 realistic human base mesh (web_male_base_male_base_mesh.glb) into Blender 5.3,
normalizes its height (1.78m) & orientation, modifies/segments it into realistic articulated anatomical
parts (head, torso with faculty collar, left/right arms with hands, left/right legs with feet) pivoted
at their natural joints, exports human_zombie_meshes.json for Three.js, saves .blend, and renders a preview!
"""
import bpy
import bmesh
import json
import math
import os
from mathutils import Vector, Matrix, Euler

ROOT = os.path.dirname(os.path.abspath(__file__))
GLB_PATH = os.path.join(ROOT, "web_male_base_male_base_mesh.glb")


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_mat(name, color, metallic=0.0, roughness=0.6):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return mat


def extract_submesh_by_faces(src_mesh, face_pred, pivot_blender, rot_euler=(0, 0, 0), zombie_sculpt=False):
    """Copy matching faces from src_mesh, shift by -pivot_blender, apply optional rot & undead sculpt."""
    bm_src = bmesh.new()
    bm_src.from_mesh(src_mesh)
    bm_src.faces.ensure_lookup_table()

    bm = bmesh.new()
    vmap = {}
    rot_m = Euler(rot_euler, 'XYZ').to_matrix().to_4x4() if any(rot_euler) else Matrix.Identity(4)

    for f in bm_src.faces:
        c = f.calc_center_median()
        if not face_pred(c):
            continue
        new_verts = []
        for v in f.verts:
            if v.index not in vmap:
                co = v.co - pivot_blender
                if zombie_sculpt:
                    # Subtle gaunt undead cheek/brow sharpening while keeping realistic human anatomy
                    if co.z > 0.04 and co.z < 0.16 and abs(co.x) > 0.035 and co.y < 0.0:
                        co.x *= 0.94
                co = (rot_m @ co.to_4d()).xyz
                vmap[v.index] = bm.verts.new(co)
            new_verts.append(vmap[v.index])
        try:
            bm.faces.new(new_verts)
        except ValueError:
            pass

    bm_src.free()
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.normal_update()

    # Export in Three.js coords: Blender (x, y, z) -> Three.js (x, z, -y)
    # Wait: verify front direction! If human faces -Y in Blender, then -y becomes +Z in Three.js!
    positions = []
    normals = []
    indices = []
    bm.verts.ensure_lookup_table()
    for i, v in enumerate(bm.verts):
        v.index = i
        positions.extend([round(v.co.x, 4), round(v.co.z, 4), round(-v.co.y, 4)])
        normals.extend([round(v.normal.x, 4), round(v.normal.z, 4), round(-v.normal.y, 4)])
    for f in bm.faces:
        if len(f.verts) == 3:
            indices.extend([f.verts[0].index, f.verts[1].index, f.verts[2].index])

    return bm, {"p": positions, "n": normals, "i": indices}


def main():
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=GLB_PATH)

    mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and len(o.data.vertices) > 100]
    print("Imported human mesh objects:", [(o.name, len(o.data.vertices)) for o in mesh_objs])
    assert mesh_objs, "No mesh found in GLB!"

    # Remove any small helper meshes (like Icosphere)
    for o in list(bpy.context.scene.objects):
        if o.type == 'MESH' and o not in mesh_objs:
            bpy.data.objects.remove(o, do_unlink=True)

    human = mesh_objs[0]
    bpy.ops.object.select_all(action='DESELECT')
    human.select_set(True)
    bpy.context.view_layer.objects.active = human
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Apply 1 level of Catmull-Clark Subdivision Surface for ultra-smooth realistic human anatomy
    sub = human.modifiers.new("Subsurf", 'SUBSURF')
    sub.levels = 1
    sub.render_levels = 1
    bpy.ops.object.modifier_apply(modifier="Subsurf")
    print("Subdivided realistic human mesh -> verts:", len(human.data.vertices))

    # Check bounding box and normalize to 1.78m tall, centered X/Y, feet at Z=0
    verts = [v.co for v in human.data.vertices]
    min_x = min(v.x for v in verts); max_x = max(v.x for v in verts)
    min_y = min(v.y for v in verts); max_y = max(v.y for v in verts)
    min_z = min(v.z for v in verts); max_z = max(v.z for v in verts)
    print(f"Raw bbox: X[{min_x:.3f},{max_x:.3f}] Y[{min_y:.3f},{max_y:.3f}] Z[{min_z:.3f},{max_z:.3f}]")

    height = max_z - min_z
    scale = 1.78 / height
    cx = (min_x + max_x) * 0.5
    cy = (min_y + max_y) * 0.5

    # Detect which way the human faces (feet toes stick out further in forward direction!)
    foot_ys = [v.y - cy for v in verts if (v.z - min_z) / height < 0.06]
    avg_foot_y = sum(foot_ys) / max(1, len(foot_ys))
    print(f"Avg foot Y relative to center: {avg_foot_y:.4f} (negative = faces -Y, positive = faces +Y)")
    flip_y = avg_foot_y > 0  # We want human facing -Y in Blender so it faces +Z in Three.js!

    for v in human.data.vertices:
        x = (v.co.x - cx) * scale
        y = (v.co.y - cy) * scale
        z = (v.co.z - min_z) * scale
        if flip_y:
            x = -x
            y = -y
        v.co = Vector((x, y, z))
    human.data.update()

    # Check normalized dimensions
    verts = [v.co for v in human.data.vertices]
    print(
        f"Normalized bbox: X[{min(v.x for v in verts):.3f},{max(v.x for v in verts):.3f}] "
        f"Y[{min(v.y for v in verts):.3f},{max(v.y for v in verts):.3f}] "
        f"Z[{min(v.z for v in verts):.3f},{max(v.z for v in verts):.3f}]"
    )

    # Check if arms are in T-pose or A-pose by measuring arm height at |x| > 0.25
    arm_zs = [v.z for v in verts if abs(v.x) > 0.26]
    arm_avg_z = sum(arm_zs) / max(1, len(arm_zs)) if arm_zs else 1.25
    arm_max_x = max(abs(v.x) for v in verts)
    print(f"Arms span max |X|={arm_max_x:.3f}, avg Z at |X|>0.26 = {arm_avg_z:.3f}")

    # Skip decimate so we keep crisp subdivided human anatomy (~4800 verts split across 6 parts)

    # Define anatomical joint pivots (Blender Z-up, facing -Y)
    neck_pivot = Vector((0.0, 0.0, 1.48))
    torso_pivot = Vector((0.0, 0.0, 0.86))
    sh_l_pivot = Vector((-0.19, 0.0, 1.42))
    sh_r_pivot = Vector((0.19, 0.0, 1.42))
    hip_l_pivot = Vector((-0.095, 0.0, 0.86))
    hip_r_pivot = Vector((0.095, 0.0, 0.86))

    # Keep arms in clean rest pose (zero jagged shoulder seams) and animate forward reach smoothly at the shoulder pivot in Three.js!
    # Clean non-overlapping anatomical face bounds:
    #   - Head + Neck: Z >= 1.48 and |X| < 0.15
    #   - Torso (chest + shoulders + waist + upper hips): 0.86 <= Z < 1.50 and |X| <= 0.205
    #   - Left Arm + Hand: X < -0.195 and Z >= 0.62
    #   - Right Arm + Hand: X > 0.195 and Z >= 0.62
    #   - Left Leg + Foot: Z < 0.88 and -0.22 < X <= 0.004
    #   - Right Leg + Foot: Z < 0.88 and -0.004 <= X < 0.22
    parts_spec = {
        "human_head": (lambda c: c.z >= 1.48 and abs(c.x) < 0.15, neck_pivot, (0, 0, 0), True),
        "human_torso": (lambda c: 0.86 <= c.z < 1.50 and abs(c.x) <= 0.205, torso_pivot, (0, 0, 0), False),
        "human_arm_l": (lambda c: c.x < -0.195 and c.z >= 0.62, sh_l_pivot, (0, 0, 0), False),
        "human_arm_r": (lambda c: c.x > 0.195 and c.z >= 0.62, sh_r_pivot, (0, 0, 0), False),
        "human_leg_l": (lambda c: c.z < 0.88 and -0.22 < c.x <= 0.004, hip_l_pivot, (0, 0, 0), False),
        "human_leg_r": (lambda c: c.z < 0.88 and -0.004 <= c.x < 0.22, hip_r_pivot, (0, 0, 0), False),
    }

    exported = {}
    preview_objs = {}
    mat_skin = make_mat("ZombieSkin", (0.32, 0.48, 0.25), roughness=0.62)
    mat_coat = make_mat("LabCoat", (0.85, 0.89, 0.92), roughness=0.78)
    mat_pants = make_mat("Trousers", (0.16, 0.20, 0.25), roughness=0.84)

    for key, (pred, pivot, rot, sculpt) in parts_spec.items():
        bm, data = extract_submesh_by_faces(human.data, pred, pivot, rot, zombie_sculpt=sculpt)
        exported[key] = data
        print(f"Exported {key}: {len(data['p']) // 3} verts, {len(data['i']) // 3} tris")

        # Create Blender preview object positioned at its joint pivot
        m = bpy.data.meshes.new(key)
        bm.to_mesh(m)
        bm.free()
        o = bpy.data.objects.new(key, m)
        bpy.context.collection.objects.link(o)
        o.location = pivot
        for p in o.data.polygons:
            p.use_smooth = True
        if "head" in key or "arm" in key:
            o.data.materials.append(mat_skin)
        elif "torso" in key:
            o.data.materials.append(mat_coat)
        else:
            o.data.materials.append(mat_pants)
        preview_objs[key] = o

    # Remove original unsegmented mesh from showcase scene
    bpy.data.objects.remove(human, do_unlink=True)

    # Save exported JSON
    out_json = os.path.join(ROOT, "human_zombie_meshes.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(exported, f, separators=(",", ":"))
    print("Saved:", out_json, f"({os.path.getsize(out_json):,} bytes)")

    # Setup studio lights & camera to render Blender-Realistic-Human-Preview.png
    for name, loc, energy, col in [
        ("Key", (-2.2, -3.2, 2.6), 280, (1.0, 0.96, 0.90)),
        ("Fill", (2.5, -2.0, 1.6), 120, (0.7, 0.85, 1.0)),
        ("Rim", (0.0, 2.6, 2.2), 180, (0.4, 0.95, 0.75)),
    ]:
        ld = bpy.data.lights.new(name, type='AREA')
        ld.energy = energy; ld.size = 1.8; ld.color = col
        lo = bpy.data.objects.new(name, ld)
        lo.location = loc
        lo.rotation_euler = (Vector((0, 0, 1.0)) - lo.location).to_track_quat('-Z', 'Y').to_euler()
        bpy.context.collection.objects.link(lo)

    cam_d = bpy.data.cameras.new("Cam")
    cam_d.lens = 45
    cam_o = bpy.data.objects.new("Cam", cam_d)
    cam_o.location = (0.75, -2.65, 1.15)
    cam_o.rotation_euler = (Vector((0.0, -0.05, 0.96)) - cam_o.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.collection.objects.link(cam_o)
    bpy.context.scene.camera = cam_o

    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.05, 0.08, 0.12, 1.0)
        bg.inputs["Strength"].default_value = 0.65
    bpy.context.scene.world = world

    blend_path = os.path.join(ROOT, "Anurag-Realistic-Human-Zombie.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)

    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 960
    scene.render.resolution_y = 960
    scene.render.image_settings.file_format = 'PNG'
    render_path = os.path.join(ROOT, "Blender-Realistic-Human-Preview.png")
    scene.render.filepath = render_path
    bpy.ops.render.render(write_still=True)
    print("Rendered:", render_path)


if __name__ == "__main__":
    main()
