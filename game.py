import time
from sprite import Sprite
from sensing import Key
from sensing import sensing
from mouse import Mouse

# MAKE ALL OF YOUR SPRITES HERE #
default_cat = Sprite(r_rule=Sprite.RotationRule.FREE_Y)


# PUT ALL YOUR CODE IN HERE #
def start():
    default_cat.say("Hello!")
    default_cat.change_effect("color", 30)


def loop2():
    if sensing.key_pressed(Key.RIGHT):
        default_cat.set_rotation(90)
        default_cat.move(5)
    if sensing.key_pressed(Key.LEFT):
        default_cat.set_rotation(270)
        default_cat.move(5)
    if sensing.key_pressed(Key.UP):
        default_cat.set_rotation(180)
        default_cat.move(5)
    if sensing.key_pressed(Key.DOWN):
        default_cat.set_rotation(0)
        default_cat.move(5)
