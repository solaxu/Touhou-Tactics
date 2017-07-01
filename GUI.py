# _*_ coding: utf-8 _*_

import pygame
import Queue
from Event import *


class Gui_Enum(Enum):

    WND_BORDER_WIDTH = 2
    Character_Plane = 10000
    Character_Control_Menu = 10001

class GuiElement(EventObject):

    def __init__(self, name, x, y, w, h, color, alpha, parent):
        super(GuiElement, self).__init__()
        self.name = name
        self.parent = parent
        self.show = True
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.alpha = alpha
        self.surface = pygame.Surface([w, h])
        self.surface.fill(color)
        self.surface.set_alpha(alpha)
        self.text_surface = None

    def set_background_surface(self, surface):
        self.surface = surface

    def set_text(self, text, color):
        from Game import CGameApp
        app = CGameApp.get_instance()
        self.text_surface = app.font.render(text, False, color)


class GuiPicture(EventObject):

    def __init__(self, name, x, y, w, h, parent):
        super(GuiPicture, self).__init__()
        self.parent = parent
        self.name = name
        self.show = True
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.surface = None

    def set_picture(self, pic):
        self.surface = pic

    def draw(self, et):
        from Game import CGameApp
        app = CGameApp.get_instance()
        if self.surface is not None:
            app.screen.blit(self.surface, ((self.x, self.y), (self.w, self.h)))
        self.process_evt_queue()


class GuiLabel(GuiElement):

    def __init__(self, name, x, y, w, h, color, alpha, text, text_color, parent):
        super(GuiLabel, self).__init__(name, x, y, w, h, color, alpha, parent)
        from Game import CGameApp
        app = CGameApp.get_instance()
        self.text_surface = app.font.render(text, False, text_color)

    def draw(self, et):
        from Game import CGameApp
        app = CGameApp.get_instance()
        app.screen.blit(self.surface, ((self.x, self.y), (self.w, self.h)))
        text_w = self.text_surface.get_width()
        text_h = self.text_surface.get_height()
        off_x = (self.w - text_w) / 2
        off_y = (self.h - text_h) / 2
        app.screen.blit(self.text_surface, ((self.x + off_x, self.y + off_y), (text_w, text_h)))

        self.process_evt_queue()


