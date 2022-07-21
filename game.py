# ↓↓↓↓↓ IMPORT AREA ↓↓↓↓↓ #
import lib.main as main
from time import sleep
from lib.sprite import Sprite
from lib.sensing import sensing, Key

# ↓↓↓↓↓ SPRITE AREA ↓↓↓↓↓ #
cat = Sprite()


# ↓↓↓↓↓ START AREA ↓↓↓↓↓ #
def start():
    cat.say("Hello!")


# ↓↓↓↓↓ LOOP AREA ↓↓↓↓↓ #
def loop():
    cat.move(10)


