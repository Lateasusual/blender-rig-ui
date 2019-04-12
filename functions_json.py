"""
JSON text handler functions for saving and loading layouts
"""

import bpy
import json


class JSONReader:

    def get_json_string(self, text_key):
        """ Return a python dict of the text data """
        if text_key in bpy.data.texts:
            return json.loads(bpy.data.texts.get(text_key))
