"""
Mesh functions (edge loops etc.) for importing meshes as button shapes
"""

import bpy
from mathutils import Vector
import bmesh
from bpy_extras import mesh_utils


def get_mesh(obj):
    data = obj.data

    bm = bmesh.new()
    bm.from_mesh(data)
    # clean the mesh
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    bm.to_mesh(data)

    vertex_count = [v.index for v in bm.verts]
    bm_loops = border_loops(bm, 0, [], vertex_count)

    loop_vertices = []

    vertices = []
    indices = []

    # apply object matrix, then reset it
    mat = obj.matrix_world

    for face in data.polygons:
        indices.append([face.vertices[0], face.vertices[1], face.vertices[2]])

    for vert in data.vertices:
        # multiply for rotation etc
        vertices.append(vert.co.xyz @ mat.transposed())

    if len(bm_loops) != 0:
        for v in bm_loops[0]:
            loop_vertices.append(v.co @ mat.transposed())
    else:
        loop_vertices = vertices



    return vertices, indices, loop_vertices


def border_loop(vert, loop):
    border_edge = [e for e in vert.link_edges if e.is_boundary or e.is_wire]

    if border_edge:
        for edge in border_edge:
            other_vert = edge.other_vert(vert)

            if not other_vert in loop:
                loop.append(other_vert)
                border_loop(other_vert, loop)

        return loop
    else:
        return [vert]


def border_loops(bm, vert_index, loops, vertex_count):
    bm.verts.ensure_lookup_table()

    loop = border_loop(bm.verts[vert_index], [bm.verts[vert_index]])
    if len(loop) > 1:
        loops.append(loop)

    for v in loop:
        vertex_count.remove(v.index)

    if len(vertex_count):
        border_loops(bm, vertex_count[0], loops, vertex_count)
    return loops
