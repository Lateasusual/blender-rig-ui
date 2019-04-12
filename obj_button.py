"""
Button object class - Has position, shape, associated operator etc.
Try to keep it as simple as possible

If button shapes are stored offset from origin, doesn't matter since we can use shape for ALL hitreg, and button x/y is
irrelevant... maybe don't even bother with x/y
"""


class RigUIButton:

    def __init__(self):
        """ Button initialisation and attributes here """

        self.x = 0
        self.y = 0
        # etc
