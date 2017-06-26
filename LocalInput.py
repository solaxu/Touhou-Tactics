# _*_ coding: utf-8 _*_

# local input, keyboard and mouse

from Event import *
from pygame.locals import*
from sys import exit
import pygame

class LocalInput(EventObject):

    mouse_pos = None
    mouse_rel = None
    mouse_keys = None
    keyboard_keys = None
    instance = None

    @staticmethod
    def get_instance():
        if LocalInput.instance is None:
            LocalInput.instance = LocalInput()
        return LocalInput.instance

    @staticmethod
    def event_loop():
        from Game import CGameApp
        from Map import *
        app = CGameApp.get_instance()
        LocalInput.keyboard = pygame.key.get_pressed()
        LocalInput.mouse_pos = pygame.mouse.get_pos()
        LocalInput.mouse_rel = pygame.mouse.get_rel()
        LocalInput.mouse_keys = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
                    (event.type == pygame.MOUSEMOTION and LocalInput.mouse_keys[0]):
                app.send_event(app.gui_manager, Event_Mouse_LBTN_DOWN(EventType.MOUSE_LBTN_DOWN, LocalInput.mouse_pos))
                if app.level_map.fsm.is_in_state(Map_State_Enum.MAP_SHOW_MINI_MAP):
                    print "Scroll Map by Mouse with Mini-map"
                    # calculate offset
                    if QuadTreeForTile.check_tile(app.level_map.mini_map_pos_x, app.level_map.mini_map_pos_y,
                                                  app.level_map.mini_map_width, app.level_map.mini_map_height,
                                                  LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
                        rect_x = float(app.level_map.mini_map_width) / app.level_map.mini_map_ratio_x
                        rect_y = float(app.level_map.mini_map_height) / app.level_map.mini_map_ratio_y
                        half_x = rect_x / 2
                        half_y = rect_y / 2
                        off_x = float(LocalInput.mouse_pos[0] - app.level_map.mini_map_pos_x - half_x) * app.level_map.mini_map_ratio_x
                        off_y = float(LocalInput.mouse_pos[1] - app.level_map.mini_map_pos_y - half_y) * app.level_map.mini_map_ratio_y
                        app.offset_x = -off_x
                        app.offset_y = -off_y
                        LocalInput.get_instance().send_event(app, Event_Roll_Map(EventType.SCROLL_MAP,
                                                        0, 0))
                else:
                    LocalInput.get_instance().send_event(app, Event_Mouse_LBTN_DOWN(EventType.MOUSE_LBTN_DOWN,
                                                                           LocalInput.mouse_pos))
            elif event.type == pygame.KEYDOWN and event.key == K_DOWN:
                LocalInput.get_instance().send_event(CGameApp.get_instance(),
                                                     Event_Roll_Map(EventType.SCROLL_MAP,
                                                                           0, -36))
            elif event.type == pygame.KEYDOWN and event.key == K_UP:
                LocalInput.get_instance().send_event(CGameApp.get_instance(),
                                                     Event_Roll_Map(EventType.SCROLL_MAP,
                                                                           0, 36))
            elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
                LocalInput.get_instance().send_event(CGameApp.get_instance(),
                                                     Event_Roll_Map(EventType.SCROLL_MAP,
                                                                           36, 0))
            elif event.type == pygame.KEYDOWN and event.key == K_RIGHT:
                LocalInput.get_instance().send_event(CGameApp.get_instance(),
                                                     Event_Roll_Map(EventType.SCROLL_MAP,
                                                                           -36, 0))
            elif event.type == pygame.KEYDOWN and event.key == K_m:
                LocalInput.get_instance().send_event(CGameApp.get_instance().level_map,
                                                     Event_Switch_MiniMap(EventType.SWITCH_MINI_MAP))
            elif LocalInput.mouse_rel[0] != 0 or LocalInput.mouse_rel[1] != 0:
                app.send_event(app.gui_manager, Event_Mouse_Hover(EventType.MOUSE_HOVER, LocalInput.mouse_pos))

