from sprite import Sprite

# MAKE ALL OF YOUR SPRITES HERE #
default_cat = Sprite()


# PUT ALL YOUR CODE IN HERE #
def start():
    default_cat.say("Hello!")
    default_cat.change_effect("color", 30)


def loop2():
    default_cat.go_to_rand()


