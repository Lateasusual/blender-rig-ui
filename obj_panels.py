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
        layout.prop_search(context.scene, "rigUI_collection", bpy.data, "collections")
        layout.prop_search(context.scene, "rigUI_build_text_name", bpy.data, "texts")
        layout.prop_search(context.scene, "rigUI_canvas_object", bpy.data, "objects")

        row = layout.row()
        row.scale_y = 2
        op = row.operator("rigui.add_button")
        op.layout_text = context.scene.rigUI_build_text_name
        op.canvas_collection = context.scene.rigUI_collection
        op.canvas_object = context.scene.rigUI_canvas_object
        row = layout.row()
        op = row.operator("rigui.create_canvas")
        row = layout.row()
        row.prop(context.scene, "rigUI_text_scale")

        if context.active_object.type == "MESH":
            row = layout.row()
            row.prop(context.active_object, "rigUI_button_type")

            row = layout.row()
            row.label(text="Button Settings:")

            if "rigUI_button_type" not in context.active_object or context.active_object["rigUI_button_type"] == 0:
                row = layout.row()
                row.prop_search(context.scene, "rigUI_build_rig", bpy.data, "armatures")
                row = layout.row()
                row.prop_search(context.active_object, "rigUI_linked_bone",
                                bpy.data.armatures[context.scene.rigUI_build_rig], "bones")
            elif context.active_object["rigUI_button_type"] == 1:
                row = layout.row()
                row.label(text="ignore this")
            row = layout.row()
            row.prop(context.active_object, "color")

        if context.active_object.type == "ARMATURE":
            row = layout.row()
            row.label(text="Rig Settings")
            row = layout.row()
            row.prop_search(context.active_object, "rigUI_ui_name", bpy.data, "texts")
