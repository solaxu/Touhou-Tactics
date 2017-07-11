# _*_ coding: utf-8 _*_

from enum import Enum
from SkillAnimations import *

class Skill_Enum(Enum):

    SINGLE_TARGET = 1000
    AOE = 1001

    BUFF_STR = 1002
    BUFF_AGI = 1003
    BUFF_INT = 1004
    BUFF_AP = 1005
    BUFF_HP = 1006
    BUFF_MP = 1007

    DEBUFF_STR = 1008
    DEBUFF_AGI = 1009
    DEBUFF_INT = 1010
    DEBUFF_AP = 1011
    DEBUFF_HP = 1012
    DEBUFF_MP = 1013

    BUFF_ATK = 1014
    BUFF_DEF = 1015
    BUFF_RES = 1016

    DEBUFF_ATK = 1017
    DEBUFF_DEF = 1018
    DEBUFF_RES = 1019

    BUFF_NONE = 1020
    DEBUFF_NONE = 1021

    BUFF_IMMORTAL = 1022

    DEBUFF_FUIN = 1023 #

# Reimu
    Hakurei_Reimu_MuSouTenSei = 0               # immortal, skill & attack immune
    Hakurei_Reimu_MuGenNoKoSoKuKiGanSaTsu = 1   # ap up
    Hakurei_Reimu_MuSoFuin = 2                  # lock target, can not Move\Attack\Items\Spell
    Hakurei_Reimu_FuMaJin = 3                   # AOE, lock targets, can not Move\Attack\Items\Spell, CAN NOT MOVE, ULT

# Marisa
    Kirisame_Marisa_SatelliteIllusion = 0   # AOE
    Kirisame_Marisa_BlazingStar = 1         # Big bang. Position translated, AOE
    Kirisame_Marisa_BlazeAway = 2           # multiple-attack
    Kirisame_Marisa_MasterSpark = 3         # ULT, cost all ap, dmg depend ap


class Skill_Buff(object):

    def __init__(self, name, src_character, target_character):
        self.name = name
        self.AP = 0
        self.HP = 0
        self.MP = 0
        self.STR = 0
        self.AGI = 0
        self.INT = 0
        self.DEF = 0
        self.RES = 0
        self.ATK = 0
        self.HEALING = 0
        self.MANA_SUP = 0
        self.IMMORTAL = False
        self.REMAIN_TIME = 1
        self.START_TIME = 0
        self.DELAY_TIME = 0
        self.FUIN = False
        self.src_character = src_character
        self.target_character = target_character


class Skill(object):

    def __init__(self, name, rng, dmg, buff, debuff, desc, anim):
        self.type = None
        self.name = name
        self.dmg = dmg
        self.rng = rng
        self.aoe_rng = 0
        self.buff = buff
        self.debuff = debuff
        self.desc = desc
        self.anim = anim
        self.lvl = 1
        self.duration = 1
        self.targets = []
        self.cool_down = 0
        self.refresh_time = 0
        self.emit_time = 0

    def get_icon(self):
        if self.anim is not None:
            return self.anim.get_icon()

    def emit(self, character, enemies, allies):
        from Game import CGameApp
        if self.refresh_time > 0:
            return
        self.emit_time = CGameApp.get_instance().total_turn
        self.refresh_time = self.cool_down
        print "Emit Skill"

    def upgrade(self):
        pass

    def update(self, et):
        from Game import CGameApp
        app = CGameApp.get_instance()
        self.refresh_time = self.emit_time + self.cool_down - app.total_turn


class Skill_Single_Target(Skill):

    def __init__(self, name, rng, dmg, buff, debuff, desc, anim):
        super(Skill_Single_Target, self).__init__(name, rng, dmg, buff, debuff, desc, anim)
        self.type = Skill_Enum.SINGLE_TARGET

