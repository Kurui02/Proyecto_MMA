import pygame
import os
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
        except FileNotFoundError:
            print(f"Advertencia: No se encontró la fuente en {font_path}.")
            self.fuente_timer = pygame.font.SysFont("Arial", 55, bold=True)
            self.fuente_ko = pygame.font.SysFont("Impact", 100)
            self.fuente_nombres = pygame.font.SysFont("Arial", 30, bold=True)
        
        self.roundTime = 99
        self.Time = 0.0
        self.GameOver = False
        self.KO = ""
    
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
        if not self.GameOver:
            self.fighter_1.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_2)
            self.fighter_2.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_1)
        
        self.Time += dt
        if self.Time >= 1.0:
            if self.roundTime > 0:
                self.roundTime -=1
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
        if self.screen:
            self.screen.fill((30,30,35))

            pygame.draw.rect(self.screen, (100, 100, 100), (0, self.suelo, self.S_WIDTH, 50))

            self.fighter_1.dibujar(self.screen)
            self.fighter_2.dibujar(self.screen)

            txt_p1 = self.fuente_nombres.render("Player 1", True, (255,255,255))
            txt_p2 = self.fuente_nombres.render("Player 2", True, (255,255,255))
            self.screen.blit(txt_p1, (40,65))
            self.screen.blit(txt_p2, (self.S_WIDTH -120, 65))

            self.draw_healthBar(self.fighter_1.health, 40, 25, is_playerOne=True)
            self.draw_healthBar(self.fighter_2.health, self.S_WIDTH - 490, 25, is_playerOne=False)

            txt_timer = self.fuente_timer.render(f"{self.roundTime:02d}", True, (255,200,0))
            rect_timer = txt_timer.get_rect(center=(self.S_WIDTH // 2 , 42))

            pygame.draw.rect(self.screen, (0,0,0), (rect_timer.x - 15, rect_timer.y - 5 , rect_timer.width + 30, rect_timer.height + 10))
            pygame.draw.rect(self.screen, (255, 200, 0), (rect_timer.x - 15, rect_timer.y - 5, rect_timer.width + 30, rect_timer.height + 10), 3)
            self.screen.blit(txt_timer, rect_timer)

            if self.GameOver:
                overlay = pygame.Surface((self.S_WIDTH, self.S_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0,0,0,180))
                self.screen.blit(overlay,(0,0))

                txt_ko = self.fuente_ko.render("K.O.", True, (255,50,50))
                rect_ko = txt_ko.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 - 60))
                self.screen.blit(txt_ko, rect_ko)

                txt_ganador = self.fuente_timer.render(self.KO, True, (255, 255, 255))
                rect_ganador = txt_ganador.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 + 50))
                self.screen.blit(txt_ganador, rect_ganador)
        

GAME_CLASS = MMAGame  