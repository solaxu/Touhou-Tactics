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


class Skill(object):

    def __init__(self, name, rng, dmg, buff, debuff, desc, anim):
        self.type = None
        self.name = name
        self.dmg = dmg
        self.rng = rng
        self.buff = buff
        self.debuff = debuff
        self.desc = desc
        self.anim = anim
        self.lvl = 1
        self.duration = 1

    def upgrade(self):
        pass


class Skill_Single_Target(Skill):

    def __init__(self, target, name, rng, dmg, buff, debuff, desc, anim):
        super(Skill_Single_Target, self).__init__(name, rng, dmg, buff, debuff, desc, anim)
        self.type = Skill_Enum.SINGLE_TARGET
        self.target = target

class Skill_AOE(Skill):
    
    def __init__(self, name, rng, dmg, buff, debuff, desc, anim, aoe_rng):
        super(Skill_AOE, self).__init__(name, rng, dmg, buff, debuff, desc, anim)
        self.type = Skill_Enum.AOE
        self.aoe_rng = aoe_rng


#
class Hakurei_Reimu_MuSouTenSei(Skill_Single_Target):

    def __init__(self, target):
        super(Hakurei_Reimu_MuSouTenSei, self).__init__(
            "MuSouTenSei", 0, 0, Skill_Enum.BUFF_IMMORTAL,
            Skill_Enum.DEBUFF_NONE, "Lv: 1\nImmune skills and attacks.\nDuration: 2 turns",
            Skill_Anim_Drawer(Skill_Animations.IMMORTAL))

    def upgrade(self):
        self.lvl += 1
        self.duration = self.lvl + 1
        self.desc = "Lv: %s\n Immune skills and attacks\nDuration: %s turns" % (self.lvl, self.duration)


class Hakurei_Reimu_MuGenNoKoSoKuKiGanSaTsu(Skill_Single_Target):

    def __init__(self, target):
        super(Hakurei_Reimu_MuGenNoKoSoKuKiGanSaTsu, self).__init__(
            "MuGenNoKoSoKuKiGanSaTsu", 0, 0, Skill_Enum.BUFF_AP,
            Skill_Enum.DEBUFF_NONE, "Lv: 1\nGain more 3 action points\nDuration: 1 turn",
            Skill_Anim_Drawer(Skill_Animations.AP_UP)
        )
        self.ap_buff = 3

    def upgrade(self):
        self.lvl += 1
        self.ap_buff += 1
        self.desc = "Lv: %s\nGain more %s action points\nDuration: 1 turn" % (self.lvl, self.ap_buff)

class Hakurei_Reimu_MuSoFuin(Skill_Single_Target):

    def __init__(self, target):
        super(Hakurei_Reimu_MuSoFuin, self).__init__(
            "MuSoFuin", 4, 0, Skill_Enum.BUFF_NONE,
            Skill_Enum.DEBUFF_FUIN, "Lv: 1\nLock one target after 2 turns\nDuration 1 turn",
            Skill_Anim_Drawer(Skill_Animations.MUSOFUIN)
        )

    def upgrade(self):
        self.lvl += 1
        self.duration += 1
        self.desc = "Lv: %s\n Lock one target after 2 turns\nDuration: %s turns" % (self.lvl, self.duration)

class Hakurei_Reimu_FuMaJin(Skill_AOE):

    def __init__(self):
        super(Hakurei_Reimu_FuMaJin, self).__init__(
            "FuMaJin", 5, 0, Skill_Enum.BUFF_NONE,
            Skill_Enum.DEBUFF_FUIN, "Lv: 1\nLock targets in target area, ReiMu can not do actions\nDuration: 2 turns",
            Skill_Anim_Drawer(Skill_Animations.FUMAJINkill)
        )

    def upgrade(self):
        self.lvl += 1
        self.duration += 1
        self.desc = "Lv: %s\nLock targets in target area, ReiMu can not do actions\nDuration: %s turns" % (self.lvl, self.duration)