class GuiButton(GuiElement):

    def __init__(self, name, x, y, w, h, color, alpha, text, text_color, parent):
        super(GuiButton, self).__init__(name, x, y, w, h, color, alpha, parent)
        from Game import CGameApp
        app = CGameApp.get_instance()
        self.text_surface = app.font.render(text, False, text_color)

        # register handlers
        self.add_handler(EventType.MOUSE_LBTN_DOWN, self.handle_click)

    def draw(self, et):
        from Game import CGameApp
        app = CGameApp.get_instance()
        app.screen.blit(self.surface, ((self.x, self.y), (self.w, self.h)))
        text_w = self.text_surface.get_width()
        text_h = self.text_surface.get_height()
        off_x = (self.w - text_w) / 2
        off_y = (self.h - text_h) / 2
        app.screen.blit(self.text_surface, ((self.x + off_x, self.y + off_y), (text_w, text_h)))
        from LocalInput import LocalInput
        from Map import QuadTreeForTile
        if QuadTreeForTile.check_tile(self.x, self.y, self.w, self.h, LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
            pygame.draw.rect(app.screen, (0, 255, 0), (self.x, self.y, self.w, self.h), Gui_Enum.WND_BORDER_WIDTH.value)
        self.process_evt_queue()

    def handle_click(self, evt):
        print str(self.name) + " Button Pressed"
        from Game import CGameApp
        app = CGameApp.get_instance()
        pygame.draw.rect(app.screen, (0, 0, 255), (self.x, self.y, self.w, self.h), 1)
        self.send_event(self.parent, Event_Gui_Btn_Pressed(EventType.GUI_BTN_PRESSED, self.name))
        return


class GuiWindow(EventObject):

    def __init__(self, name, x, y, w, h):
        super(GuiWindow, self).__init__()
        self.widgets = {}
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name
        self.show = True
        self.surface = pygame.Surface([w, h])
        self.surface.fill((0, 0, 0))
        self.widget_handlers = {}

        # register handlers
        self.add_handler(EventType.GUI_BTN_PRESSED, self.handle_gui_button_down)
        self.add_handler(EventType.GUI_MOUSE_HOVER, self.handle_gui_mouse_hover)

    def add_widget(self, widget):
        self.widgets[widget.name] = widget
        widget.parent = self
        return widget

    def del_widget(self, name):
        del self.widgets[name]

    def add_widget_handlers(self, name, handler):
        self.widget_handlers[name] = handler

    def handle_gui_button_down(self, evt):
        self.widget_handlers[evt.name]()
        return

    def handle_gui_mouse_hover(self, evt):
        self.widget_handlers[evt.name]()
        return

    def get_widget_by_mouse(self, mouse_pos):
        from Map import QuadTreeForTile
        for (name, widget) in self.widgets.items():
            if QuadTreeForTile.check_tile(widget.x, widget.y, widget.w, widget.h, mouse_pos[0], mouse_pos[1], 0, 0):
                return widget
        return None

    def draw(self, et):
        if not self.show:
            return
        self.process_evt_queue()
        from Game import CGameApp
        app = CGameApp.get_instance()
        app.screen.blit(self.surface, ((self.x, self.y), (self.w, self.h)))
        for (name, widget) in self.widgets.items():
            if widget.show:
                widget.draw(et)
        pygame.draw.rect(app.screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 2)


class GuiManager(EventObject):

    def __init__(self):
        super(GuiManager, self).__init__()
        self.gui_wnds = {}
        # register handlers
        self.add_handler(EventType.MOUSE_LBTN_DOWN, self.handle_mouse_lbtn_down)
        self.add_handler(EventType.MOUSE_HOVER, self.handle_mouse_hover)
        self.add_handler(EventType.SHOW_CHARACTER_MENU, self.handle_show_character_menu)
        self.add_handler(EventType.CLOSE_CHARACTER_MENU, self.handle_close_character_menu)
        # gui windows
        character_plane = Character_Plane()
        self.gui_wnds[character_plane.name] = character_plane
        character_menu = Character_Control_Menu()
        self.gui_wnds[character_menu.name] = character_menu

    def get_wnd_by_mouse(self, mouse_pos):
        from Map import QuadTreeForTile
        for (name, wnd) in self.gui_wnds.items():
            if QuadTreeForTile.check_tile(wnd.x, wnd.y, wnd.w, wnd.h, mouse_pos[0], mouse_pos[1], 0, 0):
                return wnd
        return None

    def draw(self, et):
        self.process_evt_queue()
        for (name, wnd) in self.gui_wnds.items():
            if wnd.show:
                wnd.draw(et)

    def handle_mouse_lbtn_down(self, evt):
        wnd = self.get_wnd_by_mouse(evt.mouse_pos)
        if wnd is not None and wnd.show:
            widget = wnd.get_widget_by_mouse(evt.mouse_pos)
            if widget is not None and widget.show:
                self.send_event(widget, Event_Mouse_LBTN_DOWN(EventType.MOUSE_LBTN_DOWN, evt.mouse_pos))
        return

    def handle_mouse_hover(self, evt):
        wnd = self.get_wnd_by_mouse(evt.mouse_pos)
        if wnd is not None and wnd.show:
            widget = wnd.get_widget_by_mouse(evt.mouse_pos)
            if widget is not None and widget.show:
                self.send_event(widget, Event_Mouse_Hover(EventType.MOUSE_HOVER, evt.mouse_pos))
        return

    def handle_show_character_menu(self, evt):
        from Game import CGameApp
        app = CGameApp.get_instance()
        if evt.character is not None:
            self.gui_wnds[Gui_Enum.Character_Plane].link_to_character(evt.character)
            if evt.character.team.name == app.cur_team.name:
                x = evt.character.pos_x + 18
                y = evt.character.pos_y + 18
                self.gui_wnds[Gui_Enum.Character_Control_Menu].set_pos(x, y)
                self.gui_wnds[Gui_Enum.Character_Control_Menu].show = True
        return

    def handle_close_character_menu(self, evt):
        #from Game import CGameApp
        #cur_team = CGameApp.get_instance().cur_team
        #if cur_team is not None and cur_team.character_selected is not None:
        self.gui_wnds[Gui_Enum.Character_Control_Menu].show = False
        return


#######################################################################################################################
# concrete ui

# character plane
class Character_Plane_Enum(Enum):

    WIDTH = 150
    HEIGHT = 325
    PROP_HEIGHT = 25
    #
    Character_Pic = 0
    Character_Name = 1
    Character_Level = 2
    Character_HP = 3
    Character_MP = 4
    Character_AP = 5
    Character_EXP = 6
    Character_AGI = 7
    Character_STR = 8
    Character_INT = 9
    Character_DEF = 10
    Character_RES = 11
    Character_ATK_RNG = 12
    Character_ATK = 13


class Character_Plane(GuiWindow):
    
    def __init__(self):
        super(Character_Plane, self).__init__(Gui_Enum.Character_Plane, 0, 0,
                                              Character_Plane_Enum.WIDTH.value,
                                              Character_Plane_Enum.HEIGHT.value)

        self.character_pic = self.add_widget(GuiPicture(Character_Plane_Enum.Character_Pic, self.x, self.y,
                                                    Character_Plane_Enum.WIDTH.value,
                                                    Character_Plane_Enum.WIDTH.value, self))

        self.character_name = self.add_widget(GuiLabel(Character_Plane_Enum.Character_Name,
                                                      self.x, self.character_pic.y + self.character_pic.h,
                                                      Character_Plane_Enum.WIDTH.value,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "???", (255, 255, 255), self))

        self.character_lvl = self.add_widget(GuiLabel(Character_Plane_Enum.Character_Level,
                                                     self.x,
                                                     self.character_name.y + self.character_name.h,
                                                     Character_Plane_Enum.WIDTH.value / 2,
                                                     Character_Plane_Enum.PROP_HEIGHT.value,
                                                     (0, 0, 0), 255, "LV:", (255, 255, 255), self))

        self.character_ap = self.add_widget(GuiLabel(Character_Plane_Enum.Character_AP,
                                                     self.x + self.character_lvl.w,
                                                     self.character_name.y + self.character_name.h,
                                                     Character_Plane_Enum.WIDTH.value / 2,
                                                     Character_Plane_Enum.PROP_HEIGHT.value,
                                                     (0, 0, 0), 255, "AP:", (255, 255, 255), self))

        self.character_hp = self.add_widget(GuiLabel(Character_Plane_Enum.Character_HP,
                                                     self.x,
                                                     self.character_lvl.y + self.character_lvl.h,
                                                     Character_Plane_Enum.WIDTH.value / 2,
                                                     Character_Plane_Enum.PROP_HEIGHT.value,
                                                     (0, 0, 0), 255, "HP:", (255, 255, 255), self))

        self.character_mp = self.add_widget(GuiLabel(Character_Plane_Enum.Character_MP,
                                                     self.x + self.character_hp.w,
                                                     self.character_lvl.y + self.character_lvl.h,
                                                     Character_Plane_Enum.WIDTH.value / 2,
                                                     Character_Plane_Enum.PROP_HEIGHT.value,
                                                     (0, 0, 0), 255, "MP:", (255, 255, 255), self))

        self.character_atk = self.add_widget(GuiLabel(Character_Plane_Enum.Character_ATK,
                                                      self.x,
                                                      self.character_hp.y + self.character_hp.h,
                                                      Character_Plane_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "ATK:", (255, 255, 255), self))

        self.character_atk_rng = self.add_widget(GuiLabel(Character_Plane_Enum.Character_ATK_RNG,
                                                          self.x + self.character_atk.w,
                                                          self.character_hp.y + self.character_hp.h,
                                                          Character_Plane_Enum.WIDTH.value / 2,
                                                          Character_Plane_Enum.PROP_HEIGHT.value,
                                                          (0, 0, 0), 255, "RNG:", (255, 255, 255), self))

        self.character_def = self.add_widget(GuiLabel(Character_Plane_Enum.Character_DEF,
                                                      self.x,
                                                      self.character_atk.y + self.character_atk.h,
                                                      Character_Plane_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "DEF:", (255, 255, 255), self))

        self.character_res = self.add_widget(GuiLabel(Character_Plane_Enum.Character_RES,
                                                      self.x + self.character_atk.w,
                                                      self.character_atk.y + self.character_atk.h,
                                                      Character_Plane_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "RES:", (255, 255, 255), self))

        self.character_str = self.add_widget(GuiLabel(Character_Plane_Enum.Character_STR,
                                                      self.x,
                                                      self.character_def.y + self.character_def.h,
                                                      Character_Plane_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "STR:", (255, 255, 255), self))

        self.character_agi = self.add_widget(GuiLabel(Character_Plane_Enum.Character_AGI,
                                                      self.x + self.character_def.w,
                                                      self.character_def.y + self.character_def.h,
                                                      Character_Plane_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "AGI:", (255, 255, 255), self))

        self.character_int = self.add_widget(GuiLabel(Character_Plane_Enum.Character_INT,
                                                      self.x,
                                                      self.character_str.y + self.character_str.h,
                                                      Character_Plane_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "INT:", (255, 255, 255), self))

        self.character_exp = self.add_widget(GuiLabel(Character_Plane_Enum.Character_EXP,
                                                      self.x + self.character_str.w,
                                                      self.character_str.y + self.character_str.h,
                                                      Character_Plane_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "EXP:", (255, 255, 255), self))

    def link_to_character(self, character):
        if character is None:
            self.character_name.set_text("???", (255, 255, 255))
            self.character_pic.set_picture(character.sprite)
            self.character_lvl.set_text("LV:", (255, 255, 255))
            self.character_str.set_text("STR:", (255, 255, 255))
            self.character_agi.set_text("AGI:", (255, 255, 255))
            self.character_int.set_text("INT:", (255, 255, 255))
            self.character_atk.set_text("ATK:", (255, 255, 255))
            self.character_atk_rng.set_text("RNG:", (255, 255, 255))
            self.character_def.set_text("DEF:", (255, 255, 255))
            self.character_res.set_text("RES:", (255, 255, 255))
            self.character_exp.set_text("EXP:", (255, 255, 255))
            self.character_ap.set_text("AP:", (255, 255, 255))
            self.character_hp.set_text("HP:", (255, 255, 255))
            self.character_mp.set_text("MP:", (255, 255, 255))
        else:
            self.character_name.set_text(character.name, (255, 255, 255))
            self.character_pic.set_picture(character.sprite)
            self.character_lvl.set_text("LV: " + str(character.lvl), (255, 255, 255))
            self.character_str.set_text("STR: " + str(character.strength), (255, 255, 255))
            self.character_agi.set_text("AGI: " + str(character.agility), (255, 255, 255))
            self.character_int.set_text("INT: " + str(character.intelligence), (255, 255, 255))
            self.character_atk.set_text("ATK: " + str(character.attack), (255, 255, 255))
            self.character_atk_rng.set_text("RNG: " + str(character.attack_range), (255, 255, 255))
            self.character_def.set_text("DEF: " + str(character.defense), (255, 255, 255))
            self.character_res.set_text("RES: " + str(character.resistance), (255, 255, 255))
            self.character_exp.set_text("EXP: " + str(character.exp), (255, 255, 255))
            self.character_ap.set_text("AP: " + str(character.ap), (255, 255, 255))
            self.character_hp.set_text("HP: " + str(character.hp), (255, 255, 255))
            self.character_mp.set_text("MP: " + str(character.mp), (255, 255, 255))

# character controller menu
# Commands: Move, Attack, Items, Skills
class Character_Control_Enum(Enum):

    MOVE_BTN = 0
    ATTACK_BTN = 1
    ITEM_BTN = 2
    SKILL_BTN = 3
    SLOT_HEIGHT = 25
    WIDTH = 75
    HEIGHT = 104


class Character_Control_Menu(GuiWindow):

    def __init__(self):
        super(Character_Control_Menu, self).__init__(Gui_Enum.Character_Control_Menu, 300, 0,
                                                     Character_Control_Enum.WIDTH.value,
                                                     Character_Control_Enum.HEIGHT.value)

        self.show = False

        self.move_btn = self.add_widget(GuiButton(Character_Control_Enum.MOVE_BTN, 300, 2,
                                                  Character_Control_Enum.WIDTH.value,
                                                  Character_Control_Enum.SLOT_HEIGHT.value,
                                                  (0, 0, 0), 255, "Move", (255, 255, 255), self))

        self.attack_btn = self.add_widget(GuiButton(Character_Control_Enum.ATTACK_BTN, 300,
                                                  self.move_btn.y + self.move_btn.h,
                                                  Character_Control_Enum.WIDTH.value,
                                                  Character_Control_Enum.SLOT_HEIGHT.value,
                                                  (0, 0, 0), 255, "Attack", (255, 255, 255), self))

        self.item_btn = self.add_widget(GuiButton(Character_Control_Enum.ITEM_BTN, 300,
                                                  self.attack_btn.y + self.attack_btn.h,
                                                  Character_Control_Enum.WIDTH.value,
                                                  Character_Control_Enum.SLOT_HEIGHT.value,
                                                  (0, 0, 0), 255, "Item", (255, 255, 255), self))

        self.skill_btn = self.add_widget(GuiButton(Character_Control_Enum.SKILL_BTN, 300,
                                                  self.item_btn.y + self.item_btn.h,
                                                  Character_Control_Enum.WIDTH.value,
                                                  Character_Control_Enum.SLOT_HEIGHT.value,
                                                  (0, 0, 0), 255, "Skill", (255, 255, 255), self))

        # new handlers
        self.add_widget_handlers(Character_Control_Enum.MOVE_BTN, self.handle_move_btn)
        self.add_widget_handlers(Character_Control_Enum.ATTACK_BTN, self.handle_attack_btn)

    def handle_move_btn(self):
        print "Handle Move Btn"
        from Game import CGameApp
        app = CGameApp.get_instance()
        self.send_event(app.cur_team.character_selected, Event(EventType.CHARACTER_MOVE_CMD))
        self.send_event(app.gui_manager, Event(EventType.CLOSE_CHARACTER_MENU))
        tile = app.level_map.get_tile_by_coord(app.cur_team.character_selected.pos_x, app.cur_team.character_selected.pos_y)
        app.level_map.bfs_travel(tile, (0, 0, 255, 196), app.cur_team.character_selected.ap)

    def handle_attack_btn(self):
        print "Handle Attack Btn"
        from Game import CGameApp
        app = CGameApp.get_instance()
        self.send_event(app.cur_team.character_selected, Event(EventType.CHARACTER_ATTACK_CMD))
        self.send_event(app.gui_manager, Event(EventType.CLOSE_CHARACTER_MENU))
        tile = app.level_map.get_tile_by_coord(app.cur_team.character_selected.pos_x,
                                               app.cur_team.character_selected.pos_y)
        app.level_map.bfs_travel(tile, (255, 0, 0, 196), app.cur_team.character_selected.attack_range)

    def set_pos(self, x, y):
        off_x = x - self.x
        off_y = y - self.y

        self.x += off_x
        self.y += off_y

        for (name, widget) in self.widgets.items():
            widget.x += off_x
            widget.y += off_y
            
    def draw(self, et):
        super(Character_Control_Menu, self).draw(et)