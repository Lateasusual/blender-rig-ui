"""
JSON text handler functions for saving and loading layouts
TODO Implement validity checker / highlighter for users
"""

import bpy
import json

default_dict = {
    "rig_name": "",
    "buttons": []
}

default_button = {
    "color": (0.5, 0.5, 0.5, 1),
    "verts": ((0, 0), (0, 1), (1, 1), (1, 0)),
    "indices": ((0, 1, 2), (0, 2, 3)),
    "scale": (100, 100),
    "offset": (100, 100)
}


def get_json_dict(text_key):
    """ Return a python dict of the text data """
    if bpy.data.texts.get(text_key) is not None:
        try:
            return json.loads(bpy.data.texts.get(text_key).as_string())
        except Exception:
            print("Error parsing JSON, check syntax")
    else:
        return None


def write_json(dict, text_key):
    text = bpy.data.texts[text_key]
    text.clear()
    text.write(json.dumps(dict))


def build_dict_buttons(buttons, dictionary=None):
    if dictionary is None:
        dictionary = default_dict
    for button in buttons:
        dictionary["buttons"].append(button.to_dict())
    return dictionary
