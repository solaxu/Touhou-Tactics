from enum import Enum
from FSM import *
from Game import *
import Queue
from Event import *
from collections import deque


class Character_State_Enum(Enum):
    
    STAND = 0       # Done
    MOVE = 1        # Done
    MOVE_LEFT = 2   # Done
    MOVE_RIGHT = 3  # Done
    MOVE_UP = 4     # Done
    MOVE_DOWN = 5   # Done
    DEAD = 6        # Undo
    ATTACK = 7      # Doing
    ITEM = 8        # Undo
    SKILL = 9       # Undo
    ATTACKED = 10   # Doing
    MOVE_TRANSITION = 100     # Done
    DIE_TRANSITION = 100      # Done

    # waiting for --> if move cmd --> STAND
    #             --> if attack cmd --> ATTACK
    #             --> if item cmd --> ITEM
    #             --> if skill cmd --> SKILL
    WAITING_FOR_CMD = 1000



class Character_Move_Frame(Enum):
    
    TOTAL_FRAME_NUM = 16
    DIRECTION_FRAME_NUM = 4
    MOVE_DOWN_BEGIN = 0
    MOVE_DOWN_END = 3
    MOVE_LEFT_BEGIN = 4
    MOVE_LEFT_END = 7
    MOVE_RIGHT_BEGIN = 8
    MOVE_RIGHT_END = 11
    MOVE_UP_BEGIN = 12
    MOVE_UP_END = 15
    FRAME_INTERVAL = 200 # 80ms
    MOVE_STEP = 4
    MOVE_ACC_OFFSET = 36


# DEAD state
class Character_State_Dead(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Dead, self).__init__(fsm)
        self.sn = Character_State_Enum.DEAD
    
    def enter(self):
        super(Character_State_Dead, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Dead, self).update(et)
    
    def draw(self, et):
        super(Character_State_Dead, self).draw(et)

    def exit(self):
        super(Character_State_Dead, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# Attacked State
class Character_State_Attacked(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Attacked, self).__init__(fsm)
        self.sn = Character_State_Enum.ATTACKED
        self.animation_time = 0
        self.animrtion_len = 200
        self.off_x = 0
        self.off_y = 0
        self.acc_time = 0
        self.acc = 0
        self.character = None

    def enter(self):
        super(Character_State_Attacked, self).enter()
        self.character = self.fsm.owner
        print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        self.acc_time += et
        if self.acc_time > 40:
            self.acc += 1
            self.acc_time = 0
        self.animation_time += et
        return

    def draw(self, et):
        if self.acc % 2 == 0:
            self.off_x = -2
            self.off_y = -2
        else:
            self.off_x = 2
            self.off_y = 2
        mouse_pos = self.fsm.owner.get_pos()
        self.fsm.owner.sprite_sheet.draw(0, (mouse_pos[0] + self.off_x, mouse_pos[1] + self.off_y))
        if self.animation_time > self.animrtion_len:
            self.fsm.change_to_state(Character_State_Enum.WAITING_FOR_CMD)

    def exit(self):
        super(Character_State_Attacked, self).exit()
        self.acc = 0
        self.acc_time = 0
        self.animation_time = 0
        print self.fsm.owner.name + " exit state " + str(self.sn)

# STAND state
class Character_State_Stand(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Stand, self).__init__(fsm)
        self.sn = Character_State_Enum.STAND
    
    def enter(self):
        super(Character_State_Stand, self).enter()
        character = self.fsm.owner
        character.team.lvl_map.get_tile_by_coord(character.pos_x, character.pos_y).occupy = True
        print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Stand, self).update(et)
        if not self.fsm.owner.command_queue.empty():
            self.fsm.owner.direction = self.fsm.owner.command_queue.get()
        if self.fsm.owner.pos_x == self.fsm.owner.moving_target_x and self.fsm.owner.pos_y == self.fsm.owner.moving_target_y:
            self.fsm.owner.send_event(self.fsm.owner.team, Event_Character_Stop_Moving(EventType.CHARACTER_STOP_MOVING))
            self.fsm.owner.moving_target_x = 0
            self.fsm.owner.moving_target_y = 0
    
    def draw(self, et):
        super(Character_State_Stand, self).draw(et)
        self.fsm.owner.sprite_sheet.draw(0, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Stand, self).exit()
        character = self.fsm.owner
        character.team.lvl_map.get_tile_by_coord(character.pos_x, character.pos_y).occupy = False
        print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE state
