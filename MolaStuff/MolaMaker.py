import pygame, math

class Controls:
    def __init__(self, buttons) -> None:
        self.setts = True
        self.buttons = buttons

    def update(self, obj, opt = None):
        if not self.setts:
            if (p := self.clickedOn()) == 'init':
                self.setts = True
            elif p == 'reset':
                self.setts = True
                obj.__init__(obj.display, obj.size, obj.slow)
        else:
            obj.clicked = False
            if not opt:
                opt = self.clickedOn()
        if opt == 'init':
            self.setts = False
            obj.start()
        elif opt == 'const':
            obj.clicked = opt
            pos = pygame.mouse.get_pos()[1]
            if pos < self.buttons['const'][0][1]:
                pos = self.buttons['const'][0][1]
            if pos > self.buttons['const'][1][1]:
                pos = self.buttons['const'][1][1]
            obj.const = 4.9 + ((pos-self.buttons['const'][0][1])/obj.getSizeOf('const')[1])*12
            obj.recalc()
        elif opt == 'reset':
            obj.__init__(obj.display, obj.size, obj.slow)
        elif opt == 'length':
            obj.clicked = opt
            pos = pygame.mouse.get_pos()[1]
            if pos < self.buttons['length'][0][1]:
                pos = self.buttons['length'][0][1]
            if pos > self.buttons['length'][1][1]:
                pos = self.buttons['length'][1][1]
            obj.pull = (pos - obj.rest*obj.centimeter)/obj.centimeter
            obj.recalc()
        elif opt == 'pmass':
            if obj.mass < 50:
                obj.mass += 5
            obj.recalc()
        elif opt == 'mmass':
            if obj.mass > 5:
                obj.mass -= 5
            obj.recalc()
        elif opt == 'slow':
            obj.slow = not obj.slow

    def clickedOn(self):
        pos = pygame.mouse.get_pos()
        for i in self.buttons:
            if pos[0] > self.buttons[i][0][0]-4 and pos[0] < self.buttons[i][1][0]+4 and pos[1] > self.buttons[i][0][1]-4 and pos[1] < self.buttons[i][1][1]+4:
                return i
        return None

