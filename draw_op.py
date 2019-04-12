"""
Main Modal operator
"""

import bpy
import bgl
import gpu

from gpu_extras.batch import batch_for_shader
from .obj_button import *


class RIGUI_OT_OpenUI(bpy.types.Operator):
    """ Draw the UI, modal operator """
    bl_idname = "rigui.ui_draw"
    bl_label = "Open RigUI"
    bl_options = {'REGISTER'}

    def __init__(self):
        # buttons are defined here for now, define add_button etc.

        self.buttons = []

    def load_buttons(self, dict):
        self.buttons.clear()
        for obj in dict.get('buttons'):
            button = RigUIButton()
            button.get_properties(obj)
            self.buttons.append(button)

    def draw_background(self, context):
        w = context.area.width
        h = context.area.height
        space = context.area.spaces[0]
        x = 0
        y = 0
        background_verts = (
            (x, y),
            (x, h),
            (w, h),
            (w, y)
        )

        background_indices = ((0, 1, 2), (0, 2, 3))
        background_shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        background_batch = batch_for_shader(background_shader, 'TRIS',
                                            {"pos": background_verts}, indices=background_indices)
        background_shader.bind()
        background_shader.uniform_float("color", (0.2, 0.2, 0.2, 1))

        background_batch.draw(background_shader)

    def draw_image(self, context):
        w = 500
        h = 500
        x = 0
        y = 0

        img_verts = (
            (x, y),
            (x, h),
            (w, h),
            (w, y)
        )
        filepath = "C:/Users/Christopher/AppData/Roaming/Blender Foundation/Blender/2.80/scripts/addons/blender-rig-ui/img/test.jpg"
        image = bpy.data.images.load(filepath, check_existing=True)

        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)

        img_shader = gpu.shader.from_builtin('2D_IMAGE')
        img_batch = batch_for_shader(img_shader, 'TRI_FAN',
                                     {"pos": img_verts,
                                      "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1))}, )
        img_shader.bind()
        img_shader.uniform_int("image", 0)
        img_batch.draw(img_shader)

    def invoke(self, context, event):
        self.draw_handle = bpy.types.SpaceImageEditor.draw_handler_add(self.draw_callback_px, (self, context), 'WINDOW',
                                                                       'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        context.scene.rigUI_active = True
        context.area.tag_redraw()  # update image editor view

        buttonlist = {
            "buttons": [
                {
                    "color": (0.5, 0.5, 0.8, 1)
                }
            ]
        }

        self.load_buttons(buttonlist)
        return {"RUNNING_MODAL"}

    def handle_events(self, context, event):
        # nothing to handle yet
        for button in self.buttons:
            if button.handle_event(context, event):
                return True

        return False

    def modal(self, context, event):
        # pass events to buttons
        if self.handle_events(context, event):
            return {'RUNNING_MODAL'}

        # kill it
        if not context.scene.rigUI_active:
            bpy.types.SpaceImageEditor.draw_handler_remove(self.draw_handle, 'WINDOW')
            if context.area:
                context.area.tag_redraw()
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        pass

    def draw(self, context):
        pass

    def draw_callback_px(self, op, context):
        # Draw everything
        self.draw_background(context)
        # Get buttons from dict, so we only need to reload the dict to re-get the buttons :D
        for button in self.buttons:
            button.draw()
