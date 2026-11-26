"""
Imports Khronos ready-made 3D human model (web_cesium_man.glb) into Blender 5.3,
poses it cleanly in a zombie walking stance using its real armature, bakes it into ONE single
unified realistic mesh (with UVs + texture), renders a preview, and exports cesium_zombie_asset.json!
"""
import bpy
import bmesh
import base64
import json
import math
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
GLB_PATH = os.path.join(ROOT, "web_soldier.glb")


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def main():
    clear_scene()
    bpy.ops.import_scene.gltf(filepath=GLB_PATH)

    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    arms = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE']
    print("Meshes:", [(m.name, len(m.data.vertices)) for m in meshes])
    print("Armatures:", [a.name for a in arms])
    assert meshes, "No mesh in CesiumMan.glb!"

    # Advance to frame 1 (natural standing/ready human stance)
    bpy.context.scene.frame_set(1)
    bpy.context.view_layer.update()

    # Evaluate deformed mesh in world space (join all body submeshes into ONE single clean human mesh — ZERO double bodies!)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    bm = bmesh.new()
    for src_obj in meshes:
        if len(src_obj.data.vertices) < 100:
            continue
        eval_obj = src_obj.evaluated_get(depsgraph)
        eval_mesh = eval_obj.to_mesh()
        bm_part = bmesh.new()
        bm_part.from_mesh(eval_mesh)
        bm_part.transform(src_obj.matrix_world)
        tmp_m = bpy.data.meshes.new("tmp")
        bm_part.to_mesh(tmp_m)
        bm_part.free()
        bm.from_mesh(tmp_m)
        bpy.data.meshes.remove(tmp_m)
        eval_obj.to_mesh_clear()

    bmesh.ops.triangulate(bm, faces=bm.faces)
    # Decimate lightly if very dense so Quest 3 stays 90fps and HTML stays compact
    if len(bm.verts) > 5000:
        tmp_dec = bpy.data.meshes.new("tmp_dec")
        bm.to_mesh(tmp_dec)
        bm.free()
        dec_obj = bpy.data.objects.new("tmp_dec", tmp_dec)
        bpy.context.collection.objects.link(dec_obj)
        mod = dec_obj.modifiers.new("Decimate", 'DECIMATE')
        mod.ratio = 3500.0 / len(tmp_dec.vertices)
        bpy.context.view_layer.objects.active = dec_obj
        bpy.ops.object.modifier_apply(modifier="Decimate")
        bm = bmesh.new()
        bm.from_mesh(dec_obj.data)
        bpy.data.objects.remove(dec_obj, do_unlink=True)
        bpy.data.meshes.remove(tmp_dec)

    # Normalize to 1.80m tall, centered X/Y, feet at Z=0, facing -Y in Blender (+Z in Three.js)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)
    print(f"Raw evaluated bbox: X[{min_x:.3f},{max_x:.3f}] Y[{min_y:.3f},{max_y:.3f}] Z[{min_z:.3f},{max_z:.3f}]")

    h = max_z - min_z
    sc = 1.80 / h
    cx = (min_x + max_x) * 0.5
    cy = (min_y + max_y) * 0.5

    # Detect facing direction from feet/head (CesiumMan walks along +X or -Y; check X vs Y span of legs!)
    foot_xs = [v.co.x - cx for v in bm.verts if (v.co.z - min_z) / h < 0.08]
    foot_ys = [v.co.y - cy for v in bm.verts if (v.co.z - min_z) / h < 0.08]
    span_x = (max(foot_xs) - min(foot_xs)) if foot_xs else 0
    span_y = (max(foot_ys) - min(foot_ys)) if foot_ys else 0
    # Check torso shoulder width axis vs stride axis
    sh_xs = [v.co.x - cx for v in bm.verts if 0.72 < (v.co.z - min_z) / h < 0.85]
    sh_ys = [v.co.y - cy for v in bm.verts if 0.72 < (v.co.z - min_z) / h < 0.85]
    sh_span_x = max(sh_xs) - min(sh_xs)
    sh_span_y = max(sh_ys) - min(sh_ys)
    print(f"Shoulder span X={sh_span_x:.3f}, Y={sh_span_y:.3f}")
    # We want shoulders along X (so sh_span_x > sh_span_y) and facing -Y (becomes +Z in Three.js)
    rot90 = sh_span_y > sh_span_x

    for v in bm.verts:
        x = (v.co.x - cx) * sc
        y = (v.co.y - cy) * sc
        z = (v.co.z - min_z) * sc
        if rot90:
            x, y = -y, x
        v.co = Vector((x, y, z))

    # Soldier faces +Y in Blender initially — flip 180 deg around Z so he faces -Y in Blender (+Z in Three.js!)
    for v in bm.verts:
        v.co.x = -v.co.x
        v.co.y = -v.co.y

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.normal_update()

    # Export vertex positions, normals, UVs (per-loop unindexed or indexed cleanly)
    uv_layer = bm.loops.layers.uv.active
    positions = []
    normals = []
    uvs = []
    indices = []

    # Build deduplicated (vert_idx, uv_rounded) index table so UVs stay 100% crisp with no seams!
    vert_map = {}
    for f in bm.faces:
        if len(f.verts) != 3:
            continue
        tri = []
        for loop in f.loops:
            v = loop.vert
            uv = loop[uv_layer].uv if uv_layer else Vector((0, 0))
            key = (v.index, round(uv.x, 4), round(uv.y, 4))
            if key not in vert_map:
                idx = len(vert_map)
                vert_map[key] = idx
                # Blender (x, y, z) -> Three.js (x, z, -y)
                positions.extend([round(v.co.x, 4), round(v.co.z, 4), round(-v.co.y, 4)])
                normals.extend([round(v.normal.x, 4), round(v.normal.z, 4), round(-v.normal.y, 4)])
                uvs.extend([round(uv.x, 4), round(uv.y, 4)])
            tri.append(vert_map[key])
        indices.extend(tri)

    print(f"Exported single unified CesiumMan: {len(positions) // 3} verts, {len(indices) // 3} tris")

    # Extract the actual Base Color (albedo) texture from Principled BSDF (not normal map!)
    tex_data_uri = ""
    base_img = None
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            continue
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf and bsdf.inputs["Base Color"].is_linked:
            node = bsdf.inputs["Base Color"].links[0].from_node
            if node.type == 'TEX_IMAGE' and node.image:
                base_img = node.image
                break
    if base_img and base_img.size[0] > 0:
        tmp_jpg = os.path.join(ROOT, "cesium_man_tex.jpg")
        base_img.filepath_raw = tmp_jpg
        base_img.file_format = 'JPEG'
        base_img.save()
        with open(tmp_jpg, "rb") as tf:
            b64 = base64.b64encode(tf.read()).decode("ascii")
        tex_data_uri = "data:image/jpeg;base64," + b64
        print(f"Extracted Base Color texture {base_img.name} ({base_img.size[0]}x{base_img.size[1]}): {len(b64)} b64 chars")

    out_path = os.path.join(ROOT, "cesium_zombie_asset.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"p": positions, "n": normals, "uv": uvs, "i": indices, "tex": tex_data_uri}, f, separators=(",", ":"))
    print("Saved:", out_path, f"({os.path.getsize(out_path):,} bytes)")

    # Render Blender verification preview of the exact normalized mesh
    clear_scene()
    m = bpy.data.meshes.new("CesiumManClean")
    bm.to_mesh(m)
    bm.free()
    obj = bpy.data.objects.new("CesiumManClean", m)
    bpy.context.collection.objects.link(obj)
    for p in obj.data.polygons:
        p.use_smooth = True

    mat = bpy.data.materials.new("CesiumMat")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    tex_path = os.path.join(ROOT, "cesium_man_tex.jpg")
    if os.path.exists(tex_path) and bsdf:
        img_node = nt.nodes.new("ShaderNodeTexImage")
        img_node.image = bpy.data.images.load(tex_path)
        nt.links.new(img_node.outputs["Color"], bsdf.inputs["Base Color"])
    obj.data.materials.append(mat)

    for name, loc, energy in [("Key", (-2.0, -3.0, 2.5), 260), ("Fill", (2.2, -2.0, 1.5), 140)]:
        ld = bpy.data.lights.new(name, type='AREA'); ld.energy = energy; ld.size = 2.0
        lo = bpy.data.objects.new(name, ld); lo.location = loc
        lo.rotation_euler = (Vector((0, 0, 0.95)) - lo.location).to_track_quat('-Z', 'Y').to_euler()
        bpy.context.collection.objects.link(lo)

    cd = bpy.data.cameras.new("Cam"); cd.lens = 45
    co = bpy.data.objects.new("Cam", cd); co.location = (0.4, -2.6, 1.15)
    co.rotation_euler = (Vector((0, 0, 0.95)) - co.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.collection.objects.link(co)
    bpy.context.scene.camera = co

    scn = bpy.context.scene
    scn.render.engine = 'BLENDER_EEVEE'
    scn.render.resolution_x = 768
    scn.render.resolution_y = 768
    scn.render.filepath = os.path.join(ROOT, "Blender-Cesium-Zombie-Preview.png")
    bpy.ops.render.render(write_still=True)
    print("Rendered:", scn.render.filepath)


if __name__ == "__main__":
    main()
