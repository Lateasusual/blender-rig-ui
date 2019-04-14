"""
Main Modal operator
"""

import bpy

from .obj_button import *
from .functions_json import *
from .functions_gpu import *


class RIGUI_OT_OpenUI(bpy.types.Operator):
    """ Opens RigUI in the Image Editor"""
    bl_idname = "rigui.ui_draw"
    bl_label = "Open RigUI"
    bl_options = {'REGISTER'}

    def __init__(self):
        # buttons are defined here for now, define add_button etc.
        self.draw_handle = None
        self.update_event = None
        self.buttons = []

    def load_buttons(self, dict):
        """ Load buttons from mesh, if use_mesh_shapes is enabled """
        self.buttons.clear()
        for obj in dict.get('buttons'):
            button = RigUIButton()
            button.get_properties(obj)
            self.buttons.append(button)


    def reload_layout(self):
        buttonlist = get_json_dict("Text")
        if buttonlist is not None:
            self.load_buttons(buttonlist)

    def invoke(self, context, event):
        if context.mode in {"EDIT_MESH", "SCULPT", "EDIT"}:
            bpy.ops.object.mode_set(mode="OBJECT")
        self.draw_handle = bpy.types.SpaceImageEditor.draw_handler_add(self.draw_callback_px, (self, context), 'WINDOW',
                                                                       'POST_PIXEL')
        # self.update_event = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        context.scene.rigUI_active = True
        bpy.context.scene["rigUI_tag_reload"] = False
        self.reload_layout()

        context.area.tag_redraw()  # update image editor view
        return {"RUNNING_MODAL"}

    def handle_events(self, context, event):
        # handle buttons
        for button in self.buttons:
            if button.handle_event(context, event):
                return True
        # if we're not over a button do a selection box
        # TODO add box select
        return False

    def modal(self, context, event):
        # pass events to buttons
        if self.handle_events(context, event):
            return {'RUNNING_MODAL'}

        # kill it
        if not context.scene.rigUI_active:
            bpy.types.SpaceImageEditor.draw_handler_remove(self.draw_handle, 'WINDOW')
            # context.window_manager.event_timer_remove(self.update_event)
            self.draw_handle = None
            self.update_event = None
            if context.area:
                context.area.tag_redraw()
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        pass

    def draw(self, context):
        pass

    def draw_callback_px(self, op, context):
        # If we're tagged to reload object positions etc.
        # NEVER let this be left on, it'll just crash
        if bpy.context.scene["rigUI_tag_reload"]:
            self.reload_layout()
            bpy.context.scene["rigUI_tag_reload"] = False

        # Draw everything
        draw_background(context)
        # Cached buttons, not loading from dict or json every time
        for button in self.buttons:
            button.draw()