class Character_State_Move(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE
    
    def enter(self):
        super(Character_State_Move, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move, self).update(et)
        if not self.fsm.owner.command_queue.empty():
            self.fsm.owner.direction = self.fsm.owner.command_queue.get()
    
    def draw(self, et):
        super(Character_State_Move, self).draw(et)
        self.fsm.owner.sprite_sheet.draw(0, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Move, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE_RIGHT state
class Character_State_Move_Right(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move_Right, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE_RIGHT
        self.frame_num = 0
        self.acc_time = 0
        self.offset = 0
    
    def enter(self):
        super(Character_State_Move_Right, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move_Right, self).update(et)
        self.acc_time += et
        self.fsm.owner.pos_x += Character_Move_Frame.MOVE_STEP.value
        self.offset += Character_Move_Frame.MOVE_STEP.value
        if self.acc_time > Character_Move_Frame.FRAME_INTERVAL.value:
            self.acc_time > 0
            self.frame_num += 1
        if self.offset >= Character_Move_Frame.MOVE_ACC_OFFSET.value:
            self.offset = 0
            if not self.fsm.owner.command_queue.empty():
                self.fsm.owner.direction = self.fsm.owner.command_queue.get()
        
    def draw(self, et):
        super(Character_State_Move_Right, self).draw(et)
        frame_index = self.frame_num % Character_Move_Frame.DIRECTION_FRAME_NUM.value + Character_Move_Frame.MOVE_RIGHT_BEGIN.value
        self.fsm.owner.sprite_sheet.draw(frame_index, self.fsm.owner.get_pos())
        # print frame_index

    def exit(self):
        super(Character_State_Move_Right, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE_LEFT state, a sub-state of MOVE
class Character_State_Move_Left(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move_Left, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE_LEFT
        self.frame_num = 0
        self.acc_time = 0
        self.offset = 0
    
    def enter(self):
        super(Character_State_Move_Left, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move_Left, self).update(et)
        self.acc_time += et
        self.fsm.owner.pos_x -= Character_Move_Frame.MOVE_STEP.value
        self.offset += Character_Move_Frame.MOVE_STEP.value
        if self.acc_time > Character_Move_Frame.FRAME_INTERVAL.value:
            self.acc_time > 0
            self.frame_num += 1
        if self.offset >= Character_Move_Frame.MOVE_ACC_OFFSET.value:
            self.offset = 0
            if not self.fsm.owner.command_queue.empty():
                self.fsm.owner.direction = self.fsm.owner.command_queue.get()
    
    def draw(self, et):
        super(Character_State_Move_Left, self).draw(et)
        frame_index = self.frame_num % Character_Move_Frame.DIRECTION_FRAME_NUM.value + Character_Move_Frame.MOVE_LEFT_BEGIN.value
        self.fsm.owner.sprite_sheet.draw(frame_index, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Move_Left, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE_UP state, a sub-state of MOVE
class Character_State_Move_Up(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move_Up, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE_UP
        self.frame_num = 0
        self.acc_time = 0
        self.offset = 0
    
    def enter(self):
        super(Character_State_Move_Up, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move_Up, self).update(et)
        self.acc_time += et
        self.fsm.owner.pos_y -= Character_Move_Frame.MOVE_STEP.value
        self.offset += Character_Move_Frame.MOVE_STEP.value
        if self.acc_time > Character_Move_Frame.FRAME_INTERVAL.value:
            self.acc_time > 0
            self.frame_num += 1
        if self.offset >= Character_Move_Frame.MOVE_ACC_OFFSET.value:
            self.offset = 0
            if not self.fsm.owner.command_queue.empty():
                self.fsm.owner.direction = self.fsm.owner.command_queue.get()
    
    def draw(self, et):
        super(Character_State_Move_Up, self).draw(et)
        frame_index = self.frame_num % Character_Move_Frame.DIRECTION_FRAME_NUM.value + Character_Move_Frame.MOVE_UP_BEGIN.value
        self.fsm.owner.sprite_sheet.draw(frame_index, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Move_Up, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

# MOVE_DOWN state, a sub-state of MOVE
class Character_State_Move_Down(FSM_State):
    
    def __init__(self, fsm):
        super(Character_State_Move_Down, self).__init__(fsm)
        self.sn = Character_State_Enum.MOVE_DOWN
        self.frame_num = 0
        self.acc_time = 0
        self.offset = 0
    
    def enter(self):
        super(Character_State_Move_Down, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Move_Down, self).update(et)
        self.acc_time += et
        self.fsm.owner.pos_y += Character_Move_Frame.MOVE_STEP.value
        self.offset += Character_Move_Frame.MOVE_STEP.value
        if self.acc_time > Character_Move_Frame.FRAME_INTERVAL.value:
            self.acc_time > 0
            self.frame_num += 1
        if self.offset >= Character_Move_Frame.MOVE_ACC_OFFSET.value:
            self.offset = 0
            if not self.fsm.owner.command_queue.empty():
                self.fsm.owner.direction = self.fsm.owner.command_queue.get()
    
    def draw(self, et):
        super(Character_State_Move_Down, self).draw(et)
        frame_index = self.frame_num % Character_Move_Frame.DIRECTION_FRAME_NUM.value + Character_Move_Frame.MOVE_DOWN_BEGIN.value
        self.fsm.owner.sprite_sheet.draw(frame_index, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Move_Down, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)


# cmd state
class Character_State_Waiting_For_Command(FSM_State):

    def __init__(self, fsm):
        super(Character_State_Waiting_For_Command, self).__init__(fsm)
        self.sn = Character_State_Enum.WAITING_FOR_CMD

    def enter(self):
        super(Character_State_Waiting_For_Command, self).enter()
        character = self.fsm.owner
        character.team.lvl_map.get_tile_by_coord(character.pos_x, character.pos_y).occupy = True
        print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Waiting_For_Command, self).update(et)
        if not self.fsm.owner.command_queue.empty():
            self.fsm.owner.direction = self.fsm.owner.command_queue.get()
        if self.fsm.owner.pos_x == self.fsm.owner.moving_target_x and self.fsm.owner.pos_y == self.fsm.owner.moving_target_y:
            self.fsm.owner.send_event(self.fsm.owner.team, Event_Character_Stop_Moving(EventType.CHARACTER_STOP_MOVING))
            self.fsm.owner.moving_target_x = 0
            self.fsm.owner.moving_target_y = 0

    def draw(self, et):
        super(Character_State_Waiting_For_Command, self).draw(et)
        self.fsm.owner.sprite_sheet.draw(0, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Waiting_For_Command, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

class Character_State_Attack(FSM_State):

    def __init__(self, fsm):
        super(Character_State_Attack, self).__init__(fsm)
        self.sn = Character_State_Enum.ATTACK

    def enter(self):
        super(Character_State_Attack, self).enter()
        character = self.fsm.owner
        character.team.lvl_map.get_tile_by_coord(character.pos_x, character.pos_y).occupy = True
        print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Attack, self).update(et)
        if not self.fsm.owner.command_queue.empty():
            self.fsm.owner.direction = self.fsm.owner.command_queue.get()
        if self.fsm.owner.pos_x == self.fsm.owner.moving_target_x and self.fsm.owner.pos_y == self.fsm.owner.moving_target_y:
            self.fsm.owner.send_event(self.fsm.owner.team, Event_Character_Stop_Moving(EventType.CHARACTER_STOP_MOVING))
            self.fsm.owner.moving_target_x = 0
            self.fsm.owner.moving_target_y = 0

    def draw(self, et):
        super(Character_State_Attack, self).draw(et)
        self.fsm.owner.sprite_sheet.draw(0, self.fsm.owner.get_pos())

    def exit(self):
        super(Character_State_Attack, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

class Character_State_Item(FSM_State):

    def __init__(self, fsm):
        super(Character_State_Item, self).__init__(fsm)
        self.sn = Character_State_Enum.ITEM

    def enter(self):
        super(Character_State_Item, self).enter()
        character = self.fsm.owner
        character.team.lvl_map.get_tile_by_coord(character.pos_x, character.pos_y).occupy = True
        print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Item, self).update(et)
        if not self.fsm.owner.command_queue.empty():
            self.fsm.owner.direction = self.fsm.owner.command_queue.get()
        if self.fsm.owner.pos_x == self.fsm.owner.moving_target_x and self.fsm.owner.pos_y == self.fsm.owner.moving_target_y:
            self.fsm.owner.send_event(self.fsm.owner.team, Event_Character_Stop_Moving(EventType.CHARACTER_STOP_MOVING))
            self.fsm.owner.moving_target_x = 0
            self.fsm.owner.moving_target_y = 0

    def draw(self, et):
        super(Character_State_Item, self).draw(et)

    def exit(self):
        super(Character_State_Item, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

class Character_State_Skill(FSM_State):

    def __init__(self, fsm):
        super(Character_State_Skill, self).__init__(fsm)
        self.sn = Character_State_Enum.SKILL

    def enter(self):
        super(Character_State_Skill, self).enter()
        character = self.fsm.owner
        character.team.lvl_map.get_tile_by_coord(character.pos_x, character.pos_y).occupy = True
        print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Character_State_Item, self).update(et)
        if not self.fsm.owner.command_queue.empty():
            self.fsm.owner.direction = self.fsm.owner.command_queue.get()
        if self.fsm.owner.pos_x == self.fsm.owner.moving_target_x and self.fsm.owner.pos_y == self.fsm.owner.moving_target_y:
            self.fsm.owner.send_event(self.fsm.owner.team, Event_Character_Stop_Moving(EventType.CHARACTER_STOP_MOVING))
            self.fsm.owner.moving_target_x = 0
            self.fsm.owner.moving_target_y = 0

    def draw(self, et):
        super(Character_State_Skill, self).draw(et)

    def exit(self):
        super(Character_State_Skill, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)


# state transition
class Character_State_Move_Transition(FSM_Transition):
    
    def __init__(self, from_state, to_state, direction, fsm):
        super(Character_State_Move_Transition, self).__init__(from_state, to_state, fsm)
        self.trans_n = Character_State_Enum.MOVE_TRANSITION
        self.direction = direction

    def check_transition(self):
        super(Character_State_Move_Transition, self).check_transition()
        if self.fsm.owner.direction == self.direction:
            return True
        return False

class Character_State_StandToMove_transition(FSM_Transition):
    
    def __init__(self, from_state, to_state, direction, fsm):
        super(Character_State_StandToMove_transition, self).__init__(from_state, to_state, fsm)
        self.trans_n = Character_State_Enum.MOVE_TRANSITION
        self.direction = direction

    def check_transition(self):
        super(Character_State_StandToMove_transition, self).check_transition()
        if self.fsm.owner.direction == self.direction:
            return True
        return False

class Character_State_Die_Transition(FSM_Transition):
    
    def __init__(self, from_state, to_state, fsm):
        super(Character_State_Die_Transition, self).__init__(from_state, to_state, fsm)
        self.trans_n = Character_State_Enum.DIE_TRANSITION

    def check_transition(self):
        super(Character_State_Die_Transition, self).check_transition()
        if self.fsm.owner.hp <= 0:
            return True
        return False


# character class
class Character(EventObject):

    def __init__(self, cn, sprite_sheet, team):
        super(Character, self).__init__()
        self.name = cn
        self.sprite = None # character picture
        self.fsm = FSM_Machine(self)
        self.sprite_sheet = sprite_sheet
        self.team = team
        self.selected = False
        team.add_character(self)

        # property for test
        self.moving_target_x = 360
        self.moving_target_y = 324
        self.pos_x = 288
        self.pos_y = 288

        self.lvl = 1            # level
        self.exp = 0            # experience
        self.ap = 10            # action point, for moving, attacking and spelling
        self.hp = 1             # health point
        self.mp = 1             # magic point
        self.agility = 1        # agility
        self.strength = 1       # strength
        self.intelligence = 1   # intelligence
        self.defense = 1        # defense
        self.resistance = 1     # resistance
        self.attack = 2
        self.attack_range = 1   # physical attack range, will be not shown at character plane

        self.direction = Character_State_Enum.STAND
        self.command_queue = Queue.Queue()
        # control for test
#        self.command_queue.put(Character_State_Enum.MOVE_DOWN)
#        self.command_queue.put(Character_State_Enum.MOVE_DOWN)
#        self.command_queue.put(Character_State_Enum.MOVE_DOWN)
#        self.command_queue.put(Character_State_Enum.MOVE_RIGHT)
#        self.command_queue.put(Character_State_Enum.MOVE_RIGHT)
#        self.command_queue.put(Character_State_Enum.MOVE_RIGHT)
#        self.command_queue.put(Character_State_Enum.MOVE_UP)
#        self.command_queue.put(Character_State_Enum.MOVE_LEFT)
#        self.command_queue.put(Character_State_Enum.MOVE_UP)
#        self.command_queue.put(Character_State_Enum.STAND)

        # add states
        self.fsm.add_state(Character_State_Stand(self.fsm))
        self.fsm.add_state(Character_State_Move_Down(self.fsm))
        self.fsm.add_state(Character_State_Move_Left(self.fsm))
        self.fsm.add_state(Character_State_Move_Right(self.fsm))
        self.fsm.add_state(Character_State_Move_Up(self.fsm))
        self.fsm.add_state(Character_State_Waiting_For_Command(self.fsm))
        self.fsm.add_state(Character_State_Attack(self.fsm))
        self.fsm.add_state(Character_State_Item(self.fsm))
        self.fsm.add_state(Character_State_Skill(self.fsm))

        self.fsm.add_state(Character_State_Attacked(self.fsm))

        self.fsm.add_state(Character_State_Dead(self.fsm))

        # add transitions
        '''
                        |---> move right -->|    
                        |---> move left  -->|   
                stand --|---> die           |--->stand
                        |---> move down  -->|
                        |---> move left  -->|
        '''
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_LEFT, Character_State_Enum.WAITING_FOR_CMD, Character_State_Enum.STAND, self.fsm))

        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_RIGHT, Character_State_Enum.WAITING_FOR_CMD, Character_State_Enum.STAND, self.fsm))

        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_DOWN, Character_State_Enum.WAITING_FOR_CMD, Character_State_Enum.STAND, self.fsm))

        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))
        self.fsm.add_transition(Character_State_Move_Transition(Character_State_Enum.MOVE_UP, Character_State_Enum.WAITING_FOR_CMD, Character_State_Enum.STAND, self.fsm))

        self.fsm.add_transition(Character_State_StandToMove_transition(Character_State_Enum.STAND, Character_State_Enum.MOVE_LEFT, Character_State_Enum.MOVE_LEFT, self.fsm))
        self.fsm.add_transition(Character_State_StandToMove_transition(Character_State_Enum.STAND, Character_State_Enum.MOVE_RIGHT,Character_State_Enum.MOVE_RIGHT, self.fsm))
        self.fsm.add_transition(Character_State_StandToMove_transition(Character_State_Enum.STAND, Character_State_Enum.MOVE_UP,Character_State_Enum.MOVE_UP, self.fsm))
        self.fsm.add_transition(Character_State_StandToMove_transition(Character_State_Enum.STAND, Character_State_Enum.MOVE_DOWN, Character_State_Enum.MOVE_DOWN, self.fsm))

        self.fsm.add_transition(Character_State_Die_Transition(Character_State_Enum.WAITING_FOR_CMD, Character_State_Enum.DEAD, self.fsm))

        self.fsm.owner = self

        self.fsm.change_to_state(Character_State_Enum.WAITING_FOR_CMD)
