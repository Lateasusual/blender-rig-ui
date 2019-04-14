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

    new_text_name = bpy.props.StringProperty(name="New Text")

    def __init__(self):
        pass

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop_search(context.scene, "rigUI_collection", bpy.data, "collections")
        row = layout.row()
        row.prop_search(context.scene, "rigUI_build_text_name", bpy.data, "texts")


        row = layout.row()
        op = row.operator("rigui.add_button")
        row = layout.row()
        op.layout_text = context.scene.rigUI_build_text_name

        if context.active_object.type == "MESH":
            row = layout.row()
            row.label(text="Button Settings:")
            row = layout.row()
            row.prop_search(context.scene, "rigUI_build_rig", bpy.data, "armatures")
            row = layout.row()
            row.prop_search(context.active_object, "rigUI_linked_bone",
                            bpy.data.armatures[context.scene.rigUI_build_rig], "bones")
            row = layout.row()
            row.prop(context.active_object, "color")

        op.canvas_collection = context.scene.rigUI_collection
        if context.active_object.type == "ARMATURE":
            row = layout.row()
            row.label(text="Rig Settings")
            row = layout.row()
            row.prop_search(context.active_object, "rigUI_ui_name", bpy.data, "texts")

