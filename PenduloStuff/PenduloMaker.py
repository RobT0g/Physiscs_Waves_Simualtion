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
        elif opt == 'angle':
            obj.clicked = opt
            pos = pygame.mouse.get_pos()
            if not math.fabs(pos[0]-obj.size[0]/2) <= obj.length*obj.centimeter-5:
                pos = [(obj.size[0]/2) + (obj.length*obj.centimeter-5 if pos[0] > (obj.size[0]/2) else -obj.length*obj.centimeter+5), pos[1]]
            obj.ballAt[0] = pos[0]
            obj.ballAt[1] = math.sqrt(((obj.length*obj.centimeter)**2) - ((obj.ballAt[0]-obj.size[0]/2)**2))+obj.apoioHeight
            size = (math.fabs(obj.ballAt[1]-obj.apoioHeight), math.fabs(obj.ballAt[0]-obj.size[0]/2))
            obj.angle = 0.0
            if size[0] != 0.0 and size[1] != 0.0:
                obj.angle = (90 - math.degrees(math.atan(size[0]/size[1])))*(-1 if obj.ballAt[0] < obj.size[0]/2 else 1)
            obj.pot = ((obj.size[1]-obj.ballAt[1])*9.8*obj.mass/(obj.centimeter*100))
        elif opt == 'reset':
            if (obj.ballAt[0] != obj.size[0]/2):
                obj.__init__(obj.display, obj.size, obj.slow)
        elif opt == 'length':
            obj.clicked = opt
            pos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
            pos[1] = obj.apoioHeight+20*obj.centimeter if pos[1] < obj.apoioHeight+20*obj.centimeter else pos[1]
            pos[1] = obj.apoioHeight+50*obj.centimeter if pos[1] > obj.apoioHeight+50*obj.centimeter else pos[1]
            obj.length = (pos[1]-obj.apoioHeight)/obj.centimeter
            obj.ballAt = [obj.size[0]/2, obj.length*obj.centimeter+obj.apoioHeight]
            obj.updateButtons()
            obj.angle = 0.0
            obj.pot = ((obj.size[1]-obj.ballAt[1])*9.8*obj.mass/(obj.centimeter*100))
        elif opt == 'pmass':
            if obj.mass < 50:
                obj.mass += 5
            obj.pot = ((obj.size[1]-obj.ballAt[1])*9.8*obj.mass/(obj.centimeter*100))
        elif opt == 'mmass':
            if obj.mass > 5:
                obj.mass -= 5
            obj.pot = ((obj.size[1]-obj.ballAt[1])*9.8*obj.mass/(obj.centimeter*100))
    def clickedOn(self):
        pos = pygame.mouse.get_pos()
        for i in self.buttons:
            if pos[0] > self.buttons[i][0][0]-4 and pos[0] < self.buttons[i][1][0]+4 and pos[1] > self.buttons[i][0][1]-4 and pos[1] < self.buttons[i][1][1]+4:
                return i
        return None


