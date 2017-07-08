from enum import Enum
from Event import *
from FSM import *


class Player_Enum(Enum):

    Player_State_Pick_Characters = 0
    Player_State_Ban_Characters = 1
    Player_State_In_Game = 2
    Player_State_Victory = 3
    Player_State_Defeat = 4


class Player_State_Pick_Characters(FSM_State):

    def __init__(self, fsm):
        super(Player_State_Pick_Characters, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_Pick_Characters

    def update(self, et):
        super(Player_State_Pick_Characters, self).update(et)
        
    def draw(self, et):
        super(Player_State_Pick_Characters, self).draw(et)

    def enter(self):
        super(Player_State_Pick_Characters, self).enter()
        
    def exit(self):
        super(Player_State_Pick_Characters, self).exit()


class Player_State_Ban_Characters(FSM_State):

    def __init__(self, fsm):
        super(Player_State_Ban_Characters, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_Ban_Characters

    def update(self, et):
        super(Player_State_Ban_Characters, self).update(et)

    def draw(self, et):
        super(Player_State_Ban_Characters, self).draw(et)

    def enter(self):
        super(Player_State_Ban_Characters, self).enter()

    def exit(self):
        super(Player_State_Ban_Characters, self).exit()


class Player_State_In_Game(FSM_State):

    def __init__(self, fsm):
        super(Player_State_In_Game, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_In_Game

    def update(self, et):
        super(Player_State_In_Game, self).update(et)

    def draw(self, et):
        super(Player_State_In_Game, self).draw(et)

    def enter(self):
        super(Player_State_In_Game, self).enter()

    def exit(self):
        super(Player_State_In_Game, self).exit()

class Player_State_Victory(FSM_State):

    def __init__(self, fsm):
        super(Player_State_Victory, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_Victory

    def update(self, et):
        super(Player_State_Victory, self).update(et)

    def draw(self, et):
        super(Player_State_Victory, self).draw(et)

    def enter(self):
        super(Player_State_Victory, self).enter()

    def exit(self):
        super(Player_State_Victory, self).exit()

class Player_State_Defeat(FSM_State):

    def __init__(self, fsm):
        super(Player_State_Defeat, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_Defeat

    def update(self, et):
        super(Player_State_Defeat, self).update(et)

    def draw(self, et):
        super(Player_State_Defeat, self).draw(et)

    def enter(self):
        super(Player_State_Defeat, self).enter()

    def exit(self):
        super(Player_State_Defeat, self).exit()

class Player(EventObject):

    def __init__(self):
        super(Player, self).__init__()
        self.team = None
        self.fsm = FSM_Machine(self)

        # add states
        self.fsm.add_state(Player_State_Pick_Characters(self.fsm))
        self.fsm.add_state(Player_State_Ban_Characters(self.fsm))
        self.fsm.add_state(Player_State_In_Game(self.fsm))
        self.fsm.add_state(Player_State_Victory(self.fsm))
        self.fsm.add_state(Player_State_Defeat(self.fsm))

        # add handlers
        self.add_handler(EventType.MOUSE_LBTN_DOWN, self.mouse_lbtn_down)

    def set_team(self, team):
        self.team = team

    def mouse_lbtn_down(self, evt):

        if self.fsm.is_in_state(Player_Enum.Player_State_Pick_Characters):
            print "Pick Character"
        elif self.fsm.is_in_state(Player_Enum.Player_State_Ban_Characters):
            print "Ban Character"


