"""
Blender UI Panels associated with the addon
For editing the UI etc.
"""

import bpy


class VIEW3D_PT_RigUIPanel(bpy.types.Panel):
    bl_label = "RigUI"
    bl_idname = "VIEW3D_RigUI_Panel"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "RigUI"

    def __init__(self):
        pass

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        label = row.label(text="blank panel for RigUI tools")
