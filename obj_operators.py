"""
Register other operators:
    / Editing UI
    / Button functions not included in bpy.ops
"""

import bpy
from . functions_mesh import *

class RIGUI_OT_AddButton(bpy.types.Operator):
    bl_idname = "rigui.add_button"
    bl_label = "Add Button"
    bl_options = {'REGISTER'}

    def __init__(self):
        pass

    def execute(self, context):
        obj = bpy.data.objects['Cube']
        verts, indcs, loops = get_mesh(obj)
        print(verts)
        print(indcs)
        print(loops)
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
