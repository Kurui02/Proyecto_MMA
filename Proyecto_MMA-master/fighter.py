import pygame
from spritesheet import SpriteSheet
from pathlib import Path

Roster_Config = {
    "YURI": {
        "folder": "Yuri",
        "scale": 2.5,
        "offset_y": 15,
        "frames":{"idle":7,"run":6,"jump":6,"attack":5,"hit":5,"block":4,"win":1,"lose":1,"crouch":1,"low_attack":8},
        "frame_data": {
            "attack": {
                "startup": 1,
                "active": 2,
                "recovery": 2,
                "damage": 10,
                "knockback": 15
            },
            "low_attack": {
                "startup": 2,  
                "active": 3,     
                "recovery": 3,   
                "damage": 7,
                "knockback": 6
            }
        }
    },
    "KIM": {
        "folder": "Kim",
        "scale": 2.5,
        "offset_y": 10,
        "frames": {"idle": 8, "run": 6, "jump": 5, "attack": 5, "hit": 6, "block": 4,"win":1,"lose":1,"crouch":1,"low_attack":7},
        "frame_data": {
            "attack": {
                "startup": 1,  
                "active": 2,     
                "recovery": 2,   
                "damage": 10,
                "knockback": 15
            },
            "low_attack": {
                "startup": 2,  
                "active": 3,     
                "recovery": 2,   
                "damage": 6,
                "knockback": 6
            }
        }
    },
    "KASUMI": {
        "folder": "Kasumi",
        "scale": 2.5,
        "offset_y": 10,
        "frames": {"idle": 8, "run": 6, "jump": 5, "attack": 7, "hit": 4, "block": 4,"win":1,"lose":1,"crouch":1,"low_attack":5},
        "frame_data": {
            "attack": {
                "startup": 3,  
                "active": 2,     
                "recovery": 2,   
                "damage": 10,
                "knockback": 15
            },
            "low_attack": {
                "startup": 1,  
                "active": 2,     
                "recovery": 2,   
                "damage": 5,
                "knockback": 6
            }
        }
    },
    "GAI": {
        "folder": "Gai",
        "scale": 2.5,
        "offset_y": 10,
        "frames":{"idle":8,"run":7,"jump":9,"attack":5,"hit":6,"block":5,"win":1,"lose":1,"crouch":1,"low_attack":5},
        "frame_data": {
            "attack": {
                "startup": 1,
                "active": 2,
                "recovery": 2,
                "damage": 10,
                "knockback": 15
            },
            "low_attack": {
                "startup": 1,  
                "active": 2,     
                "recovery": 2,   
                "damage": 5,
                "knockback": 6
            }
        }
    }
}

