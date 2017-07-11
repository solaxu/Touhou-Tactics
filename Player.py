from enum import Enum
from Event import *
from FSM import *
from GUI import *

class Player_Enum(Enum):

    Player_State_Pick_Characters = 0
    Player_State_Ban_Characters = 1
    Player_State_In_Turn = 2
    Player_State_Victory = 3
    Player_State_Defeat = 4
    Player_State_Waiting= 5


class Player_State_Pick_Characters(FSM_State):

    def __init__(self, fsm):
        super(Player_State_Pick_Characters, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_Pick_Characters
        self.pick_tile = GuiLabel("pick_title", 20, 36, 360, 25, (0, 0, 0), 255, "", (255, 255, 255), None)


    def update(self, et):
        super(Player_State_Pick_Characters, self).update(et)
        
    def draw(self, et):
        super(Player_State_Pick_Characters, self).draw(et)
        self.pick_tile.draw(et)

    def enter(self):
        super(Player_State_Pick_Characters, self).enter()
        player = self.fsm.owner
        pick_title = str(player.team.name) + "'s Turn To Pick"
        self.pick_tile.set_text(pick_title, (255, 255, 255))
        
    def exit(self):
        super(Player_State_Pick_Characters, self).exit()


class Player_State_Ban_Characters(FSM_State):

    def __init__(self, fsm):
        super(Player_State_Ban_Characters, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_Ban_Characters
        self.ban_tile = GuiLabel("ban_title", 20, 36, 360, 25, (0, 0, 0), 255, "", (255, 255, 255), None)

    def update(self, et):
        super(Player_State_Ban_Characters, self).update(et)

    def draw(self, et):
        super(Player_State_Ban_Characters, self).draw(et)
        self.ban_tile.draw(et)

    def enter(self):
        super(Player_State_Ban_Characters, self).enter()
        player = self.fsm.owner
        ban_title = str(player.team.name) + "'s Turn To Ban"
        self.ban_tile.set_text(ban_title, (255, 255, 255))

    def exit(self):
        super(Player_State_Ban_Characters, self).exit()


class Player_State_In_Turn(FSM_State):

    def __init__(self, fsm):
        super(Player_State_In_Turn, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_In_Turn

    def update(self, et):
        super(Player_State_In_Turn, self).update(et)
        self.fsm.owner.team.update(et)

    def draw(self, et):
        super(Player_State_In_Turn, self).draw(et)
        self.fsm.owner.team.draw(et)

    def enter(self):
        super(Player_State_In_Turn, self).enter()

    def exit(self):
        super(Player_State_In_Turn, self).exit()

class Player_State_Victory(FSM_State):

    def __init__(self, fsm):
        super(Player_State_Victory, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_Victory

    def update(self, et):
        super(Player_State_Victory, self).update(et)

    def draw(self, et):
        super(Player_State_Victory, self).draw(et)
        self.fsm.owner.team.draw(et)

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
        self.fsm.owner.team.update(et)

    def draw(self, et):
        super(Player_State_Defeat, self).draw(et)
        self.fsm.owner.team.draw(et)

    def enter(self):
        super(Player_State_Defeat, self).enter()

    def exit(self):
        super(Player_State_Defeat, self).exit()

class Player_State_Waiting(FSM_State):

    def __init__(self, fsm):
        super(Player_State_Waiting, self).__init__(fsm)
        self.sn = Player_Enum.Player_State_Waiting

    def update(self, et):
        super(Player_State_Waiting, self).update(et)
        self.fsm.owner.team.update(et)

    def draw(self, et):
        super(Player_State_Waiting, self).draw(et)
        self.fsm.owner.team.draw(et)

    def enter(self):
        super(Player_State_Waiting, self).enter()

    def exit(self):
        super(Player_State_Waiting, self).exit()

class Player(EventObject):

    def __init__(self):
        super(Player, self).__init__()
        self.team = None
        self.fsm = FSM_Machine(self)

        # add states
        self.fsm.add_state(Player_State_Pick_Characters(self.fsm))
        self.fsm.add_state(Player_State_Ban_Characters(self.fsm))
        self.fsm.add_state(Player_State_In_Turn(self.fsm))
        self.fsm.add_state(Player_State_Victory(self.fsm))
        self.fsm.add_state(Player_State_Defeat(self.fsm))
        self.fsm.add_state(Player_State_Waiting(self.fsm))

        # add handlers
        self.add_handler(EventType.MOUSE_LBTN_DOWN, self.mouse_lbtn_down)
        
    def update(self, et):
        self.process_evt_queue()
        self.fsm.update(et)
        
    def draw(self, et):
        self.fsm.draw(et)

    def set_team(self, team):
        self.team = team

    def calculate_buffs(self):
        from Game import CGameApp
        characters = CGameApp.get_instance().characters
        for character_name in self.team.characters:
            character = characters[character_name]
            if character.immortal:
                character.buffs = []
                character.buff_aura = {}
            else:
                character.immortal = False
                character.fuin = False

                AP = character.base_ap
                HP = character.base_hp
                MP = character.base_mp
                AGI = character.base_agility
                STR = character.base_strength
                INT = character.base_intelligence
                DEF = character.base_defense
                RES = character.base_resistance
                ATK = character.base_attack

                for buff in character.buffs:
                    if buff.DELAY_TIME <= 0:
                        AP += buff.AP
                        HP += buff.HP
                        MP += buff.MP
                        STR += buff.STR
                        AGI += buff.AGI
                        INT += buff.INT
                        DEF += buff.DEF
                        RES += buff.RES
                        ATK += buff.ATK
                    else:
                        buff.DELAY_TIME -= 1

                    if buff.IMMORTAL:
                        character.immortal = True
                    if buff.FUIN:
                        character.fuin = True

                for (name, buff) in character.buff_aura.items():
                    if buff.DELAY_TIME <= 0:
                        AP += buff.AP
                        HP += buff.HP
                        MP += buff.MP
                        STR += buff.STR
                        AGI += buff.AGI
                        INT += buff.INT
                        DEF += buff.DEF
                        RES += buff.RES
                        ATK += buff.ATK
                    else:
                        buff.DELAY_TIME -= 1

                    if buff.IMMORTAL:
                        character.immortal = True
                    if buff.FUIN:
                        character.fuin = True

                character.ap = AP
                print "AP: "+ str(AP)
                character.hp = HP
                character.mp = MP
                character.agility = AGI
                character.strength = STR
                character.intelligence = INT
                character.defense = DEF
                character.resistance = RES
                character.attack = ATK


    def mouse_lbtn_down(self, evt):
        from LocalInput import LocalInput
        from Map import QuadTreeForTile
        from Game import CGameApp
        from Team import*
        mouse_x = LocalInput.mouse_pos[0]
        mouse_y = LocalInput.mouse_pos[1]
        app = CGameApp.get_instance()
        bp_ui = app.gui_manager.character_bp
        if self.fsm.is_in_state(Player_Enum.Player_State_Pick_Characters):
            for character_btn in bp_ui.character_pool_btn:
                if QuadTreeForTile.check_tile(character_btn.x, character_btn.y, character_btn.w, character_btn.h,
                                              mouse_x, mouse_y, 0, 0) and character_btn.in_character_pool:
                    if character_btn.in_character_pool:
                        character_btn.in_character_pool = False
                        if self.team.name == Team_Enum.TEAM_RED:
                            bp_ui.character_red_pick.append(character_btn)
                            app.team_red.add_character(app.characters[character_btn.name])
                        elif self.team.name == Team_Enum.TEAM_BLUE:
                            bp_ui.character_blue_pick.append(character_btn)
                            app.team_blue.add_character(app.characters[character_btn.name])
                    print "Pick Character"
                    self.send_event(CGameApp.get_instance(), Event(EventType.GAME_BAN_PICK_TURN))
        elif self.fsm.is_in_state(Player_Enum.Player_State_Ban_Characters):
            for character_btn in bp_ui.character_pool_btn:
                if QuadTreeForTile.check_tile(character_btn.x, character_btn.y, character_btn.w, character_btn.h,
                                              mouse_x, mouse_y, 0, 0) and character_btn.in_character_pool:
                    if character_btn.in_character_pool:
                        character_btn.in_character_pool = False
                        if self.team.name == Team_Enum.TEAM_RED:
                            bp_ui.character_red_ban.append(character_btn)
                        elif self.team.name == Team_Enum.TEAM_BLUE:
                            bp_ui.character_blue_ban.append(character_btn)
                    print "Ban Character"
                    self.send_event(CGameApp.get_instance(), Event(EventType.GAME_BAN_PICK_TURN))
        elif self.fsm.is_in_state(Player_Enum.Player_State_In_Turn):
            print str(self.team.name) + "'s turn"
            self.send_event(self.team, evt)
        elif self.fsm.is_in_state(Player_Enum.Player_State_Waiting):
            print str(self.team.name) + " is waiting for its turn"
