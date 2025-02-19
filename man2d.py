#S. Diane, 2d-man draw function, 2024

import math
import pygame
import sys
import numpy as np

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Man Model")

# Цвета
COLOR = (0, 128, 255)

def drawCenteredEllipse(screen, x, y, r1, r2):
    pygame.draw.ellipse(screen, COLOR, (x-r1, y-r2, r1*2, r2*2), 2)

class Man:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.body_radius = 20
        self.head_radius = 10
        self.arm_length = 5
        self.leg_length = 10
        self.phase = 0

    def control(self, goal, dt): #тактический уровень управления
        def lim_ang(a):
            while a>math.pi: a-=2*math.pi
            while a<=-math.pi: a+=2*math.pi
            return a
        da1 = math.atan2(goal[1]-self.y, goal[0]-self.x)
        da2 = lim_ang(da1-self.angle)
        self.angle += 2*da2*dt
        self.v = 30

    def sim(self, dt):
        s, c = math.sin(self.angle), math.cos(self.angle)
        self.x+=self.v*c*dt
        self.y+=self.v*s*dt

    def draw(self, screen):
        k = 180 / 3.1415926
        sf = pygame.Surface((self.body_radius * 3, self.body_radius * 3), pygame.SRCALPHA)
        x, y = sf.get_width() / 2, sf.get_height() / 2
        K=[[0,0,0,0], [1,-1,0.3,-0.3], [-1,1,-0.3,0.3], [0,0,0,0]]
        k1, k2, k3, k4=np.add(K[self.phase], [0,0,0.8,0.8])
        A=[2, 1, 2, 3]
        B=[-2, 0, 2, 3]
        # Отрисовка туловища
        drawCenteredEllipse(sf, x, y, self.body_radius, self.body_radius//2)
        # Отрисовка головы
        pygame.draw.circle(sf, COLOR, (x, y+self.head_radius//4), self.head_radius, 2)
        # Отрисовка рук
        armY=A[self.phase]*self.arm_length
        armDY=B[self.phase]*self.arm_length
        armDY2=-armDY
        if self.phase==3: armDY2=armDY
        drawCenteredEllipse(sf, x - self.body_radius, y+armDY, self.arm_length, armY)
        drawCenteredEllipse(sf, x + self.body_radius, y+armDY2, self.arm_length, armY)
        # Отрисовка ног
        pygame.draw.circle(sf, COLOR, (x - self.body_radius // 2, y + k3*self.body_radius//2), self.leg_length // 2, 2)  # Левая нога
        pygame.draw.circle(sf, COLOR, (x + self.body_radius // 2, y + k4*self.body_radius//2), self.leg_length // 2, 2)  # Правая нога
        sf = pygame.transform.rotate(sf, k * self.angle)
        dx, dy = sf.get_width() / 2, sf.get_height() / 2
        screen.blit(sf, (self.x - dx, self.y - dy))

def main():
    clock = pygame.time.Clock()
    man = Man(30, 30)
    man.angle=1
    fps=10
    dt=1/fps

    i=0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        man.control([300,300], dt)
        man.sim(dt)

        man.phase=i%3
        screen.fill((255, 255, 255))  # Очистка экрана (белый фон)
        man.draw(screen)  # Отрисовка человечка

        pygame.display.flip()  # Обновление экрана
        clock.tick(fps)  # Ограничение FPS
        i+=1

if __name__ == "__main__":
    main()