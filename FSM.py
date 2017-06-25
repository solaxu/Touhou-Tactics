import pygame


class FSM_State(object):

    def __init__(self, fsm):
        super(FSM_State, self).__init__()
        self.sn = None
        self.fsm = fsm

    def update(self, et):
        return

    def draw(self, et):
        return

    def enter(self):
        return
    
    def exit(self):
        return

class FSM_Transition(object):
    
    def __init__(self, from_state, to_state, fsm):
        self.from_sn = from_state
        self.to_sn = to_state
        self.trans_n = None
        self.fsm = fsm

    def check_transition(self):
        return True

class FSM_Machine(object):

    def __init__(self, owner):
        self.owner = owner
        self.states = {}
        self.transitions = []
        self.cur_state = None
        self.pre_state = None

    def add_state(self, state):
        self.states[state.sn] = state

    def add_transition(self, transition):
        self.transitions.append(transition) 

    def del_state(self, sn):
        del self.states[sn]

    def change_to_state(self, sn):
        self.pre_state = self.cur_state
        if self.cur_state is not None:
            self.cur_state.exit()
        self.cur_state = self.states[sn]
        if self.cur_state is not None:
            self.cur_state.enter()

    def go_back(self):
        self.chage_to_state(self.pre_state.sn)

    def update(self, et):
        for trans in self.transitions:
            if trans.from_sn == self.cur_state.sn:
                if trans.check_transition():
                    self.change_to_state(trans.to_sn)
                    break
        self.cur_state.update(et)

    def draw(self, et):
        self.cur_state.draw(et)

    def is_in_state(self, sn):
        return sn == self.cur_state.sn
