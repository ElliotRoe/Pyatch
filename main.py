import threading

import pygame

from pyatch_group import PyatchGroup
import sprite

# Define some colors


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# init sprite font
font = pygame.font.Font('data/fonts/arial.ttf', 20)


from sensing import sensing

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

screen.set_colorkey(sprite.Sprite.key_color)

sprite_list = PyatchGroup()

## INIT ##
import game

members = list(vars(game).keys())
loop_list = []
loop_keyword = 'loop'
for m in members:
    temp = getattr(game, m)
    if callable(temp) and loop_keyword in m:
        #print(temp)
        loop_list.append(temp)
    if isinstance(temp, sprite.Sprite):
        sprite_list.add(temp)
## INIT ##


# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

init_thread = threading.Thread(target=game.start)
init_thread.start()
loop_thread = threading.Thread()
while not sensing.done:
    sensing.parse_events(pygame.event.get())
    screen.fill(WHITE)

    ## LOOP ##

    for loop in loop_list:
        loop()

    ## LOOP ##

    for sprite in sprite_list.sprites():
        for line in sprite.get_line_path():
            pygame.draw.lines(screen, (0, 0, 0), False, line, sprite.pen_size())
    sprite_list.draw(screen)
    sprite_list.update()
    pygame.display.flip()
    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
