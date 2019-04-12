"""
Shared GPU functions for drawing shapes, collision detections etc.
"""

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import bgl
import mathutils

"""
This file may actually be useless, given that bgl is now mostly deprecated
possibly put custom GL_2D shaders in here for things like outlines / textures etc.
"""
