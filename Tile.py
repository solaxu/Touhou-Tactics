# _*_ coding: utf-8 _*_

import pygame
from SpriteSheet import *
from enum import Enum
from Game import *

class MapTile(object):

    def __init__(self, img, width, height, is_occupy):
        self.width = width
        self.height = height
        self.img = img
        self.pos_x = 0
        self.pos_y = 0
        
        # color
        self.color = None

        # for path finding
        self.occupy = False
        # for A* algorithm
        self.H = 0
        self.G = 0
        self.parent_tile = None
        self.in_close_list = False
        self.in_open_list = False
        # for travel map
        self.vis = False
        self.occupy = is_occupy

        # for quad tree, do not used now. check quad tree (in Map.py) for details
        self.marked = False

        # tile advantage, not use now
        # ...

    # compare for path finding
    def __cmp__(self, other):
        return self.H + self.G > other.H + other.G

    def reset(self):
        self.color = None
        # for A* algorithm
        self.H = 0
        self.G = 0
        self.parent_tile = None
        self.in_close_list = False
        self.in_open_list = False
        # for travel map
        self.marked = False

    def set_occupy(self, is_occupy):
        self.occupy = is_occupy

    def change_img(self, img):
        self.img = img

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def draw(self, et):
        from Game import CGameApp
        app = CGameApp.get_instance()
        x = self.pos_x + app.offset_x
        y = self.pos_y + app.offset_y
        app.screen.blit(self.img, ((x, y), (self.width, self.height)))
        if self.color is not None:
            pygame.draw.rect(CGameApp.get_instance().screen, self.color, (x, y, self.width, self.height), 1)
