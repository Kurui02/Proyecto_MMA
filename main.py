import pygame
import sys
from fighter import Fighter
from menu import MenuManager
from pathlib import Path

class MMAGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.S_WIDTH = 1280
        self.S_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.S_WIDTH, self.S_HEIGHT))
        pygame.display.set_caption("Art of Fighters")
        self.clock = pygame.time.Clock()
        self.suelo = self.S_HEIGHT -50
        self.running = True

        self.BASE_DIR = Path(__file__).resolve().parent
        
        font_path = self.BASE_DIR / "assets" / "font" / "The King of Fighters Font.ttf"
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

        self.audioDir = self.BASE_DIR / "assets" / "sound effect"
        self.current_bgm = None
        self.sfx_library = {}
        self.load_audio()
        self.play_bgm("menu.mp3")

        self.roundTime = 99
        self.Time = 0.0
        self.is_paused = False

        self.p1_wins = 0
        self.p2_wins = 0
        self.max_wins = 2
        self.roundNumber = 1

        self.round_over = False
        self.match_over = False
        self.roundDelay = 0.0
        self.winner_msg = ""
        self.state = "MENU"
        self.input_cooldown = 30
        self.game_mode = "P2"
        

        self.roster = ["YURI","KIM","GAI","KASUMI",]
        self.stages = [
            {"name": "Escenario 1", "bgm": "Ost 1.mp3"},
            {"name": "Escenario 2", "bgm": "Ost 2.mp3"},
            {"name": "Escenario 3", "bgm": "Ost 3.mp3"},
            {"name": "Escenario 4", "bgm": "Ost 4.mp3"}
        ]
        
        self.p1_cursor = 0
        self.p2_cursor = 1
        self.stage_cursor = 0

        self.load_visual()

        isCpu =(self.game_mode == "CPU")
        self.menu = MenuManager(self)
        self.fighter_1 = Fighter(player=1, x =200, y=self.suelo -180, char_name=self.roster[self.p1_cursor])
        self.fighter_2 = Fighter(player=2, x =1000, y=self.suelo -180,char_name=self.roster[self.p2_cursor],is_cpu=isCpu)

    def run(self):
        while self.running:

            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.update(dt)
            self.draw()

            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def update(self,dt):
        
        key = pygame.key.get_pressed()

        if self.input_cooldown > 0:
            self.input_cooldown -=1
        
        if self.state in ["MENU", "SELECT", "STAGE"]:
            self.menu.update(dt, key)
        elif self.state == "COMBAT":
            self.update_combat(dt, key)

    def draw(self):
        self.screen.fill((30, 30, 35))

        if self.state in ["MENU", "SELECT", "STAGE"]:
            self.menu.draw()
        elif self.state == "COMBAT":
            self.draw_combat()
               
    def load_visual(self):
        self.stage_backgrounds = []
        bg_folder = self.BASE_DIR / "assets" / "background"
        bg_files = ["background 1.png", "background 2.png", "background3.png", "background4.png"] 
        
        for bg_file in bg_files:
            path = bg_folder / bg_file

            if path.exists():
                img = pygame.image.load(str(path)).convert()
                self.stage_backgrounds.append(pygame.transform.scale(img, (self.S_WIDTH, self.S_HEIGHT)))
            else:
                self.stage_backgrounds.append(None)
                print(f"[Aviso] No se encontró el fondo en: {path}")

        self.portraits = {}
        for char in self.roster:
            path = self.BASE_DIR / "assets" / "Portrait" / f"{char.capitalize()}.png"
            if path.exists():
                self.portraits[char] = pygame.image.load(str(path)).convert_alpha()
            else:
                print(f"[Aviso] No se encontró el portrait en: {path}")

    def load_audio(self):
        sfx_files = {
            "select": "select.wav",
            "hit": "hit.wav",
            "ko": "ko.wav",
            "back": "back.wav",
            "win": "win.wav",
            "selectCharacter": "selectCharacter.wav",
            "fight":"fight.wav"
        }
        for name, filename in sfx_files.items():
            path = self.audioDir / filename
            if path.exists():
                try:
                    sound = pygame.mixer.Sound(str(path))
                    sound.set_volume(0.18) 
                    self.sfx_library[name] = sound
                except Exception as e:
                    print(f"Error cargando SFX {filename}: {e}")
            else:
                print(f"Aviso: Archivo de sonido no encontrado: {path}")

    def play_bgm(self, filename):
        if self.current_bgm == filename:
            return
        
        path = self.audioDir / filename
        if path.exists():
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.set_volume(0.25)
                pygame.mixer.music.play(-1) 
                self.current_bgm = filename
            except Exception as e:
                print(f"No se pudo reproducir la música {filename}: {e}")
        else:
            print(f"Aviso BGM: No se encuentra el archivo {path}")
    
    def play_sfx(self, name):
        if name in self.sfx_library:
            self.sfx_library[name].play()
    
    def reset_match(self):
        self.p1_wins = 0
        self.p2_wins = 0
        self.round_number = 1
        self.match_over = False
        self.reset_round()
    
    def reset_round(self):
        self.fighter_1.health = 100
        self.fighter_2.health = 100
        self.fighter_1.rect.x = 200
        self.fighter_2.rect.x = 1000

    
        for f in [self.fighter_1, self.fighter_2]:
            f.is_winner = False
            f.is_loser = False
            f.action = "idle"
            f.frame_index = 0
            f.hit = False
            f.stun = 0
            f.knockback = 0
            f.attacking = False
            f.attack_phase = "idle"

        self.roundTime = 99
        self.Time = 0.0
        self.round_over = False
        self.winner_msg = ""
    
    def update_combat(self, dt, key):
        if self.is_paused:
            if self.input_cooldown == 0: 
                if key[pygame.K_ESCAPE]: 
                    self.is_paused = False
                    pygame.mixer.music.unpause()
                    self.input_cooldown = 15
                elif key[pygame.K_TAB]: 
                    self.current_bgm = None
                    self.play_bgm("menu.mp3")
                    self.state = "MENU"
                    self.is_paused = False
                    self.input_cooldown = 15
            return
            
        if self.match_over:
            if key[pygame.K_RETURN]:
                self.play_bgm("menu.mp3")
                self.state = "MENU"
                self.input_cooldown = 15

            self.fighter_1.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_2)
            self.fighter_2.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_1)
            self.fighter_1.update_animation()
            self.fighter_2.update_animation()
            return
            
        if self.input_cooldown == 0:
            if key[pygame.K_ESCAPE] and not self.round_over:
                self.is_paused = True
                pygame.mixer.music.pause()
                self.input_cooldown = 15
                return
        
        if self.round_over:
            self.roundDelay -= dt

            if self.roundDelay <= 0:
                if self.p1_wins >= self.max_wins or self.p2_wins >= self.max_wins:
                    self.match_over = True
                    self.play_sfx("win")
                else:
                    self.roundNumber += 1 
                    self.reset_round()
                    self.play_sfx("fight")
                    pygame.mixer.music.unpause()
            
            if self.roundDelay < 2.5:
                if self.fighter_1.health <= 0 and self.fighter_2.health > 0:
                    self.fighter_1.is_loser = True
                    self.fighter_2.is_winner = True
                elif self.fighter_2.health <= 0 and self.fighter_1.health > 0:
                    self.fighter_2.is_loser = True
                    self.fighter_1.is_winner = True
                elif self.fighter_1.health <= 0 and self.fighter_2.health <= 0: 
                    self.fighter_1.is_loser = True
                    self.fighter_2.is_loser = True
                
            self.fighter_1.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_2)
            self.fighter_2.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_1)
            self.fighter_1.update_animation()
            self.fighter_2.update_animation()
            return

        p1_pre_health = self.fighter_1.health
        p2_pre_health = self.fighter_2.health

        self.fighter_1.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_2)
        self.fighter_2.move(self.S_WIDTH, self.S_HEIGHT, self.suelo, self.fighter_1)
        
        self.fighter_1.update_animation()
        self.fighter_2.update_animation()
        
        if self.fighter_1.health < p1_pre_health or self.fighter_2.health < p2_pre_health:
            self.play_sfx("hit")

        self.Time += dt
        if self.Time >= 1.0:
            if self.roundTime > 0:
                self.roundTime -= 1
            self.Time = 0.0

        if self.fighter_1.health <= 0 or self.fighter_2.health <= 0 or self.roundTime <= 0: 
            self.round_over = True
            self.roundDelay = 3.0
            self.play_sfx("ko")

            if self.fighter_1.health < self.fighter_2.health:
                self.winner_msg = "P2 WINS ROUND"
                self.p2_wins += 1
            elif self.fighter_2.health < self.fighter_1.health:
                self.winner_msg = "P1 WINS ROUND"
                self.p1_wins += 1
            else:
                self.winner_msg = "DRAW"
    
    def draw_combat(self):
        if self.stage_cursor < len(self.stage_backgrounds) and self.stage_backgrounds[self.stage_cursor]:
            self.screen.blit(self.stage_backgrounds[self.stage_cursor], (0, 0))
        else:
            self.screen.fill((30, 30, 35))
            pygame.draw.rect(self.screen, (100, 100, 100), (0, self.suelo, self.S_WIDTH, 50))

        self.fighter_1.dibujar(self.screen)
        self.fighter_2.dibujar(self.screen)

        nombre_p1_texto = self.roster[self.p1_cursor]
        nombre_p2_texto = self.roster[self.p2_cursor]

        nombre_p1 = self.fuente_nombres.render(nombre_p1_texto, True, (255, 255, 255))
        nombre_p2 = self.fuente_nombres.render(nombre_p2_texto, True, (255, 255, 255))

        pos_texto_p1 = (50, 70) 
        pos_texto_p2 = (self.S_WIDTH - 50 - nombre_p2.get_width(), 70)
        padding_x = 10
        padding_y = 4 
        rect_bg_p1 = pygame.Rect(
            pos_texto_p1[0] - padding_x, pos_texto_p1[1] - padding_y, 
            nombre_p1.get_width() + (padding_x * 2), nombre_p1.get_height() + (padding_y * 2)
        )
        rect_bg_p2 = pygame.Rect(
            pos_texto_p2[0] - padding_x, pos_texto_p2[1] - padding_y, 
            nombre_p2.get_width() + (padding_x * 2), nombre_p2.get_height() + (padding_y * 2)
        )

        color_p1 = (15, 25, 60)      
        color_p2 = (80, 15, 15)       
        color_borde = (255, 215, 0)
        
        pygame.draw.rect(self.screen, color_p1, rect_bg_p1)
        pygame.draw.rect(self.screen, color_p2, rect_bg_p2)
        pygame.draw.rect(self.screen, color_borde, rect_bg_p1, 2)
        pygame.draw.rect(self.screen, color_borde, rect_bg_p2, 2)

        self.screen.blit(nombre_p1, pos_texto_p1)
        self.screen.blit(nombre_p2, pos_texto_p2)

        shadow_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (2, 2)]

        txt_round = self.fuente_nombres.render(f"ROUND {self.roundNumber}", True, (200, 200, 200)) 
        rect_r = txt_round.get_rect(center=(self.S_WIDTH // 2, 90))
        
        for dx, dy in shadow_offsets:
            txt_round_shadow = self.fuente_nombres.render(f"ROUND {self.roundNumber}", True, (0, 0, 0))
            self.screen.blit(txt_round_shadow, (rect_r.x + dx, rect_r.y + dy))
        self.screen.blit(txt_round, rect_r)

        self.draw_healthBar(self.fighter_1.health, 40, 25, is_playerOne=True)
        self.draw_healthBar(self.fighter_2.health, self.S_WIDTH - 490, 25, is_playerOne=False)

        self.draw_wins(self.p1_wins, 50, 120, align_left=True)
        self.draw_wins(self.p2_wins, self.S_WIDTH - 50, 120, align_left=False)

        txt_timer = self.fuente_timer.render(f"{self.roundTime:02d}", True, (255, 200, 0))
        rect_timer = txt_timer.get_rect(center=(self.S_WIDTH // 2, 42))

        pygame.draw.rect(self.screen, (0, 0, 0), (rect_timer.x - 15, rect_timer.y - 5, rect_timer.width + 30, rect_timer.height + 10))
        pygame.draw.rect(self.screen, (255, 200, 0), (rect_timer.x - 15, rect_timer.y - 5, rect_timer.width + 30, rect_timer.height + 10), 3)
        self.screen.blit(txt_timer, rect_timer)

        if self.match_over:
            winner_final = "P1 WINS MATCH!" if self.p1_wins > self.p2_wins else "P2 WINS MATCH!"
            txt_ko = self.fuente_ko.render("K.O.", True, (255, 50, 50))
            rect_ko = txt_ko.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 - 60))
            self.screen.blit(txt_ko, rect_ko)

            txt_ganador = self.fuente_timer.render(winner_final, True, (255, 215, 0))
            rect_ganador = txt_ganador.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 + 50))
            self.screen.blit(txt_ganador, rect_ganador)
                
            txt_exit = self.fuente_nombres.render("Presiona ENTER para Volver al Menu", True, (200, 200, 200))
            self.screen.blit(txt_exit, txt_exit.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT - 100)))
        else:
            txt_ganador = self.fuente_timer.render(self.winner_msg, True, (255, 255, 255))
            rect_ganador = txt_ganador.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2))
            self.screen.blit(txt_ganador, rect_ganador)

        if self.is_paused and not self.round_over:
            overlay = pygame.Surface((self.S_WIDTH, self.S_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            txt_pausa = self.fuente_ko.render("PAUSED", True, (255, 255, 255))
            rect_pausa = txt_pausa.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 - 30))
            self.screen.blit(txt_pausa, rect_pausa)

            txt_sub = self.fuente_nombres.render("Presiona ESC para continuar", True, (200, 200, 200))
            rect_sub = txt_sub.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 + 70))
            self.screen.blit(txt_sub, rect_sub)

            txt_sub2 = self.fuente_nombres.render("Presiona TAB para volver al Menu", True, (200, 200, 200))
            rect_sub2 = txt_sub2.get_rect(center=(self.S_WIDTH // 2, self.S_HEIGHT // 2 + 20))
            self.screen.blit(txt_sub2, rect_sub2)

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
    
    def draw_wins(self, wins, x, y, align_left=True):
        radius = 12
        spacing = 35

        for i in range(self.max_wins):
            cx = x + (i * spacing) if align_left else x - (i * spacing)

            pygame.draw.circle(self.screen, (200, 200, 200), (cx, y), radius, 2)
            
            if i < wins:
                pygame.draw.circle(self.screen, (255, 100, 0), (cx, y), radius - 3)
            else:
                pygame.draw.circle(self.screen, (50, 50, 50), (cx, y), radius - 3)

if __name__ == "__main__":
    juego = MMAGame()
    juego.run()
    