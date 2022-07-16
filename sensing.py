import pygame


class Key:
    A = pygame.K_a
    B = pygame.K_b
    C = pygame.K_c
    D = pygame.K_d
    E = pygame.K_e
    F = pygame.K_f
    G = pygame.K_g
    H = pygame.K_h
    I = pygame.K_i
    J = pygame.K_j
    K = pygame.K_k
    L = pygame.K_l
    M = pygame.K_m
    N = pygame.K_n
    O = pygame.K_o
    P = pygame.K_p
    Q = pygame.K_q
    R = pygame.K_r
    S = pygame.K_s
    T = pygame.K_t
    U = pygame.K_u
    V = pygame.K_v
    W = pygame.K_w
    Y = pygame.K_y
    X = pygame.K_x
    Z = pygame.K_z
    N0 = pygame.K_0
    N1 = pygame.K_1
    N2 = pygame.K_2
    N3 = pygame.K_3
    N4 = pygame.K_4
    N5 = pygame.K_5
    N6 = pygame.K_6
    N7 = pygame.K_7
    N8 = pygame.K_8
    N9 = pygame.K_9
    SPACE = pygame.K_SPACE
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT


class Sensing:

    def __init__(self):
        self.__t_edge = False
        self.__t_mouse_p = False
        self.__down_keys = {}
        self.done = False

    def parse_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print('go forward')
                if event.key == pygame.K_s:
                    print('go backward')
                self.__down_keys[event.key] = 1
            if event.type == pygame.KEYUP:
                self.__down_keys[event.key] = 0
            if event.type == pygame.QUIT:
                self.done = True
        #print (self.__down_keys)

    def key_pressed(self, key):
        return self.__down_keys.get(key, 0) == 1


sensing = Sensing()
