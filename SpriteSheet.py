import pygame


class Sprite_Sheet(object):

    def __init__(self, tex_path, frame_w, frame_h, row_num, col_num):
        self.frames = []
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.img = pygame.image.load(tex_path).convert_alpha()
        for i in range(0, row_num):
            for j in range(0, col_num):
                sub_img = self.img.subsurface(j * self.frame_h, i * self.frame_w, self.frame_w, self.frame_h)
                self.frames.append(sub_img)

    def draw(self, fi, pos):
        from Game import CGameApp
        app = CGameApp.get_instance()
        app.screen.blit(
            self.frames[fi], ((pos[0] + app.offset_x, pos[1] + app.offset_y), (self.frame_w, self.frame_h)))
