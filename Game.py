# _*_ coding: utf-8 _*_

import pygame
from pygame.locals import *
from sys import exit
from enum import Enum
from SpriteSheet import *
from Team import *
from Character import * 
from Event import *
from Map import *
from LocalInput import *
from pygame.font import *
from GUI import GuiManager
from Skill import *
from FSM import *
from Player import *


class Game_Enum(Enum):

    Game_Team_Select = 0
    Game_Characters_Ban_Pick = 1
    Game_Playing = 2
    Game_Init = 3


class Game_State_Team_Select(FSM_State):

    def __init__(self, fsm):
        super(Game_State_Team_Select, self).__init__(fsm)
        self.sn = Game_Enum.Game_Team_Select
        self.select_team = pygame.image.load("Media/team_select.png").convert_alpha()
        x = int((self.fsm.owner.screen_w - self.select_team.get_width()) / 2)
        y = int((self.fsm.owner.screen_h - self.select_team.get_height()) / 2)
        self.red_team_area = (x, y, self.select_team.get_width(), int(self.select_team.get_height() / 2))
        self.blue_team_area = (x, y + int(self.select_team.get_height() / 2), self.select_team.get_width(), int(self.select_team.get_height() / 2))
    
    def update(self, et):
        super(Game_State_Team_Select, self).update(et)
        
    def draw(self, et):
        super(Game_State_Team_Select, self).draw(et)
        if self.select_team is not None:
            self.fsm.owner.screen.blit(self.select_team, (self.red_team_area[0], self.red_team_area[1]))
            if QuadTreeForTile.check_tile(self.red_team_area[0], self.red_team_area[1], self.red_team_area[2],
                                          self.red_team_area[3], LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
                pygame.draw.rect(self.fsm.owner.screen, (0, 255, 0), self.red_team_area, 1)
            if QuadTreeForTile.check_tile(self.blue_team_area[0], self.blue_team_area[1], self.blue_team_area[2],
                                          self.blue_team_area[3], LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
                pygame.draw.rect(self.fsm.owner.screen, (0, 255, 0), self.blue_team_area, 1)
        
    def enter(self):
        super(Game_State_Team_Select, self).enter()
        
    def exit(self):
        super(Game_State_Team_Select, self).exit()


class Game_State_Ban_Pick(FSM_State):
    def __init__(self, fsm):
        super(Game_State_Ban_Pick, self).__init__(fsm)
        self.sn = Game_Enum.Game_Characters_Ban_Pick
        self.bp_ui = None

    def update(self, et):
        super(Game_State_Ban_Pick, self).update(et)
        self.fsm.owner.player_host.update(et)
        self.fsm.owner.player_guest.update(et)

    def draw(self, et):
        super(Game_State_Ban_Pick, self).draw(et)
        if self.bp_ui is not None:
            self.bp_ui.draw(et)
        app = self.fsm.owner
        app.cur_player.draw(et)

    def enter(self):
        super(Game_State_Ban_Pick, self).enter()
        app = self.fsm.owner
        app.player_host.fsm.change_to_state(Player_Enum.Player_State_Pick_Characters)
        app.cur_player = app.player_host
        app.player_guest.fsm.change_to_state(Player_Enum.Player_State_Pick_Characters)
        self.bp_ui = CGameApp.get_instance().gui_manager.character_bp

    def exit(self):
        super(Game_State_Ban_Pick, self).exit()


class Game_State_Init(FSM_State):
    def __init__(self, fsm):
        super(Game_State_Init, self).__init__(fsm)
        self.sn = Game_Enum.Game_Init

    def update(self, et):
        super(Game_State_Init, self).update(et)

    def draw(self, et):
        super(Game_State_Init, self).draw(et)
        app = self.fsm.owner
        if app.title_screen is not None:
            app.screen.blit(app.title_screen, ((0, 0), (app.screen_w, app.screen_h)))
            app.screen.blit(app.begin_game, (250, 250))
            w = app.begin_game.get_width()
            h = app.begin_game.get_height()
            from Map import QuadTreeForTile
            if QuadTreeForTile.check_tile(250, 250, w, h, LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
                pygame.draw.rect(app.screen, (0, 255, 0), (250, 250, w, h), 1)

    def enter(self):
        super(Game_State_Init, self).enter()

    def exit(self):
        super(Game_State_Init, self).exit()


class Game_State_Playing(FSM_State):
    def __init__(self, fsm):
        super(Game_State_Playing, self).__init__(fsm)
        self.sn = Game_Enum.Game_Playing
        self.team_label = None

    def update(self, et):
        super(Game_State_Playing, self).update(et)
        self.fsm.owner.level_map.update(et)
        app = self.fsm.owner
        app.player_host.update(et)
        app.player_guest.update(et)
        self.team_label.set_text(str(app.cur_player.team.name) + "'s Turn", (255, 255, 255))

    def draw(self, et):
        super(Game_State_Playing, self).draw(et)
        self.fsm.owner.level_map.draw(et)
        self.fsm.owner.player_guest.draw(et)
        self.fsm.owner.player_host.draw(et)
        self.fsm.owner.gui_manager.draw(et)
        self.team_label.draw(et)
        app = self.fsm.owner
        app.screen.blit(app.end_turn, (400, 700, 200, 50))
        if QuadTreeForTile.check_tile(400, 700, 200, 50, LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
            pygame.draw.rect(app.screen, (255, 255, 255), (400, 700, 200, 50), 1)

    def enter(self):
        super(Game_State_Playing, self).enter()
        # characters' position
        self.team_label = GuiLabel("team label", 400, 0, 200, 30, (0, 0, 0), 255, "", (255, 255, 255), None)
        team_red = self.fsm.owner.team_red
        team_blue = self.fsm.owner.team_blue
        team_red_x = 36
        team_red_y = 3276
#        team_blue_x = 3276
#        team_blue_y = 108
        team_blue_x = 216
        team_blue_y = 3276
        count = 0
        for (name, character) in team_red.characters.items():
            count += 1
            character.set_pos(team_red_x, team_red_y)
            if count % 4 == 0:
                team_red_x = 36
                team_red_y += 36
            else:
                team_red_x += 36

        count = 0
        for (name, character) in team_blue.characters.items():
            count += 1
            character.set_pos(team_blue_x, team_blue_y)
            if count % 4 == 0:
                team_blue_x = 216
                team_blue_y += 36
            else:
                team_blue_x += 36

    def exit(self):
        super(Game_State_Playing, self).exit()


class CGameApp(EventObject):
    
    instance = None

    def __init__(self, name, width, height):
        super(CGameApp, self).__init__()
        self.name = name
        self.screen_w = width
        self.screen_h = height
        self.fsm = FSM_Machine(self)
        pygame.init()
        title_screen = pygame.image.load("Media/title_screen.png")
        self.end_turn = pygame.image.load("Media/end_turn.png")
        self.title_screen = pygame.transform.scale(title_screen, (self.screen_w, self.screen_h))
        self.screen = pygame.display.set_mode((width, height), 0, 32)
        self.font = pygame.font.Font("Media/DeliusSwashCaps-Regular.ttf", 12)
        self.title_menu_font = pygame.font.Font("Media/DeliusSwashCaps-Regular.ttf", 20)
        self.clock = pygame.time.Clock()
        self.begin_game = self.title_menu_font.render("New Game", False, (0, 0, 0))
        self.team_red = None
        self.team_blue = None
        self.level_map = None
        self.cur_team = None
        self.offset_x = 0
        self.offset_y = 0
        self.gui_manager = None
        self.total_turn = 0
        self.characters = {}
        self.player_host = None
        self.player_guest = None
        # add states
        self.fsm.add_state(Game_State_Init(self.fsm))
        self.fsm.add_state(Game_State_Ban_Pick(self.fsm))
        self.fsm.add_state(Game_State_Playing(self.fsm))
        self.fsm.add_state(Game_State_Team_Select(self.fsm))

        self.fsm.change_to_state(Game_Enum.Game_Init)

        self.cur_player = None

        # register event handlers
        # left mouse
        self.add_handler(EventType.MOUSE_LBTN_DOWN, self.handle_mouse_lbtn_down)
        self.add_handler(EventType.GAME_BAN_PICK_TURN, self.handle_bp_turn_change)
        # arrow keys
        self.add_handler(EventType.SCROLL_MAP, self.handle_scroll_map)


    def create(self):
        Skill_Animations.load_skill_res()
        # character sheets
        hakurei_reimu_sprite_sheet = Sprite_Sheet("Media/walkings/博丽灵梦1.png", 36, 36, 4, 4)
        kirisame_marisa_sprite_sheet = Sprite_Sheet("Media/walkings/雾雨魔理沙1.png", 36, 36, 4, 4)
        remilia_scarlet_sprite_sheet = Sprite_Sheet("Media/walkings/蕾米莉亚·斯卡雷特1.png", 36, 36, 4, 4)
        flandre_scarlet_sprite_sheet = Sprite_Sheet("Media/walkings/芙兰朵露·斯卡雷特1.png", 36, 36, 4, 4)
        izayoi_sakuya_sprite_sheet = Sprite_Sheet("Media/walkings/十六夜咲夜1.png", 36, 36, 4, 4)
        patchouli_knowledge_sprite_sheet = Sprite_Sheet("Media/walkings/帕秋莉·诺蕾姬1.png", 36, 36, 4, 4)
        saigyouji_yuyuko_sprite_sheet = Sprite_Sheet("Media/walkings/西行寺幽幽子1.png", 36, 36, 4, 4)
        konpaku_youmu_sprite_sheet = Sprite_Sheet("Media/walkings/魂魄妖梦1.png", 36, 36, 4, 4)
        yakumo_yukari_sprite_sheet = Sprite_Sheet("Media/walkings/八云紫1.png", 36, 36, 4, 4)
        huziwara_no_mokou_sprite_sheet = Sprite_Sheet("Media/walkings/藤原妹红1.png", 36, 36, 4, 4)
        houraisan_kaguya_sprite_sheet = Sprite_Sheet("Media/walkings/蓬莱山辉夜1.png", 36, 36, 4, 4)
        kamishirasawa_keine_sprite_sheet = Sprite_Sheet("Media/walkings/上白泽慧音1.png", 36, 36, 4, 4)
        syameimaru_aya_sprite_sheet = Sprite_Sheet("Media/walkings/射命丸文1.png", 36, 36, 4, 4)
        kazami_yuka_sprite_sheet = Sprite_Sheet("Media/walkings/风见幽香1.png", 36, 36, 4, 4)
        shikieiki_yamaxanadu_sprite_sheet = Sprite_Sheet("Media/walkings/四季映姬1.png", 36, 36, 4, 4)
        kochiya_sanae_sprite_sheet = Sprite_Sheet("Media/walkings/东风谷早苗1.png", 36, 36, 4, 4)
        yasaka_kanako_sprite_sheet = Sprite_Sheet("Media/walkings/八坂神奈子1.png", 36, 36, 4, 4)
        kawasiro_nitori_sprite_sheet = Sprite_Sheet("Media/walkings/河城荷取1.png", 36, 36, 4, 4)
        hinanawi_tenshi_sprite_sheet = Sprite_Sheet("Media/walkings/比那名居天子1.png", 36, 36, 4, 4)
        moriya_suwako_sprite_sheet = Sprite_Sheet("Media/walkings/泄矢诹访子1.png", 36, 36, 4, 4)
        reiuzi_utsuho_sprite_sheet = Sprite_Sheet("Media/walkings/灵乌路空1.png", 36, 36, 4, 4)
        onozuka_komachi_sprite_sheet = Sprite_Sheet("Media/walkings/小野塚小町1.png", 36, 36, 4, 4)
        reisen_udongein_inaba_sprite_sheet = Sprite_Sheet("Media/walkings/铃仙·优昙华院·因幡1.png", 36, 36, 4, 4)
        hoan_meirin_sprite_sheet = Sprite_Sheet("Media/walkings/红美铃1.png", 36, 36, 4, 4)
        letty_whiterock_sprite_sheet = Sprite_Sheet("Media/walkings/蕾迪·霍瓦特罗克1.png", 36, 36, 4, 4)
        ibuki_suika_sprite_sheet = Sprite_Sheet("Media/walkings/伊吹萃香1.png", 36, 36, 4, 4)
        hoshiguma_yugi_sprite_sheet = Sprite_Sheet("Media/walkings/星熊勇仪1.png", 36, 36, 4, 4)
        rumia_sprite_sheet = Sprite_Sheet("Media/walkings/露米娅1.png", 36, 36, 4, 4)
        medicine_melancholy_sprite_sheet = Sprite_Sheet("Media/walkings/梅迪馨·梅兰克莉1.png", 36, 36, 4, 4)
        cirno_sprite_sheet = Sprite_Sheet("Media/walkings/琪露诺1.png", 36, 36, 4, 4)
        aki_minoriko_sprite_sheet = Sprite_Sheet("Media/walkings/秋穰子1.png", 36, 36, 4, 4)
        kagiyama_hina_sprite_sheet = Sprite_Sheet("Media/walkings/键山雏1.png", 36, 36, 4, 4)
        wriggle_nightbug_sprite_sheet = Sprite_Sheet("Media/walkings/莉格露·奈特巴格1.png", 36, 36, 4, 4)
        alice_margatroid_sprite_sheet = Sprite_Sheet("Media/walkings/爱丽丝·玛格特罗依德1.png", 36, 36, 4, 4)
        chen_sprite_sheet = Sprite_Sheet("Media/walkings/橙1.png", 36, 36, 4, 4)
        yakumo_ran_sprite_sheet = Sprite_Sheet("Media/walkings/八云蓝1.png", 36, 36, 4, 4)
        yagokoro_eirin_sprite_sheet = Sprite_Sheet("Media/walkings/八意永琳1.png", 36, 36, 4, 4)

        self.characters = {}
        self.level_map = PrototypeLevelMap("SLG Prototype")
        self.level_map.create()
        self.team_red = Team(Team_Enum.TEAM_RED, self.level_map)
        self.team_blue = Team(Team_Enum.TEAM_BLUE, self.level_map)
        self.player_host = Player()
        self.player_guest = Player()
        self.level_map.team_red = self.team_red
        self.level_map.team_blue = self.team_blue

        hakurei_reimu = Character("Hakurei Reimu", hakurei_reimu_sprite_sheet, None)
        hakurei_reimu.set_picture("Media/characters/博丽灵梦.png")
        self.characters["Hakurei Reimu"] = hakurei_reimu
        hakurei_reimu.add_skill(Hakurei_Reimu_MuSouTenSei())
        hakurei_reimu.add_skill(Hakurei_Reimu_MuSoFuin())
        hakurei_reimu.add_skill(Hakurei_Reimu_MuGenNoKoSoKuKiGanSaTsu())
        hakurei_reimu.add_skill(Hakurei_Reimu_FuMaJin())

        kirisame_marisa = Character("Kirisame Marisa", kirisame_marisa_sprite_sheet, None)
        kirisame_marisa.set_picture("Media/characters/雾雨魔理沙.png")
        self.characters["Kirisame Marisa"] = kirisame_marisa

        remilia_scarlet = Character("Remilia Scarlet", remilia_scarlet_sprite_sheet, None)
        remilia_scarlet.set_picture("Media/characters/蕾米莉亚.png")
        self.characters["Remilia Scarlet"] = remilia_scarlet

        flandre_scarlet = Character("Flandre Scarlet", flandre_scarlet_sprite_sheet, None)
        flandre_scarlet.set_picture("Media/characters/芙兰朵露.png")
        self.characters["Flandre Scarlet"] = flandre_scarlet

        izayoi_sakuya = Character("Izayoi Sakuya", izayoi_sakuya_sprite_sheet, None)
        izayoi_sakuya.set_picture("Media/characters/十六夜咲夜.png")
        self.characters["Izayoi Sakuya"] = izayoi_sakuya

        patchouli_knowledge = Character("Patchouli", patchouli_knowledge_sprite_sheet, None)
        patchouli_knowledge.set_picture("Media/characters/帕秋莉_诺蕾姬.png")
        self.characters["Patchouli"] = patchouli_knowledge

        saigyouji_yuyuko = Character("Yuyuko", saigyouji_yuyuko_sprite_sheet, None)
        saigyouji_yuyuko.set_picture("Media/characters/幽幽子.png")
        self.characters["Yuyuko"] = saigyouji_yuyuko

        konpaku_youmu = Character("Konpaku Youmu", konpaku_youmu_sprite_sheet, None)
        konpaku_youmu.set_picture("Media/characters/魂魄妖梦.png")
        self.characters["Konpaku Youmu"] = konpaku_youmu

        yakumo_yukari = Character("Yakumo Yukari", yakumo_yukari_sprite_sheet, None)
        yakumo_yukari.set_picture("Media/characters/八云紫.png")
        self.characters["Yakumo Yukari"] = yakumo_yukari

        huziwara_no_mokou = Character("Mokou", huziwara_no_mokou_sprite_sheet, None)
        huziwara_no_mokou.set_picture("Media/characters/藤原妹红.png")
        self.characters["Mokou"] = huziwara_no_mokou

        houraisan_kaguya = Character("Kaguya", houraisan_kaguya_sprite_sheet, None)
        houraisan_kaguya.set_picture("Media/characters/辉夜.png")
        self.characters["Kaguya"] = houraisan_kaguya

        kamishirasawa_keine = Character("Keine", kamishirasawa_keine_sprite_sheet, None)
        kamishirasawa_keine.set_picture("Media/characters/慧音.png")
        self.characters["Keine"] = kamishirasawa_keine

        syameimaru_aya = Character("Aya", syameimaru_aya_sprite_sheet, None)
        syameimaru_aya.set_picture("Media/characters/射命丸文.png")
        self.characters["Aya"] = syameimaru_aya

        kazami_yuka = Character("Kazami Yuka", kazami_yuka_sprite_sheet, None)
        kazami_yuka.set_picture("Media/characters/风见幽香.png")
        self.characters["Kazami Yuka"] = kazami_yuka

        shikieiki_yamaxanadu = Character("Shikieiki", shikieiki_yamaxanadu_sprite_sheet, None)
        shikieiki_yamaxanadu.set_picture("Media/characters/四季映姬.png")
        self.characters["Shikieiki"] = shikieiki_yamaxanadu

        kochiya_sanae = Character("Kochiya Sanae", kochiya_sanae_sprite_sheet, None)
        kochiya_sanae.set_picture("Media/characters/东风谷早苗.png")
        self.characters["Kochiya Sanae"] = kochiya_sanae

        yasaka_kanako = Character("Yasaka Kanako", yasaka_kanako_sprite_sheet, None)
        yasaka_kanako.set_picture("Media/characters/八坂神奈子.png")
        self.characters["Yasaka Kanako"] = yasaka_kanako

        kawasiro_nitori = Character("Kawasiro Nitori", kawasiro_nitori_sprite_sheet, None)
        kawasiro_nitori.set_picture("Media/characters/河城荷取.png")
        self.characters["Kawasiro Nitori"] = kawasiro_nitori

        hinanawi_tenshi = Character("Tenshi", hinanawi_tenshi_sprite_sheet, None)
        hinanawi_tenshi.set_picture("Media/characters/比那名居天子.png")
        self.characters["Tenshi"] = hinanawi_tenshi

        moriya_suwako = Character("Moriya Suwako", moriya_suwako_sprite_sheet, None)
        moriya_suwako.set_picture("Media/characters/洩矢诹访子.png")
        self.characters["Moriya Suwako"] = moriya_suwako

        reiuzi_utsuho = Character("Reiuzi Utsuho", reiuzi_utsuho_sprite_sheet, None)
        reiuzi_utsuho.set_picture("Media/characters/灵乌路空.png")
        self.characters["Reiuzi Utsuho"] = reiuzi_utsuho

        onozuka_komachi = Character("Komachi", onozuka_komachi_sprite_sheet, None)
        onozuka_komachi.set_picture("Media/characters/小野塚小町.png")
        self.characters["Komachi"] = onozuka_komachi

        reisen_udongein = Character("Reisen", reisen_udongein_inaba_sprite_sheet, None)
        reisen_udongein.set_picture("Media/characters/铃仙.png")
        self.characters["Reisen"] = reisen_udongein

        hoan_meirin = Character("Hoan Meirin", hoan_meirin_sprite_sheet, None)
        hoan_meirin.set_picture("Media/characters/红美玲.png")
        self.characters["Hoan Meirin"] = hoan_meirin

        letty_whiterock = Character("Letty", letty_whiterock_sprite_sheet, None)
        letty_whiterock.set_picture("Media/characters/蕾蒂_霍瓦特洛克.png")
        self.characters["Letty"] = letty_whiterock

        ibuki_suika = Character("Ibuki Suika", ibuki_suika_sprite_sheet, None)
        ibuki_suika.set_picture("Media/characters/伊吹萃香.png")
        self.characters["Ibuki Suika"] = ibuki_suika

        hoshiguma_yugi = Character("Yugi", hoshiguma_yugi_sprite_sheet, None)
        hoshiguma_yugi.set_picture("Media/characters/星熊勇仪.png")
        self.characters["Yugi"] = hoshiguma_yugi

        rumia = Character("Rumia", rumia_sprite_sheet, None)
        rumia.set_picture("Media/characters/露米娅.png")
        self.characters["Rumia"] = rumia

        medicine_melancholy = Character("Melancholy", medicine_melancholy_sprite_sheet, None)
        medicine_melancholy.set_picture("Media/characters/梅蒂欣_梅兰可莉 .png")
        self.characters["Melancholy"] = medicine_melancholy

        cirno = Character("Cirno", cirno_sprite_sheet, None)
        cirno.set_picture("Media/characters/琪露诺.png")
        self.characters["Cirno"] = cirno

        aki_minoriko = Character("Aki Minoriko", aki_minoriko_sprite_sheet, None)
        aki_minoriko.set_picture("Media/characters/秋穰子.png")
        self.characters["Aki Minoriko"] = aki_minoriko

        kagiyama_hina = Character("Kagiyama Hina", kagiyama_hina_sprite_sheet, None)
        kagiyama_hina.set_picture("Media/characters/键山雏.png")
        self.characters["Kagiyama Hina"] = kagiyama_hina

        wriggle_nightbug = Character("Wriggle", wriggle_nightbug_sprite_sheet, None)
        wriggle_nightbug.set_picture("Media/characters/莉格露_奈特巴格.png")
        self.characters["Wriggle"] = wriggle_nightbug

        alice_margatroid = Character("Alice", alice_margatroid_sprite_sheet, None)
        alice_margatroid.set_picture("Media/characters/爱丽丝.png")
        self.characters["Alice"] = alice_margatroid

        chen = Character("Chen", chen_sprite_sheet, None)
        chen.set_picture("Media/characters/橙.png")
        self.characters["Chen"] = chen

        yakumo_ran = Character("Yakumo Ran", yakumo_ran_sprite_sheet, None)
        yakumo_ran.set_picture("Media/characters/八云蓝.png")
        self.characters["Yakumo Ran"] = yakumo_ran

        yagokoro_eirin = Character("Yagokoro Eirin", yagokoro_eirin_sprite_sheet, None)
        yagokoro_eirin.set_picture("Media/characters/八意永琳.png")
        self.characters["Yagokoro Eirin"] = yagokoro_eirin

        self.gui_manager = GuiManager()

        return

    def select_character_by_mouse(self, mouse_pos):
        character_red = self.team_red.select_character_by_mouse(mouse_pos)
        if character_red is not None:
            return character_red
        else:
            character_blue = self.team_blue.select_character_by_mouse(mouse_pos)
            if character_blue is not None:
                return character_blue
        return None

    def loop(self):
        while True:
            LocalInput.get_instance().event_loop()

            self.screen.fill((0, 0, 0, 0))
            self.update(self.clock.tick())
            self.draw(self.clock.tick())

            pygame.display.update()

    def update(self, et):
        self.process_evt_queue()
        self.fsm.update(et)
        return
    
    def draw(self, et):
        self.fsm.draw(et)
        return
    
    def handle_mouse_lbtn_down(self, evt):
        if self.fsm.is_in_state(Game_Enum.Game_Init):
            w = self.begin_game.get_width()
            h = self.begin_game.get_height()
            if QuadTreeForTile.check_tile(250, 250, w, h, LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
                print "Begin Game"
                self.fsm.change_to_state(Game_Enum.Game_Team_Select)
        elif self.fsm.is_in_state(Game_Enum.Game_Team_Select):
            state = self.fsm.states[Game_Enum.Game_Team_Select]
            if QuadTreeForTile.check_tile(state.red_team_area[0], state.red_team_area[1], state.red_team_area[2],
                                          state.red_team_area[3], LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
                pygame.draw.rect(self.screen, (0, 255, 0), state.red_team_area, 1)
                print "Choose Red Team"
                self.player_host.set_team(self.team_red)
                self.player_guest.set_team(self.team_blue)
                self.fsm.change_to_state(Game_Enum.Game_Characters_Ban_Pick)
            elif QuadTreeForTile.check_tile(state.blue_team_area[0], state.blue_team_area[1], state.blue_team_area[2],
                                          state.blue_team_area[3], LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
                pygame.draw.rect(self.screen, (0, 255, 0), state.blue_team_area, 1)
                print "Choose Blue Team"
                self.player_host.set_team(self.team_blue)
                self.player_guest.set_team(self.team_red)
                self.fsm.change_to_state(Game_Enum.Game_Characters_Ban_Pick)
        elif self.fsm.is_in_state(Game_Enum.Game_Characters_Ban_Pick):
            self.send_event(self.cur_player, Event_Mouse_LBTN_DOWN(EventType.MOUSE_LBTN_DOWN, LocalInput.mouse_pos))
        elif self.fsm.is_in_state(Game_Enum.Game_Playing):
            self.send_event(self.player_guest, evt)
            self.send_event(self.player_host, evt)
            if QuadTreeForTile.check_tile(400, 700, 200, 50, LocalInput.mouse_pos[0], LocalInput.mouse_pos[1], 0, 0):
                if self.cur_player.team.name == self.player_host.team.name:
                    self.player_host.fsm.change_to_state(Player_Enum.Player_State_Waiting)
                    self.player_guest.fsm.change_to_state(Player_Enum.Player_State_In_Turn)
                    self.cur_player = self.player_guest
                elif self.cur_player.team.name == self.player_guest.team.name:
                    self.player_guest.fsm.change_to_state(Player_Enum.Player_State_Waiting)
                    self.player_host.fsm.change_to_state(Player_Enum.Player_State_In_Turn)
                    self.cur_player = self.player_host
                self.player_host.calculate_buffs()
                self.player_guest.calculate_buffs()
                self.player_host.team.team_money += 5
                self.player_guest.team.team_money += 5
                self.cur_player.team.total_turn += 1
                self.total_turn += 1
        return

    def handle_scroll_map(self, evt):
        self.offset_x += evt.offset_x
        self.offset_y += evt.offset_y
        return

    def handle_bp_turn_change(self, evt):
        if self.cur_player == self.player_host:
            if self.cur_player.fsm.is_in_state(Player_Enum.Player_State_Pick_Characters):
                self.cur_player.fsm.change_to_state(Player_Enum.Player_State_Ban_Characters)
            elif self.cur_player.fsm.is_in_state(Player_Enum.Player_State_Ban_Characters):
                self.cur_player.fsm.change_to_state(Player_Enum.Player_State_Pick_Characters)
            self.cur_player = self.player_guest
        elif self.cur_player == self.player_guest:
            if self.cur_player.fsm.is_in_state(Player_Enum.Player_State_Pick_Characters):
                self.cur_player.fsm.change_to_state(Player_Enum.Player_State_Ban_Characters)
            elif self.cur_player.fsm.is_in_state(Player_Enum.Player_State_Ban_Characters):
                self.cur_player.fsm.change_to_state(Player_Enum.Player_State_Pick_Characters)
            self.cur_player = self.player_host
        bp_ui = self.gui_manager.character_bp
        if len(bp_ui.character_red_pick) == 8 and len(bp_ui.character_blue_pick) == 8:
            self.fsm.change_to_state(Game_Enum.Game_Playing)
            self.player_host.fsm.change_to_state(Player_Enum.Player_State_In_Turn)
            self.player_guest.fsm.change_to_state(Player_Enum.Player_State_Waiting)

    @staticmethod
    def get_instance():
        if CGameApp.instance is None:
            print "Create App Instance"
            CGameApp.instance = CGameApp("A Prototype", 1000, 750)
        return CGameApp.instance
