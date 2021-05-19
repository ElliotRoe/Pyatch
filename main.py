import threading

import pygame

from pen_group import PenGroup
from sprite import Sprite

# Define some colors


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

pen_list = pygame.sprite.Group()
sprite_list = PenGroup(pen_list)
## INIT ##

import game
members = list(vars(game).keys())
for m in members:
    temp = getattr(game, m)
    if isinstance(temp, Sprite):
        sprite_list.add(temp)
## INIT ##


# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

init_thread = threading.Thread(target=game.main)
init_thread.start()
loop_thread = threading.Thread()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print('go forward')
            if event.key == pygame.K_s:
                print('go backward')
        if event.type == pygame.QUIT:
            done = True
    screen.fill(WHITE)

    ## LOOP ##

    #game.loop()

    ## LOOP ##

    pen_list.draw(screen)
    sprite_list.draw(screen)
    sprite_list.update()
    pygame.display.flip()
    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
