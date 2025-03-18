#2025, by S. Diane

import pygame
from pygame.locals import*
import sys, pygame, math
import numpy as np

#звено манипулятора
class Link:
    def __init__(self, L, alpha):
        self.L = L             #длина звена
        self.alpha = alpha     #локальный угол поворота
        self.P1 = np.zeros(2)  #координаты точки основания
        self.Angle = 0         #глобальный угол поворота
        self.P2 = np.zeros(2)  #координаты конечной точки
    def calc(self): #расчет
        s,c=math.sin(self.Angle), math.cos(self.Angle)
        self.P2 = self.P1 + self.L * np.array([c,s])
    def draw(self, screen):
        pygame.draw.line(screen, (0,0,0), self.P1, self.P2, 3)
        pygame.draw.circle(screen, (0,0,255), self.P1, 3)
        pygame.draw.circle(screen, (0,0,255), self.P2, 3)
        
# манипуляционный робот с ангулярной кинематикой
class RobotManipulator:
    def __init__(self, lengths):
        self.lengths = lengths
        self.links = [Link(lengths[i], -0.3) for i in range(len(lengths))]
        self.endPos = np.zeros(2)
    def draw(self, screen): #отрисовка
        for l in self.links:
            l.draw(screen)
        self.drawBasement(screen)
    def drawBasement(self, screen):
        pC = self.links[0].P1
        pL, pR = [pC[0] - 10, pC[1]], [pC[0] + 10, pC[1]]
        pygame.draw.line(screen, (0, 0, 0), pL, pR, 3)
        for p in [pL, pC, pR]:
            pygame.draw.line(screen, (0, 0, 0), p, [p[0] - 5, p[1] + 5], 3)
    def setAngles(self, angles): #прямая задача кинематики
        for i in range(len(self.links)):
            self.links[i].alpha = angles[i]
        self.calc()
        return(self.endPos)
    def calc(self): #расчет
        for l in self.links:
            l.Angle = 0
        for i in range (len(self.links)):
            self.links[i].Angle = self.links[i].alpha
            if (i>0):
                self.links[i].Angle += self.links[i-1].Angle
                self.links[i].P1 = self.links[i - 1].P2
            self.links[i].calc()
            self.endPos = self.links[-1].P2


if __name__=="__main__":

    # графические переменные
    width = 300
    height = 200
    timer = pygame.time.Clock()
    fps = 30
    dt=1/fps
    screen=pygame.display.set_mode((width,height))
    pos = (0,0)

    #основные переменные
    
    r = RobotManipulator([100, 60])
    r.links[0].P1 = [100, 150]

    while True: #цикл моделирования
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)

        screen.fill((255,255,255))
        r.links[0].alpha+=-0.2*dt
        r.links[1].alpha+=0.4*dt
        r.calc()
        r.draw(screen)

        pygame.display.flip()
        timer.tick(fps)
