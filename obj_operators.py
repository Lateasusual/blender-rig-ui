"""
Register other operators:
    / Editing UI
    / Button functions not included in bpy.ops
"""

import bpy
from . functions_json import *


class RIGUI_OT_AddButton(bpy.types.Operator):
    bl_idname = "rigui.add_button"
    bl_label = "Build UI"
    bl_options = {'REGISTER'}

    # TODO implement bone selection
    # bone = bpy.props.StringProperty("Bone")

    canvas_collection = bpy.props.StringProperty("collection")

    def execute(self, context):
        col = bpy.data.collections[self.canvas_collection]
        bpy.ops.object.mode_set(mode="OBJECT")
        clear_json("Text")
        for obj in col.all_objects:
            if obj.type == "MESH":

                button = json_add_button_obj("Text", obj)
                button.use_shape = False
        context.scene["rigUI_tag_reload"] = True
        return {'FINISHED'}


class RIGUI_OT_CloseUI(bpy.types.Operator):
    """ Closes RigUI """
    bl_idname = "rigui.ui_close"
    bl_description = "Close RigUI"
    bl_label = "Close UI"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        context.scene.rigUI_active = False
        return {'FINISHED'}