class Mola:
    def __init__(self, display, dim, slow=False):
        self.display = display
        self.size = dim
        self.slow = slow
        self.length = 30
        self.mass = 5
        self.const = 4.9
        self.centimeter = 8
        self.apoioHeight = 40
        self.periodo = 0
        self.freq = 0
        self.ballAt = [self.size[0]/2, self.length*self.centimeter+self.apoioHeight+(self.mass*9.8/(self.const*1000))*self.centimeter*100]
        self.rest = self.ballAt[1]/self.centimeter
        self.pull = 0
        self.buttons = {
            'init': [(self.size[0]-80, 25), (self.size[0]-80+54, 25+28)], 
            'const': [(self.size[0]-32, self.ballAt[1]-10*self.centimeter), (self.size[0]-32, self.ballAt[1]+10*self.centimeter)],
            'reset': [(self.size[0]-80, 60), (self.size[0]-80+54, 60+28)],
            'length': [(32, self.ballAt[1]-10*self.centimeter), (32, self.ballAt[1]+10*self.centimeter)],
            'mmass': [(35, 50), (55, 70)],
            'pmass': [(71, 50), (91, 70)],
            'slow' : [(80, 75), (100, 95)]
        }
        self.cont = Controls(self.buttons)
        self.clicked = False
        self.vel = 0
        self.pot = ((self.size[1]-self.apoioHeight-(self.length*self.centimeter))/self.centimeter)*self.mass*9.8/100
        self.cin = 0
        self.font = pygame.font.SysFont('Times New Roman', 18)
        self.frame = pygame.Surface(self.size)
        pygame.draw.rect(self.frame, (55, 71, 79), pygame.Rect(0, 0, *self.size))
        pygame.draw.rect(self.frame, (20, 20, 20), pygame.Rect(0, 0, *self.size), 16)
        pygame.draw.rect(self.frame, (50, 50, 50), pygame.Rect(0, 0, *self.size), 1)
        pygame.draw.rect(self.frame, (0, 0, 0), pygame.Rect(15, 15, self.size[0]-30, self.size[1]-30), 1)
    
    def update(self):
        if self.cont.setts:
            if self.clicked:
                self.cont.update(self, self.clicked)
        else:
            self.calc()

    def start(self):
        self.periodo = 2*math.pi*math.sqrt((self.mass/1000)/self.const)
        self.freq = 1/self.periodo if self.periodo != 0 else 0
        self.angle = 0 if self.ballAt[1] >= self.rest*self.centimeter else 180
        self.step = 360/(self.periodo*(1000/60)*(5 if self.slow else 1))
        self.wholeEnergy = self.pot
        self.maxY = math.fabs(self.rest*self.centimeter-self.ballAt[1])

    def calc(self):
        self.angle = (self.angle+self.step)%360
        self.ballAt[1] = self.rest*self.centimeter+self.maxY*math.cos(math.radians(self.angle))

    def drawUi(self):
        pygame.draw.line(self.display, (255, 255, 255), ((self.size[0]/2)-50, self.rest*self.centimeter), ((self.size[0]/2)+50, self.rest*self.centimeter))
        txt = self.font.render(f'''{'Parar' if not self.cont.setts else 'Iniciar'}''', False, (0, 0, 0))
        flow = pygame.Surface(self.getSizeOf('init'))
        pygame.draw.rect(flow, (255, 255, 255), pygame.Rect(0, 0, flow.get_size()[0], flow.get_size()[1]))
        pygame.draw.rect(flow, (0, 0, 0), pygame.Rect(0, 0, flow.get_size()[0], flow.get_size()[1]), 2)
        self.display.blit(flow, self.buttons['init'][0])
        self.display.blit(txt, (self.buttons['init'][0][0] + (8 if not self.cont.setts else 3), self.buttons['init'][0][1]+3))
        txt = self.font.render(f'''Reset''', False, (0, 0, 0))
        flow = pygame.Surface(self.getSizeOf('reset'))
        pygame.draw.rect(flow, (255, 255, 255), pygame.Rect(0, 0, flow.get_size()[0], flow.get_size()[1]))
        pygame.draw.rect(flow, (0, 0, 0), pygame.Rect(0, 0, flow.get_size()[0], flow.get_size()[1]), 2)
        self.display.blit(flow, self.buttons['reset'][0])
        self.display.blit(txt, (self.buttons['reset'][0][0] + 6, self.buttons['reset'][0][1]+3))
        pygame.draw.line(self.display, (210, 105, 30), ((self.size[0]/2)-200, 21), (self.size[0]/2, self.apoioHeight), 10)
        pygame.draw.line(self.display, (210, 105, 30), ((self.size[0]/2)+200, 21), (self.size[0]/2, self.apoioHeight), 10)
        self.drawBodies()
        txt = self.font.render(f'K: {self.const:.1f}N/m', False, (255, 255, 255))
        self.display.blit(txt, (self.buttons['const'][0][0]-txt.get_size()[0], self.buttons['const'][1][1]))
        pygame.draw.line(self.display, (255, 255, 255), self.buttons['const'][0], self.buttons['const'][1], 4)
        pygame.draw.line(self.display, (255, 255, 255), self.buttons['length'][0], self.buttons['length'][1], 4)
        pygame.draw.circle(self.display, (255, 255, 255), (self.buttons['const'][0][0]+1, self.buttons['const'][0][1]+((self.const-4.9)*self.getSizeOf('const')[1]/12)), 5)
        pygame.draw.circle(self.display, (255, 255, 255), (self.buttons['length'][0][0]+1, self.ballAt[1]), 5)
        self.display.blit(self.font.render(f'''{(self.ballAt[1]-self.apoioHeight)/self.centimeter:.1f}cm''', False, (255, 255, 255)), (self.buttons['length'][0][0]+8, self.ballAt[1]-10))
        txt = self.font.render(f'Massa:{self.mass:.2f}g', False, (0, 0, 0))
        pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(20, 20, (p:=txt.get_size())[0]+4, 4*p[1]+4))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(20, 20, (p:=txt.get_size())[0]+4, 4*p[1]+4), 2)
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(*self.buttons['pmass'][0], 20, 20))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(*self.buttons['mmass'][0], 20, 20))
        self.display.blit(self.font.render('Slow', False, (0, 0, 0)), (self.buttons['slow'][0][0]-50, self.buttons['slow'][0][1]))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(*self.buttons['slow'][0], *self.getSizeOf('slow')), 1)
        if self.slow:
            pygame.draw.line(self.display, (0, 0, 0), (self.buttons['slow'][0][0]+2, self.buttons['slow'][0][1]+2), (self.buttons['slow'][1][0]-3, self.buttons['slow'][1][1]-3))
            pygame.draw.line(self.display, (0, 0, 0), (self.buttons['slow'][0][0]+2, self.buttons['slow'][1][1]-3), (self.buttons['slow'][1][0]-3, self.buttons['slow'][0][1]+2))
        self.display.blit(txt, (22, 22))
        self.display.blit(self.font.render('+', False, (255, 255, 255)), (self.buttons['pmass'][0][0]+5, self.buttons['pmass'][0][1]))
        self.display.blit(self.font.render('-', False, (255, 255, 255)), (self.buttons['mmass'][0][0]+7, self.buttons['mmass'][0][1]-2))
        txt = self.font.render(f'''T: {self.periodo:.1f} s''', False, (255, 255, 255))
        coords = (self.size[0]-30-txt.get_size()[0], self.size[1]-45-txt.get_size()[1])
        self.display.blit(txt, (coords[0], coords[1]))
        txt = self.font.render(f'''F: {(self.freq):.1f} hz''', False, (255, 255, 255))
        self.display.blit(txt, (coords[0], coords[1]-20))
        pygame.draw.line(self.display, (255, 255, 255), (70 + self.size[0]/2, 2+self.apoioHeight), (70 + self.size[0]/2, 2+self.apoioHeight+self.centimeter*50), 3)
        for i in range(11):
            pygame.draw.line(self.display, (255, 255, 255), ((self.size[0]/2)+65, 2+self.apoioHeight+(i*5*self.centimeter)), ((self.size[0]/2)+75, 2+self.apoioHeight+(i*5*self.centimeter)))
            self.display.blit(self.font.render(f'{i*5}cm', False, (255, 255, 255)), ((self.size[0]/2)+80, self.apoioHeight+(i*5*self.centimeter)-8))

    def recalc(self):
        self.rest = ((self.length*self.centimeter)+self.apoioHeight+(self.mass*9.8/(self.const*1000))*self.centimeter*100)/self.centimeter
        self.ballAt[1] = (self.rest + self.pull)*self.centimeter
        self.periodo = 2*math.pi*math.sqrt((self.mass/1000)/self.const)
        self.freq = 1/self.periodo if self.periodo != 0 else 0
        self.updateButtons()

    def drawBodies(self):
        pygame.draw.line(self.display, (255, 255, 255), (self.size[0]/2, self.apoioHeight), (self.size[0]/2, self.apoioHeight + 50))
        pygame.draw.line(self.display, (255, 255, 255), ((self.size[0]/2), self.apoioHeight-5), (self.size[0]/2, self.apoioHeight+5), 3)
        pygame.draw.line(self.display, (255, 255, 255), ((self.size[0]/2), self.apoioHeight+5), (self.ballAt[0], self.ballAt[1]), 3)
        pygame.draw.circle(self.display, (0, 0, 0), (self.ballAt[0]+1, self.ballAt[1]), math.pow(self.mass*3/(4*3.14*0.00119), (1/3)))

    def putOnScreen(self):
        self.display.blit(self.frame, (0, 0))
        self.drawUi()
        pygame.display.flip()

    def getSizeOf(self, opt):
        return (self.buttons[opt][1][0]-self.buttons[opt][0][0], self.buttons[opt][1][1]-self.buttons[opt][0][1])

    def updateButtons(self):
        self.buttons['length'] = [(32, (self.rest-10)*self.centimeter), (32, (self.rest+10)*self.centimeter)]

    def refresh(self):
        self.cont.update(self)



