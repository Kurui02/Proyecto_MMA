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

        self.color = (50,150,255) if self.player == 1 else (255,50,50)
    
    def move(self, screen_width, screen_height, floor_y):
        Speed = self.speed
        dx=0
        dy=0

        key = pygame.key.get_pressed()

        if self.player == 1:
            if key[pygame.K_a]:
                dx = -Speed
            if key[pygame.K_d]:
                dx = Speed
            if key[pygame.K_w] and not self.isJumping:
                self.vel_y = self.jump_force
                self.isJumping = True
        
        if self.player == 2:
            if key[pygame.K_j]:
                dx = -Speed
            if key[pygame.K_l]:
                dx = Speed
            if key[pygame.K_i] and not self.isJumping:
                self.vel_y = self.jump_force
                self.isJumping = True
        
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
    
    def dibujar(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)