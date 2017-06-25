# _*_ coding: utf-8 _*_

from enum import Enum
import Queue

class EventType(Enum):

    MOUSE_LBTN_DOWN = 0
    SELECT_CHARACTER = 100
    MOVE_CHARACTER = 101
    CHARACTER_STOP_MOVING = 102
    SCROLL_MAP = 103
    SWITCH_MINI_MAP = 104


class Event(object):

    def __init__(self, type):
        self.evt_type = type
        self.sender = None
        self.reciver = None
        self.delay = 0      # time bomb

class Event_Mouse_LBTN_DOWN(Event):

    def __init__(self, type, mouse_pos):
        super(Event_Mouse_LBTN_DOWN, self).__init__(type)
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
            self.handler_map[evt.evt_type](evt)
    