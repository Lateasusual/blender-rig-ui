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

class RigUIButton():
    def __init__(self, context):
        """ Button initialisation and attributes here """
        # Shape attributes
        self.vertices = ((0, 0), (0, 100), (100, 100), (100, 0))
        self.indices = ((0, 1, 2), (0, 2, 3))
        self.scale = (100, 100)
        self.color = (0.8, 0.8, 0.2, 1)
        self.shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'TRIS', {"pos": self.vertices}, indices=self.indices)
        self.context = context

    def draw(self):
        self.shader.bind()
        self.shader.uniform_float("color", self.color)

        bgl.glEnable(bgl.GL_BLEND)
        self.batch.draw(self.shader)
        bgl.glDisable(bgl.GL_BLEND)

    def handle_event(self, context, event):
        # Button presses etc, True if action is valid e.g. button was pressed
        if event.type == 'MOUSEMOVE':
            if self.is_in_shape(event.mouse_region_x, event.mouse_region_y):
                # Run this op if left mouse pressed and valid
                self.color = (1, 0.2, 0.2, 1)
                context.area.tag_redraw()
                return True
        else:
            self.color = (0.8, 0.8, 0.2, 1)
            context.area.tag_redraw()
        return False

    def is_in_shape(self, x, y):
        tri_indices = self.indices
        verts = self.vertices
        # x, y = bpy.types.View2D.view_to_region(x, y, clip=True)

        for tri in tri_indices:
            if intersect_point_tri_2d(Vector((x, y)), verts[tri[0]], verts[tri[1]], verts[tri[2]]):
                return True
        return False