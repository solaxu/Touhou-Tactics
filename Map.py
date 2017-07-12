# _*_ coding: utf-8 _*_

import pygame
from SpriteSheet import *
from enum import Enum
import csv
import Queue
from Tile import *
from Event import *
from FSM import *


class LevelMap(EventObject):

    def __init__(self, name):
        super(LevelMap, self).__init__()
        self.name = name
        self.tile_rows = 0
        self.tile_cols = 0
        self.tile_width = 0
        self.tile_height = 0
        self.mini_map_width = 0
        self.mini_map_height = 0
        self.mini_map_pos_x = 0
        self.mini_map_pos_y = 0
        self.mini_map_ratio_x = 0.0
        self.mini_map_ratio_y = 0.0
        self.tile_sets = {}
        self.tile_imgs = {}
        self.tiles = []
        self.skilled_tiles = []
        self.quad_root = None
        self.render_quads = []
        self.mini_map_show = False
        self.team_red = None
        self.team_blue = None
        self.fsm = FSM_Machine(self)

        # for A* algorithm
        self.open_list = Queue.PriorityQueue()
        self.close_list = Queue.PriorityQueue()

    def create(self):
        return

    def update(self, et):
        return

    def draw(self, et):
        return

    def get_tile_by_coord(self, x, y):
        ix = x / self.tile_width
        iy = y / self.tile_height
        return self.get_tile_by_index(ix, iy)

    def get_tile_by_index(self, ix, iy):
        index = iy * self.tile_cols + ix
        if index >= self.tile_rows * self.tile_cols:
            return None
        return self.tiles[index]

    def get_tile_index(self, tile):
        return (tile.pos_x / self.tile_width, tile.pos_y / self.tile_height)

    def reset_map(self):
        for quad in self.render_quads:
            for tile in quad.tiles:
                tile.reset()

    def reset_skill_map(self):
        self.skilled_tiles = []
        for quad in self.render_quads:
            for tile in quad.tiles:
                tile.skill_marked = False
                tile.skill_step = 0

    def select_tile_by_mouse(self, mouse_pos):
        from Game import CGameApp
        app = CGameApp.get_instance()
        x = mouse_pos[0] - int(app.offset_x)
        y = mouse_pos[1] - int(app.offset_y)
        return self.get_tile_by_coord(x, y)

    def init_a_star_open_list(self, c_x, c_y, t_x, t_y, start_tile):
        self.open_list = Queue.PriorityQueue()
        self.close_list = Queue.PriorityQueue()
        if c_x > 0:
            x = c_x - 1
            tile = self.get_tile_by_index(x, c_y)
            tile.G = abs(t_x - x) + abs(t_y - c_y)
#            print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if not tile.occupy:
                tile.parent_tile = start_tile
                tile.in_open_list = True
                self.open_list.put(tile)
        if c_x < self.tile_rows - 1:
            x = c_x + 1
            tile = self.get_tile_by_index(x, c_y)
            tile.G = abs(t_x - x) + abs(t_y - c_y)
#            print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if not tile.occupy:
                tile.parent_tile = start_tile
                tile.in_open_list = True
                self.open_list.put(tile)
        if c_y > 0:
            y = c_y - 1
            tile = self.get_tile_by_index(c_x, y)
            tile.G = abs(t_x - c_x) + abs(t_y - y)
#            print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if not tile.occupy:
                tile.parent_tile = start_tile
                tile.in_open_list = True
                self.open_list.put(tile)
        if c_y < self.tile_cols - 1:
            y = c_y + 1
            tile = self.get_tile_by_index(c_x, y)
            tile.G = abs(t_x - c_x) + abs(t_y - y)
#            print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if not tile.occupy:
                tile.parent_tile = start_tile
                tile.in_open_list = True
                self.open_list.put(tile)

    def a_star_path_finding(self, t_x, t_y, target_tile):
