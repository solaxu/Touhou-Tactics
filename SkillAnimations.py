from Event import *
import pygame


class Skill_Animation_Sheet(object):

    def __init__(self, tex_path, frame_w, frame_h, row_num, col_num, begin, end, anim_len, frame_time, icon_frame):
        self.frames = []
        self.frame_w = frame_w
        self.frame_time = frame_time
        self.frame_h = frame_h
        self.anim_len = anim_len
        self.img = pygame.image.load(tex_path).convert_alpha()
        self.total_frames = end - begin + 1
        self.icon_frame = icon_frame
        for i in range(0, row_num):
            for j in range(0, col_num):
                sub_img = self.img.subsurface(j * self.frame_h, i * self.frame_w, self.frame_w, self.frame_h)
                _sub_img = pygame.transform.scale(sub_img, (36, 36))
                self.frames.append(_sub_img)
                if i * col_num + j >= self.total_frames:
                    self.icon = self.frames[self.icon_frame]
                    return

    def get_icon(self):
        return self.icon

class Skill_Anim_Drawer(EventObject):

    def __init__(self, skill_anim_sheet):
        self.acc = 0
        self.acc_time = 0
        self.skill_anim_sheet = skill_anim_sheet
        self.anim_time = 0
        self.show = True
        self.loops = 0
        self.pos = (0, 0)
        self.is_loop = False

    def stop(self):
        self.show = False

    def get_icon(self):
        return self.skill_anim_sheet.get_icon()

    def draw(self, et):
        if not self.show:
            return
        self.anim_time += et
        self.acc_time += et
        if self.acc_time > self.skill_anim_sheet.frame_time:
            self.acc += 1
            self.acc_time = 0
            self.acc %= self.skill_anim_sheet.total_frames
        if self.anim_time > self.skill_anim_sheet.anim_len:
            self.acc = 0
            self.acc_time = 0
            self.anim_time = 0
            self.loops += 1
            if not self.is_loop:
                self.show = False
        else:
            from Game import CGameApp
            app = CGameApp.get_instance()
            app.screen.blit(self.skill_anim_sheet.frames[self.acc], ((self.pos[0] + app.offset_x, self.pos[1] + app.offset_y), (36, 36)))


class Skill_Animations(object):

    IMMORTAL = None
    AP_UP = None
    MUSOFUIN = None
    FUMAJIN = None

    @staticmethod
    def load_skill_res():
        # Reimu
        Skill_Animations.IMMORTAL = Skill_Animation_Sheet("Media/skills/Holy2.png", 192, 192, 6, 5, 0, 6, 70, 10, 6)
        Skill_Animations.AP_UP = Skill_Animation_Sheet("Media/skills/Recovery1.png", 192, 192, 6, 5, 0, 14, 150, 10, 8)
        Skill_Animations.MUSOFUIN = Skill_Animation_Sheet("Media/skills/Curse.png", 192, 192, 4, 5, 0, 9, 100, 10, 9)
        Skill_Animations.FUMAJIN = Skill_Animation_Sheet("Media/skills/Recovery3.png", 192, 192, 5, 5, 0, 21, 220, 10, 14)