#        self.fsm.cur_state = self.fsm.states[Character_State_Enum.STAND]

        # register event handler
        self.add_handler(EventType.CHARACTER_MOVE_CMD, self.handle_move_cmd)
        self.add_handler(EventType.CHARACTER_ATTACK_CMD, self.handle_attack_cmd)
        self.add_handler(EventType.CHARACTER_ITEM_CMD, self.handle_item_cmd)
        self.add_handler(EventType.CHARACTER_SKILL_CMD, self.handle_skill_cmd)
        self.add_handler(EventType.MOUSE_LBTN_DOWN, self.handle_mouse_lbtn_down)
        self.add_handler(EventType.CHARACTER_ATTACK_EVT, self.handle_character_attacked)

    def get_range(self, x, y):
        from Game import CGameApp
        app = CGameApp.get_instance()
        tx = x / app.level_map.tile_width
        ty = y / app.level_map.tile_height
        ctx = self.pos_x / app.level_map.tile_width
        cty = self.pos_y / app.level_map.tile_height

        return abs(ctx - tx) + abs(cty - ty)

    def handle_character_attacked(self, evt):
        dmg = evt.src_character.attack - self.defense
        self.hp -= dmg
        evt.src_character.fsm.change_to_state(Character_State_Enum.WAITING_FOR_CMD)
        if self.hp <= 0:
            self.fsm.change_to_state(Character_State_Enum.DEAD)
            from Game import CGameApp
            lvl_map = CGameApp.get_instance().level_map
            tile = lvl_map.get_tile_by_coord(self.pos_x, self.pos_y)
            tile.occupy = False
            self.team.dead_characters[self.name] = self
            del self.team.characters[self.name]
        else:
            self.fsm.change_to_state(Character_State_Enum.ATTACKED)

    def handle_mouse_lbtn_down(self, evt):
        from Team import Team_Enum

        # attack
        if self.fsm.is_in_state(Character_State_Enum.ATTACK):
            from Game import CGameApp
            app = CGameApp.get_instance()
            print "Do Attack and Play Attack Animations"
            self.team.lvl_map.reset_map()
            mouse_character = app.select_character_by_mouse(evt.mouse_pos)

            if mouse_character is not None:
                rng = self.get_range(mouse_character.pos_x, mouse_character.pos_y)
                if mouse_character.name == self.name:
                    self.fsm.change_to_state(Character_State_Enum.WAITING_FOR_CMD)
                elif rng <= self.attack_range:
                    print "Do Attack"
                    self.fsm.change_to_state(Character_State_Enum.WAITING_FOR_CMD)
                    self.send_event(mouse_character, Event_Character_Attack(EventType.CHARACTER_ATTACK_EVT, self, mouse_character))
                # so sorry there's no attack animations
            else:
                self.fsm.change_to_state(Character_State_Enum.WAITING_FOR_CMD)


        # stand for moving
        elif self.fsm.is_in_state(Character_State_Enum.STAND):
            tile = self.team.lvl_map.select_tile_by_mouse(evt.mouse_pos)

            if not tile.marked:
                self.team.lvl_map.reset_map()
                self.fsm.change_to_state(Character_State_Enum.WAITING_FOR_CMD)
                self.team.fsm.change_to_state(Team_Enum.TEAM_NORMAL)
            else:
                # do A* to find moving path, and change state to character moving
                #                print "A* to find moving path"
                start_tile = self.team.lvl_map.get_tile_by_index(self.pos_x / self.team.lvl_map.tile_width,
                                                                 self.pos_y / self.team.lvl_map.tile_height)
                s_x = start_tile.pos_x / self.team.lvl_map.tile_width
                s_y = start_tile.pos_y / self.team.lvl_map.tile_height
                t_x = tile.pos_x / self.team.lvl_map.tile_width
                t_y = tile.pos_y / self.team.lvl_map.tile_height
                self.team.lvl_map.init_a_star_open_list(s_x, s_y, t_x, t_y, start_tile)
                #                print "Finding"
                self.team.lvl_map.a_star_path_finding(t_x, t_y, tile)
                start_tile.occupy = False
                tile.occupy = True
                path = deque()
                while tile.parent_tile is not None:
                    #                    print "Path Coords: %s, %s" % (tile.pos_x, tile.pos_y)
                    if tile.pos_x > tile.parent_tile.pos_x:
                        path.append(Character_State_Enum.MOVE_RIGHT)
                    elif tile.pos_x < tile.parent_tile.pos_x:
                        path.append(Character_State_Enum.MOVE_LEFT)
                    elif tile.pos_y > tile.parent_tile.pos_y:
                        path.append(Character_State_Enum.MOVE_DOWN)
                    elif tile.pos_y < tile.parent_tile.pos_y:
                        path.append(Character_State_Enum.MOVE_UP)
                    tile = tile.parent_tile
                while len(path) != 0:
                    self.command_queue.put(path.pop())
                self.command_queue.put(Character_State_Enum.STAND)
                self.team.lvl_map.reset_map()
                self.team.fsm.change_to_state(Team_Enum.TEAM_NORMAL)
        return

    def handle_move_cmd(self, evt):
        from Team import Team_Enum
        if self.fsm.is_in_state(Character_State_Enum.WAITING_FOR_CMD):
            print "Change to Stand for moving"
            self.fsm.owner.team.fsm.change_to_state(Team_Enum.TEAM_CHARACTER_MOVE)
            self.fsm.change_to_state(Character_State_Enum.STAND)

    def handle_attack_cmd(self, evt):
        if self.fsm.is_in_state(Character_State_Enum.WAITING_FOR_CMD):
            self.fsm.change_to_state(Character_State_Enum.ATTACK)

    def handle_item_cmd(self, evt):
        if self.fsm.is_in_state(Character_State_Enum.WAITING_FOR_CMD):
            self.fsm.change_to_state(Character_State_Enum.ITEM)

    def handle_skill_cmd(self, evt):
        if self.fsm.is_in_state(Character_State_Enum.WAITING_FOR_CMD):
            self.fsm.change_to_state(Character_State_Enum.SKILL)

    def set_picture(self, pic_path):
        self.sprite = pygame.image.load(pic_path).convert_alpha()

    def update(self, et):
        self.process_evt_queue()
        self.fsm.update(et)

    def draw(self, et):
        self.fsm.draw(et)

    def get_pos(self):
        return self.pos_x, self.pos_y

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        from Game import CGameApp
        lvl_map = CGameApp.get_instance().level_map
        tile = lvl_map.get_tile_by_coord(self.pos_x, self.pos_y)
        tile.occupy = True
        return

    def set_moving_target(self, x, y):
        self.moving_target_x = x
        self.moving_target_y = y
