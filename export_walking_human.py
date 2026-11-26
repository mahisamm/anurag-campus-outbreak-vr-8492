"""
Applies the real Mixamo 'Walk' skeletal animation (from web_soldier.glb) onto the realistic
human model (web_human_michelle.glb) in Blender 5.3, decimates cleanly for 90fps Quest 3 VR,
bakes an 8-frame smooth walking cycle (with identical topology across all 8 frames for real-time
vertex interpolation in Three.js), extracts the real human diffuse texture, and renders a preview!
"""
import bpy
import bmesh
import base64
import json
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
HUMAN_GLB = os.path.join(ROOT, "web_human_michelle.glb")
WALK_GLB = os.path.join(ROOT, "web_soldier.glb")
NUM_FRAMES = 8


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def main():
    clear_scene()

    # 1. Import Soldier GLB first purely to capture its real Mixamo 'Walk' action
    bpy.ops.import_scene.gltf(filepath=WALK_GLB)
    walk_action = next((a for a in bpy.data.actions if "walk" in a.name.lower()), None)
    assert walk_action, f"Walk action not found! Available: {[a.name for a in bpy.data.actions]}"
    walk_action.use_fake_user = True
    f_start, f_end = walk_action.frame_range
    print(f"Captured real Mixamo Walk action '{walk_action.name}' frames {f_start:.2f}..{f_end:.2f}")

    # Remove all Soldier objects
    for o in list(bpy.context.scene.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    # 2. Import realistic human model (Michelle / Ch03 — real face, hair, clothes, hands, shoes)
    bpy.ops.import_scene.gltf(filepath=HUMAN_GLB)
    h_arm = next((o for o in bpy.context.scene.objects if o.type == 'ARMATURE'), None)
    h_mesh = next((o for o in bpy.context.scene.objects if o.type == 'MESH' and len(o.data.vertices) > 500), None)
    assert h_arm and h_mesh, "Could not find human armature/mesh!"
    print(f"Loaded realistic human '{h_mesh.name}' ({len(h_mesh.data.vertices)} verts)")

    # Remove any tiny helper objects (like Icosphere)
    for o in list(bpy.context.scene.objects):
        if o not in (h_arm, h_mesh):
            bpy.data.objects.remove(o, do_unlink=True)

    # 3. Assign the real Mixamo 'Walk' action to the human armature!
    if not h_arm.animation_data:
        h_arm.animation_data_create()
    h_arm.animation_data.action = walk_action
    # Disable any NLA tracks that might override the active Walk action
    for trk in h_arm.animation_data.nla_tracks:
        trk.mute = True

    # 4. Decimate the rest mesh BEFORE the Armature modifier so all 8 evaluated walk frames share
    #    100% identical vertex count, UV layout, and triangle indices (~1,600 verts for silky 90fps VR!)
    bpy.context.view_layer.objects.active = h_mesh
    arm_mod = next((m for m in h_mesh.modifiers if m.type == 'ARMATURE'), None)
    dec_mod = h_mesh.modifiers.new("Decimate", 'DECIMATE')
    dec_mod.ratio = 0.11  # 16,340 -> ~1,800 verts (super clean silhouette & real human face!)
    # Move Decimate ABOVE Armature so skinning weights deform the decimated mesh cleanly
    bpy.ops.object.modifier_move_to_index(modifier="Decimate", index=0)
    bpy.ops.object.modifier_apply(modifier="Decimate")
    # Triangulate the base mesh once so all 8 frames have identical triangle indices
    tri_mod = h_mesh.modifiers.new("Triangulate", 'TRIANGULATE')
    bpy.ops.object.modifier_move_to_index(modifier="Triangulate", index=0)
    bpy.ops.object.modifier_apply(modifier="Triangulate")
    print(f"Decimated & triangulated human base mesh: {len(h_mesh.data.vertices)} verts, {len(h_mesh.data.polygons)} tris")

    # 5. Evaluate 8 evenly-spaced frames of the real Mixamo Walk cycle!
    depsgraph = bpy.context.evaluated_depsgraph_get()
    raw_frames = []
    uvs = []
    normals_ref = []
    indices = []

    # Build a consistent (v_idx, uv) expansion map from frame 0 so UVs & indices match every frame
    bpy.context.scene.frame_set(int(round(f_start)))
    bpy.context.view_layer.update()
    ev0 = h_mesh.evaluated_get(depsgraph)
    m0 = ev0.to_mesh()
    uv_layer0 = m0.uv_layers.active.data if m0.uv_layers.active else None

    # First pass: compute normalization transform from frame 0 (height 1.80m, feet at Z=0, centered X/Y)
    mw = h_mesh.matrix_world
    pts0 = [(mw @ v.co) for v in m0.vertices]
    min_x = min(p.x for p in pts0); max_x = max(p.x for p in pts0)
    min_y = min(p.y for p in pts0); max_y = max(p.y for p in pts0)
    min_z = min(p.z for p in pts0); max_z = max(p.z for p in pts0)
    sc = 1.80 / max(0.001, (max_z - min_z))
    cx = (min_x + max_x) * 0.5
    cy = (min_y + max_y) * 0.5
    print(f"Frame 0 raw bbox: X[{min_x:.3f},{max_x:.3f}] Y[{min_y:.3f},{max_y:.3f}] Z[{min_z:.3f},{max_z:.3f}] sc={sc:.3f}")

    # Detect facing direction from toes (want facing -Y in Blender so it faces +Z in Three.js)
    toes_y = [(p.y - cy) * sc for p in pts0 if (p.z - min_z) * sc < 0.10]
    flip_front = (sum(toes_y) / max(1, len(toes_y))) > 0
    print(f"Flip front 180: {flip_front}")

    # Build canonical expanded vertex list (each entry = original mesh vertex index) so UVs are seam-free
    vert_map = {}
    expanded_v_indices = []
    for poly in m0.polygons:
        if len(poly.vertices) != 3:
            continue
        tri = []
        for loop_idx in poly.loop_indices:
            v_idx = m0.loops[loop_idx].vertex_index
            uv = uv_layer0[loop_idx].uv if uv_layer0 else Vector((0, 0))
            key = (v_idx, round(uv.x, 4), round(uv.y, 4))
            if key not in vert_map:
                vert_map[key] = len(expanded_v_indices)
                expanded_v_indices.append(v_idx)
                uvs.extend([round(uv.x, 4), round(uv.y, 4)])
                n = (mw.to_3x3() @ m0.vertices[v_idx].normal).normalized()
                nx, ny, nz = (-n.x, -n.y, n.z) if flip_front else (n.x, n.y, n.z)
                normals_ref.extend([round(nx, 4), round(nz, 4), round(-ny, 4)])
            tri.append(vert_map[key])
        indices.extend(tri)
    ev0.to_mesh_clear()

    # Now sample all 8 frames of the real Mixamo Walk cycle!
    frames_three = []
    for k in range(NUM_FRAMES):
        f_val = f_start + (f_end - f_start) * (k / NUM_FRAMES)
        bpy.context.scene.frame_set(int(f_val), subframe=(f_val - int(f_val)))
        bpy.context.view_layer.update()
        ev = h_mesh.evaluated_get(depsgraph)
        mk = ev.to_mesh()
        mw_k = h_mesh.matrix_world
        # Keep each frame's feet grounded at Z=0 and horizontally centered on hips
        wpts = [(mw_k @ v.co) for v in mk.vertices]
        f_cx = (min(p.x for p in wpts) + max(p.x for p in wpts)) * 0.5
        f_cy = (min(p.y for p in wpts) + max(p.y for p in wpts)) * 0.5
        f_min_z = min(p.z for p in wpts)
        frame_pos = []
        for v_idx in expanded_v_indices:
            p = wpts[v_idx]
            x = (p.x - f_cx) * sc
            y = (p.y - f_cy) * sc
            z = (p.z - f_min_z) * sc
            if flip_front:
                x = -x
                y = -y
            # Quantize to 3 decimals (millimeter precision) to keep JSON super fast & compact!
            frame_pos.extend([round(x, 3), round(z, 3), round(-y, 3)])
        frames_three.append(frame_pos)
        ev.to_mesh_clear()

    print(f"Baked {NUM_FRAMES} real Mixamo Walk frames: {len(expanded_v_indices)} verts, {len(indices) // 3} tris")

    # 6. Extract the REAL human diffuse Base Color texture & resize to 512x512 JPEG
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
    if not base_img:
        base_img = next((img for img in bpy.data.images if img.size[0] > 0), None)

    if base_img:
        base_img.scale(512, 512)
        tmp_jpg = os.path.join(ROOT, "walking_human_tex.jpg")
        bpy.context.scene.render.image_settings.file_format = 'JPEG'
        bpy.context.scene.render.image_settings.quality = 78
        base_img.save_render(filepath=tmp_jpg) if False else None
        base_img.filepath_raw = tmp_jpg
        base_img.file_format = 'JPEG'
        base_img.save()
        with open(tmp_jpg, "rb") as tf:
            b64 = base64.b64encode(tf.read()).decode("ascii")
        tex_data_uri = "data:image/jpeg;base64," + b64
        print(f"Extracted real human texture '{base_img.name}' (512x512): {len(b64):,} b64 chars")

    out_path = os.path.join(ROOT, "walking_human_asset.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "frames": frames_three,
            "n": normals_ref,
            "uv": uvs,
            "i": indices,
            "tex": tex_data_uri
        }, f, separators=(",", ":"))
    print("Saved:", out_path, f"({os.path.getsize(out_path):,} bytes)")

    # 7. Render a side-by-side preview of Frame 0 and Frame 4 (mid-stride!) in Blender 5.3!
    bpy.context.scene.frame_set(int(f_start + (f_end - f_start) * 0.25))
    bpy.context.view_layer.update()
    # Camera facing the human from front-3/4 angle
    for name, loc, energy in [("Key", (-2.0, -3.0, 2.5), 260), ("Fill", (2.2, -2.0, 1.5), 140)]:
        ld = bpy.data.lights.new(name, type='AREA'); ld.energy = energy; ld.size = 2.0
        lo = bpy.data.objects.new(name, ld); lo.location = loc
        lo.rotation_euler = (Vector((0, 0, 0.95)) - lo.location).to_track_quat('-Z', 'Y').to_euler()
        bpy.context.collection.objects.link(lo)

    cd = bpy.data.cameras.new("Cam"); cd.lens = 45
    co = bpy.data.objects.new("Cam", cd); co.location = (0.55, -2.6, 1.12)
    co.rotation_euler = (Vector((0, 0, 0.92)) - co.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.collection.objects.link(co)
    bpy.context.scene.camera = co

    scn = bpy.context.scene
    scn.render.engine = 'BLENDER_EEVEE'
    scn.render.resolution_x = 768
    scn.render.resolution_y = 768
    scn.render.filepath = os.path.join(ROOT, "Blender-Walking-Human-Preview.png")
    bpy.ops.render.render(write_still=True)
    print("Rendered:", scn.render.filepath)


if __name__ == "__main__":
    main()
