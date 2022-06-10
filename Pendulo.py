import pygame
from PenduloStuff.FazedorDePendulo import Pendulo

pygame.init()                                                           # inicialização

width = 31*32                                                    # largura da tela
height = 16*32                                                   # altura da tela

refresh = 80
clock = pygame.time.Clock() 
update = pygame.USEREVENT + 1
pygame.time.set_timer(update, refresh)

display = pygame.display.set_mode((width, height))        # tela definida
pygame.display.set_caption('Hidrodinamics')   
pendulum = Pendulo(display, (width, height))
pendulum.putOnScreen()

running = True                      # Variável de looping
while running:                      # looping
    for e in pygame.event.get():
        if e.type == update:
            pendulum.update()
            pendulum.putOnScreen()
        if e.type == pygame.MOUSEBUTTONDOWN:
            pendulum.refresh()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False