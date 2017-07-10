# _*_ coding: utf-8 _*_

import pygame
import Queue
from Event import *
from Skill import *


class Gui_Enum(Enum):

    WND_BORDER_WIDTH = 2
    Character_Plane = 10000
    Character_Control_Menu = 10001
    Character_Skill_Item_Menu = 10002
    Character_Ban_Pick = 10003

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
        self.color = color
        self.alpha = alpha
        self.surface = pygame.Surface([w, h])
        self.surface.fill(color)
        self.surface.set_alpha(alpha)
        self.text_surface = None

    def set_background_surface(self, surface):
        self.surface = surface

    def adjust_text_surface(self):
        text_w = self.text_surface.get_width()
        text_h = self.text_surface.get_height()
        if text_w >= self.w:
            self.w = text_w + 4
        if text_h >= self.h:
            self.h = text_h + 4
        self.surface = pygame.Surface([self.w, self.h])
        self.surface.fill(self.color)
        self.surface.set_alpha(self.alpha)

    def set_text(self, text, color):
        from Game import CGameApp
        app = CGameApp.get_instance()
        self.text_surface = app.font.render(text, False, color)
        self.adjust_text_surface()


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
        self.adjust_text_surface()

    def draw(self, et):
        from Game import CGameApp
        app = CGameApp.get_instance()
        app.screen.blit(self.surface, ((self.x, self.y), (self.w, self.h)))
        text_w = self.text_surface.get_width()
        text_h = self.text_surface.get_height()
        off_x = (self.w - text_w) / 2
        off_y = (self.h - text_h) / 2
        app.screen.blit(self.text_surface, ((self.x + off_x, self.y + off_y), (text_w, text_h)))
        pygame.draw.rect(app.screen, (255, 0, 255), (self.x, self.y, self.w, self.h), 1)

        self.process_evt_queue()