#        print "Target info: H %s G %s Pos_x %s Pos_y %s" % (target_tile.H, target_tile.G, target_tile.pos_x, target_tile.pos_y)
        while (not self.open_list.empty()) and (not target_tile.in_open_list):
            otile = self.open_list.get()
            otile.in_close_list = True
            self.close_list.put(otile)

            c_x = otile.pos_x / self.tile_width
            c_y = otile.pos_y / self.tile_height
            if c_x > 0:
                x = c_x - 1
                tile = self.get_tile_by_coord(otile.pos_x - self.tile_width, otile.pos_y)
                # print "step: %s, H: %s" % (tile.step, tile.a_star_h)
                if (not tile.occupy) and (not tile.in_close_list) and tile.marked:
                    if not tile.in_open_list:
                        tile.parent_tile = otile
                        tile.in_open_list = True
                        tile.G = abs(t_x - x) + abs(t_y - c_y)
                        self.open_list.put(tile)
                    else:  # update tiles in open list
                        if tile.H < otile.H:
                            tile.parent_tile = otile
 #                   print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if c_x < self.tile_cols - 1:
                x = c_x + 1
                tile = self.get_tile_by_coord(otile.pos_x + self.tile_width, otile.pos_y)
                # print "step: %s, H: %s" % (tile.step, tile.a_star_h)
                if (not tile.occupy) and (not tile.in_close_list) and tile.marked:
                    if not tile.in_open_list:
                        tile.parent_tile = otile
                        tile.in_open_list = True
                        tile.G = abs(t_x - x) + abs(t_y - c_y)
                        self.open_list.put(tile)
                    else:  # update tiles in open list
                        if tile.H < otile.H:
                            tile.parent_tile = otile
 #                   print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if c_y > 0:
                y = c_y - 1
                tile = self.get_tile_by_coord(otile.pos_x, otile.pos_y - self.tile_height)
                # print "step: %s, H: %s" % (tile.step, tile.a_star_h)
                if (not tile.occupy) and (not tile.in_close_list) and tile.marked:
                    if not tile.in_open_list:
                        tile.parent_tile = otile
                        tile.in_open_list = True
                        tile.G = abs(t_x - c_x) + abs(t_y - y)
                        self.open_list.put(tile)
                    else:  # update tiles in open list
                        if tile.H < otile.H:
                            tile.parent_tile = otile
 #                   print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if c_y < self.tile_rows - 1:
                y = c_y + 1
                tile = self.get_tile_by_coord(otile.pos_x, otile.pos_y + self.tile_height)
                # print "step: %s, H: %s" % (tile.step, tile.a_star_h)
                if (not tile.occupy) and (not tile.in_close_list) and tile.marked:
                    if not tile.in_open_list:
                        tile.parent_tile = otile
                        tile.in_open_list = True
                        tile.G = abs(t_x - c_x) + abs(t_y - y)
                        self.open_list.put(tile)
                    else:  # update tiles in open list
                        if tile.H < otile.H:
                            tile.parent_tile = otile
#                    print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)

