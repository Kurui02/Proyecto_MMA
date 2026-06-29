import pygame

class Fighter:
    def __init__(self, player,x,y):
        self.player = player

        self.width = 80
        self.height = 180
        self.rect = pygame.Rect((x,y,self.width, self.height))

        self.vel_y =0
        self.speed = 8
        self.jump_force = -25
        self.gravity = 2
        self.isJumping = False 

        self.flip = False
        self.attacking = False 
        self.attackCooldown = 0

        self.attack_rect= pygame.Rect(0,0,0,0)

        self.health = 100
        self.hit = False
        self.damage = 10 

        self.stun = 0
        self.knockback = 0
        self.isBlocking = False

        self.base = (50,150,255) if self.player == 1 else (255,50,50)
        self.color = self.base
    
    def move(self, screen_width, screen_height, floor_y, target):
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
                self.knockback -= 1
            elif self.knockback < 0:
                self.knockback += 1
            
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            if self.rect.bottom > floor_y:
                self.rect.bottom = floor_y
                self.vel_y = 0
                self.isJumping = False
            
            return

        key = pygame.key.get_pressed()
        self.isBlocking = False
        if not self.attacking:
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
                if key[pygame.K_r] or key[pygame.K_t]: 
                    self.attack()
        
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
                if key[pygame.K_o] or key[pygame.K_p]: 
                    self.attack()
        
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
        
        if self.attacking: 
            self.color = (255,255,255)
            self.attackCooldown -=1
        
            if self.flip:
                self.attack_rect = pygame.Rect(self.rect.left -80, self.rect.y + 40, 80, 40)
            else:
                self.attack_rect = pygame.Rect(self.rect.right, self.rect.y + 40, 80,40)

            if self.attack_rect.colliderect(target.rect) and not self.hit:
                damage_base = self.damage
                force_knockback = 10
                frames_stun = 20
                
                if target.isBlocking :
                    target.health -= damage_base * 0.2
                    target.stun = frames_stun // 2
                    force_knockback = force_knockback // 2
                    print(f"BLOQUEO! Vida de Jugador {target.player}: {target.health}")
                else:
                    target.health -= damage_base
                    target.stun = frames_stun
                    print(f"GOLPE! Vida de Jugador {target.player}: {target.health}")
                
                if self.rect.centerx < target.rect.centerx:
                    target.knockback = force_knockback
                else:
                    target.knockback = -force_knockback
                
                self.hit = True

        if self.attackCooldown <=0: 
            self.attacking = False
            self.hit = False
            self.color = self.base
            self.attack_rect = pygame.Rect(0,0,0,0)

    def attack(self):
        self.attacking = True
        self.attackCooldown = 20 
           
    def dibujar(self, surface):
        pygame.draw.rect(surface, self.color, self.rect) 

        if self.attacking:
            pygame.draw.rect(surface,(0,255,0), self.attack_rect)