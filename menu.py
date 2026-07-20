import pygame
import math
from fighter import Fighter 
class MenuManager:
    def __init__(self, game):

        self.game = game 
        self.menu_options = ["JUGAR", "SALIR"]
        self.selected_option = 0
        self.bg_scroll = 0.0

        self.p1_cursor = 0
        self.p2_cursor = 1
        self.p1_selected = False
        self.p2_selected = False
        self.stage_cursor = 0

    def update(self, dt, key):
        if self.game.state == "MENU":
            self.update_menu(dt, key)
        elif self.game.state == "SELECT":
            self.update_select(key)
        elif self.game.state == "STAGE":
            self.update_stage(key)

    def draw(self):
        if self.game.state == "MENU":
            self.draw_menu()
        elif self.game.state == "SELECT":
            self.draw_select()
        elif self.game.state == "STAGE":
            self.draw_stage()

    def ejecutar_opcion_menu(self):
        if self.menu_options[self.selected_option] == "JUGAR":
            self.game.play_sfx("select")
            self.p1_selected = False
            self.p2_selected = False
            self.game.state = "SELECT"
            self.game.play_sfx("selectCharacter")
        elif self.menu_options[self.selected_option] == "SALIR":
            self.game.play_sfx("back")
            pygame.mixer.music.stop()
            self.game.running = False
        self.game.input_cooldown = 15

    def update_menu(self, dt, key):
        self.bg_scroll = (self.bg_scroll + 50 * dt) % 100
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if self.game.input_cooldown == 0:
            if key[pygame.K_UP]:
                self.game.play_sfx("select")
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                self.game.input_cooldown = 15
            elif key[pygame.K_DOWN]:
                self.game.play_sfx("select")
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                self.game.input_cooldown = 15
            elif key[pygame.K_RETURN]:
                self.ejecutar_opcion_menu()

            for i, option in enumerate(self.menu_options):
                txt_option = self.game.fuente_menu.render(option, True, (255, 255, 255))
                rect_option = txt_option.get_rect(center=(self.game.S_WIDTH // 2, 400 + (i * 70)))
                
                if rect_option.collidepoint(mouse_pos):
                    if self.selected_option != i:
                        self.game.play_sfx("select")
                    self.selected_option = i
                    if mouse_click:
                        self.ejecutar_opcion_menu()

    def update_select(self, key):
        if self.game.input_cooldown == 0:
            if not self.p1_selected:
                if key[pygame.K_a]:
                    self.game.play_sfx("select")
                    self.p1_cursor = (self.p1_cursor - 1) % len(self.game.roster)
                    self.game.input_cooldown = 15
                elif key[pygame.K_d]:
                    self.game.play_sfx("select")
                    self.p1_cursor = (self.p1_cursor + 1) % len(self.game.roster)
                    self.game.input_cooldown = 15
                elif key[pygame.K_f]:
                    self.game.play_sfx("select")
                    self.p1_selected = True
                    self.game.input_cooldown = 15

            if not self.p2_selected:
                if key[pygame.K_LEFT]:
                    self.game.play_sfx("select")
                    self.p2_cursor = (self.p2_cursor - 1) % len(self.game.roster)
                    self.game.input_cooldown = 15
                elif key[pygame.K_RIGHT]:
                    self.game.play_sfx("select")
                    self.p2_cursor = (self.p2_cursor + 1) % len(self.game.roster)
                    self.game.input_cooldown = 15
                elif key[pygame.K_RETURN]:
                    self.game.play_sfx("select")
                    self.p2_selected = True
                    self.game.input_cooldown = 15    
            
            if key[pygame.K_ESCAPE]:
                self.game.play_sfx("select")
                if self.p1_selected or self.p2_selected:
                    self.p1_selected = False
                    self.p2_selected = False
                else:
                    self.game.state = "MENU"
                self.game.input_cooldown = 15
            
            if self.p1_selected and self.p2_selected:
                self.game.state = "STAGE"
                self.game.input_cooldown = 15

    def update_stage(self, key):
        if self.game.input_cooldown == 0:
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                self.game.play_sfx("select")
                self.stage_cursor = (self.stage_cursor - 1) % len(self.game.stages)
                self.game.input_cooldown = 15
            elif key[pygame.K_RIGHT] or key[pygame.K_d]:
                self.game.play_sfx("select")
                self.stage_cursor = (self.stage_cursor + 1) % len(self.game.stages)
                self.game.input_cooldown = 15
            elif key[pygame.K_RETURN]:
                self.game.play_sfx("select")

                char_p1 = self.game.roster[self.p1_cursor]
                char_p2 = self.game.roster[self.p2_cursor]

                self.game.p1_cursor = self.p1_cursor
                self.game.p2_cursor = self.p2_cursor
                self.game.stage_cursor = self.stage_cursor

                self.game.fighter_1 = Fighter(player=1, x=200, y=self.game.suelo-180, char_name=char_p1)
                self.game.fighter_2 = Fighter(player=2, x=1000, y=self.game.suelo-180, char_name=char_p2)

                self.game.reset_match()
                selected_bgm = self.game.stages[self.stage_cursor]["bgm"]
                self.game.play_bgm(selected_bgm)
                self.game.play_sfx("fight")
                self.game.state = "COMBAT"
                self.game.input_cooldown = 15
                
            elif key[pygame.K_ESCAPE]:
                self.game.play_sfx("select")
                self.game.state = "SELECT"
                self.p1_selected = False
                self.p2_selected = False
                self.game.input_cooldown = 15

    def draw_menu(self):
        self.game.screen.fill((30, 30, 35))

        for i in range(-self.game.S_HEIGHT, self.game.S_WIDTH, 80):
            start_pos = (i + self.bg_scroll, 0)
            end_pos = (i + self.bg_scroll - self.game.S_HEIGHT, self.game.S_HEIGHT)
            pygame.draw.line(self.game.screen, (45, 45, 50), start_pos, end_pos, 10)
        
        scale_factor = 1.0 + math.sin(pygame.time.get_ticks() / 300.0) * 0.05
        font_size = int(100 * scale_factor)

        font_path = self.game.BASE_DIR / "Assets" / "font" / "The King of Fighters Font.ttf"
        try:
            fuente_pulsante = pygame.font.Font(str(font_path), font_size)
        except:
            fuente_pulsante = pygame.font.SysFont("Impact", font_size)
        
        txt_titulo = fuente_pulsante.render("ART OF FIGHTERS", True, (255,200,0))
        txt_sombra = fuente_pulsante.render("ART OF FIGHTERS", True, (0,0,0))
        rect_titulo = txt_titulo.get_rect(center=(self.game.S_WIDTH //2, 200))
        self.game.screen.blit(txt_sombra, (rect_titulo.x + 5, rect_titulo.y + 5))
        self.game.screen.blit(txt_titulo, rect_titulo)

        for i , option in enumerate(self.menu_options):
            color = (255,255,255) if i == self.selected_option else (100,100,100)
            txt_option = self.game.fuente_menu.render(option, True, color)
            rect_option = txt_option.get_rect(center=(self.game.S_WIDTH // 2, 400 + (i * 70)))
            self.game.screen.blit(txt_option, rect_option)

            if i == self.selected_option:
                cursor_rect = pygame.Rect(rect_option.left - 40, rect_option.centery - 10, 20, 20)
                pygame.draw.rect(self.game.screen, (255, 0, 0), cursor_rect)

    def draw_select(self):
        self.game.screen.fill((15,15,20))

        txt_title = self.game.fuente_timer.render("CHARACTER SELECT", True, (255, 255, 255))
        self.game.screen.blit(txt_title, txt_title.get_rect(center=(self.game.S_WIDTH // 2, 50)))

        char_p1 = self.game.roster[self.p1_cursor]
        if char_p1 in self.game.portraits:
            img_p1 = pygame.transform.smoothscale(self.game.portraits[char_p1],(450,600))
            self.game.screen.blit(img_p1, (50, 150))
            txt_p1_shadow = self.game.fuente_timer.render(char_p1, True, (0, 0, 0))
            self.game.screen.blit(txt_p1_shadow, (103, self.game.S_HEIGHT - 77))
            txt_p1 = self.game.fuente_timer.render(char_p1, True, (50, 150, 255))
            self.game.screen.blit(txt_p1, (100, self.game.S_HEIGHT - 80))
        
        char_p2 = self.game.roster[self.p2_cursor]
        if char_p2 in self.game.portraits:
            raw_p2 = pygame.transform.smoothscale(self.game.portraits[char_p2], (450, 600))
            img_p2 = pygame.transform.flip(raw_p2, True, False) 
            self.game.screen.blit(img_p2, (self.game.S_WIDTH - 500, 150))
            txt_p2_shadow = self.game.fuente_timer.render(char_p2, True, (0, 0, 0))
            self.game.screen.blit(txt_p2_shadow, (self.game.S_WIDTH - 247, self.game.S_HEIGHT - 77))
            txt_p2 = self.game.fuente_timer.render(char_p2, True, (255, 50, 50))
            self.game.screen.blit(txt_p2, (self.game.S_WIDTH - 250, self.game.S_HEIGHT - 80))
        
        box_size = 80
        padding = 10
        total_width = len(self.game.roster) * (box_size + padding)
        start_x = (self.game.S_WIDTH // 2) - (total_width // 2)
        start_y = self.game.S_HEIGHT - 150

        for i, char in enumerate(self.game.roster):
            rect_x = start_x + (i * (box_size + padding))
            rect = pygame.Rect(rect_x, start_y, box_size, box_size)

            if char in self.game.portraits:
                mini_img = pygame.transform.smoothscale(self.game.portraits[char], (box_size, box_size))
                self.game.screen.blit(mini_img, rect)
            else:
                pygame.draw.rect(self.game.screen, (100, 100, 100), rect) 
                
            pygame.draw.rect(self.game.screen, (255, 255, 255), rect, 2) 

            if i == self.p1_cursor:
                pygame.draw.rect(self.game.screen, (50, 150, 255), rect, 5) 
                txt = self.game.fuente_nombres.render("P1", True, (50, 150, 255))
                self.game.screen.blit(txt, (rect_x, start_y - 30))
            if i == self.p2_cursor:
                offset = 5 if i == self.p1_cursor else 0
                pygame.draw.rect(self.game.screen, (255, 50, 50), rect.inflate(-offset, -offset), 5)
                txt = self.game.fuente_nombres.render("P2", True, (255, 50, 50))
                self.game.screen.blit(txt, (rect_x + box_size - 30, start_y - 30))

    def draw_stage(self):
        txt_titulo = self.game.fuente_menu.render("SELECCION DE ESCENARIO Y BGM", True, (255, 255, 255))
        rect_titulo = txt_titulo.get_rect(center=(self.game.S_WIDTH // 2, 100))
        txt_titulo_sombra = self.game.fuente_menu.render("SELECCION DE ESCENARIO Y BGM", True, (0, 0, 0))
        self.game.screen.blit(txt_titulo_sombra, (rect_titulo.x + 4, rect_titulo.y + 4))
        self.game.screen.blit(txt_titulo, rect_titulo)

        prev_idx = (self.stage_cursor - 1) % len(self.game.stages)
        next_idx = (self.stage_cursor + 1) % len(self.game.stages)

        center_w, center_h = 400, 250
        cx = self.game.S_WIDTH // 2 - center_w // 2
        cy = self.game.S_HEIGHT // 2 - center_h // 2 - 20
        
        side_w, side_h = 250, 150
        lx = cx - side_w - 50
        ly = self.game.S_HEIGHT // 2 - side_h // 2 - 20
        
        rx = cx + center_w + 50
        ry = self.game.S_HEIGHT // 2 - side_h // 2 - 20

        if hasattr(self.game, 'stage_backgrounds') and self.game.stage_backgrounds[prev_idx]:
            img_left = pygame.transform.smoothscale(self.game.stage_backgrounds[prev_idx], (side_w, side_h))
            self.game.screen.blit(img_left, (lx, ly))
        else:
            pygame.draw.rect(self.game.screen, (50, 50, 50), (lx, ly, side_w, side_h))
        pygame.draw.rect(self.game.screen, (200, 200, 200), (lx, ly, side_w, side_h), 3)

        txt_left_shadow = self.game.fuente_nombres.render(self.game.stages[prev_idx]["name"], True, (0, 0, 0))
        txt_left = self.game.fuente_nombres.render(self.game.stages[prev_idx]["name"], True, (180, 180, 180))
        rect_left = txt_left.get_rect(center=(lx + side_w // 2, ly + side_h + 20))
        self.game.screen.blit(txt_left_shadow, (rect_left.x + 2, rect_left.y + 2))
        self.game.screen.blit(txt_left, rect_left)

        if hasattr(self.game, 'stage_backgrounds') and self.game.stage_backgrounds[next_idx]:
            img_right = pygame.transform.smoothscale(self.game.stage_backgrounds[next_idx], (side_w, side_h))
            self.game.screen.blit(img_right, (rx, ry))
        else:
            pygame.draw.rect(self.game.screen, (50, 50, 50), (rx, ry, side_w, side_h))
        pygame.draw.rect(self.game.screen, (200, 200, 200), (rx, ry, side_w, side_h), 3)

        txt_right_shadow = self.game.fuente_nombres.render(self.game.stages[next_idx]["name"], True, (0, 0, 0))
        txt_right = self.game.fuente_nombres.render(self.game.stages[next_idx]["name"], True, (180, 180, 180))
        rect_right = txt_right.get_rect(center=(rx + side_w // 2, ry + side_h + 20))
        self.game.screen.blit(txt_right_shadow, (rect_right.x + 2, rect_right.y + 2))
        self.game.screen.blit(txt_right, rect_right)

        if hasattr(self.game, 'stage_backgrounds') and self.game.stage_backgrounds[self.stage_cursor]:
            img_center = pygame.transform.smoothscale(self.game.stage_backgrounds[self.stage_cursor], (center_w, center_h))
            self.game.screen.blit(img_center, (cx, cy))
        else:
            pygame.draw.rect(self.game.screen, (100, 100, 100), (cx, cy, center_w, center_h))
        pygame.draw.rect(self.game.screen, (255, 200, 0), (cx, cy, center_w, center_h), 6)

        txt_center_shadow = self.game.fuente_menu.render(self.game.stages[self.stage_cursor]["name"], True, (0, 0, 0))
        txt_center = self.game.fuente_menu.render(self.game.stages[self.stage_cursor]["name"], True, (255, 255, 255))
        rect_center = txt_center.get_rect(center=(self.game.S_WIDTH // 2, cy + center_h + 35))
        self.game.screen.blit(txt_center_shadow, (rect_center.x + 3, rect_center.y + 3))
        self.game.screen.blit(txt_center, rect_center)

        txt_bgm = self.game.fuente_nombres.render(f"TRACK: {self.game.stages[self.stage_cursor]['bgm']}", True, (0, 255, 255))
        txt_bgm_shadow = self.game.fuente_nombres.render(f"TRACK: {self.game.stages[self.stage_cursor]['bgm']}", True, (0, 0, 0))
        rect_bgm = txt_bgm.get_rect(center=(self.game.S_WIDTH // 2, cy + center_h + 75))
        self.game.screen.blit(txt_bgm_shadow, (rect_bgm.x + 2, rect_bgm.y + 2))
        self.game.screen.blit(txt_bgm, rect_bgm)

        txt_arrows_shadow = self.game.fuente_nombres.render("< PREV        NEXT >", True, (0, 0, 0))
        txt_arrows = self.game.fuente_nombres.render("< PREV        NEXT >", True, (255, 200, 0))
        rect_arrows = txt_arrows.get_rect(center=(self.game.S_WIDTH // 2, cy - 40))
        self.game.screen.blit(txt_arrows_shadow, (rect_arrows.x + 2, rect_arrows.y + 2))
        self.game.screen.blit(txt_arrows, rect_arrows)

        overlay = pygame.Surface((self.game.S_WIDTH, 60), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.game.screen.blit(overlay, (0, self.game.S_HEIGHT - 80))

        txt_info = self.game.fuente_nombres.render("Usa A/D o FLECHAS para cambiar. ENTER para COMBATIR", True, (200, 200, 200))
        rect_info = txt_info.get_rect(center=(self.game.S_WIDTH // 2, self.game.S_HEIGHT - 50))
        self.game.screen.blit(txt_info, rect_info)