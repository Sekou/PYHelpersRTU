
import sys, pygame
import numpy as np
import math

pygame.font.init()
def drawText(screen, s, x, y, sz=20, color=(0,0,0)): #отрисовка текста
    font = pygame.font.SysFont('Comic Sans MS', sz)
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

def rot(v, ang): #поворот вектора на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def limAng(ang): #ограничение угла в пределах +/-pi
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def rotArr(vv, ang): # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]

def dist(p1, p2): #расстояние между точками
    return np.linalg.norm(np.subtract(p1, p2))

sz = (800, 600)

class Robot:
    def __init__(self, x, y):
        self.radius=20
        self.color=(0,0,0)
        self.x, self.y, self.a=x,y,0
        self.vlin, self.vrot=0,0
    def get_pos(self):
        return [self.x, self.y]
    def draw(self, screen):
        p1=np.array(self.get_pos())
        pygame.draw.circle(screen, self.color, p1, self.radius, 2)
        s,c=math.sin(self.a), math.cos(self.a)
        pygame.draw.line(screen, self.color, p1, p1+[self.radius*c, self.radius*s],2)
    def sim(self, dt):
        s,c=math.sin(self.a), math.cos(self.a)
        self.x+=c*self.vlin*dt
        self.y+=s*self.vlin*dt
        self.a+=self.vrot*dt

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20
    robot = Robot(200, 200)

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w: robot.vlin=50
                if ev.key == pygame.K_s: robot.vlin=-50
                if ev.key == pygame.K_a: robot.vrot=-1
                if ev.key == pygame.K_d: robot.vrot=+1

        dt=1/fps
        robot.sim(dt)

        screen.fill((255, 255, 255))
        robot.draw(screen)
        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024
