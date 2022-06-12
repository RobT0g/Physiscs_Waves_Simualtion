import pygame
from MolaStuff.MolaMak import Mola

pygame.init()                                                           # inicialização

width = 31*32                                                    # largura da tela
height = 16*32                                                   # altura da tela

refresh = 60
clock = pygame.time.Clock() 
update = pygame.USEREVENT + 1
pygame.time.set_timer(update, refresh)

display = pygame.display.set_mode((width, height))        # tela definida
pygame.display.set_caption('Pendulo Simples')   
mola = Mola(display, (width, height))
mola.putOnScreen()

running = True
while running:
    for e in pygame.event.get():
        if e.type == update:
            mola.update()
            mola.putOnScreen()
        if e.type == pygame.MOUSEBUTTONDOWN:
            mola.refresh()
        if e.type == pygame.MOUSEBUTTONUP:
            mola.clicked = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False