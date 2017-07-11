# _*_ coding: utf-8 _*_

from enum import Enum

import Queue

class EventType(Enum):

    #
    MOUSE_LBTN_DOWN = 0
    MOUSE_RBTN_DOWN = 1
    MOUSE_HOVER = 2 # equals mouse motion
    #
    GUI_BTN_PRESSED = 50
    GUI_MOUSE_HOVER = 51
    #
    SELECT_CHARACTER = 100
    MOVE_CHARACTER = 101
    CHARACTER_STOP_MOVING = 102
    SCROLL_MAP = 103
    SWITCH_MINI_MAP = 104
    SHOW_CHARACTER_MENU = 105
    CLOSE_CHARACTER_MENU = 106
    CHARACTER_MOVE_CMD = 107
    CHARACTER_ITEM_CMD = 108
    CHARACTER_ATTACK_CMD = 109
    CHARACTER_SKILL_CMD = 110
    CHARACTER_ATTACK_EVT = 111  # character attacked

    CHARACTER_BUFF = 130
    CHARACTER_AURA = 131
    #
    GAME_BAN_PICK_TURN = 1000


class Event(object):

    def __init__(self, type):
        self.evt_type = type
        self.sender = None
        self.reciver = None
        self.delay = 0      # time bomb

class Event_Skill(Event):

    def __init__(self, type, buff):
        super(Event_Skill, self).__init__(type)
        self.buff = buff


class Event_Character_Attack(Event):

    def __init__(self, type, src_character, target_character):
        super(Event_Character_Attack, self).__init__(type)
        self.src_character = src_character
        self.target_character = target_character

class Event_Character_Attacked(Event):

    def __init__(self, type, src_character):
        super(Event_Character_Attacked, self).__init__(type)
        self.src_character = src_character


class Event_Mouse_LBTN_DOWN(Event):

    def __init__(self, type, mouse_pos):
        super(Event_Mouse_LBTN_DOWN, self).__init__(type)
        self.mouse_pos = mouse_pos


class Event_Mouse_RBTN_DOWN(Event):
    
    def __init__(self, type, mouse_pos):
        super(Event_Mouse_RBTN_DOWN, self).__init__(type)
        self.mouse_pos = mouse_pos


class Event_Mouse_Hover(Event):

    def __init__(self, type, mouse_pos):
        super(Event_Mouse_Hover, self).__init__(type)
        self.mouse_pos = mouse_pos


class Event_Character_Stop_Moving(Event):
    
    def __init__(self, type):
        super(Event_Character_Stop_Moving, self).__init__(type)

class Event_Roll_Map(Event):

    def __init__(self, type, offset_x, offset_y):
        super(Event_Roll_Map, self).__init__(type)
        self.offset_x = offset_x
        self.offset_y = offset_y
        
class Event_Switch_MiniMap(Event):
    
    def __init__(self, type):
        super(Event_Switch_MiniMap, self).__init__(type)

# Gui Event

class Event_Gui_Show_Character_Menu(Event):

    def __init__(self, type, character):
        super(Event_Gui_Show_Character_Menu, self).__init__(type)
        self.character = character

class Event_Gui_Btn_Pressed(Event):

    def __init__(self, type, name):
        super(Event_Gui_Btn_Pressed, self).__init__(type)
        self.name = name

class EventObject(object):

    def __init__(self):
        self.handler_map = {}
        self.evt_queue = Queue.Queue()

    def add_handler(self, evt_type, handler):
        self.handler_map[evt_type] = handler
    
    def del_handler(self, evt_type):
        del self.handler_map[evt_type]

    def send_event(self, receiver, evt):
        evt.sender = self
        evt.receiver = receiver
        receiver.evt_queue.put(evt)

    def process_evt_queue(self):
        while not self.evt_queue.empty():
            evt = self.evt_queue.get()
            if self.handler_map.has_key(evt.evt_type):
                self.handler_map[evt.evt_type](evt)
    