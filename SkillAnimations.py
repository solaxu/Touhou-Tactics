from Event import *
import pygame


class Skill_Animation_Sheet(object):

    Frame_Time = 40

    def __init__(self, tex_path, frame_w, frame_h, row_num, col_num, begin, end, anim_len):
        self.frames = []
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.anim_len = anim_len
        self.img = pygame.image.load(tex_path).convert_alpha()
        self.total_frames = end - begin + 1
        for i in range(0, row_num):
            for j in range(0, col_num):
                if i * col_num + j >= self.total_frames:
                    return
                sub_img = self.img.subsurface(j * self.frame_h, i * self.frame_w, self.frame_w, self.frame_h)
                self.frames.append(sub_img)


class Skill_Anim_Drawer(EventObject):

    def __init__(self, skill_anim_sheet):
        self.acc = 0
        self.acc_time = 0
        self.skill_anim_sheet = skill_anim_sheet
        self.anim_time = 0
        self.show = True

    def stop(self):
        self.show = False

    def draw(self, et, pos, is_loop):
        if not self.show:
            return
        if self.acc_time > Skill_Animation_Sheet.Frame_Time.value:
            self.acc_time += et
            self.acc += 1
            self.acc %= self.skill_anim_sheet.total_frames
        self.anim_time += et
        if self.anim_time > self.skill_anim_sheet.anim_len:
            self.acc = 0
            self.acc_time = 0
            self.anim_time = 0
            if not is_loop:
                self.show = False
        else:
            from Game import CGameApp
            app = CGameApp.get_instance()
            app.screen.blit(self.frames[self.acc], ((pos[0] + app.offset_x, pos[1] + app.offset_y), (36, 36)))


class Skill_Animations(object):

    IMMORTAL = Skill_Animation_Sheet("Media/skills/Immortal.jpg", 192, 192, 5, 4, 0, 16, 680)
    AP_UP = Skill_Animation_Sheet("Media/skills/agi_ap_up.jpg", 192, 192, 5, 4, 0, 16, 680)
    MUSOFUIN = Skill_Animation_Sheet("Media/skills/musofuin.jpg", 192, 192, 5, 3, 0, 13, 560)
    FUMAJIN = Skill_Animation_Sheet("Media/skills/fumajin.jpg", 192, 192, 5, 3, 0, 11, 480)