class Pendulo:
    def __init__(self, display, dim, slow):
        self.display = display
        self.size = dim
        self.slow = slow
        self.length = 50
        self.centimeter = 8
        self.apoioHeight = 40
        self.buttons = {
            'init': [(self.size[0]-80, 25), (self.size[0]-80+54, 25+28)], 
            'angle': [((self.size[0]/2)-(self.length*self.centimeter), self.size[1]-32), ((self.size[0]/2)+(self.length*self.centimeter), self.size[1]-32)],
            'reset': [(self.size[0]-80, 60), (self.size[0]-80+54, 60+28)],
            'length': [(32, self.apoioHeight+20*self.centimeter), (32, self.apoioHeight+50*self.centimeter)],
            'mmass': [(35, 50), (55, 70)],
            'pmass': [(71, 50), (91, 70)]
        }
        self.cont = Controls(self.buttons)
        self.ballAt = [self.size[0]/2, self.length*self.centimeter+self.apoioHeight]
        self.angle = 0.0
        self.mass = 5
        self.clicked = False
        self.vel = 0
        self.pot = ((self.size[1]-self.apoioHeight-(self.length*self.centimeter))/self.centimeter)*self.mass*9.8/100
        self.cin = 0
        self.font = pygame.font.SysFont('Times New Roman', 18)
        self.frame = pygame.image.load('Images/Frame.png')

    def start(self):
        self.maxXPos = self.ballAt[0]
        self.strAngle = 0
        self.wholeEnergy = ((self.size[1]-self.ballAt[1])/self.centimeter)*self.mass*9.8/100
        self.baseEnergy = ((self.size[1]-self.apoioHeight-(self.length*self.centimeter))/self.centimeter)*self.mass*9.8/100
        self.period = (2*math.pi)*math.sqrt(self.length/(100*9.8))*(2.5 if self.slow else 1)
        self.step = 360/(self.period*(1000/60))

    def calc(self):
        self.strAngle = (self.strAngle+self.step)%360
        self.ballAt[0] = (self.size[0]/2) + (math.fabs(self.maxXPos - self.size[0]/2))*math.cos(math.radians(self.strAngle))
        self.ballAt[1] = self.apoioHeight + math.sqrt(((self.length*self.centimeter)**2) - (((self.size[0]/2)-self.ballAt[0])**2))
        sizes = (math.fabs(self.ballAt[1]-self.apoioHeight), math.fabs(self.ballAt[0]-self.size[0]/2))
        if 0.0 not in sizes:
            self.angle = (90 - math.fabs(math.degrees(math.atan(sizes[0]/sizes[1]))))*(-1 if self.ballAt[0] < self.size[0]/2 else 1)
        else:
            self.angle = 0.0
        self.vel = self.wholeEnergy-((self.size[1]-self.ballAt[1])*9.8*self.mass/(self.centimeter*100))
        self.vel = math.sqrt(2*self.vel/self.mass)
        self.pot = ((self.size[1]-self.ballAt[1])*9.8*self.mass/(self.centimeter*100))
        self.cin = self.wholeEnergy-self.pot

    def update(self):
        if self.cont.setts:
            if self.clicked:
                self.cont.update(self, self.clicked)
        else:
            self.calc()

    def putOnScreen(self):
        self.display.blit(self.frame, (0, 0))
        self.drawUi()
        pygame.display.flip()

    def drawUi(self):
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
        pygame.draw.line(self.display, (255, 255, 255), (self.size[0]/2, self.apoioHeight), (self.size[0]/2, self.apoioHeight + 50))
        pygame.draw.line(self.display, (255, 255, 255), ((self.size[0]/2), self.apoioHeight-5), (self.size[0]/2, self.apoioHeight+5), 3)
        pygame.draw.line(self.display, (255, 255, 255), ((self.size[0]/2), self.apoioHeight+5), (self.ballAt[0], self.ballAt[1]), 3)
        pygame.draw.circle(self.display, (0, 0, 0), (self.ballAt[0]+1, self.ballAt[1]), math.pow(self.mass*3/(4*3.14*0.00119), (1/3)))
        pygame.draw.line(self.display, (255, 255, 255), self.buttons['angle'][0], self.buttons['angle'][1], 4)
        pygame.draw.line(self.display, (255, 255, 255), self.buttons['length'][0], self.buttons['length'][1], 4)
        pygame.draw.circle(self.display, (255, 255, 255), (self.ballAt[0]+1, self.buttons['angle'][0][1]+1), 5)
        pygame.draw.circle(self.display, (255, 255, 255), (self.buttons['length'][0][0]+1, self.apoioHeight+self.length*self.centimeter), 5)
        self.display.blit(self.font.render(f'''{self.length:.1f}cm''', False, (255, 255, 255)), (self.buttons['length'][0][0]+8, self.apoioHeight+self.length*self.centimeter-6))
        txt = self.font.render(f'''{self.angle:.1f}°''', False, (255, 255, 255))
        self.display.blit(txt, (5+(self.size[0]/2)-txt.get_size()[0]/2, 16))
        txt = self.font.render(f'Massa:{self.mass:.2f}g', False, (0, 0, 0))
        pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(20, 20, (p:=txt.get_size())[0]+4, 3*p[1]+4))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(20, 20, (p:=txt.get_size())[0]+4, 3*p[1]+4), 2)
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(*self.buttons['pmass'][0], 20, 20))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(*self.buttons['mmass'][0], 20, 20))
        self.display.blit(txt, (22, 22))
        self.display.blit(self.font.render('+', False, (255, 255, 255)), (self.buttons['pmass'][0][0]+5, self.buttons['pmass'][0][1]))
        self.display.blit(self.font.render('-', False, (255, 255, 255)), (self.buttons['mmass'][0][0]+7, self.buttons['mmass'][0][1]-2))
        txt = self.font.render(f'''Vel {self.vel:.2f} m/s''', False, (0, 0, 0))
        coords = (self.size[0]-25-txt.get_size()[0], self.size[1]-45-txt.get_size()[1])
        pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(coords[0]-5, coords[1]-42, txt.get_size()[0]+10, 64))
        pygame.draw.rect(self.display, (0, 0, 0), pygame.Rect(coords[0]-5, coords[1]-42, txt.get_size()[0]+10, 64), 1)
        pygame.draw.line(self.display, (0, 0, 0), (coords[0]+28, coords[1]-42), (coords[0]+28, coords[1]+20))
        pygame.draw.line(self.display, (0, 0, 0), (coords[0]+65, coords[1]-42), (coords[0]+65, coords[1]+20))
        pygame.draw.line(self.display, (0, 0, 0), (coords[0]-5, coords[1]-20), (coords[0]+txt.get_size()[0]+4, coords[1]-20))
        pygame.draw.line(self.display, (0, 0, 0), (coords[0]-5, coords[1]), (coords[0]+txt.get_size()[0]+4, coords[1]))
        self.display.blit(txt, coords)
        txt = self.font.render((f'''Ept {self.pot:.2f} mJ''' if self.pot < 10 else (f'''Ept {self.pot:.1f} mJ''' if self.pot < 100 else f'''Ept {self.pot:.0f}  mJ''')), False, (0, 0, 0))
        self.display.blit(txt, (coords[0], coords[1]-20))
        txt = self.font.render((f'''Ecn {self.cin:.2f} mJ''' if self.cin < 10 else f'''Ecn {self.cin:.1f} mJ'''), False, (0, 0, 0))
        self.display.blit(txt, (coords[0], coords[1]-40))

    def getVelVector(self):
        x = math.sqrt((5)/(1+(math.tan(math.radians(self.angle))**2)))*self.vel
        y = -x*math.fabs(math.tan(math.radians(self.angle)))*(-1 if self.angle < 0 else 1)*self.vel
        dir = -math.sin(math.radians(self.strAngle))
        if dir >= 0:
            return (self.ballAt[0] + x*30, self.ballAt[1] + y*30)
        return (self.ballAt[0] - x*30, self.ballAt[1] - y*30)   

    def getSizeOf(self, opt):
        return (self.buttons[opt][1][0]-self.buttons[opt][0][0], self.buttons[opt][1][1]-self.buttons[opt][0][1])

    def updateButtons(self):
        self.buttons['angle'] = [((self.size[0]/2)-(self.length*self.centimeter), self.size[1]-32), ((self.size[0]/2)+(self.length*self.centimeter), self.size[1]-32)]

    def refresh(self):
        self.cont.update(self)
