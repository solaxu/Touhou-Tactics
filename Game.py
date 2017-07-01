# _*_ coding: utf-8 _*_

import pygame
from pygame.locals import *
from sys import exit
from enum import Enum
from SpriteSheet import *
from Team import *
from Character import * 
from Event import *
from Map import *
from LocalInput import *
from pygame.font import *
from GUI import GuiManager

class CGameApp(EventObject):
    
    instance = None

    def __init__(self, name, width, height):
        super(CGameApp, self).__init__()
        self.name = name
        self.screen_w = width
        self.screen_h = height
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), 0, 32)
        self.font = pygame.font.Font("Media/DeliusSwashCaps-Regular.ttf", 12)
        self.clock = pygame.time.Clock()
        self.team_red = None
        self.team_blue = None
        self.level_map = None
        self.cur_team = None
        self.offset_x = 0
        self.offset_y = 0
        self.gui_manager = None

    def create(self):
        self.gui_manager = GuiManager()
        # test character
        hakurei_reimu_sprite_sheet = Sprite_Sheet("Media/walkings/博丽灵梦1.png", 36, 36, 4, 4)
        kirisame_marisa_sprite_sheet = Sprite_Sheet("Media/walkings/雾雨魔理沙1.png", 36, 36, 4, 4)

        self.level_map = PrototypeLevelMap("SLG Prototype")
        self.level_map.create()
        self.team_red = Team(Team_Enum.TEAM_RED, self.level_map)
        self.team_blue = Team(Team_Enum.TEAM_BLUE, self.level_map)
        self.level_map.team_red = self.team_red
        self.level_map.team_blue = self.team_blue

        hakurei_reimu = Character("Hakurei Reimu", hakurei_reimu_sprite_sheet, self.team_red)
        hakurei_reimu.set_picture("Media/characters/博丽灵梦.png")

        kirisame_marisa = Character("Kirisame Marisa", kirisame_marisa_sprite_sheet, self.team_blue)
        kirisame_marisa.set_picture("Media/characters/雾雨魔理沙.png")

        self.team_red.add_character(hakurei_reimu)
        self.team_blue.add_character(kirisame_marisa)

        # set character's positions
        hakurei_reimu.set_pos(288, 288)
        kirisame_marisa.set_pos(288, 396)

        # set current team for test
        self.cur_team = self.team_red

        # register event handlers
        # left mouse
        self.add_handler(EventType.MOUSE_LBTN_DOWN, self.handle_mouse_lbtn_down)
        # arrow keys
        self.add_handler(EventType.SCROLL_MAP, self.handle_scroll_map)
        return

    def select_character_by_mouse(self, mouse_pos):
        character_red = self.team_red.select_character_by_mouse(mouse_pos)
        if character_red is not None:
            return character_red
        else:
            character_blue = self.team_blue.select_character_by_mouse(mouse_pos)
            if character_blue is not None:
                return character_blue
        return None

    def loop(self):
        while True:
            LocalInput.get_instance().event_loop()

            self.screen.fill((0, 0, 0, 0))
            self.update(self.clock.tick())
            self.draw(self.clock.tick())

            pygame.display.update()

    def update(self, et):
        self.process_evt_queue()
        self.level_map.update(et)
        return
    
    def draw(self, et):
        self.level_map.draw(et)
        self.gui_manager.draw(et)
        return
    
    def handle_mouse_lbtn_down(self, evt):
        if self.cur_team is not None:
            self.send_event(self.cur_team, evt)
        return

    def handle_scroll_map(self, evt):
        self.offset_x += evt.offset_x
        self.offset_y += evt.offset_y
        return

    @staticmethod
    def get_instance():
        if CGameApp.instance is None:
            print "Create App Instance"
            CGameApp.instance = CGameApp("A Prototype", 1000, 750)
        return CGameApp.instance