class Fighter:
    def __init__(self, player,x,y, char_name="YURI"):
        self.player = player
        self.char_name = char_name.upper()

        self.width = 80
        self.height = 180
        self.rect = pygame.Rect((x,y,self.width, self.height))

        self.vel_y =0
        self.speed = 8
        self.jump_force = -25
        self.gravity = 2
        self.isJumping = False 
        self.isCrouching = False

        self.flip = False
        self.attacking = False 
        self.attack_phase = "idle"
        self.attackCooldown = 0
        self.attackingc = False 
        self.attack_phasec = "idle"

        self.attack_rect= pygame.Rect(0,0,0,0)
        self.attack_rectc= pygame.Rect(0,0,0,0)

        self.health = 100
        self.hit = False
        self.damage = 10 

        self.stun = 0
        self.knockback = 0
        self.isBlocking = False

        self.is_winner = False
        self.is_loser = False

        self.base = (50,150,255) if self.player == 1 else (255,50,50)
        self.color = self.base

        self.base_dir = Path(__file__).resolve().parent
        self.config = Roster_Config.get(self.char_name)
        if not self.config:
            print(f"Advertencia: {self.char_name} no existe en ROSTER_CONFIG. Cargando fallback.")
            self.config = Roster_Config["YURI"]
        self.scale = self.config["scale"]
        self.offset_y = self.config["offset_y"]
        self.fd = self.config["frame_data"]["attack"]
        self.fdc = self.config["frame_data"]["low_attack"]

        self.animation_list = {}
        self.action = "idle"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        self.load_animations()

        if "idle" in self.animation_list and len(self.animation_list["idle"]) > 0:
            self.image = self.animation_list[self.action][self.frame_index]
        else:
            self.image = None
    
    def load_animations(self):
        folder = self.config["folder"]
        frame_counts = self.config["frames"]
        path = self.base_dir / "Assets" / "Sprites" / folder

        for animation_name, num_frames in frame_counts.items():
            filename = path / f"{animation_name}.png"

            try:
                if filename.exists():
                    sheet = SpriteSheet(str(filename))
                    self.animation_list[animation_name] = sheet.load_strip(num_frames=num_frames, scale_factor=self.scale)
                else:
                    print(f"Aviso: No se encuentra el archivo {filename}")
                    self.animation_list[animation_name] = []
            except Exception as e:
                print(f"Error cargando animación {animation_name} para {self.char_name}: {e}")
                self.animation_list[animation_name] = []

    def update_action(self, new_action):
        if new_action != self.action and new_action in self.animation_list:
            if len(self.animation_list[new_action]) > 0:
                self.action = new_action
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()
    
    def update_animation(self):

        if self.is_winner:
            self.update_action("win")
            self.image = self.animation_list[self.action][0] if self.animation_list[self.action] else None
            return
        
        if self.is_loser:
            self.update_action("lose")
            self.image = self.animation_list[self.action][0] if self.animation_list[self.action] else None
            return
        
        Animation_cooldown = 120

        if self.action in self.animation_list and len(self.animation_list[self.action]) > 0:
            
            safe_index = min(self.frame_index, len(self.animation_list[self.action]) - 1)
            self.image = self.animation_list[self.action][safe_index]
            
            if pygame.time.get_ticks() - self.update_time > Animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
                
                if self.action == "attack":
                    if self.frame_index < self.fd["startup"]:
                        self.attack_phase = "startup"
                    
                    elif self.frame_index < (self.fd["startup"] + self.fd["active"]):
                        self.attack_phase = "active"
                
                        if not self.hit: 
                            if self.flip:
                                self.attack_rect = pygame.Rect(self.rect.left - 80, self.rect.y + 40, 80, 40)
                            else:
                                self.attack_rect = pygame.Rect(self.rect.right, self.rect.y + 40, 80, 40)
                            
                    elif self.frame_index < (self.fd["startup"] + self.fd["active"] + self.fd["recovery"]):
                        self.attack_phase = "recovery"
                        self.attack_rect = pygame.Rect(0, 0, 0, 0) 
                        self.hit = True 
                    
                    else: 
                        self.attacking = False
                        self.hit = False
                        self.frame_index = 0
                        self.attack_phase = "idle"
                        self.attack_rect = pygame.Rect(0, 0, 0, 0)

                if self.action == "low_attack":
                    if self.frame_index < self.fdc["startup"]:
                        self.attack_phasec = "startup"
                                    
                    elif self.frame_index < (self.fdc["startup"] + self.fdc["active"]):
                        self.attack_phasec = "active"
                                
                        if not self.hit: 
                            if self.flip:
                                self.attack_rectc = pygame.Rect(self.rect.left - 80, self.rect.y + 40, 80, 40)
                            else:
                                self.attack_rectc = pygame.Rect(self.rect.right, self.rect.y + 40, 80, 40)
                                            
                    elif self.frame_index < (self.fdc["startup"] + self.fdc["active"] + self.fdc["recovery"]):
                        self.attack_phasec = "recovery"
                        self.attack_rectc = pygame.Rect(0, 0, 0, 0) 
                        self.hit = True 
                                    
                    else: 
                        self.attackingc = False
                        self.hit = False
                        self.frame_index = 0
                        self.attack_phasec = "idle"
                        self.attack_rectc = pygame.Rect(0, 0, 0, 0)

                elif self.action == "hit":
                    if self.frame_index >= len(self.animation_list["hit"]):
                        self.stun = 0 
                        self.frame_index = 0
                        
                else:
                    if self.frame_index >= len(self.animation_list[self.action]):
                        self.frame_index = 0


    def move(self, screen_width, screen_height, floor_y, target):

        if self.is_winner or self.is_loser:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            if self.rect.bottom > floor_y:
                self.rect.bottom = floor_y
            self.update_animation()
            return
        
        Speed = self.speed
        dx=0
        dy=0

        if self.stun > 0:
            self.rect.x += self.knockback
            self.stun -= 1

            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > screen_width:
                self.rect.right = screen_width

            if self.knockback > 0:
                self.knockback = max(0, self.knockback - 1)
            elif self.knockback < 0:
                self.knockback = min(0, self.knockback + 1)
            
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            if self.rect.bottom > floor_y:
                self.rect.bottom = floor_y
                self.vel_y = 0
                self.isJumping = False
            
            self.update_action("hit" if not self.isBlocking else "block")
            self.update_animation()
            return

        key = pygame.key.get_pressed()
        self.isBlocking = False
        if not self.attacking and not self.attackingc:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -Speed
                    if target.rect.centerx > self.rect.centerx:
                        self.isBlocking = True
                if key[pygame.K_d]:
                    dx = Speed
                    if target.rect.centerx < self.rect.centerx:
                        self.isBlocking = True
                if key[pygame.K_w] and not self.isJumping: 
                    self.vel_y = self.jump_force
                    self.isJumping = True
                if (key[pygame.K_r] or key[pygame.K_t]) and not self.isCrouching: 
                    self.attack()
                if (key[pygame.K_r] or key[pygame.K_t]) and self.isCrouching: 
                    self.attackc()
                if key[pygame.K_s]:
                    self.isCrouching = True
                else:
                    self.isCrouching = False
        
            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -Speed
                    if target.rect.centerx > self.rect.centerx:
                        self.isBlocking = True
                if key[pygame.K_RIGHT]:
                    dx = Speed
                    if target.rect.centerx < self.rect.centerx:
                        self.isBlocking = True
                if key[pygame.K_UP] and not self.isJumping: 
                    self.vel_y = self.jump_force
                    self.isJumping = True
                if (key[pygame.K_o] or key[pygame.K_p]) and not self.isCrouching: 
                    self.attack()
                if (key[pygame.K_o] or key[pygame.K_p]) and self.isCrouching: 
                    self.attackc()
                if key[pygame.K_DOWN]:
                    self.isCrouching = True
                else:
                    self.isCrouching = False
        
        self.vel_y += self.gravity
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        
        if self.rect.bottom + dy > floor_y:
            self.vel_y = 0
            dy = floor_y - self.rect.bottom
            self.isJumping = False
        
        self.rect.x += dx
        self.rect.y += dy

        if target.rect.centerx > self.rect.centerx: 
            self.flip = False
        else:
            self.flip = True
        
        if self.attacking and self.attack_phase == "active" and not self.hit: 
            if self.attack_rect.colliderect(target.rect):
                
                damage_base = self.fd["damage"]
                force_knockback = self.fd["knockback"]
                
                frames_stun = len(target.animation_list.get("hit", [1] * 4)) * 10
                
                if target.isBlocking:
                    target.health -= damage_base * 0.2
                    target.stun = 15 
                    target.update_action("block") 
                else:
                    target.health -= damage_base
                    target.stun = frames_stun 
                    target.update_action("hit") 
                
                if self.rect.centerx < target.rect.centerx:
                    target.knockback = force_knockback
                else:
                    target.knockback = -force_knockback
                
                self.hit = True 

        if self.attackingc and self.attack_phasec == "active" and not self.hit and self.isCrouching: 
                    if self.attack_rectc.colliderect(target.rect):
                    
                        damage_base = self.fdc["damage"]
                        force_knockback = self.fdc["knockback"]
                       
                        
                        frames_stun = len(target.animation_list.get("hit", [1] * 4)) * 10
                        
                        if target.isBlocking:
                            target.health -= damage_base * 0.2
                            target.stun = 15 
                            target.update_action("block") 
                        else:
                            target.health -= damage_base
                            target.stun = frames_stun 
                            target.update_action("hit") 
                        
                        if self.rect.centerx < target.rect.centerx:
                            target.knockback = force_knockback
                        else:
                            target.knockback = -force_knockback
                        
                        self.hit = True

        if self.attacking:
            self.update_action("attack")
        elif self.attackingc and self.isCrouching and dx == 0:
            self.update_action("low_attack")
        elif self.isBlocking and dx != 0:
            self.update_action("block")
        elif self.isJumping or self.vel_y != 0:
            self.update_action("jump")
        elif dx != 0:
            self.update_action("run")
        elif self.isCrouching and dx == 0:
            self.update_action("crouch")
        else:
            self.update_action("idle")

        self.update_animation()

    def attack(self):
        if not self.attacking and self.stun <= 0: 
            self.attacking = True
            self.hit = False
            self.frame_index = 0
          
            self.action = "attack"

            self.attack_phase = "startup"
            self.update_time = pygame.time.get_ticks()

    def attackc(self):
        if not self.attackingc and self.stun <= 0: 
            self.attackingc = True
            self.hit = False
            self.frame_index = 0
            
            self.action = "low_attack"
            
            self.attack_phasec = "startup"
            self.update_time = pygame.time.get_ticks()

    
           
    def dibujar(self, surface):
       
        if self.image:
            img = pygame.transform.flip(self.image, True, False) if self.flip else self.image
            
            img_rect = img.get_rect()
            img_rect.centerx = self.rect.centerx
            img_rect.bottom = self.rect.bottom + self.offset_y
            
            surface.blit(img, img_rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)

