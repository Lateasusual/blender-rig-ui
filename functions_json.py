"""
JSON text handler functions for saving and loading layouts
TODO set use_mesh_shapes so we can pack the JSON without everything else
"""

import bpy
import json
from . obj_button import RigUIButton

default_dict = {
    "rig_name": "",
    "use_mesh_shapes": True,
    "buttons": []
}

default_button = {
    "color": (0.5, 0.5, 0.5, 1),
    "verts": ((0, 0), (0, 1), (1, 1), (1, 0)),
    "indices": ((0, 1, 2), (0, 2, 3)),
    "scale": (100, 100),
    "offset": (100, 100)
}


def get_json_dict(text_key, create_new=False):
    """ Return a python dict of the text data """
    if text_key in bpy.data.texts:
        try:
            return json.loads(bpy.data.texts.get(text_key).as_string())
        except Exception:
            print("Error parsing JSON, check syntax")
    elif create_new:
        bpy.data.texts.new(text_key)
        clear_json(text_key)
        return get_json_dict(text_key)
    else:
        return None


def write_json(dict, text_key):
    text = bpy.data.texts[text_key]
    text.clear()
    text.write(json.dumps(dict))  # No need to be neat


def clear_json(text_key):
    if text_key not in bpy.data.texts:
        bpy.data.texts.new(text_key)
    text = bpy.data.texts[text_key]
    text.clear()
    text.write(json.dumps(default_dict))


def json_add_button_obj(text_key, shape_obj, color=(0.5, 0.5, 1, 1), bone="Bone"):
    """
     convert object properties to button properties
     TODO - Add object properties as arguments
     E.G:
        - Object colour
        - Object scale / rotation (?)
        - Bone to link / Operator (add ops later, just bones for now)
        - Whether to load shape from object or not...
        - Support for looping through all objects in collection etc.
     """
    dictionary = get_json_dict(text_key)
    button = RigUIButton()
    """ Set button properties from object data here """
    button.set_color(color)
    button.set_linked_bone(bone)
    button.load_shape_from_obj(shape_obj.name)
    button.set_use_shape(False)


    dictionary["buttons"].append(button.to_dict())
    write_json(dictionary, text_key)
    return button  # just in case we want to keep it