#   神TM三个bfs……踩得坑不够多. f**king 3 bfs functions...

    def bfs_travel_skill(self, tile, color, step):
        tile_queue = Queue.Queue()
        tile_queue.put(tile)

        while not tile_queue.empty():
            tile = tile_queue.get()
            tile.skill_marked = True
            tile.draw_skill_rect(color)
            self.skilled_tiles.append(tile)
            #            print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if tile.skill_step >= step:
                continue

            tile_i = self.get_tile_index(tile)

            # left
            left_ix = tile_i[0] - 1
            left_iy = tile_i[1]
            if left_ix > 0:
                left_tile = self.get_tile_by_index(left_ix, left_iy)
                if not left_tile.skill_marked:
                    left_tile.skill_step = tile.skill_step + 1
                    tile_queue.put(left_tile)

            # right
            right_ix = tile_i[0] + 1
            right_iy = tile_i[1]
            if right_ix < (self.tile_rows - 1):
                right_tile = self.get_tile_by_index(right_ix, right_iy)
                if not right_tile.skill_marked:
                    right_tile.skill_step = tile.skill_step + 1
                    tile_queue.put(right_tile)

            # up
            up_ix = tile_i[0]
            up_iy = tile_i[1] - 1
            if up_iy > 0:
                up_tile = self.get_tile_by_index(up_ix, up_iy)
                if not up_tile.skill_marked:
                    up_tile.skill_step = tile.skill_step + 1
                    tile_queue.put(up_tile)

            # down
            down_ix = tile_i[0]
            down_iy = tile_i[1] + 1
            if down_iy < (self.tile_cols - 1):
                down_tile = self.get_tile_by_index(down_ix, down_iy)
                if not down_tile.skill_marked:
                    down_tile.skill_step = tile.skill_step + 1
                    tile_queue.put(down_tile)

    def bfs_travel_no_occupy(self, tile, color, step):
        tile_queue = Queue.Queue()
        tile_queue.put(tile)

        while not tile_queue.empty():
            tile = tile_queue.get()
            tile.marked = True
            tile.color = color
            #            print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if tile.H >= step:
                continue

            tile_i = self.get_tile_index(tile)

            # left
            left_ix = tile_i[0] - 1
            left_iy = tile_i[1]
            if left_ix > 0:
                left_tile = self.get_tile_by_index(left_ix, left_iy)
                if not left_tile.marked:
                    left_tile.H = tile.H + 1
                    tile_queue.put(left_tile)

            # right
            right_ix = tile_i[0] + 1
            right_iy = tile_i[1]
            if right_ix < (self.tile_rows - 1):
                right_tile = self.get_tile_by_index(right_ix, right_iy)
                if not right_tile.marked:
                    right_tile.H = tile.H + 1
                    tile_queue.put(right_tile)

            # up
            up_ix = tile_i[0]
            up_iy = tile_i[1] - 1
            if up_iy > 0:
                up_tile = self.get_tile_by_index(up_ix, up_iy)
                if not up_tile.marked:
                    up_tile.H = tile.H + 1
                    tile_queue.put(up_tile)

            # down
            down_ix = tile_i[0]
            down_iy = tile_i[1] + 1
            if down_iy < (self.tile_cols - 1):
                down_tile = self.get_tile_by_index(down_ix, down_iy)
                if not down_tile.marked:
                    down_tile.H = tile.H + 1
                    tile_queue.put(down_tile)

    def bfs_travel(self, tile, color, step):
        tile_queue = Queue.Queue()
        tile_queue.put(tile)

        while not tile_queue.empty():
            tile = tile_queue.get()
            tile.marked = True
            tile.color = color
#            print "Tile info: H %s G %s Pos_x %s Pos_y %s" % (tile.H, tile.G, tile.pos_x, tile.pos_y)
            if tile.H >= step:
                continue

            tile_i = self.get_tile_index(tile)

            # left
            left_ix = tile_i[0] - 1
            left_iy = tile_i[1]
            if left_ix > 0:
                left_tile = self.get_tile_by_index(left_ix, left_iy)
                if not (left_tile.marked or left_tile.occupy):
                    left_tile.H = tile.H + 1
                    tile_queue.put(left_tile)

            # right
            right_ix = tile_i[0] + 1
            right_iy = tile_i[1]
            if right_ix < (self.tile_rows - 1):
                right_tile = self.get_tile_by_index(right_ix, right_iy)
                if not (right_tile.marked or right_tile.occupy):
                    right_tile.H = tile.H + 1
                    tile_queue.put(right_tile)

            # up
            up_ix = tile_i[0]
            up_iy = tile_i[1] - 1
            if up_iy > 0:
                up_tile = self.get_tile_by_index(up_ix, up_iy)
                if not (up_tile.marked or up_tile.occupy):
                    up_tile.H = tile.H + 1
                    tile_queue.put(up_tile)

            # down
            down_ix = tile_i[0]
            down_iy = tile_i[1] + 1
            if down_iy < (self.tile_cols - 1):
                down_tile = self.get_tile_by_index(down_ix, down_iy)
                if not (down_tile.marked or down_tile.occupy):
                    down_tile.H = tile.H + 1
                    tile_queue.put(down_tile)

