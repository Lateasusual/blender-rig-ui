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
from statistics import mean
from . functions_mesh import get_mesh
from . functions_gpu import draw_text


def average_position(in_vectors):
    x = [lst[0] for lst in in_vectors]
    y = [lst[1] for lst in in_vectors]
    # Flattens the vector since we don't need z
    return Vector((mean(x), mean(y), 0))


def vertex_to_float_array(vertices):
    out = []
    for v in vertices:
        out.append([v[0], v[1], v[2]])
    return out


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


def is_triangle_in_rect(verts, x_range, y_range):
    # if both are >= 1 then the triangle is within the range (must overlap)
    x_overlap_counts = 0
    y_overlap_counts = 0
    for v in verts:
        if x_range[0] < v[0] < x_range[1]:
            x_overlap_counts += 1
        if y_range[0] < v[1] < y_range[1]:
            y_overlap_counts += 1
    return x_overlap_counts > 0 and y_overlap_counts > 0


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

        self.scale = (100, 100)  # maybe use for zoom, currently converting 1m to 100px
        self.offset = (0, 0)  # maybe use for zoom

        self.color = (0.8, 0.8, 0.2, 1)
        self.state = button_state.default

        self.parent_op = None
        # Button function, e.g. bone to select bones, or tab for tabs etc. etc.
        self.type = "bone"
        self.linked_bone = ""
        self.use_shape = True
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

    def is_shape_in_rect(self, x_range, y_range):
        for triple in self.indices:
            triangle = [self.vertices[triple[0]], self.vertices[triple[1]], self.vertices[triple[2]]]
            if is_triangle_in_rect(triangle, x_range, y_range):
                return True
        return False

    def set_parent_op(self, op):
        self.parent_op = op

    def set_vertices(self, vertices):
        self.vertices = vertices

    def set_indices(self, indices):
        self.indices = indices

    def set_scale(self, scale):
        self.scale = scale

    def set_offset(self, offset):
        self.offset = offset

    def set_linked_bone(self, bone):
        self.linked_bone = bone

    def set_color(self, color):
        colours = []
        for c in color:
            colours.append(c)
        self.color = colours

    def set_outline_vertices(self, vertices):
        self.vertices_lines = vertices

    def set_outline_indices(self, indices):
        self.indices_lines = indices

    def set_use_shape(self, state):
        self.use_shape = state

    def set_type(self, type):
        self.type = type

    def load_shape_from_obj(self, obj_name, offset_obj=None):
        # Tagged not to load from bpy, use cached JSON instead
        if not self.use_shape:
            return

        self.shape_object_name = obj_name
        if obj_name not in bpy.data.objects:
            return
        obj = bpy.data.objects[obj_name]

        verts, indices, loop = get_mesh(obj, offset_obj)
        self.vertices = verts
        self.indices = indices

        if loop is None or len(loop) == 0:
            return

        loop_indices = []

        for i, v in enumerate(loop):
            if i < len(loop) - 1:
                loop_indices.append([i, i + 1])
            else:
                loop_indices.append([i, 0])

        self.vertices_lines = loop
        self.indices_lines = loop_indices

        self.update_shader()

    def to_dict(self):
        return {
            "use_shape": self.use_shape,
            "type": self.type,
            "verts": vertex_to_float_array(self.vertices),
            "indices": self.indices,
            "outline_verts": vertex_to_float_array(self.vertices_lines),
            "outline_indices": self.indices_lines,
            "object": self.shape_object_name,
            "scale": self.scale,
            "offset": self.offset,
            "color": self.color,
            "bone": self.linked_bone
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
            "object": self.load_shape_from_obj,
            "use_shape": self.set_use_shape,
            "bone": self.set_linked_bone,
            "type": self.set_type
        }
        for key in dictionary.keys():
            val = dictionary[key]
            func = refs.get(key, lambda: None)
            func(val)
        # refresh vertex position etc.
        self.update_shader()

    def draw(self):
        if bpy.context.active_object.type == "ARMATURE":
            if self.linked_bone not in bpy.context.active_object.data.bones:
                return  # don't draw if there's nothing to draw :D
            bone_selected = bpy.context.active_object.data.bones[self.linked_bone].select
            if bone_selected:
                self.state = button_state.selected
            elif self.state == button_state.hovered:
                pass
            elif self.state == button_state.selected:
                self.state = button_state.default
        self.shader.bind()
        color = (0.3, 0.3, 0.3, 1)

        if self.state is button_state.hovered:
            color = (0.5, 0.5, 0.5, 1)
        elif self.state is button_state.selected:
            color = (0.4, 0.4, 0.4, 1)

        # draw background
        self.shader.uniform_float("color", color)
        self.batch.draw(self.shader)

        # draw lines
        self.shader.uniform_float("color", self.color)
        self.batch_lines.draw(self.shader)

        # draw text
        verts, notverts = self.scale_and_offset_verts()
        draw_text(self.linked_bone, [average_position(verts)[0], average_position(verts)[1]], size=round(self.scale[0] / 6))

    # Change this to do things other than selecting bones
    def select_button(self, shift=False):
        if bpy.context.active_object.type == "ARMATURE":
            if self.linked_bone not in bpy.context.active_object.data.bones:
                return
            bone_selected = bpy.context.active_object.data.bones[self.linked_bone].select
            bpy.ops.object.mode_set(mode='POSE')
            if shift:
                bpy.context.active_object.data.bones[self.linked_bone].select = not bone_selected
                if bone_selected:
                    self.state = button_state.selected
                else:
                    self.state = button_state.hovered
            else:
                bpy.ops.pose.select_all(action='DESELECT')
                bpy.context.active_object.data.bones[self.linked_bone].select = True
                self.state = button_state.selected

    '''
    Refactor all of this so it handles event types discreetly, and support for setting selection other than clicks
    '''
    def handle_event(self, context, event):
        # Button presses etc, True if action is valid e.g. button was pressed
        ret = False
        if event.type == "LEFTMOUSE":
            if event.value == 'PRESS' and self.is_in_shape(event.mouse_region_x, event.mouse_region_y):
                self.select_button(shift=event.shift)

        if event.type == 'MOUSEMOVE':
            if self.is_in_shape(event.mouse_region_x, event.mouse_region_y):
                if not self.state == button_state.selected:
                    self.state = button_state.hovered
                # Run this op if left mouse pressed and valid
                # do nothing just yet
                ret = True
            else:
                if self.state is button_state.hovered and not self.state is button_state.selected:
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
