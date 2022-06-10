import pygame, math, thorpy

class Ui:
    def __init__(self, display, dim):
        self.font = pygame.font.SysFont('Times New Roman', 18)
        self.display = display
        self.size = dim
        self.length = 50
        self.centimeter = 8
        self.apoioHeight = 40
        self.buttons = {
            'init': [(self.size[0]-80, 25), (self.size[0]-80+54, 25+28)], 
            'angle': [((self.size[0]/2)-(self.length*self.centimeter), self.size[1]-32), ((self.size[0]/2)+(self.length*self.centimeter), self.size[1]-32)],
            'reset': [(self.size[0]-80, 60), (self.size[0]-80+54, 60+28)],
            'length': [(32, self.apoioHeight+20*self.centimeter), (32, self.apoioHeight+50*self.centimeter)],
        }
        self.angle = 0.0
        self.ballAt = [self.size[0]/2, self.length*self.centimeter+self.apoioHeight]
        self.mass = 5
        self.on = False
        self.opt = False
    
    def drawUi(self):
        self.drawButtons()
        pygame.draw.line(self.display, (210, 105, 30), ((self.size[0]/2)-200, 21), (self.size[0]/2, self.apoioHeight), 10)
        pygame.draw.line(self.display, (210, 105, 30), ((self.size[0]/2)+200, 21), (self.size[0]/2, self.apoioHeight), 10)
        pygame.draw.line(self.display, (255, 255, 255), (self.size[0]/2, self.apoioHeight), (self.size[0]/2, self.apoioHeight + 50))
        pygame.draw.line(self.display, (255, 255, 255), ((self.size[0]/2), self.apoioHeight-5), (self.size[0]/2, self.apoioHeight+5), 3)
        pygame.draw.line(self.display, (255, 255, 255), ((self.size[0]/2), self.apoioHeight+5), (self.ballAt[0], self.ballAt[1]), 3)
        pygame.draw.circle(self.display, (0, 0, 0), (self.ballAt[0]+1, self.ballAt[1]), self.mass*2)
        if not self.on:
            pygame.draw.line(self.display, (255, 255, 255), self.buttons['angle'][0], self.buttons['angle'][1], 4)
            pygame.draw.line(self.display, (255, 255, 255), self.buttons['length'][0], self.buttons['length'][1], 4)
            pygame.draw.circle(self.display, (255, 255, 255), (self.ballAt[0]+1, self.buttons['angle'][0][1]+1), 5)
            pygame.draw.circle(self.display, (255, 255, 255), (self.buttons['length'][0][0]+1, self.apoioHeight+self.length*self.centimeter), 5)
            self.display.blit(self.font.render(f'''{self.length:.1f}cm''', False, (255, 255, 255)), (self.buttons['length'][0][0]+8, self.apoioHeight+self.length*self.centimeter-6))
            txt = self.font.render(f'''{self.angle:.1f}°''', False, (255, 255, 255))
            self.display.blit(txt, (5+(self.size[0]/2)-txt.get_size()[0]/2, 16))
        
    def drawButtons(self):
        txt = self.font.render(f'''{'Parar' if self.on else 'Iniciar'}''', False, (0, 0, 0))
        flow = pygame.Surface(self.getSizeOf('init'))
        pygame.draw.rect(flow, (255, 255, 255), pygame.Rect(0, 0, flow.get_size()[0], flow.get_size()[1]))
        pygame.draw.rect(flow, (0, 0, 0), pygame.Rect(0, 0, flow.get_size()[0], flow.get_size()[1]), 2)
        self.display.blit(flow, self.buttons['init'][0])
        self.display.blit(txt, (self.buttons['init'][0][0] + (8 if self.on else 3), self.buttons['init'][0][1]+3))
        if not self.on:
            txt = self.font.render(f'''Reset''', False, (0, 0, 0))
            flow = pygame.Surface(self.getSizeOf('reset'))
            pygame.draw.rect(flow, (255, 255, 255), pygame.Rect(0, 0, flow.get_size()[0], flow.get_size()[1]))
            pygame.draw.rect(flow, (0, 0, 0), pygame.Rect(0, 0, flow.get_size()[0], flow.get_size()[1]), 2)
            self.display.blit(flow, self.buttons['reset'][0])
            self.display.blit(txt, (self.buttons['reset'][0][0] + 6, self.buttons['reset'][0][1]+3))
    
    def getSizeOf(self, opt):
        return (self.buttons[opt][1][0]-self.buttons[opt][0][0], self.buttons[opt][1][1]-self.buttons[opt][0][1])

    def update(self):
        if self.on:
            if self.clickedOn() == 'init':
                self.on = False
            pass
        else:
            opt = self.opt
            if not self.opt:
                opt = self.clickedOn()
            if opt == 'init':
                self.on = not self.on
                return
            elif opt == 'angle':
                self.opt = 'angle'
                pos = pygame.mouse.get_pos()
                if not math.fabs(pos[0]-self.size[0]/2) <= self.length*self.centimeter-5:
                    pos = [(self.size[0]/2) + (self.length*self.centimeter-5 if pos[0] > (self.size[0]/2) else -self.length*self.centimeter+5), pos[1]]
                self.ballAt[0] = pos[0]
                self.ballAt[1] = math.sqrt(((self.length*self.centimeter)**2) - ((self.ballAt[0]-self.size[0]/2)**2))+self.apoioHeight
                size = (math.fabs(self.ballAt[1]-self.apoioHeight), math.fabs(self.ballAt[0]-self.size[0]/2))
                self.angle = 0.0
                if size[0] != 0.0 and size[1] != 0.0:
                    self.angle = (90 - math.degrees(math.atan(size[0]/size[1])))*(-1 if self.ballAt[0] < self.size[0]/2 else 1)
            elif opt == 'reset':
                if (self.ballAt[0] != self.size[0]/2):
                    self.__init__(self.display, self.size)
            elif opt == 'length':
                self.opt = 'length'
                pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
                pos[1] = self.apoioHeight+20*self.centimeter if pos[1] < self.apoioHeight+20*self.centimeter else pos[1]
                pos[1] = self.apoioHeight+50*self.centimeter if pos[1] > self.apoioHeight+50*self.centimeter else pos[1]
                self.length = (pos[1]-self.apoioHeight)/self.centimeter
                self.ballAt = [self.size[0]/2, self.length*self.centimeter+self.apoioHeight]
                self.updateButtons()
                self.angle = 0.0
    
    def start(self):
        self.energy = (self.size[1]-self.ballAt[1])*9.8*1/100
        pass

    def updateButtons(self):
            self.buttons['angle'] = [((self.size[0]/2)-(self.length*self.centimeter), self.size[1]-32), ((self.size[0]/2)+(self.length*self.centimeter), self.size[1]-32)]

    def clickedOn(self):
        pos = pygame.mouse.get_pos()
        for i in self.buttons:
            if pos[0] > self.buttons[i][0][0]-4 and pos[0] < self.buttons[i][1][0]+4 and pos[1] > self.buttons[i][0][1]-4 and pos[1] < self.buttons[i][1][1]+4:
                return i
        return None

class Pendulo:
    def __init__(self, display, dim):
        self.ui = Ui(display, dim)
        self.display = display
        self.size = dim
        self.half = self.size[0]/2
        self.frame = pygame.image.load('Images/Frame.png')
        self.adjusting = False
        
    def update(self):
        if not self.ui.on and self.adjusting:
            self.ui.update()
        if not pygame.mouse.get_pressed()[0]:
            self.adjusting = False
            self.ui.opt = False
        
    def putOnScreen(self):
        self.display.blit(self.frame, (0, 0))
        self.ui.drawUi()
        pygame.display.flip()
    
    def refresh(self):
        if not self.ui.on:
            self.adjusting = True
        self.ui.update()
