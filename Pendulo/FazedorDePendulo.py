import pygame

class Pendulo:
    def __init__(self, display, dim):
        self.font = pygame.font.SysFont('Times New Roman', 18)
        self.display = display
        self.size = dim
        self.frame = pygame.image.load('Frame.png')
        
    def update(self):
        pass

    def putOnScreen(self):
        self.display.blit(self.frame, (0, 0))
        pygame.draw.line(self.display, (255, 255, 255), ((self.size[0]/2)-200, 16), (self.size[0]/2, 56), 10)
        pygame.display.flip()