class Skill_AOE(Skill):
    
    def __init__(self, name, rng, dmg, buff, debuff, desc, anim, aoe_rng):
        super(Skill_AOE, self).__init__(name, rng, dmg, buff, debuff, desc, anim)
        self.type = Skill_Enum.AOE
        self.aoe_rng = aoe_rng


#
class Hakurei_Reimu_MuSouTenSei(Skill_Single_Target):

    def __init__(self):
        super(Hakurei_Reimu_MuSouTenSei, self).__init__(
            "MuSouTenSei", 0, 0, Skill_Enum.BUFF_IMMORTAL,
            Skill_Enum.DEBUFF_NONE, "MuSouTenSei, Lv: 1. Immune skills and attacks. Duration: 2 turns. Cool Down: 8 turns",
            Skill_Anim_Drawer(Skill_Animations.IMMORTAL))
        self.cool_down = 8

    def upgrade(self):
        self.lvl += 1
        self.duration = self.lvl + 1
        self.desc = "MuSouTenSei, Lv: %s. Immune skills and attacks. Duration: %s turns. Cool Down: %s turns" % (self.lvl, self.duration, self.refresh_time)

    def emit(self, character, enemies, allies):
        super(Hakurei_Reimu_MuSouTenSei, self).emit(character, enemies, allies)
        from Game import CGameApp
        app = CGameApp.get_instance()
        if character is None:
            return

        for ally in allies:
            skill_drawer = Skill_Anim_Drawer(Skill_Animations.IMMORTAL)
            skill_drawer.pos = (ally.pos_x, ally.pos_y)
            skill_drawer.is_loop = False
            app.cur_player.skills_objects.add_data(skill_drawer)
            buff = Skill_Buff("MuSouTenSei", character, ally)
            buff.IMMORTAL = True
            buff.REMAIN_TIME = self.duration
            buff.START_TIME = app.total_turn
            character.send_event(ally, Event_Skill(EventType.CHARACTER_AURA, buff))


class Hakurei_Reimu_MuGenNoKoSoKuKiGanSaTsu(Skill_Single_Target):

    def __init__(self):
        super(Hakurei_Reimu_MuGenNoKoSoKuKiGanSaTsu, self).__init__(
            "MuGenNoKoSoKuKiGanSaTsu", 0, 0, Skill_Enum.BUFF_AP,
            Skill_Enum.DEBUFF_NONE, "MuGenNoKoSoKuKiGanSaTsu, Lv: 1. Bonus 3 action points. Duration: 1 turn. Cool Down: 5 turns",
            Skill_Anim_Drawer(Skill_Animations.AP_UP)
        )
        self.ap_buff = 3
        self.cool_down = 5

    def upgrade(self):
        self.lvl += 1
        self.ap_buff += 1
        self.desc = "MuGenNoKoSoKuKiGanSaTsu, Lv: %s. Bonus more %s action points. Duration: 1 turn. Cool Down: %s turns" % (self.lvl, self.ap_buff, self.refresh_time)

    def emit(self, character, enemies, allies):
        super(Hakurei_Reimu_MuGenNoKoSoKuKiGanSaTsu, self).emit(character, enemies, allies)
        from Game import CGameApp
        app = CGameApp.get_instance()
        if character is None:
            return

        for ally in allies:
            skill_drawer = Skill_Anim_Drawer(Skill_Animations.AP_UP)
            skill_drawer.pos = (ally.pos_x, ally.pos_y)
            skill_drawer.is_loop = False
            app.cur_player.skills_objects.add_data(skill_drawer)
            buff = Skill_Buff("MuGenNoKoSoKuKiGanSaTsu", character, ally)
            buff.AP = self.ap_buff
            buff.REMAIN_TIME = self.duration
            buff.START_TIME = app.total_turn
            character.send_event(ally, Event_Skill(EventType.CHARACTER_AURA, buff))


