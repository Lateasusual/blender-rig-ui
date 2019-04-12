"""
Main Modal operator
"""

import bpy
import bgl
import gpu

from gpu_extras.batch import batch_for_shader

class RIGUI_OT_OpenUI(bpy.types.Operator):
    """ Draw the UI, modal operator """
    bl_idname = "rigui.ui_draw"
    bl_label = "Open RigUI"
    bl_options= {'REGISTER'}

    def __init__(self):
        # Called whenever the window is drawn
        # Called every 0.1 seconds
        self.draw_handle = None
        # all buttons in UI
        self.buttons = []

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
        background_shader.uniform_float("color", (1, 0.2, 0.2, 0.2))

        bgl.glEnable(bgl.GL_BLEND)
        background_batch.draw(background_shader)
        bgl.glDisable(bgl.GL_BLEND)

    def draw_callback_px(self, context):
        # Draw everything
        self.draw_background(context)

        for b in self.buttons:
            b.draw()

    def register_handlers(self, context):
        self.draw_handle = bpy.types.SpaceImageEditor.draw_handler_add(self.draw_callback_px,
                                                                       (context,), 'WINDOW', 'POST_PIXEL')
        # self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

    def unregister_handlers(self, context):
        # context.window_manager.event_timer_remove(self.draw_event)

        bpy.types.SpaceImageEditor.draw_handler_remove(self.draw_handle, 'WINDOW')
        self.draw_handle = None

    def invoke(self, context, event):
        if context.scene.rigUI_active:
            context.scene.rigUI_active = False
            return {'CANCELLED'}
        self.register_handlers(context)
        context.window_manager.modal_handler_add(self)
        context.scene.rigUI_active = True

        context.area.tag_redraw()
        return {"RUNNING_MODAL"}

    def handle_events(self, context, event):
        # nothing to handle yet
        for button in self.buttons:
            if button.handle_event(context, event):
                return True

        return False

    def modal(self, context, event):
        # pass events to handler, if they're handled then don't passthrough
        if self.handle_events(context, event):
            return {'RUNNING_MODAL'}
        return {'PASS_THROUGH'}

    def execute(self, context):
        pass

    def cancel(self, context):
        self.unregister_handlers(context)

    def draw(self, context):
        pass

