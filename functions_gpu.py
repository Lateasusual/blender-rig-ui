"""
Shared GPU functions for drawing shapes, collision detections etc.
"""

import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import bgl
import mathutils

"""
Here we will put:
    - Drawing only, no shape maths.
    - Draw handlers etc.
"""

def draw_image(context, pos1, pos2, image=None, filepath=""):
    """This is shit, delete it"""
    if image:
        image.gl_load()
    elif filepath:
        try:
            image = bpy.data.images.load(filepath, check_existing=True)
        except:
            print("Image loading error")
            pass

    shader_img = gpu.shader.from_builtin('2D_IMAGE')
    batch_img = batch_for_shader(shader_img, 'TRI_FAN')

    bgl.glEnable(bgl.GL_BLEND)

    try:
        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)

        shader_img.bind()
        shader_img.uniform_int("image", 0)
        batch_img.draw(shader_img)
        return True
    except:
        pass

    bgl.glDisable(bgl.GL_BLEND)

    return False
