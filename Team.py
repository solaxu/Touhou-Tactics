from Character import *
from Event import *
from Map import *
from enum import Enum
from FSM import *
from collections import deque


class Team_Enum(Enum):
    
    TEAM_RED = 0
    TEAM_BLUE = 1
    TEAM_CHARACTER_MOVE = 2
    TEAM_NORMAL = 3

# Team state

# Normal state
class Team_State_Normal(FSM_State):

    def __init__(self, fsm):
        super(Team_State_Normal, self).__init__(fsm)
        self.sn = Team_Enum.TEAM_NORMAL

    def enter(self):
        super(Team_State_Normal, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Team_State_Normal, self).update(et)
        for (name, c) in self.fsm.owner.characters.items():
            c.update(et)

    def draw(self, et):
        super(Team_State_Normal, self).draw(et)
        for (name, c) in self.fsm.owner.characters.items():
            c.draw(et)

    def exit(self):
        super(Team_State_Normal, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# Character selected

class Team_State_Character_Selected(FSM_State):

    def __init__(self, fsm):
        super(Team_State_Character_Selected, self).__init__(fsm)
        self.sn = Team_Enum.TEAM_CHARACTER_MOVE

    def enter(self):
        super(Team_State_Character_Selected, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Team_State_Character_Selected, self).update(et)
        for (name, c) in self.fsm.owner.characters.items():
            c.update(et)

    def draw(self, et):
        super(Team_State_Character_Selected, self).draw(et)
        # update characters
        for (name, c) in self.fsm.owner.characters.items():
            c.draw(et)

    def exit(self):
        super(Team_State_Character_Selected, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# Team class

class Team(EventObject):

    def __init__(self, name, lvl_map):
        super(Team, self).__init__()
        self.name = name
        self.lvl_map = lvl_map
        self.fsm = FSM_Machine(self)
        self.character_selected = None
        self.fog_of_war = []
        self.characters = {}

        # add states
        self.fsm.add_state(Team_State_Normal(self.fsm))
        self.fsm.add_state(Team_State_Character_Selected(self.fsm))

        self.fsm.cur_state = self.fsm.states[Team_Enum.TEAM_NORMAL]

        # register event handlers
        self.add_handler(EventType.MOUSE_LBTN_DOWN, self.handle_mouse_lbtn_down)
        self.add_handler(EventType.CHARACTER_STOP_MOVING, self.handle_character_stop_moving)

    def add_character(self, c):
        self.characters[c.name] = c

    def del_character(self, name):
        del self.characters[name]

    def update_fog_of_war(self):
        return

    def mist_map(self):
        return

    def select_character_by_mouse(self, mouse_pos):
        from Game import CGameApp
        app = CGameApp.get_instance()
        x = mouse_pos[0] - app.offset_x
        y = mouse_pos[1] - app.offset_y

        for (name,character) in self.characters.items():
            if QuadTreeForTile.check_tile(character.pos_x, character.pos_y,
            Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value, x, y, character.sprite_sheet.frame_w, character.sprite_sheet.frame_h):
                self.character_selected = character
                self.character_selected.selected = True
                return character
        self.character_selected = None
        return None

    def update(self, et):
        self.process_evt_queue()
        self.fsm.update(et)
        self.update_fog_of_war()

    def draw(self, et):
        # draw characters
        self.fsm.draw(et)

    def handle_character_stop_moving(self, evt):
        print "Character stops"
        self.fsm.change_to_state(Team_Enum.TEAM_NORMAL)

    def handle_character_move(self, evt):
        if self.character_selected is not None:
            pass
        return

    def handle_attack(self, evt):
        #
        return

    def handle_spell(self, evt):
        return

    def handle_mouse_lbtn_down(self, evt):
        from LocalInput import LocalInput
        from Game import CGameApp
        app = CGameApp.get_instance()
        if self.character_selected is None:
            self.character_selected = self.select_character_by_mouse(evt.mouse_pos)
        if self.character_selected is not None:
            if self.character_selected.fsm.is_in_state(Character_State_Enum.WAITING_FOR_CMD):
                self.send_event(self.character_selected, Event(EventType.CHARACTER_MOVE_CMD))
                self.send_event(app.gui_manager, Event(EventType.SHOW_CHARACTER_MENU))
            self.send_event(self.character_selected, Event_Mouse_LBTN_DOWN(EventType.MOUSE_LBTN_DOWN, LocalInput.mouse_pos))
