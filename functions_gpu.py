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


def draw_image():
    """
    This is doesn't work for now (black image?)
    Must be called inside a draw call context to work
    """
    w = 500
    h = 500
    x = 0
    y = 0

    img_verts = (
        (x, y),
        (x, h),
        (w, h),
        (w, y)
    )
    filepath = "C:/Users/Christopher/AppData/Roaming/Blender Foundation/" \
               "Blender/2.80/scripts/addons/blender-rig-ui/img/test.jpg"
    image = bpy.data.images.load(filepath, check_existing=True)

    bgl.glActiveTexture(bgl.GL_TEXTURE0)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)

    img_shader = gpu.shader.from_builtin('2D_IMAGE')
    img_batch = batch_for_shader(img_shader, 'TRI_FAN',
                                 {"pos": img_verts,
                                  "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)),
                                  "image": image}, )
    img_shader.bind()
    img_shader.uniform_int("image", 0)
    img_batch.draw(img_shader)


def draw_background(context):
    w = context.area.width
    h = context.area.height
    space = context.area.spaces[0]
    x = 0
    y = 0
    background_verts = (
        (x, y),
        (x, h),
        (w, h),
        (w, y)
    )

    background_indices = ((0, 1, 2), (0, 2, 3))
    background_shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    background_batch = batch_for_shader(background_shader, 'TRIS',
                                        {"pos": background_verts}, indices=background_indices)
    background_shader.bind()
    background_shader.uniform_float("color", (0.2, 0.2, 0.2, 1))

    background_batch.draw(background_shader)