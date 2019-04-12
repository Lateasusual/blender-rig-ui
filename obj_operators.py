"""
Register other operators:
    / Editing UI
    / Button functions not included in bpy.ops
"""

import bpy

class RIGUI_OT_AddButton(bpy.types.Operator):
    bl_idname = "rigui.add_button"
    bl_label = "Add Button"
    bl_options = {'REGISTER'}

    def __init__(self):
        pass

    def execute(self, context):
        pass