class Hakurei_Reimu_MuSoFuin(Skill_Single_Target):

    def __init__(self):
        super(Hakurei_Reimu_MuSoFuin, self).__init__(
            "MuSoFuin", 4, 0, Skill_Enum.BUFF_NONE,
            Skill_Enum.DEBUFF_FUIN, "MuSoFuin, Lv: 1. Lock one target after 2 turns. Duration 1 turn. Cool Down: 10 turns",
            Skill_Anim_Drawer(Skill_Animations.MUSOFUIN)
        )
        self.cool_down = 10
        self.delay_time = 2

    def upgrade(self):
        self.lvl += 1
        self.duration += 1
        self.desc = "MuSoFuin, Lv: %s. Lock one target after 2 turns. Duration: %s turns. Cool Down: %s turns." % (self.lvl, self.duration, self.refresh_time)

    def emit(self, character, enemies, allies):
        super(Hakurei_Reimu_MuSoFuin, self).emit(character, enemies, allies)
        from Game import CGameApp
        app = CGameApp.get_instance()
        if character is None:
            return

        for ally in allies:
            skill_drawer = Skill_Anim_Drawer(Skill_Animations.MUSOFUIN)
            skill_drawer.pos = (ally.pos_x, ally.pos_y)
            skill_drawer.is_loop = False
            app.cur_player.skills_objects.add_data(skill_drawer)
            buff = Skill_Buff("MuSoFuin", character, ally)
            buff.REMAIN_TIME = self.duration
            buff.START_TIME = app.total_turn
            buff.DELAY_TIME = 2
            character.send_event(ally, Event_Skill(EventType.CHARACTER_AURA, buff))


class Hakurei_Reimu_FuMaJin(Skill_AOE):

    def __init__(self):
        super(Hakurei_Reimu_FuMaJin, self).__init__(
            "FuMaJin", 5, 0, Skill_Enum.BUFF_NONE,
            Skill_Enum.DEBUFF_FUIN, "FuMaJin, Lv: 1. Lock targets in target area, ReiMu can not do actions. Duration: 2 turns. Cool Down: 15 turns",
            Skill_Anim_Drawer(Skill_Animations.FUMAJIN), 1
        )
        self.cool_down = 15

    def upgrade(self):
        self.lvl += 1
        self.duration += 1
        if self.lvl % 2 == 0:
            self.aoe_rng += 1
        self.desc = "FuMaJin, Lv: %s. Lock targets in target area, ReiMu can not do actions. Duration: %s turns. Cool Down: %s turn" % (self.lvl, self.duration, self.refresh_time)

    def emit(self, character, enemies, allies):
        super(Hakurei_Reimu_FuMaJin, self).emit(character, enemies, allies)
        from Game import CGameApp
        app = CGameApp.get_instance()
        if character is None:
            return

        for ally in allies:
            if ally.name != character.name:
                skill_drawer = Skill_Anim_Drawer(Skill_Animations.FUMAJIN)
                skill_drawer.pos = (ally.pos_x, ally.pos_y)
                skill_drawer.is_loop = False
                app.cur_player.skills_objects.add_data(skill_drawer)
                buff = Skill_Buff("FuMaJin", character, ally)
                buff.FUIN = True
                buff.REMAIN_TIME = self.duration
                buff.START_TIME = app.total_turn
                character.send_event(ally, Event_Skill(EventType.CHARACTER_AURA, buff))

        for enemy in enemies:
            skill_drawer = Skill_Anim_Drawer(Skill_Animations.FUMAJIN)
            skill_drawer.pos = (enemy.pos_x, enemy.pos_y)
            skill_drawer.is_loop = False
            app.cur_player.skills_objects.add_data(skill_drawer)
            buff = Skill_Buff("FuMaJin", character, enemy)
            buff.FUIN = True
            buff.REMAIN_TIME = self.duration
            buff.START_TIME = app.total_turn
            character.send_event(enemy, Event_Skill(EventType.CHARACTER_AURA, buff))
