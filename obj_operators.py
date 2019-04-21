"""
Register other operators:
    / Editing UI
    / Button functions not included in bpy.ops
"""

import bpy
from . functions_json import *


def get_collection(name):
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection

    if name not in bpy.context.scene.collection.children.keys():
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    else:
        col = bpy.data.collections[name]

    return col


class RIGUI_OT_AddButton(bpy.types.Operator):
    bl_idname = "rigui.add_button"
    bl_label = "Build UI"
    bl_options = {'REGISTER'}

    canvas_collection = bpy.props.StringProperty("collection")
    layout_text = bpy.props.StringProperty("text")
    canvas_object = bpy.props.StringProperty("root object")


    def execute(self, context):
        col = bpy.data.collections[self.canvas_collection]
        bpy.ops.object.mode_set(mode="OBJECT")
        clear_json(self.layout_text)
        if self.canvas_object in bpy.data.objects:
            obj = bpy.data.objects[self.canvas_object]
            bpy.ops.object.select_all(action="DESELECT")
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            bpy.ops.object.scale_clear(clear_delta=False)
        for obj in col.all_objects:
            if obj.type == "MESH":
                button = json_add_button_obj(self.layout_text,
                                             obj, color=obj.color,
                                             bone=obj.rigUI_linked_bone,
                                             offset_obj_key=self.canvas_object,
                                             tab_key="buttons")
        context.scene["rigUI_tag_reload"] = True
        return {'FINISHED'}


class RIGUI_OT_CloseUI(bpy.types.Operator):
    """ Closes RigUI """
    bl_idname = "rigui.ui_close"
    bl_description = "Close RigUI"
    bl_label = "Close UI"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        context.scene.rigUI_active = False
        return {'FINISHED'}


class RIGUI_OT_CreateCanvas(bpy.types.Operator):
    """ Creates a new text datablock, and a new empty collection to put objects in """
    bl_idname = "rigui.create_canvas"
    bl_description = "Create new Canvas"
    bl_label = "New UI canvas"
    bl_options = {'REGISTER', 'UNDO'}

    new_ui_name = bpy.props.StringProperty(name="Layout name", default="RIGUI_Layout")
    new_ui_canvas = bpy.props.StringProperty(name="Canvas Collection", default="Collection")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        text = bpy.data.texts.new(self.new_ui_name)
        canvas = get_collection(self.new_ui_canvas)
        context.scene.rigUI_collection = self.new_ui_canvas
        context.scene.rigUI_build_text_name = self.new_ui_name
        return {'FINISHED'}

