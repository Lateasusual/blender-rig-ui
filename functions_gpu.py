"""
Shared GPU functions for drawing shapes, collision detections etc.
"""

import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from gpu_extras.presets import draw_texture_2d

"""
This file may actually be useless, given that bgl is now mostly deprecated
possibly put custom GL_2D shaders in here for things like outlines / textures etc.
"""


def draw_buffer_backgrounds(verts, indices, colours):
    shader = gpu.shader.from_builtin('2D_SMOOTH_COLOR')
    batch = batch_for_shader(shader, 'TRIS', {"pos": verts, "color": colours}, indices=indices)
    shader.bind()
    batch.draw(shader)


def draw_buffer_outlines(outline_verts=None,
                         indices_all=(
                                 ([0, 1, 2],),
                                 ([0, 1, 2],),
                                 ([0, 1, 2],)
                         ),
                         colours=(
                                 (0.3, 0.3, 0.3, 1),
                                 (0.5, 0.5, 0.8, 1),
                                 (0.8, 0.8, 1.0, 1)
                         )):
    if outline_verts is None:
        outline_verts = [
            [0, 0],
            [1, 0],
            [0, 1]
        ]
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch_default = batch_for_shader(shader, 'LINES', {"pos": outline_verts}, indices=indices_all[0])
    batch_hovered = batch_for_shader(shader, 'LINES', {"pos": outline_verts}, indices=indices_all[1])
    batch_selected = batch_for_shader(shader, 'LINES', {"pos": outline_verts}, indices=indices_all[2])
    shader.bind()

    shader.uniform_float("color", colours[0])
    batch_default.draw(shader)
    shader.uniform_float("color", colours[1])
    batch_hovered.draw(shader)
    shader.uniform_float("color", colours[2])
    batch_selected.draw(shader)


def draw_text(text, position, size=16, color=(1, 1, 1, 1)):
    blf.size(0, size, 72)
    size = blf.dimensions(0, text)

    # centre text on position
    pos_x = position[0] - size[0] / 2
    pos_y = position[1] - size[1] / 2

    blf.position(0, pos_x, pos_y, 0)

    r, g, b, a = color
    blf.color(0, r, g, b, a)
    blf.draw(0, text)


def draw_box(point1, point2, color=(0.4, 0.4, 0.4, 1)):
    w = point2[0]
    h = point2[1]
    x = point1[0]
    y = point1[1]
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
    background_shader.uniform_float("color", color)

    background_batch.draw(background_shader)


def draw_image():
    """
    This is doesn't work for now (black image?) -> Bug with BGL, just doesn't work no matter what unfortunately :(
    """
    w = 500
    h = 500
    x = 0
    y = 0

    filepath = "G:/TEMP/4.png"
    image = bpy.data.images.load(filepath, check_existing=True)
    draw_texture_2d(image.bindcode, (x, y), w, h)


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
