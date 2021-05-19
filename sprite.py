import math
import pygame
from enum import Enum
import queue


class Sprite(pygame.sprite.Sprite):
    # Free x and y refers free to flip around that axis
    class RotationRule(Enum):
        FREE = 0
        FREE_Y = 1
        FREE_X = 2
        LOCKED = 3

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, image_path="data/ScratchCat.png", scale=1, rotation_offset=90, x=700/2 - 120, y=400/2 - 100, r_rule=RotationRule.FREE):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.__scale = scale
        self.__rotation_offset = rotation_offset
        self.__rotation = 0
        self.__rotation_rule = r_rule
        # Pen starts up
        self.__pen_state = False
        self.__pen_size = 1
        # Each instruct must follow the format: (String name, int args**)
        self.__intruct_queue = queue.Queue()
        # Basically keeps track of the front queue
        self.__current_instruct = None
        self.__move_speed = 5
        self.__rotate_speed = 10
        self.__scale_speed = 1
        self.orig_image = pygame.image.load(image_path)
        self.orig_image = pygame.transform.rotate(self.orig_image, -1 * self.__rotation_offset)
        self.image = pygame.transform.rotate(self.orig_image, 0)
        if scale != 1:
            self.__exec_set_scale(self.__scale)
        self.rect = self.image.get_rect()

        self.__exec_set_x(x)
        self.__exec_set_y(y)
        self.__exec_set_rotation(self.__rotation_offset)

    # Executes each coinciding function in the queue until there are no instructions in queue left
    def update(self, *args, **kwargs):
        if self.__intruct_queue.qsize() > 0 or self.__current_instruct is not None:
            if self.__current_instruct is None:
                self.__current_instruct = self.__intruct_queue.get()
            if self.__current_instruct[1] > self.__current_instruct[2]:
                getattr(self, '_Sprite__exec_' + self.__current_instruct[0])(self.__current_instruct[2])
                self.__current_instruct[1] = self.__current_instruct[1] - self.__current_instruct[2]
            else:
                getattr(self, '_Sprite__exec_' + self.__current_instruct[0])(self.__current_instruct[1])
                self.__current_instruct = None



    def move(self, dist):
        self.__intruct_queue.put(['move', dist, self.__move_speed])

    def set_x(self, x):
        self.__intruct_queue.put(['set_x', x, x])

    def set_y(self, y):
        self.__intruct_queue.put(['set_y', y, y])

    def rotate(self, angle):
        self.__intruct_queue.put(['rotate', angle, self.__rotate_speed])

    def set_rotation(self, angle):
        self.__intruct_queue.put(['set_rotation', angle, angle])

    def pen_down(self):
        self.__intruct_queue.put(['pen_down', 1, 1])

    def pen_up(self):
        self.__intruct_queue.put(['pen_up', 1, 1])

    def set_pen_size(self, size):
        self.__intruct_queue.put(['set_pen_size', size, size])

    def set_scale(self, scale):
        self.__intruct_queue.put(['set_scale', scale, scale])

    def set_move_speed(self, speed):
        self.__intruct_queue.put(['set_move_speed', speed, speed])

    def point_towards(self, x, y):
        rel_x = x - self.rect.x
        rel_y = y - self.rect.y

        angle = math.degrees(math.atan2(-rel_y, rel_x))

        self.set_rotation(angle + self.__rotation_offset)

    def __exec_set_scale(self, scale):
        self.__scale = scale
        size = self.orig_image.get_size()
        self.image = pygame.transform.scale(self.orig_image, (int(size[0] * self.__scale), int(size[1] * self.__scale)))

    def __exec_set_rotation(self, rotation):
        self.__rotation = rotation
        if self.__rotation_rule == self.RotationRule.FREE:
            self.image = pygame.transform.rotate(self.orig_image, self.__rotation)
        elif self.__rotation_rule == self.RotationRule.FREE_Y:
            if abs(self.__rotation % 360) - 90 > 90:
                self.image = pygame.transform.flip(self.orig_image, True, False)
            else:
                self.image = self.orig_image
        elif self.__rotation_rule == self.RotationRule.FREE_X:
            if abs(self.__rotation % 360) > 90:
                self.image = pygame.transform.flip(self.orig_image, False, True)
            else:
                self.image = self.orig_image

    def __exec_set_rotation_rule(self, rule):
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

    def pen_state(self):
        return self.__pen_state

    # Parameter is to preserve compatibility with update method
    def __exec_pen_down(self, dummy):
        self.__pen_state = True

    # Parameter is to preserve compatibility with update method
    def __exec_pen_up(self, dummy):
        self.__pen_state = False

    def __exec_set_pen_size(self, size):
        self.__pen_size = size

    def pen_size(self):
        return self.__pen_size

    def __exec_set_move_speed(self, speed):
        self.__move_speed = speed


