import bpy

bl_info = {
    "name": "ViewLayer Manager",
    "description": "Create, Rename and Remove view layers without changing currently active view layer",
    "author": "Lateasusual",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "location": "Header -> View Layer",
    "warning": '',  # used for warning icon and text in addons panel
    "wiki_url": "",
    "category": "User Interface"}


class VLM_UL_layers(bpy.types.UIList):

    def draw_item(self,
                  context,
                  layout,
                  data,
                  item,
                  icon: int,
                  active_data,
                  active_property: str,
                  index: int = 0,
                  flt_flag: int = 0):
        self.use_filter_show = True
        split = layout.split(factor=0.80, align=True)
        row = split.row()
        row.alignment = "LEFT"
        row.prop(item, "name", text="", expand=False)
        row.label()
        row = split.row()
        row.alignment = "RIGHT"
        row.operator("scene.remove_view_layer", icon="PANEL_CLOSE", text="")
        row.prop(item, "use", icon="RENDER_STILL", text="")


def disable_collection(col):
    for child in col.children:
        disable_collection(child)
    col.exclude = True



class VLM_OT_remove_view_layer(bpy.types.Operator):
    bl_label = "Remove view layer by index"
    bl_idname = "scene.remove_view_layer"

    def execute(self, context):
        layer = context.scene.view_layers[context.scene.active_view_layer_index]
        context.scene.view_layers.remove(layer)
        return {'FINISHED'}


class VLM_OT_add_blank_layer(bpy.types.Operator):
    bl_label = "Create blank view layer"
    bl_idname = "scene.view_layer_add_blank"

    def execute(self, context):
        layer = context.scene.view_layers.new(context.view_layer.name)
        for c in layer.layer_collection.children:
            disable_collection(c)
        return {'FINISHED'}


def update_active_layer(self, context):
    context.window.view_layer = context.scene.view_layers[context.scene.active_view_layer_index]


class ViewLayerManager(bpy.types.Operator):
    bl_label = "ViewLayer Manager"
    bl_idname = "scene.view_layer_manager"

    view_layer_active = ""

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.template_list("VLM_UL_layers", "", scene, "view_layers", scene, "active_view_layer_index", rows=15)
        layout.operator("scene.view_layer_add_blank", icon="PLUS")

    def execute(self, context):
        wm = context.window_manager
        return wm.invoke_popup(self)  # ,width=500


def icon_button(self, context):
    if context.region.alignment == 'RIGHT':
        self.layout.operator("scene.view_layer_manager", icon="RENDERLAYERS", text="")


classes = [
    VLM_OT_add_blank_layer,
    VLM_OT_remove_view_layer,
    VLM_UL_layers,
    ViewLayerManager,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.active_view_layer_index = bpy.props.IntProperty(default=0, name="Active view layer index",
                                                                    update=update_active_layer)
    bpy.types.TOPBAR_HT_upper_bar.append(icon_button)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)




if __name__ == '__main__':
    register()
