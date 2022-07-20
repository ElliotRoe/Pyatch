import math
import random
import time

import cv2
import numpy as np
import pygame
from enum import Enum
import queue
import imagemodder as imd


from line_path import LinePath


class Sprite(pygame.sprite.Sprite):
    # Free x and y refers free to flip around that axis
    class RotationRule(Enum):
        FREE = 0
        FREE_Y = 1
        FREE_X = 2
        LOCKED = 3

    key_color = (255, 0, 255)

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, image_path="data/sprites/ScratchCat.png", scale=1, rotation_offset=90, x=700 / 2 - 120,
                 y=400 / 2 - 100,
                 r_rule=RotationRule.FREE):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.__scale = scale
        self.__rotation_offset = rotation_offset
        self.__rotation = 0
        self.__rotation_rule = r_rule
        # Pen starts up
        self.__pen_state = False
        self.__pen_size = 1
        # used to store path of sprite so lines can be drawn
        self.__line_path = LinePath()
        # Load the image and prep it for colorkey, and color effects
        # Color key set when sprite is rendered. Idk why it works only there but not here
        temp_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        new_temp_image = np.zeros((temp_image.shape[0], temp_image.shape[1], 3), dtype=np.uint8)
        for i in range(temp_image.shape[0]):
            for j in range(temp_image.shape[1]):
                if temp_image[i][j][3] == 0:
                    new_temp_image[j][i] = self.key_color
                else:
                    new_temp_image[j][i] = (temp_image[i][j][2], temp_image[i][j][1], temp_image[i][j][0])
        self.base_image = pygame.surfarray.make_surface(new_temp_image)
        #self.base_image = pygame.transform.rotate(self.base_image, -1 * self.__rotation_offset)
        self.image = pygame.transform.rotate(self.base_image, 0)

        # Rotates the image to fix the weirdness of pyatch images
        self.imd = imd.ImageArrMod(new_temp_image)
        if scale != 1:
            self.set_scale(self.__scale)
        self.rect = self.image.get_rect()

        self.__exec_set_x(x)
        self.__exec_set_y(y)
        self.__exec_set_rotation(self.__rotation_offset)

        self.__font = pygame.font.SysFont("Arial", 28)
        self.say_bubble = None
        self.__has_say = False
        self.__say_background_color = (255, 255, 255)
        self.__say_text_color = (0, 0, 0)
        self.__say_border_color = (200, 200, 200)

        self.alpha = 255

        self.__screen_width = 700
        self.__screen_height = 400

    def move(self, dist):
        self.__exec_move(dist)
        if self.__pen_state:
            self.__update_cur_line()

    def set_x(self, x):
        if self.__pen_state:
            self.__new_line_seg()
        self.__exec_set_x(x)
        if self.__pen_state:
            self.__update_cur_line()

    def set_y(self, y):
        if self.__pen_state:
            self.__new_line_seg()
        self.__exec_set_y(y)
        if self.__pen_state:
            self.__update_cur_line()

    def change_x(self, x):
        if self.__pen_state:
            self.__new_line_seg()
        self.__exec_change_x(x)
        if self.__pen_state:
            self.__update_cur_line()

    def change_y(self, y):
        if self.__pen_state:
            self.__new_line_seg()
        self.__exec_change_y(y)
        if self.__pen_state:
            self.__update_cur_line()

    def rotate(self, angle):
        self.__exec_rotate(angle)
        if self.__pen_state:
            self.__new_line_seg()

    def set_rotation(self, angle):
        self.__exec_set_rotation(angle)
        if self.__pen_state:
            self.__new_line_seg()

    def point_towards(self, pos):
        self.__exec_point_towards(pos[0], pos[1])
        if self.__pen_state:
            self.__new_line_seg()

    def go_to(self, x, y):
        if self.__pen_state:
            self.__new_line_seg()
        self.__exec_set_x(x)
        self.__exec_set_y(y)
        if self.__pen_state:
            self.__update_cur_line()

    def go_to_rand(self):
        if self.__pen_state:
            self.__new_line_seg()
        self.__exec_go_to_rand()
        if self.__pen_state:
            self.__update_cur_line()

    def __update_cur_line(self):
        self.__line_path.update([self.get_center_x(), self.get_center_y()])

    def __new_line_seg(self):
        self.__line_path.add([[self.get_center_x(), self.get_center_y()], [self.get_center_x(), self.get_center_y()]])

    def get_center_x(self):
        return self.rect.x + self.rect.width / 2

    def get_center_y(self):
        return self.rect.y + self.rect.height / 2

    ## Movement Functions ##

    def __exec_point_towards(self, x, y):
        rel_x = x - self.get_center_x()
        rel_y = y - self.get_center_y()

        angle = math.degrees(math.atan2(-rel_y, rel_x))

        self.__exec_set_rotation(angle + self.__rotation_offset)

    def set_scale(self, scale):
        self.__scale = scale
        size = self.base_image.get_size()
        self.image = pygame.transform.scale(self.base_image, (int(size[0] * self.__scale), int(size[1] * self.__scale)))

    def __exec_set_rotation(self, rotation):
        self.__rotation = rotation
        if self.__rotation_rule == self.RotationRule.FREE:
            self.image = pygame.transform.rotate(self.base_image, self.__rotation + -1 * self.__rotation_offset)
        elif self.__rotation_rule == self.RotationRule.FREE_Y:
            if abs(self.__rotation % 360) - 90 > 90:
                self.image = pygame.transform.flip(self.base_image, True, False)
            else:
                self.image = self.base_image
        elif self.__rotation_rule == self.RotationRule.FREE_X:
            if abs(self.__rotation % 360) > 90:
                self.image = pygame.transform.flip(self.base_image, False, True)
            else:
                self.image = self.base_image

    def set_rotation_rule(self, rule):
        if isinstance(rule, self.RotationRule):
            self.__rotation_rule = rule
        # Refresh sprite rotation so it matches the rule
        self.__exec_set_rotation(self.__rotation)

    def __exec_rotate(self, angle):
        self.__exec_set_rotation(self.__rotation + angle)

    def __exec_set_x(self, x):
        self.rect.x = x

    def __exec_change_x(self, x):
        dist = math.ceil(self.rect.x + x)
        self.__exec_set_x(dist)

    def __exec_set_y(self, y):
        self.rect.y = y

    def __exec_change_y(self, y):
        dist = math.floor(self.rect.y + y)
        self.__exec_set_y(dist)

    def __exec_move(self, dist):
        dist_x = dist * math.sin(math.radians(self.__rotation))
        dist_y = dist * math.cos(math.radians(self.__rotation))
        self.__exec_change_x(dist_x)
        self.__exec_change_y(dist_y)

    def __exec_go_to(self, x, y):
        self.__exec_set_x(x)
        self.__exec_set_y(y)

    def __exec_go_to_rand(self):
        self.__exec_go_to(random.randint(0, self.__screen_width - self.rect.width), random.randint(0, self.__screen_height - self.rect.height))

    ## Pen Functions ##

    def pen_state(self):
        return self.__pen_state

    # Parameter is to preserve compatibility with update method
    def pen_down(self):
        self.__pen_state = True
        self.__new_line_seg()

    # Parameter is to preserve compatibility with update method
    def pen_up(self):
        self.__pen_state = False
        self.__line_path.clear()

    def set_pen_size(self, size):
        self.__pen_size = size

    def pen_size(self):
        return self.__pen_size

    def get_line_path(self):
        return self.__line_path

    ## Looks Functions ##

    # Sets the font of the sprite
    def set_font(self, font):
        self.__font = font

    def has_say(self):
        return self.__has_say

    def say(self, message, seconds=-1, left=False):
        text = self.__font.render(message, True, self.__say_text_color)
        text_rect = text.get_rect()
        text_surface = text_rect.inflate(10, 10)
        self.say_bubble = pygame.Surface(text_surface.size)
        self.say_bubble.fill(self.key_color)
        self.say_bubble.set_colorkey(self.key_color)
        pygame.draw.rect(self.say_bubble, self.__say_background_color, (0, 0, text_surface.w, text_surface.h), border_radius=5)
        pygame.draw.rect(self.say_bubble, self.__say_border_color, (0, 0, text_surface.w, text_surface.h), 3, 5)
        self.say_bubble.blit(text, (text_surface.w / 2 - text_rect.w / 2, text_surface.h / 2 - text_rect.h / 2))
        self.__has_say = True

    def think(self, message, second=-1, left=False):
        self.say(message, second, left)
        self.__set_alpha(20)

    def set_effect(self, effect, value):
        if effect == "ghost":
            self.__set_alpha(value)
        if effect == "color":
            self.imd.restore_image_arr()
            self.__change_hue(value)

    def change_effect(self, effect, value):
        if effect == "ghost":
            self.__alpha += value
            self.__alpha %= 200
            self.__set_alpha(self.__alpha)
        if effect == "color":
            self.__change_hue(value)

    # set alpha of sprite
    def __set_alpha(self, alpha):
        self.__alpha = alpha
        self.image.set_alpha(self.__alpha)

    def __change_hue(self, hue):
        #start = time.time()
        self.imd.hue_shift_image_arr(hue)
        self.image = pygame.surfarray.make_surface(self.imd.get_image_arr())
        self.base_image = self.image
        #self.__exec_set_rotation(self.__rotation)
        #end = time.time()
        #print("Hue shift took: " + str(end - start))

