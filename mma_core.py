import pygame
import os
import math
from .fighter import Fighter
from games import BaseGame

GAME_METADATA = {
    'id': 'mma_project',
    'title': 'Proyecto MMA',
    'description': 'Juego de combates 2D',
    'authors': ['Joswar Ramirez, Jose Areinamo'], 
    'group_number': 2 , 
    'cover_path': 'assets/covers/mma.png',
}

class MMAGame(BaseGame):
    def __init__(self):
        super().__init__()

        self.S_WIDTH = 1280
        self.S_HEIGHT = 720
        self.suelo = self.S_HEIGHT -50

        self.fighter_1 = Fighter(player=1, x =200, y=self.suelo -180)
        self.fighter_2 = Fighter(player=2, x =1000, y=self.suelo -180)

        pygame.font.init()

        font_path = os.path.join("games", "Assets", "font", "The King of Fighters Font.ttf")

        try:
            self.fuente_timer = pygame.font.Font(font_path, 55)
            self.fuente_ko = pygame.font.Font(font_path, 100)
            self.fuente_nombres = pygame.font.Font(font_path, 30)
            self.fuente_menu = pygame.font.Font(font_path, 40)
        except FileNotFoundError:
            print(f"Advertencia: No se encontró la fuente en {font_path}.")
            self.fuente_timer = pygame.font.SysFont("Arial", 55, bold=True)
            self.fuente_ko = pygame.font.SysFont("Impact", 100)
            self.fuente_nombres = pygame.font.SysFont("Arial", 30, bold=True)
            self.fuente_menu = pygame.font.SysFont("Arial", 40, bold=True)

        self.roundTime = 99
        self.Time = 0.0
        self.GameOver = False
        self.KO = ""
        self.is_paused = False
        self.pause_cooldown = 0

        self.state = "MENU"
        self.menu_options = ["JUGAR","SALIR"]
        self.selected_option = 0
        self.input_cooldown = 30
        self.bg_scroll = 0.0

        self.roster = ["RYU","TERRY","MAI","KYO"]
        self.p1_cursor = 0
        self.p2_cursor = 1
        self.p1_selected = False
        self.p2_selected = False

        self.stages = [
            {"name": "Escenario 1", "bgm": "OST 1"},
            {"name": "Escenario 2", "bgm": "OST 2"},
            {"name": "Escenario 3", "bgm": "OST 3"},
            {"name": "Escenario 4", "bgm": "OST 4"}
        ]
        self.stage_cursor = 0
    
    def draw_healthBar(self, health,x,y,is_playerOne):
        health = max(0,health)
        ratio = health / 100.0
        anchoMax = 450
        altoBarra = 35

        pygame.draw.rect(self.screen, (0, 0, 0), (x - 6, y - 6, anchoMax + 12, altoBarra + 12))
        pygame.draw.rect(self.screen, (200, 200, 200), (x - 3, y - 3, anchoMax + 6, altoBarra + 6))
        
        pygame.draw.rect(self.screen, (150, 0, 0), (x, y, anchoMax, altoBarra))

        anchoActual = anchoMax * ratio
        if is_playerOne:
            pygame.draw.rect(self.screen, (255,200,0), (x,y, anchoActual, altoBarra))
        else:
            pygame.draw.rect(self.screen, (255,200,0),(x + (anchoMax - anchoActual), y, anchoActual, altoBarra))
    
    def update(self, dt):
        key = pygame.key.get_pressed()

        if self.input_cooldown > 0:
            self.input_cooldown -= 1

        if self.state == "MENU":
            self.update_menu(dt,key)
        elif self.state == "SELECT":
            self.update_select(key)
        elif self.state == "STAGE":
            self.update_stage(key)
        elif self.state == "COMBAT":
            self.update_combat(dt, key)

    def ejecutar_opcion_menu(self):

        if self.menu_options[self.selected_option] == "JUGAR":
            self.state = "SELECT"
        elif self.menu_options[self.selected_option] == "SALIR":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.input_cooldown = 15

    def update_menu(self, dt, key):
        self.bg_scroll = (self.bg_scroll + 50 * dt) % 100

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if self.input_cooldown == 0:
            if key[pygame.K_UP]:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                self.input_cooldown = 15
            elif key[pygame.K_DOWN]:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                self.input_cooldown = 15
            elif key[pygame.K_RETURN]:
                self.ejecutar_opcion_menu()

            for i, option in enumerate(self.menu_options):
                txt_option = self.fuente_menu.render(option, True, (255, 255, 255))
                rect_option = txt_option.get_rect(center=(self.S_WIDTH // 2, 400 + (i * 70)))
                
                if rect_option.collidepoint(mouse_pos):
                    self.selected_option = i 
                    if mouse_click:
                        self.ejecutar_opcion_menu()
    
    def update_select(self,key):
        if self.input_cooldown == 0:

            if not self.p1_selected:
                if key[pygame.K_a]:
                    self.p1_cursor = (self.p1_cursor - 1) % len(self.roster)
                    self.input_cooldown = 15
                elif key[pygame.K_d]:
                    self.p1_cursor = (self.p1_cursor + 1) % len(self.roster)
                    self.input_cooldown = 15
                elif key[pygame.K_f]:
                    self.p1_selected = True
                    self.input_cooldown = 15

            if not self.p2_selected:
                if key[pygame.K_LEFT]:
                    self.p2_cursor = (self.p2_cursor - 1) % len(self.roster)
                    self.input_cooldown = 15
                elif key[pygame.K_RIGHT]:
                    self.p2_cursor = (self.p2_cursor + 1) % len(self.roster)
                    self.input_cooldown = 15
                elif key[pygame.K_RETURN]:
                    self.p2_selected = True
                    self.input_cooldown = 15    
            
            if key[pygame.K_ESCAPE]:
                if self.p1_selected or self.p2_selected:
                    self.p1_selected = False
                    self.p2_selected = False
                    self.input_cooldown = 15
                else:
                    self.state = "MENU"
                    self.input_cooldown = 15
            
            if self.p1_selected and self.p2_selected:
                self.state = "STAGE"
                self.input_cooldown = 15
    
    def update_stage(self,key):
        if self.input_cooldown == 0:
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                self.stage_cursor = (self.stage_cursor - 1) % len(self.stages)
                self.input_cooldown = 15
            elif key[pygame.K_RIGHT] or key[pygame.K_d]:
                self.stage_cursor = (self.stage_cursor + 1) % len(self.stages)
                self.input_cooldown = 15
            elif key[pygame.K_RETURN]:
                self.state = "COMBAT"
                self.input_cooldown = 15
            elif key[pygame.K_ESCAPE]:
                self.state = "SELECT"
                self.p1_selected = False
                self.p2_selected = False
                self.input_cooldown = 15

    def update_combat(self, dt,key):
        if key[pygame.K_ESCAPE] and self.input_cooldown == 0:
            self.is_paused = not self.is_paused
            self.input_cooldown = 15

        if self.is_paused or self.GameOver:
            return
            
        self.fighter_1.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_2)
        self.fighter_2.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_1)
        
        self.Time += dt
        if self.Time >= 1.0:
            if self.roundTime > 0:
                self.roundTime -= 1
            self.Time = 0.0

        if self.fighter_1.health <= 0 or self.fighter_2.health <= 0 or self.roundTime <= 0: 
            self.GameOver = True
            if self.fighter_1.health < self.fighter_2.health:
                self.KO = "P2 WINS"
            elif self.fighter_2.health < self.fighter_1.health:
                self.KO = "P1 WINS"
            else:
                self.KO = "DRAW"

    def draw(self):
        if not self.screen:
            return

        self.screen.fill((30,30,35))

        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "SELECT":
            self.draw_select()
        elif self.state == "STAGE":
            self.draw_stage()
        elif self.state == "COMBAT":
            self.draw_combat()

    def draw_menu(self):

        for i in range(-self.S_HEIGHT, self.S_WIDTH, 80):
            start_pos = (i + self.bg_scroll, 0)
            end_pos = (i + self.bg_scroll - self.S_HEIGHT, self.S_HEIGHT)
            pygame.draw.line(self.screen, (45, 45, 50), start_pos, end_pos, 10)
        
        scale_factor = 1.0 + math.sin(pygame.time.get_ticks() / 300.0) * 0.05

        font_size = int(100 * scale_factor)

        try:
            fuente_pulsante = pygame.font.Font(os.path.join("games", "Assets", "font", "The King of Fighters Font.ttf"), font_size)
        except:
            fuente_pulsante = pygame.font.SysFont("Impact", font_size)
        
        txt_titulo = fuente_pulsante.render("ART OF FIGHTERS", True, (255,200,0))
        txt_sombra = fuente_pulsante.render("ART OF FIGHTERS", True, (0,0,0))
        rect_titulo = txt_titulo.get_rect(center=(self.S_WIDTH //2,200))
        self.screen.blit(txt_sombra, (rect_titulo.x + 5, rect_titulo.y + 5))
        self.screen.blit(txt_titulo, rect_titulo)

        for i , option in enumerate(self.menu_options):
            color = (255,255,255) if i == self.selected_option else (100,100,100)
            txt_option = self.fuente_menu.render(option, True, color)
            rect_option = txt_option.get_rect(center=(self.S_WIDTH // 2, 400 + (i * 70)))
            self.screen.blit(txt_option, rect_option)

            if i == self.selected_option:
                cursor_rect = pygame.Rect(rect_option.left - 40, rect_option.centery - 10, 20, 20)
                pygame.draw.rect(self.screen, (255, 0, 0), cursor_rect)

    def draw_select(self):
        txt_titulo = self.fuente_menu.render("SELECCION DE PERSONAJE", True, (255, 255, 255))
        rect_titulo = txt_titulo.get_rect(center=(self.S_WIDTH // 2, 100))
        self.screen.blit(txt_titulo, rect_titulo)

        box_width = 160
        box_height = 160
        spacing = 40
        total_width = (len(self.roster) * box_width) + ((len(self.roster) - 1) * spacing)
        start_x = (self.S_WIDTH - total_width) // 2
        start_y = self.S_HEIGHT // 2 - box_height // 2

        for i, char_name in enumerate(self.roster):
            x = start_x + i * (box_width + spacing)
            y = start_y

            pygame.draw.rect(self.screen, (70,70,70), (x, y, box_width, box_height))

            txt_name = self.fuente_nombres.render(char_name, True, (200,200,200))
            rect_name = txt_name.get_rect(center=(x + box_width // 2, y + box_height + 25))
            self.screen.blit(txt_name, rect_name)

            if i == self.p1_cursor:
                color_p1 = (255,50,50)
                pygame.draw.rect(self.screen, color_p1, (x - 4, y - 4, box_width + 8, box_height + 8), 4)
                txt_p1 = self.fuente_nombres.render("P1", True, color_p1)
                self.screen.blit(txt_p1, (x + 5, y + 5))

                if self.p1_selected:
                    overlay = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
                    overlay.fill((255, 50, 50, 80))
                    self.screen.blit(overlay, (x, y))
            
            if i == self.p2_cursor:
                color_p2 = (50, 150, 255)
                offset = 10 if i == self.p1_cursor else -4
                pygame.draw.rect(self.screen, color_p2, (x - offset, y - offset, box_width + offset*2, box_height + offset*2), 4)
                txt_p2 = self.fuente_nombres.render("P2", True, color_p2)
                self.screen.blit(txt_p2, (x + box_width - 35, y + 5))

                if self.p2_selected:
                    overlay = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
                    overlay.fill((50, 150, 255, 80))
                    self.screen.blit(overlay, (x, y))
        
        inst_p1 = self.fuente_nombres.render("P1: A/D (Mover) - F (Elegir)", True, (255,100,100))
        inst_p2 = self.fuente_nombres.render("P2: Flechas (Mover) - ENTER (Elegir)", True, (100, 200, 255))
        self.screen.blit(inst_p1, (50, self.S_HEIGHT - 60))
        self.screen.blit(inst_p2, (self.S_WIDTH - inst_p2.get_width() - 50, self.S_HEIGHT - 60))
        
    def draw_stage(self):
        txt_titulo = self.fuente_menu.render("SELECCION DE ESCENARIO Y BGM", True, (255, 255, 255))
        rect_titulo = txt_titulo.get_rect(center=(self.S_WIDTH // 2, 100))
        self.screen.blit(txt_titulo, rect_titulo)

        prev_idx = (self.stage_cursor - 1) % len(self.stages)
        next_idx = (self.stage_cursor + 1) % len(self.stages)

        center_w, center_h = 400, 250
        cx = self.S_WIDTH // 2 - center_w // 2
        cy = self.S_HEIGHT // 2 - center_h // 2 - 20
        pygame.draw.rect(self.screen, (100, 100, 100), (cx, cy, center_w, center_h))
        pygame.draw.rect(self.screen, (255, 200, 0), (cx, cy, center_w, center_h), 6)

        txt_center = self.fuente_menu.render(self.stages[self.stage_cursor]["name"], True, (255, 255, 255))
        self.screen.blit(txt_center, txt_center.get_rect(center=(self.S_WIDTH // 2, cy + center_h + 30)))

        txt_bgm = self.fuente_nombres.render(f"BGM: {self.stages[self.stage_cursor]['bgm']}", True, (0, 255, 255))
        self.screen.blit(txt_bgm, txt_bgm.get_rect(center=(self.S_WIDTH // 2, cy + center_h + 70)))

        side_w, side_h = 250, 150
        lx = cx - side_w - 50
        ly = self.S_HEIGHT // 2 - side_h // 2 - 20
        pygame.draw.rect(self.screen, (50, 50, 50), (lx, ly, side_w, side_h))
        txt_left = self.fuente_nombres.render(self.stages[prev_idx]["name"], True, (100, 100, 100))
        self.screen.blit(txt_left, txt_left.get_rect(center=(lx + side_w // 2, ly + side_h + 20)))

        rx = cx + center_w + 50
        ry = self.S_HEIGHT // 2 - side_h // 2 - 20
        pygame.draw.rect(self.screen, (50, 50, 50), (rx, ry, side_w, side_h))
        txt_right = self.fuente_nombres.render(self.stages[next_idx]["name"], True, (100, 100, 100))
        self.screen.blit(txt_right, txt_right.get_rect(center=(rx + side_w // 2, ry + side_h + 20)))
        
        txt_arrows = self.fuente_nombres.render("< PREV        NEXT >", True, (200, 200, 200))
        self.screen.blit(txt_arrows, txt_arrows.get_rect(center=(self.S_WIDTH // 2, cy - 40)))

        txt_info = self.fuente_nombres.render("Usa A/D o FLECHAS para cambiar. ENTER para COMBATIR", True, (150, 150, 150))
        rect_info = txt_info.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT - 50))
        self.screen.blit(txt_info, rect_info)

    def draw_combat(self):
        pygame.draw.rect(self.screen, (100, 100, 100), (0, self.suelo, self.S_WIDTH, 50))

        self.fighter_1.dibujar(self.screen)
        self.fighter_2.dibujar(self.screen)

        txt_p1 = self.fuente_nombres.render("Player 1", True, (255, 255, 255))
        txt_p2 = self.fuente_nombres.render("Player 2", True, (255, 255, 255))
        self.screen.blit(txt_p1, (40, 65))
        self.screen.blit(txt_p2, (self.S_WIDTH - 120, 65))

        self.draw_healthBar(self.fighter_1.health, 40, 25, is_playerOne=True)
        self.draw_healthBar(self.fighter_2.health, self.S_WIDTH - 490, 25, is_playerOne=False)

        txt_timer = self.fuente_timer.render(f"{self.roundTime:02d}", True, (255, 200, 0))
        rect_timer = txt_timer.get_rect(center=(self.S_WIDTH // 2, 42))

        pygame.draw.rect(self.screen, (0, 0, 0), (rect_timer.x - 15, rect_timer.y - 5, rect_timer.width + 30, rect_timer.height + 10))
        pygame.draw.rect(self.screen, (255, 200, 0), (rect_timer.x - 15, rect_timer.y - 5, rect_timer.width + 30, rect_timer.height + 10), 3)
        self.screen.blit(txt_timer, rect_timer)

        if self.GameOver:
            overlay = pygame.Surface((self.S_WIDTH, self.S_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            txt_ko = self.fuente_ko.render("K.O.", True, (255, 50, 50))
            rect_ko = txt_ko.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 - 60))
            self.screen.blit(txt_ko, rect_ko)

            txt_ganador = self.fuente_timer.render(self.KO, True, (255, 255, 255))
            rect_ganador = txt_ganador.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 + 50))
            self.screen.blit(txt_ganador, rect_ganador)

        if self.is_paused and not self.GameOver:
            overlay = pygame.Surface((self.S_WIDTH, self.S_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            txt_pausa = self.fuente_ko.render("PAUSED", True, (255, 255, 255))
            rect_pausa = txt_pausa.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 - 30))
            self.screen.blit(txt_pausa, rect_pausa)

            txt_sub = self.fuente_nombres.render("Presiona ESC para continuar", True, (200, 200, 200))
            rect_sub = txt_sub.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 + 70))
            self.screen.blit(txt_sub, rect_sub)
        

GAME_CLASS = MMAGame  