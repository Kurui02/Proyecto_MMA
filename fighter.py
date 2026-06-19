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
        self.isJumping = False # parte de avance 1 parametros de moviento de jugador

        self.flip = False
        self.attacking = False #avance 2 logica de estados y colisiones de jugador
        self.attackCooldown = 0

        self.attack_rect= pygame.Rect(0,0,0,0)

        self.health = 100
        self.hit = False
        self.damage = 10 

        self.base = (50,150,255) if self.player == 1 else (255,50,50)
        self.color = self.base
    
    def move(self, screen_width, screen_height, floor_y, target):
        Speed = self.speed
        dx=0
        dy=0

        key = pygame.key.get_pressed()
        if not self.attacking:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -Speed
                if key[pygame.K_d]:
                    dx = Speed
                if key[pygame.K_w] and not self.isJumping: #avance 1
                    self.vel_y = self.jump_force
                    self.isJumping = True
                if key[pygame.K_r] or key[pygame.K_t]: #avance 2
                    self.attack()
        
            if self.player == 2:
                if key[pygame.K_j]:
                    dx = -Speed
                if key[pygame.K_l]:
                    dx = Speed
                if key[pygame.K_i] and not self.isJumping: #avance 1
                    self.vel_y = self.jump_force
                    self.isJumping = True
                if key[pygame.K_o] or key[pygame.K_p]: #avance 2
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

        if target.rect.centerx > self.rect.centerx: #de aqui hasta el metodo attack es parte del avance 2
            self.flip = False
        else:
            self.flip = True
        
        if self.attacking: #avance 2 si esta en el estado atacando cambia de color para identificar y comprueba la colision para restar vida
            self.color = (255,255,255)
            self.attackCooldown -=1
        
            if self.flip:
                self.attack_rect = pygame.Rect(self.rect.left -80, self.rect.y + 40, 80, 40)
            else:
                self.attack_rect = pygame.Rect(self.rect.right, self.rect.y + 40, 80,40)

            if self.attack_rect.colliderect(target.rect) and not self.hit:
                target.health -= self.damage
                self.hit = True
                print(f"Golpe Vida de Jugador {target.player}: {target.health}")

        if self.attackCooldown <=0: #avance 2 devuelve los valores iniciales una vez impactado el golpe
            self.attacking = False
            self.hit = False
            self.color = self.base
            self.attack_rect = pygame.Rect(0,0,0,0)

    def attack(self):
        self.attacking = True
        self.attackCooldown = 20 # cooldown para no poder golpear sin parar, al trabajar con 60fps, este corresponde a un pequeño frame, suficiente para evitar spam, pero permitiendo combos mas adelante
           
    def dibujar(self, surface):
        pygame.draw.rect(surface, self.color, self.rect) #dibujar del avance 1

        if self.attacking:
            pygame.draw.rect(surface,(0,255,0), self.attack_rect)