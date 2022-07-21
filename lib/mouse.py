import pygame


class Mouse:

    @staticmethod
    def is_l_mouse_down():
        return pygame.mouse.get_pressed()[0] == 1

    @staticmethod
    def is_m_mouse_down():
        return pygame.mouse.get_pressed()[1] == 1

    @staticmethod
    def is_r_mouse_down():
        return pygame.mouse.get_pressed()[2] == 1

    @staticmethod
    def mouse_x():
        return pygame.mouse.get_pos()[0]

    @staticmethod
    def mouse_y():
        return pygame.mouse.get_pos()[1]