class GuiButton(GuiElement):

    def __init__(self, name, x, y, w, h, color, alpha, text, text_color, parent):
        super(GuiButton, self).__init__(name, x, y, w, h, color, alpha, parent)
        from Game import CGameApp
        app = CGameApp.get_instance()
        self.text_surface = app.font.render(text, False, text_color)
        self.desc = None
        self.skill_attached = None
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
        pygame.draw.rect(app.screen, (128, 128, 128), (self.x, self.y, self.w, self.h), Gui_Enum.WND_BORDER_WIDTH.value)
        from LocalInput import LocalInput
        from Map import QuadTreeForTile
        if QuadTreeForTile.check_tile(self.x, self.y, self.w, self.h, LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
            pygame.draw.rect(app.screen, (0, 255, 0), (self.x, self.y, self.w, self.h), Gui_Enum.WND_BORDER_WIDTH.value)
            if self.desc is not None:
                self.desc.show = True
        else:
            if self.desc is not None:
                self.desc.show = False

        self.process_evt_queue()

    def set_picture(self, pic):
        self.surface = pic

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

    def set_pos(self, x, y):
        off_x = x - self.x
        off_y = y - self.y

        self.x += off_x
        self.y += off_y

        for (name, widget) in self.widgets.items():
            widget.x += off_x
            widget.y += off_y

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
        skill_slots = Character_Skill_Item_Menu()
        self.gui_wnds[skill_slots.name] = skill_slots
        # ban pick stage
        self.character_bp = Character_Ban_Pick_Stage()

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
            if evt.character.team.name == app.cur_player.team.name:
                x = evt.character.pos_x + 18
                y = evt.character.pos_y + 18
                x += app.offset_x
                y += app.offset_y
                self.gui_wnds[Gui_Enum.Character_Control_Menu].set_pos(x, y)
                self.gui_wnds[Gui_Enum.Character_Control_Menu].show = True
        return

    def handle_close_character_menu(self, evt):
        #from Game import CGameApp
        #cur_team = CGameApp.get_instance().cur_team
        #if cur_team is not None and cur_team.character_selected is not None:
        self.gui_wnds[Gui_Enum.Character_Control_Menu].show = False
        self.gui_wnds[Gui_Enum.Character_Skill_Item_Menu].show = False
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
        self.add_widget_handlers(Character_Control_Enum.ITEM_BTN, self.handle_item_btn)
        self.add_widget_handlers(Character_Control_Enum.SKILL_BTN, self.handle_skill_btn)

    def handle_item_btn(self):
        print "Select Item"


    def handle_skill_btn(self):
        print "Select Skill"
        from Game import CGameApp
        from Team import Team_Enum
        app = CGameApp.get_instance()
        app.cur_player.team.fsm.change_to_state(Team_Enum.TEAM_CHARACTER_SELECTED)
        if self.show:
            from Game import CGameApp
            app = CGameApp.get_instance()
            gui_mgr = app.gui_manager
            cur_team = CGameApp.get_instance().cur_team
            gui_mgr.gui_wnds[Gui_Enum.Character_Skill_Item_Menu].show = True
            gui_mgr.gui_wnds[Gui_Enum.Character_Skill_Item_Menu].link_to_character(cur_team.character_selected)
            gui_mgr.gui_wnds[Gui_Enum.Character_Skill_Item_Menu].set_pos(self.x + self.w, self.y)
            self.send_event(app.cur_player.team.character_selected, Event(EventType.CHARACTER_SKILL_CMD))

    def handle_move_btn(self):
        print "Handle Move Btn"
        from Game import CGameApp
        from Team import Team_Enum
        app = CGameApp.get_instance()
        app.cur_player.team.fsm.change_to_state(Team_Enum.TEAM_CHARACTER_SELECTED)
        if app.cur_player.team.character_selected is not None:
            self.send_event(app.cur_player.team.character_selected, Event(EventType.CHARACTER_MOVE_CMD))
            self.send_event(app.gui_manager, Event(EventType.CLOSE_CHARACTER_MENU))
            tile = app.level_map.get_tile_by_coord(app.cur_player.team.character_selected.pos_x, app.cur_player.team.character_selected.pos_y)
            app.level_map.bfs_travel(tile, (0, 0, 255, 196), app.cur_player.team.character_selected.ap)

    def handle_attack_btn(self):
        print "Handle Attack Btn"
        from Game import CGameApp
        from Team import Team_Enum
        app = CGameApp.get_instance()
        app.cur_player.team.fsm.change_to_state(Team_Enum.TEAM_CHARACTER_SELECTED)
        self.send_event(app.cur_player.team.character_selected, Event(EventType.CHARACTER_ATTACK_CMD))
        self.send_event(app.gui_manager, Event(EventType.CLOSE_CHARACTER_MENU))
        tile = app.level_map.get_tile_by_coord(app.cur_player.team.character_selected.pos_x,
                                               app.cur_player.team.character_selected.pos_y)
        app.level_map.bfs_travel_no_occupy(tile, (255, 0, 0, 196), app.cur_player.team.character_selected.attack_range)
            
    def draw(self, et):
        super(Character_Control_Menu, self).draw(et)


# skill items
class Character_Skill_Slots_Enum(Enum):

    Skill_BTN_1 = 0
    Skill_BTN_2 = 1
    Skill_BTN_3 = 2
    Skill_BTN_4 = 3
    Skill_DESC_1 = 4
    Skill_DESC_2 = 5
    Skill_DESC_3 = 6
    Skill_DESC_4 = 7
    Skill_LV_UP_BTN_1 = 8
    Skill_LV_UP_BTN_2 = 9
    Skill_LV_UP_BTN_3 = 10
    Skill_LV_UP_BTN_4 = 11
    SLOT_SIZE = 48
    HEIGHT = 52      # 48 + 2 * 2
    WIDTH = 196    # 48 * 4 + 2 * 2

class Character_Skill_Item_Menu(GuiWindow):

    def __init__(self):
        super(Character_Skill_Item_Menu, self).__init__(Gui_Enum.Character_Skill_Item_Menu,
                                                        300, 0,
                                                        Character_Skill_Slots_Enum.WIDTH.value,
                                                        Character_Skill_Slots_Enum.HEIGHT.value)

        self.show = False

        self.skill_btn_1 = self.add_widget(GuiButton(Character_Skill_Slots_Enum.Skill_BTN_1, 302, 2,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     (0, 0, 0), 255, "", (255, 255, 255), self))

        self.skill_btn_2 = self.add_widget(GuiButton(Character_Skill_Slots_Enum.Skill_BTN_2,
                                                     self.skill_btn_1.x + self.skill_btn_1.w,
                                                     self.skill_btn_1.y,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     (0, 0, 0), 255, "", (255, 255, 255), self))

        self.skill_btn_3 = self.add_widget(GuiButton(Character_Skill_Slots_Enum.Skill_BTN_3,
                                                     self.skill_btn_2.x + self.skill_btn_2.w,
                                                     self.skill_btn_2.y,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     (0, 0, 0), 255, "", (255, 255, 255), self))

        self.skill_btn_4 = self.add_widget(GuiButton(Character_Skill_Slots_Enum.Skill_BTN_4,
                                                     self.skill_btn_3.x + self.skill_btn_3.w,
                                                     self.skill_btn_3.y,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     (0, 0, 0), 255, "", (255, 255, 255), self))

        self.skill_lvl_btn_1 = self.add_widget(GuiButton(Character_Skill_Slots_Enum.Skill_LV_UP_BTN_1,
                                                         self.skill_btn_1.x,
                                                         self.skill_btn_1.y - Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         (0, 0, 0), 255, "LvlUp", (255, 255, 255), self))
        self.skill_lvl_btn_1.show = False

        self.skill_lvl_btn_2 = self.add_widget(GuiButton(Character_Skill_Slots_Enum.Skill_LV_UP_BTN_2,
                                                         self.skill_btn_2.x,
                                                         self.skill_btn_2.y - Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         (0, 0, 0), 255, "LvlUp", (255, 255, 255), self))

        self.skill_lvl_btn_2.show = False

        self.skill_lvl_btn_3 = self.add_widget(GuiButton(Character_Skill_Slots_Enum.Skill_LV_UP_BTN_3,
                                                         self.skill_btn_3.x,
                                                         self.skill_btn_3.y - Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         (0, 0, 0), 255, "LvlUp", (255, 255, 255), self))
        self.skill_lvl_btn_3.show = False

        self.skill_lvl_btn_4 = self.add_widget(GuiButton(Character_Skill_Slots_Enum.Skill_LV_UP_BTN_4,
                                                         self.skill_btn_4.x,
                                                         self.skill_btn_4.y - Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                         (0, 0, 0), 255, "LvlUp", (255, 255, 255), self))
        self.skill_lvl_btn_4.show = False

        self.skill_desc_1 = self.add_widget(GuiLabel(Character_Skill_Slots_Enum.Skill_DESC_1,
                                                     self.x,
                                                     self.y + self.h,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     (0, 0, 0), 255, "Desc", (255, 255, 255), self))
        self.skill_btn_1.desc = self.skill_desc_1
        self.skill_desc_1.show = False

        self.skill_desc_2 = self.add_widget(GuiLabel(Character_Skill_Slots_Enum.Skill_DESC_2,
                                                     self.x,
                                                     self.y + self.h,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     (0, 0, 0), 255, "Desc", (255, 255, 255), self))
        self.skill_btn_2.desc = self.skill_desc_2
        self.skill_desc_2.show = False

        self.skill_desc_3 = self.add_widget(GuiLabel(Character_Skill_Slots_Enum.Skill_DESC_3,
                                                     self.x,
                                                     self.y + self.h,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     (0, 0, 0), 255, "Desc", (255, 255, 255), self))
        self.skill_btn_3.desc = self.skill_desc_3
        self.skill_desc_3.show = False

        self.skill_desc_4 = self.add_widget(GuiLabel(Character_Skill_Slots_Enum.Skill_DESC_4,
                                                     self.x,
                                                     self.y + self.h,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     Character_Skill_Slots_Enum.SLOT_SIZE.value,
                                                     (0, 0, 0), 255, "Desc", (255, 255, 255), self))
        self.skill_btn_4.desc = self.skill_desc_4
        self.skill_desc_4.show = False

        # add handle skill btns
        self.add_widget_handlers(Character_Skill_Slots_Enum.Skill_BTN_1, self.handle_skill_1)
        self.add_widget_handlers(Character_Skill_Slots_Enum.Skill_BTN_2, self.handle_skill_2)
        self.add_widget_handlers(Character_Skill_Slots_Enum.Skill_BTN_3, self.handle_skill_3)
        self.add_widget_handlers(Character_Skill_Slots_Enum.Skill_BTN_4, self.handle_skill_4)

    def handle_skill(self, skill):
        if skill is None:
            return
        from Game import CGameApp
        from Character import Character_State_Enum
        app = CGameApp.get_instance()
        map = app.level_map
        team = app.cur_player.team
        tile = app.level_map.get_tile_by_coord(team.character_selected.pos_x, team.character_selected.pos_y)
        map.bfs_travel_no_occupy(tile, (0, 0, 255), skill.rng)
        self.send_event(app.gui_manager, Event(EventType.CLOSE_CHARACTER_MENU))
        team.character_selected.fsm.change_to_state(Character_State_Enum.SKILL_TARGET_SEARCH)
        print skill.name
        if isinstance(skill, Skill_Single_Target):
            print "Single Target Skill"
            team.character_selected.cur_skill = skill
        elif isinstance(skill, Skill_AOE):
            print "AOE Skill"
            team.character_selected.cur_skill = skill

    def handle_skill_1(self):
        skill = self.skill_btn_1.skill_attached
        self.handle_skill(skill)

    def handle_skill_2(self):
        skill = self.skill_btn_2.skill_attached
        self.handle_skill(skill)

    def handle_skill_3(self):
        skill = self.skill_btn_3.skill_attached
        self.handle_skill(skill)

    def handle_skill_4(self):
        skill = self.skill_btn_4.skill_attached
        self.handle_skill(skill)

    def draw(self, et):
        super(Character_Skill_Item_Menu, self).draw(et)

    def link_to_character(self, character):
        if character is not None:
            self.skill_btn_1.set_picture(character.skills[0].get_icon())
            self.skill_btn_2.set_picture(character.skills[1].get_icon())
            self.skill_btn_3.set_picture(character.skills[2].get_icon())
            self.skill_btn_4.set_picture(character.skills[3].get_icon())

            self.skill_btn_1.skill_attached = character.skills[0]
            self.skill_btn_2.skill_attached = character.skills[1]
            self.skill_btn_3.skill_attached = character.skills[2]
            self.skill_btn_4.skill_attached = character.skills[3]

            self.skill_desc_1.set_text(character.skills[0].desc, (255, 255, 255))
            self.skill_desc_2.set_text(character.skills[1].desc, (255, 255, 255))
            self.skill_desc_3.set_text(character.skills[2].desc, (255, 255, 255))
            self.skill_desc_4.set_text(character.skills[3].desc, (255, 255, 255))


# ban pick stage
class Character_BP_Stage_Enum(Enum):

    WIDTH = 244


class Character_BP_Pic(GuiPicture):

    def __init__(self, name, x, y, w, h, parent):
        super(Character_BP_Pic, self).__init__(name, x, y, w, h, parent)
        self.in_character_pool = True


class Character_Ban_Pick_Stage(GuiWindow):

    def __init__(self):
        from Game import CGameApp
        app = CGameApp.get_instance()
        super(Character_Ban_Pick_Stage, self).__init__(Gui_Enum.Character_Ban_Pick,
                                                        0, 0, app.screen_w, app.screen_h)
        self.show = False
        self.ui_frame = pygame.image.load("Media/banpick_screen.png").convert_alpha()
        self.character_pool_btn = []
        self.character_red_pick = []
        self.character_red_ban = []
        self.character_blue_pick = []
        self.character_blue_ban = []

        # ban picks
        self.bp_x = 430
        self.red_pick_y = 72
        self.red_ban_y = 259
        self.blue_pick_y = 447
        self.blue_ban_y = 634

        from Game import CGameApp
        app = CGameApp.get_instance()
        x = 20
        y = 72
        character_num = 0

        for (name, character) in app.characters.items():
            character_icon = character.sprite_sheet.frames[0]
            character_btn = Character_BP_Pic(character.name, x, y, 36, 36, self)
            character_btn.set_picture(character_icon)
            self.character_pool_btn.append(character_btn)
            character_num += 1
            if character_num % 10 == 0:
                x = 20
                y += 36
            else:
                x += 36

        # character plane
        self.character_pic = self.add_widget(GuiPicture(Character_Plane_Enum.Character_Pic, 3, 378,
                                                        Character_Plane_Enum.WIDTH.value,
                                                        Character_Plane_Enum.WIDTH.value, self))

        self.character_name = self.add_widget(GuiLabel(Character_Plane_Enum.Character_Name,
                                                       153, 378,
                                                       Character_BP_Stage_Enum.WIDTH.value,
                                                       Character_Plane_Enum.PROP_HEIGHT.value,
                                                       (0, 0, 0), 255, "???", (255, 255, 255), self))

        self.character_ap = self.add_widget(GuiLabel(Character_Plane_Enum.Character_AP,
                                                     153,
                                                     self.character_name.y + self.character_name.h,
                                                     Character_BP_Stage_Enum.WIDTH.value / 2,
                                                     Character_Plane_Enum.PROP_HEIGHT.value,
                                                     (0, 0, 0), 255, "AP:", (255, 255, 255), self))

        self.character_hp = self.add_widget(GuiLabel(Character_Plane_Enum.Character_HP,
                                                     153 + self.character_ap.w,
                                                     self.character_name.y + self.character_name.h,
                                                     Character_BP_Stage_Enum.WIDTH.value / 2,
                                                     Character_Plane_Enum.PROP_HEIGHT.value,
                                                     (0, 0, 0), 255, "HP:", (255, 255, 255), self))

        self.character_mp = self.add_widget(GuiLabel(Character_Plane_Enum.Character_MP,
                                                     153,
                                                     self.character_ap.y + self.character_ap.h,
                                                     Character_BP_Stage_Enum.WIDTH.value / 2,
                                                     Character_Plane_Enum.PROP_HEIGHT.value,
                                                     (0, 0, 0), 255, "MP:", (255, 255, 255), self))

        self.character_atk = self.add_widget(GuiLabel(Character_Plane_Enum.Character_ATK,
                                                      153 + self.character_mp.w,
                                                      self.character_ap.y + self.character_ap.h,
                                                      Character_BP_Stage_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "ATK:", (255, 255, 255), self))

        self.character_atk_rng = self.add_widget(GuiLabel(Character_Plane_Enum.Character_ATK_RNG,
                                                          153,
                                                          self.character_mp.y + self.character_mp.h,
                                                          Character_BP_Stage_Enum.WIDTH.value / 2,
                                                          Character_Plane_Enum.PROP_HEIGHT.value,
                                                          (0, 0, 0), 255, "RNG:", (255, 255, 255), self))

        self.character_def = self.add_widget(GuiLabel(Character_Plane_Enum.Character_DEF,
                                                      153 + self.character_atk_rng.w,
                                                      self.character_mp.y + self.character_mp.h,
                                                      Character_BP_Stage_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "DEF:", (255, 255, 255), self))

        self.character_res = self.add_widget(GuiLabel(Character_Plane_Enum.Character_RES,
                                                      153,
                                                      self.character_atk_rng.y + self.character_atk_rng.h,
                                                      Character_BP_Stage_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "RES:", (255, 255, 255), self))

        self.character_str = self.add_widget(GuiLabel(Character_Plane_Enum.Character_STR,
                                                      153 + self.character_res.w,
                                                      self.character_atk_rng.y + self.character_atk_rng.h,
                                                      Character_BP_Stage_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "STR:", (255, 255, 255), self))

        self.character_agi = self.add_widget(GuiLabel(Character_Plane_Enum.Character_AGI,
                                                      153,
                                                      self.character_res.y + self.character_res.h,
                                                      Character_BP_Stage_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "AGI:", (255, 255, 255), self))

        self.character_int = self.add_widget(GuiLabel(Character_Plane_Enum.Character_INT,
                                                      153 + self.character_agi.w,
                                                      self.character_res.y + self.character_res.h,
                                                      Character_BP_Stage_Enum.WIDTH.value / 2,
                                                      Character_Plane_Enum.PROP_HEIGHT.value,
                                                      (0, 0, 0), 255, "INT:", (255, 255, 255), self))

    def draw(self, et):
        from Map import QuadTreeForTile
        from LocalInput import LocalInput
        from Game import CGameApp
        app = CGameApp.get_instance()
        mouse_x = LocalInput.mouse_pos[0]
        mouse_y = LocalInput.mouse_pos[1]

        app.screen.blit(self.ui_frame, (0, 0))

        for character_btn in self.character_pool_btn:
            if character_btn.in_character_pool:
                character_btn.draw(et)
            if QuadTreeForTile.check_tile(character_btn.x, character_btn.y, character_btn.w - 1, character_btn.h - 1,
                                          mouse_x, mouse_y, 0, 0) and character_btn.in_character_pool:
                if character_btn.in_character_pool:
                    pygame.draw.rect(app.screen, (255, 0, 255), (character_btn.x, character_btn.y, 36, 36), 2)
                    self.link_to_character(character_btn.name)

        # bp coords
        x = self.bp_x
        y = self.blue_pick_y
        count = 0
        for character_btn in self.character_blue_pick:
            count += 1
            character_btn.x = x
            character_btn.y = y
            character_btn.draw(et)
            if QuadTreeForTile.check_tile(character_btn.x, character_btn.y, character_btn.w - 1, character_btn.h - 1,
                                          mouse_x, mouse_y, 0, 0):
                pygame.draw.rect(app.screen, (255, 0, 255), (character_btn.x, character_btn.y, 36, 36), 2)
                self.link_to_character(character_btn.name)
            if count % 15 == 0:
                x = self.bp_x
                y += 36
            else:
                x += 36

        x = self.bp_x
        y = self.blue_ban_y
        count = 0
        for character_btn in self.character_blue_ban:
            count += 1
            character_btn.x = x
            character_btn.y = y
            character_btn.draw(et)
            if QuadTreeForTile.check_tile(character_btn.x, character_btn.y, character_btn.w - 1, character_btn.h - 1,
                                          mouse_x, mouse_y, 0, 0):
                pygame.draw.rect(app.screen, (255, 0, 255), (character_btn.x, character_btn.y, 36, 36), 2)
                self.link_to_character(character_btn.name)
            count += 1
            if count % 15 == 0:
                x = self.bp_x
                y += 36
            else:
                x += 36

        x = self.bp_x
        y = self.red_pick_y
        count = 0
        for character_btn in self.character_red_pick:
            count += 1
            character_btn.x = x
            character_btn.y = y
            character_btn.draw(et)
            if QuadTreeForTile.check_tile(character_btn.x, character_btn.y, character_btn.w - 1, character_btn.h - 1,
                                          mouse_x, mouse_y, 0, 0):
                pygame.draw.rect(app.screen, (255, 0, 255), (character_btn.x, character_btn.y, 36, 36), 2)
                self.link_to_character(character_btn.name)
            count += 1
            if count % 15 == 0:
                x = self.bp_x
                y += 36
            else:
                x += 36

        x = self.bp_x
        y = self.red_ban_y
        count = 0
        for character_btn in self.character_red_ban:
            count += 1
            character_btn.x = x
            character_btn.y = y
            character_btn.draw(et)
            if QuadTreeForTile.check_tile(character_btn.x, character_btn.y, character_btn.w - 1, character_btn.h - 1,
                                          mouse_x, mouse_y, 0, 0):
                pygame.draw.rect(app.screen, (255, 0, 255), (character_btn.x, character_btn.y, 36, 36), 2)
                self.link_to_character(character_btn.name)
            count += 1
            if count % 15 == 0:
                x = self.bp_x
                y += 36
            else:
                x += 36

        self.character_name.draw(et)
        self.character_pic.draw(et)
        pygame.draw.rect(app.screen, (255, 0, 255), (3, 378, 150, 150), 1)
        self.character_str.draw(et)
        self.character_agi.draw(et)
        self.character_int.draw(et)
        self.character_atk.draw(et)
        self.character_atk_rng.draw(et)
        self.character_def.draw(et)
        self.character_res.draw(et)
        self.character_ap.draw(et)
        self.character_hp.draw(et)
        self.character_mp.draw(et)


    def link_to_character(self, name):
        from Game import CGameApp
        characters = CGameApp.get_instance().characters
        if name in characters:
            character = characters[name]
            self.character_name.set_text(character.name, (255, 255, 255))
            self.character_pic.set_picture(character.sprite)
            self.character_str.set_text("STR: " + str(character.strength), (255, 255, 255))
            self.character_agi.set_text("AGI: " + str(character.agility), (255, 255, 255))
            self.character_int.set_text("INT: " + str(character.intelligence), (255, 255, 255))
            self.character_atk.set_text("ATK: " + str(character.attack), (255, 255, 255))
            self.character_atk_rng.set_text("RNG: " + str(character.attack_range), (255, 255, 255))
            self.character_def.set_text("DEF: " + str(character.defense), (255, 255, 255))
            self.character_res.set_text("RES: " + str(character.resistance), (255, 255, 255))
            self.character_ap.set_text("AP: " + str(character.ap), (255, 255, 255))
            self.character_hp.set_text("HP: " + str(character.hp), (255, 255, 255))
            self.character_mp.set_text("MP: " + str(character.mp), (255, 255, 255))
        else:
            self.character_name.set_text("???", (255, 255, 255))
            self.character_pic.set_picture(None)
            self.character_str.set_text("STR:", (255, 255, 255))
            self.character_agi.set_text("AGI:", (255, 255, 255))
            self.character_int.set_text("INT:", (255, 255, 255))
            self.character_atk.set_text("ATK:", (255, 255, 255))
            self.character_atk_rng.set_text("RNG:", (255, 255, 255))
            self.character_def.set_text("DEF:", (255, 255, 255))
            self.character_res.set_text("RES:", (255, 255, 255))
            self.character_ap.set_text("AP:", (255, 255, 255))
            self.character_hp.set_text("HP:", (255, 255, 255))
            self.character_mp.set_text("MP:", (255, 255, 255))
