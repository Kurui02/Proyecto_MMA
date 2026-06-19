import pygame
from fighter import Fighter

pygame.init()

Screen_width = 1280
Screen_heigt = 720
screen = pygame.display.set_mode((Screen_width,Screen_heigt))
pygame.display.set_caption("Proyecto MMA")

clock = pygame.time.Clock()
FPS=60

suelo= Screen_heigt - 50

fighter_1= Fighter(player=1,x=200,y=suelo -180)
fighter_2= Fighter(player=2,x=1000,y=suelo -180)

running = True
while running:
    clock.tick(FPS)

    screen.fill((30,30,35))

    pygame.draw.rect(screen, (100,100,100),(0,suelo,Screen_width,50))

    fighter_1.move(Screen_width,Screen_heigt,suelo)
    fighter_2.move(Screen_width,Screen_heigt,suelo)

    fighter_1.dibujar(screen)
    fighter_2.dibujar(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()