class Prototype_Map_Enum(Enum):
    
    TILE_ROW_NUM = 96
    TILE_COL_NUM = 96
    TILE_WIDTH = 36
    TILE_HEIGHT = 36
    TILE_SET_OUTSIDE_A5 = 100
    TILE_SET_OUTSIDE_B = 101
    TILE_SET_MAGIC_CIRCLE = 102
    TILE_SET_MINI_MAP = 103
    TILE_BASE = 0
    TILE_BORDER = 1
    TILE_WALL = 2
    TILE_TELEPORTER = 3
    TILE_SAFE_AREA = 4
    TILE_KEEPER = 5
    TILE_MAGIC_CIRCLR = 6
    TILE_RESOURCE = 7
    TILE_SAND = 8
    TILE_TREE = 9
    TILE_GRASS = 10
    MINI_MAP_WIDTH = 576
    MINI_MAP_HEIGHT = 576
    MINI_MAP_CELL_WIDTH = 6
    MINI_MAP_CELL_HEIGHT = 6

# quad tree for tiles 

class QuadTreeForTile(object):
    
    LEFT_UP = 0
    RIGHT_UP = 1
    LEFT_DOWN = 2
    RIGHT_DOWN = 3
        
    def __init__(self, x, y, width, height, tile_rows, tile_cols):
        self.tile_rows = tile_rows
        self.tile_cols = tile_cols
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tiles = []
        self.children_nodes = []

    @staticmethod
    def check_tile(x, y, w, h, pos_x, pos_y, r_w, r_h):
        se_x = x + w
        se_y = y + h
        te_x = pos_x + r_w
        te_y = pos_y + r_h
        reject = pos_x > se_x or te_x < x or pos_y > se_y or te_y < y
        if reject:
            return False
        return True

    @staticmethod
    def build_quad_tree(x, y, width, height, root, depth):
        if depth >= 4:
            return
        child_tile_rows = root.tile_rows / 2
        child_tile_cols = root.tile_cols / 2
        child_width = Prototype_Map_Enum.TILE_WIDTH.value * child_tile_rows
        child_height = Prototype_Map_Enum.TILE_HEIGHT.value * child_tile_cols

        left_up_x = x
        left_up_y = y
        left_up = QuadTreeForTile(left_up_x, left_up_y, child_width, child_height, child_tile_rows, child_tile_cols)

        right_up_x = x + child_width
        right_up_y = y
        right_up = QuadTreeForTile(right_up_x, right_up_y, child_width, child_height, child_tile_rows, child_tile_cols)

        left_down_x = x
        left_down_y = y + child_height
        left_down = QuadTreeForTile(left_down_x, left_down_y, child_width, child_height, child_tile_rows, child_tile_cols)

        right_down_x = x + child_width
        right_down_y = y + child_height
        right_down = QuadTreeForTile(right_down_x, right_down_y, child_width, child_height, child_tile_rows, child_tile_cols)

        # children
        for tile in root.tiles:
            # left-up
            if QuadTreeForTile.check_tile(left_up_x, left_up_y, child_width, child_height, tile.pos_x, tile.pos_y, tile.width, tile.height):
                left_up.tiles.append(tile)
            # right-up
            if QuadTreeForTile.check_tile(right_up_x, right_up_y, child_width, child_height, tile.pos_x, tile.pos_y, tile.width, tile.height):
                right_up.tiles.append(tile)
            # left-down
            if QuadTreeForTile.check_tile(left_down_x, left_down_y, child_width, child_height, tile.pos_x, tile.pos_y, tile.width, tile.height):
                left_down.tiles.append(tile)
            # right-down
            if QuadTreeForTile.check_tile(right_down_x, right_down_y, child_width, child_height, tile.pos_x, tile.pos_y, tile.width, tile.height):
                right_down.tiles.append(tile)

        root.children_nodes.append(left_up)
        QuadTreeForTile.build_quad_tree(left_up_x, left_up_y, child_width, child_height, left_up, depth + 1)

        QuadTreeForTile.build_quad_tree(right_up_x, right_up_y, child_width, child_height, right_up, depth + 1)
        root.children_nodes.append(right_up)

        QuadTreeForTile.build_quad_tree(left_down_x, left_down_y, child_width, child_height, left_down, depth + 1)
        root.children_nodes.append(left_down)

        QuadTreeForTile.build_quad_tree(right_down_x, right_down_y, child_width, child_height, right_down, depth + 1)
        root.children_nodes.append(right_down)

