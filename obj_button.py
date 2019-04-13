"""
Button object class - Has position, shape, associated operator etc.
Try to keep it as simple as possible

If button shapes are stored offset from origin, doesn't matter since we can use shape for ALL hitreg, and button x/y is
irrelevant... maybe don't even bother with x/y
"""

import bpy
import gpu
import bgl
from gpu_extras.batch import batch_for_shader
from mathutils.geometry import intersect_point_tri_2d
from mathutils import Vector
from enum import Enum
from . functions_mesh import get_mesh


def scale_verts(verts, scale):
    scaled_verts = []
    for vert in verts:
        scaled_verts.append(Vector((vert[0] * scale[0], vert[1] * scale[1])))
    return scaled_verts


def offset_verts(verts, offset):
    offset_verts = []
    for vert in verts:
        offset_verts.append(Vector((vert[0] + offset[0], vert[1] + offset[1])))
    return offset_verts

class button_state(Enum):
    default = 0
    hovered = 1
    pressed = 2
    selected = 3


class RigUIButton:
    def __init__(self):
        """ Button initialisation and attributes here """
        # Shape attributes
        self.vertices = [(0, 0), (0, 1), (1, 1), (1, 0)]
        self.vertices_lines = [(0, 0), (0, 1), (1, 1), (1, 0)]
        self.indices = [(0, 1, 2), (0, 2, 3)]
        self.indices_lines = [(0, 1), (1, 2), (2, 3), (3, 0)]

        self.scale = (100, 100)
        self.offset = (20, 20) # Border buffer / maybe use for zoom?

        self.color = (0.8, 0.8, 0.2, 1)
        self.state = button_state.default

        self.shape_object_name = ""
        self.shader = None
        self.batch = None
        self.batch_lines = None
        self.update_shader()

    def update_shader(self):
        vertices_offset, vertices_lines = self.scale_and_offset_verts()
        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'TRIS',
                                      {"pos": vertices_offset}, indices=self.indices)
        self.batch_lines = batch_for_shader(self.shader, 'LINES',
                                            {"pos": vertices_lines}, indices=self.indices_lines)

    def scale_and_offset_verts(self):
        vertices_scaled = scale_verts(self.vertices, self.scale)
        vertices__lines_scaled = scale_verts(self.vertices_lines, self.scale)
        return offset_verts(vertices_scaled, self.offset), offset_verts(vertices__lines_scaled, self.offset)

    def set_vertices(self, vertices):
        self.vertices = vertices

    def set_indices(self, indices):
        self.indices = indices

    def set_scale(self, scale):
        self.scale = scale

    def set_offset(self, offset):
        self.offset = offset

    def set_color(self, color):
        self.color = color

    def mouse_down(self, event):
        pass

    def set_outline_vertices(self, vertices):
        self.vertices_lines = vertices

    def set_outline_indices(self, indices):
        self.indices_lines = indices

    def load_shape_from_obj(self, obj_name):
        self.shape_object_name = obj_name
        if obj_name not in bpy.data.objects:
            return
        obj = bpy.data.objects[obj_name]

        verts, indices, loop_verts = get_mesh(obj)
        self.vertices = verts
        self.indices = indices
        loop_indices = []
        for i, v in enumerate(loop_verts):
            if i < len(loop_verts) - 1:
                loop_indices.append([i, i+1])
            else:
                loop_indices.append([i, 0])
        print(loop_indices)
        self.vertices_lines = loop_verts
        self.indices_lines = loop_indices
        self.update_shader()

    def to_dict(self):
        return {
            "verts": self.vertices,
            "indices": self.indices,
            "outline_verts": self.vertices_lines,
            "outline_indices": self.indices_lines,
            "object": self.shape_object_name,
            "scale": self.scale,
            "offset": self.offset,
            "color": self.color
        }

    def get_properties(self, dictionary: dict):
        refs = {
            "verts": self.set_vertices,
            "indices": self.set_indices,
            "outline_verts": self.set_outline_vertices,
            "outline_indices": self.set_outline_indices,
            "scale": self.set_scale,
            "offset": self.set_offset,
            "color": self.set_color,
            "object": self.load_shape_from_obj
        }
        for key in dictionary.keys():
            val = dictionary[key]
            func = refs.get(key, lambda: None)
            func(val)

    def draw(self):
        self.shader.bind()
        color = (0.3, 0.3, 0.3, 1)

        if self.state is button_state.hovered:
            color = (0.5, 0.5, 0.5, 1)

        # draw background
        self.shader.uniform_float("color", color)
        self.batch.draw(self.shader)

        # draw lines
        self.shader.uniform_float("color", self.color)
        self.batch_lines.draw(self.shader)

    def handle_event(self, context, event):
        # Button presses etc, True if action is valid e.g. button was pressed
        ret = False
        if event.type == 'MOUSEMOVE':
            if self.is_in_shape(event.mouse_region_x, event.mouse_region_y):
                self.state = button_state.hovered
                # Run this op if left mouse pressed and valid
                # do nothing just yet
                self.mouse_down(event)
                ret = True
            else:
                if self.state is button_state.hovered:
                    self.state = button_state.default
        context.area.tag_redraw()
        return ret

    def is_in_shape(self, x, y):
        tri_indices = self.indices
        verts, lineverts = self.scale_and_offset_verts()
        # x, y = bpy.types.View2D.view_to_region(x, y, clip=True)

        for tri in tri_indices:
            if intersect_point_tri_2d(Vector((x, y)), verts[tri[0]], verts[tri[1]], verts[tri[2]]):
                return True
        return False
