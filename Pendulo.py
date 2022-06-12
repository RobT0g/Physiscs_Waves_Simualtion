import pygame
from PenduloStuff.PenduloMaker import Pendulo

pygame.init()                                                           # inicialização

width = 31*32                                                    # largura da tela
height = 16*32                                                   # altura da tela

refresh = 60
clock = pygame.time.Clock() 
update = pygame.USEREVENT + 1
pygame.time.set_timer(update, refresh)

display = pygame.display.set_mode((width, height))        # tela definida
pygame.display.set_caption('Pendulo Simples')   
pendulum = Pendulo(display, (width, height))
pendulum.putOnScreen()

running = True
while running:
    for e in pygame.event.get():
        if e.type == update:
            pendulum.update()
            pendulum.putOnScreen()
        if e.type == pygame.MOUSEBUTTONDOWN:
            pendulum.refresh()
        if e.type == pygame.MOUSEBUTTONUP:
            pendulum.clicked = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False