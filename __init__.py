"""
Starting point for full code refactor
This is a work in progress
"""

from .draw_op import *
from .obj_operators import *
from .obj_panels import *
import bpy

bl_info = {
    "name": "blender-rig-ui",
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
    RIGUI_OT_AddButton,
    VIEW3D_PT_RigUIPanel,
    RIGUI_OT_CreateCanvas
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
    bpy.types.Scene.rigUI_active = bpy.props.BoolProperty(name="RigUI is Active", default=False, options={'SKIP_SAVE'})
    bpy.types.Scene.rigUI_collection = bpy.props.StringProperty(name="Canvas Collection", default="None")
    bpy.types.Scene.rigUI_tag_reload = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.rigUI_build_text_name = bpy.props.StringProperty(name="Text target", default="RigUI_Layout")
    bpy.types.Scene.rigUI_build_rig = bpy.props.StringProperty(name="Rig", default="")
    bpy.types.Object.rigUI_linked_bone = bpy.props.StringProperty(name="Bone", default="")
    bpy.types.Object.rigUI_ui_name = bpy.props.StringProperty(name="UI", default="")
    bpy.types.Object.rigUI_tab_key = bpy.props.StringProperty(name="Tab", default="buttons")
    bpy.types.Scene.rigUI_canvas_object = bpy.props.StringProperty(name="Offset Object")

    # Prepend for image header here
    bpy.types.IMAGE_HT_header.prepend(ui_icon)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    # Property removals, maybe don't bother since we'll need to restart after unregistering anyway
    del bpy.types.Scene.rigUI_active
    del bpy.types.Scene.rigUI_collection
    del bpy.types.Scene.rigUI_tag_reload
    del bpy.types.Scene.rigUI_build_text_name
    del bpy.types.Scene.rigUI_build_rig
    del bpy.types.Object.rigUI_linked_bone
    del bpy.types.Object.rigUI_ui_name
    del bpy.types.Scene.rigUI_canvas_object
    del bpy.types.Object.rigUI_tab_key


if __name__ == '__main__':
    register()