# Prototype Map States

class Map_State_Enum(Enum):

    MAP_NORMAL = 0
    MAP_SHOW_MINI_MAP = 1


class Map_State_Normal(FSM_State):
    def __init__(self, fsm):
        super(Map_State_Normal, self).__init__(fsm)
        self.sn = Map_State_Enum.MAP_NORMAL

    def enter(self):
        super(Map_State_Normal, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Map_State_Normal, self).update(et)

    def draw(self, et):
        super(Map_State_Normal, self).draw(et)

    def exit(self):
        super(Map_State_Normal, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

class Map_State_Show_MiniMap(FSM_State):
    def __init__(self, fsm):
        super(Map_State_Show_MiniMap, self).__init__(fsm)
        self.sn = Map_State_Enum.MAP_SHOW_MINI_MAP

    def enter(self):
        super(Map_State_Show_MiniMap, self).enter()
        # print self.fsm.owner.name + " enter state " + str(self.sn)

    def update(self, et):
        super(Map_State_Show_MiniMap, self).update(et)

    def draw(self, et):
        super(Map_State_Show_MiniMap, self).draw(et)
        lvl_map = self.fsm.owner
        from Game import CGameApp
        app = CGameApp.get_instance()
        app.screen.blit(lvl_map.tile_sets[Prototype_Map_Enum.TILE_SET_MINI_MAP],
                        ((lvl_map.mini_map_pos_x, lvl_map.mini_map_pos_y),
                         (lvl_map.mini_map_width, lvl_map.mini_map_height)))
        rect_x = float(lvl_map.mini_map_width) / lvl_map.mini_map_ratio_x
        rect_y = float(lvl_map.mini_map_height) / lvl_map.mini_map_ratio_y
        off_x = float(app.offset_x) / lvl_map.mini_map_ratio_x
        off_y = float(app.offset_y) / lvl_map.mini_map_ratio_y
        off_x = lvl_map.mini_map_pos_x - off_x
        off_y = lvl_map.mini_map_pos_y - off_y
        pygame.draw.rect(app.screen, (0, 255, 0), (off_x, off_y, rect_x, rect_y), 2)

        # show character icons
        for (name, character) in app.team_red.characters.items():
            x = character.pos_x / Prototype_Map_Enum.TILE_WIDTH.value * Prototype_Map_Enum.MINI_MAP_CELL_WIDTH.value + lvl_map.mini_map_pos_x
            y = character.pos_y / Prototype_Map_Enum.TILE_HEIGHT.value * Prototype_Map_Enum.MINI_MAP_CELL_HEIGHT.value + lvl_map.mini_map_pos_y
            pygame.draw.rect(app.screen, (255, 0, 0), (x, y, Prototype_Map_Enum.MINI_MAP_CELL_WIDTH.value, Prototype_Map_Enum.MINI_MAP_CELL_HEIGHT.value), 2)

        for (name, character) in app.team_blue.characters.items():
            x = character.pos_x / Prototype_Map_Enum.TILE_WIDTH.value * Prototype_Map_Enum.MINI_MAP_CELL_WIDTH.value + lvl_map.mini_map_pos_x
            y = character.pos_y / Prototype_Map_Enum.TILE_HEIGHT.value * Prototype_Map_Enum.MINI_MAP_CELL_HEIGHT.value + lvl_map.mini_map_pos_y
            pygame.draw.rect(app.screen, (0, 0, 255), (x, y, Prototype_Map_Enum.MINI_MAP_CELL_WIDTH.value, Prototype_Map_Enum.MINI_MAP_CELL_HEIGHT.value), 2)

    def exit(self):
        super(Map_State_Show_MiniMap, self).exit()
        # print self.fsm.owner.name + " exit state " + str(self.sn)

class PrototypeLevelMap(LevelMap):
    
    def __init__(self, name):
        super(PrototypeLevelMap, self).__init__(name)

    def create(self):
        from Game import CGameApp
        self.tile_rows = Prototype_Map_Enum.TILE_ROW_NUM.value
        self.tile_cols = Prototype_Map_Enum.TILE_COL_NUM.value
        self.tile_width = Prototype_Map_Enum.TILE_WIDTH.value
        self.tile_height = Prototype_Map_Enum.TILE_HEIGHT.value
        self.mini_map_width = Prototype_Map_Enum.MINI_MAP_WIDTH.value
        self.mini_map_height = Prototype_Map_Enum.MINI_MAP_HEIGHT.value

        self.mini_map_pos_x = (CGameApp.get_instance().screen_w - self.mini_map_width) / 2
        self.mini_map_pos_y = (CGameApp.get_instance().screen_h - self.mini_map_height) / 2

        self.mini_map_ratio_x = float(self.tile_cols * self.tile_width) / float(self.mini_map_width)
        self.mini_map_ratio_y = float(self.tile_rows * self.tile_height) / float(self.mini_map_height)

        self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_A5] = pygame.image.load("Media/mapset/Outside_A5.png").convert_alpha()
        self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_B] = pygame.image.load("Media/mapset/Outside_B.png").convert_alpha()
        self.tile_sets[Prototype_Map_Enum.TILE_SET_MAGIC_CIRCLE] = pygame.image.load("Media/mapset/magic_circle.png").convert_alpha()
        self.tile_sets[Prototype_Map_Enum.TILE_SET_MINI_MAP] = pygame.image.load("Media/mini_map.png").convert_alpha()

        self.tile_imgs[Prototype_Map_Enum.TILE_GRASS.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_A5].subsurface((0, 72, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_BASE.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_B].subsurface((0, 468, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_BORDER.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_A5].subsurface((108, 396, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_WALL.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_A5].subsurface((160, 288, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_TELEPORTER.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_MAGIC_CIRCLE].subsurface((36, 0, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_SAFE_AREA.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_A5].subsurface((144, 0, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_KEEPER.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_B].subsurface((288, 144, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_MAGIC_CIRCLR.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_MAGIC_CIRCLE].subsurface((0, 0, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_RESOURCE.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_A5].subsurface((144, 288, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_SAND.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_A5].subsurface((72,72, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))
        self.tile_imgs[Prototype_Map_Enum.TILE_TREE.value] = self.tile_sets[Prototype_Map_Enum.TILE_SET_OUTSIDE_B].subsurface((468, 180, Prototype_Map_Enum.TILE_WIDTH.value, Prototype_Map_Enum.TILE_HEIGHT.value))

        # teleporters
        self.teleporters = []

        # load from csv file
        with open("Media/map.csv", "rb") as lvMap:
            reader = csv.reader(lvMap)
            index_y = -1
            for row in reader:
                index_y += 1
                index_x = -1
                print "\n",
                for elem in row:
                    index_x += 1
                    t = int(elem)
                    occupy = t == Prototype_Map_Enum.TILE_GRASS.value or \
                             t == Prototype_Map_Enum.TILE_MAGIC_CIRCLR.value
                    if t == Prototype_Map_Enum.TILE_SAND.value or t == Prototype_Map_Enum.TILE_SAFE_AREA.value:
                        occupy = True
                    tile = MapTile(self.tile_imgs[t], self.tile_width, self.tile_height, not occupy)
                    if t == Prototype_Map_Enum.TILE_TELEPORTER.value:
                        self.teleporters.append(tile)
#                    print str(occupy) + " ",
                    tile.set_pos(self.tile_width * index_x, self.tile_height * index_y)
                    self.tiles.append(tile)
                
        self.quad_root = QuadTreeForTile(0, 0, 
        Prototype_Map_Enum.TILE_ROW_NUM.value *  Prototype_Map_Enum.TILE_WIDTH.value, 
        Prototype_Map_Enum.TILE_COL_NUM.value *  Prototype_Map_Enum.TILE_HEIGHT.value,
        Prototype_Map_Enum.TILE_ROW_NUM.value,  Prototype_Map_Enum.TILE_COL_NUM.value)
        self.quad_root.tiles = self.tiles

        QuadTreeForTile.build_quad_tree(0, 0,
        Prototype_Map_Enum.TILE_ROW_NUM.value * Prototype_Map_Enum.TILE_WIDTH.value,
        Prototype_Map_Enum.TILE_COL_NUM.value * Prototype_Map_Enum.TILE_HEIGHT.value,
        self.quad_root, 0)

        # test how many tiles are drawn
        self.tiles_drawn = 0

        #
        self.fsm.add_state(Map_State_Show_MiniMap(self.fsm))
        self.fsm.add_state(Map_State_Normal(self.fsm))
        self.fsm.change_to_state(Map_State_Enum.MAP_NORMAL)

        # register handlers
        self.add_handler(EventType.SWITCH_MINI_MAP, self.handle_switch_mini_map)

    def get_render_quads(self, view_port, quad_root):
        if len(quad_root.children_nodes) == 0:
            self.render_quads.append(quad_root)
            return
        # check node rect
        if QuadTreeForTile.check_tile(view_port[0], view_port[1], view_port[2], view_port[3], quad_root.x, quad_root.y, quad_root.width, quad_root.height):
            self.get_render_quads(view_port, quad_root.children_nodes[0])
            self.get_render_quads(view_port, quad_root.children_nodes[1])
            self.get_render_quads(view_port, quad_root.children_nodes[2])
            self.get_render_quads(view_port, quad_root.children_nodes[3])


    def get_view_port(self):
        from Game import CGameApp
        app = CGameApp.get_instance()
        return (-app.offset_x, -app.offset_y, app.screen_w, CGameApp.get_instance().screen_h)

    def update(self, et):
        self.process_evt_queue()
        self.render_quads = []
        self.get_render_quads(self.get_view_port(), self.quad_root)
        self.fsm.update(et)
        self.team_red.update(et)
        self.team_blue.update(et)

    def draw(self, et):
        view_pot = self.get_view_port()
        for quad in self.render_quads:
            for tile in quad.tiles:
                if QuadTreeForTile.check_tile(view_pot[0], view_pot[1], view_pot[2], view_pot[3], tile.pos_x, tile.pos_y, tile.width, tile.height):
                    tile.draw(et)
        self.fsm.draw(et)
        return

    def handle_switch_mini_map(self, evt):
        if self.mini_map_show:
            print "Mini-map Close"
            self.mini_map_show = False
            self.fsm.change_to_state(Map_State_Enum.MAP_NORMAL)
            pass
        else:
            print "Mini-map Show"
            self.mini_map_show = True
            self.fsm.change_to_state(Map_State_Enum.MAP_SHOW_MINI_MAP)
            pass
        return
