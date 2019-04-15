"""
Main Modal operator
"""

import bpy

from .obj_button import *
from .functions_json import *
from .functions_gpu import *

def is_mouse_in_area(context, event):
    width = context.area.width
    height = context.area.height
    x = event.mouse_region_x
    y = event.mouse_region_y
    return 0 < x < width and 0 < y < height

class RIGUI_OT_OpenUI(bpy.types.Operator):
    """ Opens RigUI in the Image Editor"""
    bl_idname = "rigui.ui_draw"
    bl_label = "Open RigUI"
    bl_options = {'REGISTER'}

    def __init__(self):
        self.draw_handle = None
        self.update_event = None
        self.buttons = []
        self.active_object = None
        self.text_key = None
        self.tab_key = "buttons"
        self.scale_mod = 1
        self.transform_mod = [0, 0]
        self.transform_start = [0, 0]
        self.is_moving = False

    def load_buttons(self, dict):
        """ Load buttons from mesh, if use_mesh_shapes is enabled """
        # change dict.get to other tab names, and check for errors
        self.buttons.clear()
        if dict.get(self.tab_key) is None:
            return
        for obj in dict.get('buttons'):
            button = RigUIButton()
            button.get_properties(obj)
            button.set_parent_op(self)
            self.buttons.append(button)

    def default_layout(self):
        """ Called if we have no layout to display """
        self.buttons.clear()

    def reload_layout(self):
        if self.text_key is None:
            return
        text = get_json_dict(self.text_key, create_new=False)  # If there isn't a layout just don't load it
        if text is not None:
            self.load_buttons(text)
        else:
            self.default_layout()

    def invoke(self, context, event):
        if context.mode in {"EDIT_MESH", "SCULPT", "EDIT"}:
            bpy.ops.object.mode_set(mode="OBJECT")
        self.draw_handle = bpy.types.SpaceImageEditor.draw_handler_add(self.draw_callback_px, (self, context), 'WINDOW',
                                                                       'POST_PIXEL')
        self.update_event = context.window_manager.event_timer_add(0.1, window=context.window)
        context.window_manager.modal_handler_add(self)
        self.active_object = context.active_object
        context.scene.rigUI_active = True
        bpy.context.scene["rigUI_tag_reload"] = False

        self.text_key = context.active_object.name

        self.reload_layout()

        context.area.tag_redraw()  # update image editor view
        return {"RUNNING_MODAL"}

    def handle_events(self, context, event):
        # check for object selection changes
        if event.type == "TIMER":
            bpy.context.scene["rigUI_tag_reload"] = True
        if event.type == "WHEELUPMOUSE":
            if is_mouse_in_area(context, event):
                self.scale_mod += 0.1
        if event.type == "WHEELDOWNMOUSE":
            if is_mouse_in_area(context, event):
                self.scale_mod -= 0.1

        if event.type == "MOUSEMOVE" and event.ctrl and is_mouse_in_area(context, event):
            x = context.area.width - event.mouse_region_x
            y = context.area.height - event.mouse_region_y
            if not self.is_moving:
                self.is_moving = True
                self.transform_start = [x + self.transform_mod[0], y + self.transform_mod[1]]
            else:
                self.transform_mod = [self.transform_start[0] - x, self.transform_start[1] - y]
        else:
            self.is_moving = False

        if event.type in {"ESC"}:
            bpy.context.scene.rigUI_active = False
        # handle buttons
        for button in self.buttons:
            if button.handle_event(context, event):
                return True
        # if we're not over a button do a selection box
        # TODO add box select
        return False

    def modal(self, context, event):
        # pass events to buttons
        if event.type == "TIMER":
            # self.draw_callback_px(self, context) # CRASHES! >_< (probably wrong context but we can't fix that)
            return {'PASS_THROUGH'}
        if self.handle_events(context, event):
            return {'RUNNING_MODAL'}

        # kill it
        if not context.scene.rigUI_active:
            bpy.types.SpaceImageEditor.draw_handler_remove(self.draw_handle, 'WINDOW')
            context.window_manager.event_timer_remove(self.update_event)
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
        if self.text_key != context.active_object.rigUI_ui_name:
            self.text_key = context.active_object.rigUI_ui_name
            self.reload_layout()
        elif context.active_object is None:
            draw_background()
            return
        # If we're tagged to reload object positions etc.
        if bpy.context.scene["rigUI_tag_reload"]:
            self.reload_layout()
            bpy.context.scene["rigUI_tag_reload"] = False

        # Draw everything
        draw_background(context)
        # Cached buttons, not loading from dict or json every time

        width = context.area.width
        height = context.area.height


        for button in self.buttons:
            button.set_offset([width / 2 + self.transform_mod[0], height / 2 + self.transform_mod[1]])
            button.set_scale([100 * self.scale_mod, 100 * self.scale_mod])
            button.update_shader()
            button.draw()
