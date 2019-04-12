"""
Starting point for full code refactor
This is a work in progress
"""

from .draw_op import *
from .obj_operators import *
from .obj_panels import *
import bpy

bl_info = {
    "name": "RigUI_New",
    "description": "Editable UI interface for rig animation",
    "author": "Lateasusual",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "Image Editor",
    "category": "animation"
}

classes = {
    RIGUI_OT_OpenUI,
    RIGUI_OT_CloseUI,
    VIEW3D_PT_RigUIPanel
}


def ui_icon(self, context):
    if not context.scene.rigUI_active:
        op = self.layout.operator("rigui.ui_draw", icon='MOD_ARMATURE', text='')
    else:
        op = self.layout.operator("rigui.ui_close", icon='MOD_ARMATURE', text='', depress=True)



def register():
    for c in classes:
        bpy.utils.register_class(c)

    # Property definitions
    bpy.types.Scene.rigUI_active = bpy.props.BoolProperty(name="RigUI Active", default=False)

    # Prepend for image header here
    bpy.types.IMAGE_HT_header.prepend(ui_icon)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    # Property removals, maybe don't bother since we'll need to restart after unregistering anyway
    del bpy.types.Scene.rigUI_active

if __name__ == '__main__':
    register()
