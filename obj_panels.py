"""
Blender UI Panels associated with the addon
For editing the UI etc.
"""

import bpy


class VIEW3D_PT_RigUIPanel(bpy.types.Panel):
    """ Panel for adding buttons to layout """
    bl_label = "RigUI"
    bl_idname = "VIEW3D_PT_RigUI_Panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RigUI"

    def __init__(self):
        pass

    def draw(self, context):
        layout = self.layout
        canvas = layout.prop_search(context.scene, "rigUI_collection", bpy.data, "collections")
        row = layout.row()
        op = row.operator("rigui.add_button")
        op.canvas_collection = context.scene.rigUI_collection
