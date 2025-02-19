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

def drawRotRect(screen, color, pc, w, h, ang): #точка центра, ширина высота прямоуг и угол поворота прямогуольника
    pts = [[- w/2, - h/2], [+ w/2, - h/2], [+ w/2, + h/2], [- w/2, + h/2]]
    pts = rotArr(pts, ang)
    pts = np.add(pts, pc)
    pygame.draw.polygon(screen, color, pts, 2)

sz = (800, 600)

class LunarModule:
    def __init__(self, x, y, ang):
        self.pts = [[0, -25], [15, -15], [25, 18], [25, 25], [17, 25], [17, 18], [10, 18],
                    [10, 25], [3, 25], [3, 18], [-3, 18], [-3, 25], [-10, 25], [-10, 18],
                    [-17, 18], [-17, 25], [-25, 25], [-25, 18], [-15, -15]]
        self.x, self.y, self.ang=x, y, ang
        self.m=1
        self.J=50
        self.vx=0
        self.vy=0
        self.vang=0
        self.collision=False
        self.gas=[0,0,0,0]
    def getPos(self):
        return [self.x, self.y]
    def draw_flame(self, screen, p, val):
        pygame.draw.line(screen, (255,0,0), p, np.add(p,rot([0,val*30], self.ang)), 3)
    def draw(self, screen):
        color=(255,0,0) if self.collision else (0,0,0)
        pts=rotArr(self.pts, self.ang)+np.array(self.getPos())
        pygame.draw.polygon(screen, color, pts, 2)
        for i,x in enumerate([22, 7, -7, -22]):
            self.draw_flame(screen, np.add(self.getPos(),rot([x,29], self.ang)), self.gas[i])

    def sim(self, dt):
        if self.collision: return
        gLunar=5
        Fy, Fx=self.m*gLunar,0
        if self.gas is not None:
            ff=10*np.array(self.gas, dtype=float)
            force=np.sum(ff)
            vecForce=force*np.array(rot([0, -1], self.ang))
            Fx+=vecForce[0]
            Fy+=vecForce[1]
            torque=np.dot(ff, [-17, -10, 10, 17])
            eps=torque/self.J
            self.vang+= eps * dt
            self.ang+= self.vang * dt
        ax, ay = Fx / self.m, Fy / self.m
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def checkCollision(self, terrain):
        pts=rotArr(self.pts, self.ang)+np.array(self.getPos())
        pts2=terrain.getPts()
        for p in pts:
            dd=[dist(p, p2) for p2 in pts2]
            if any(d<10 for d in dd):
                self.collision=True

class Terrain:
    def __init__(self, y0, x0, x1, n):
        self.y0,self.heights=y0,[]
        self.x0, self.x1, self.n=x0, x1, n
        for i in range(self.n):
            self.heights.append(200*np.random.random())
    def draw(self, screen):
        dx=(self.x1-self.x0)/self.n
        yPrev=self.y0
        for i in range(self.n):
            y=self.y0-self.heights[i]
            x1=self.x0+i*dx
            x2=x1+dx
            pygame.draw.line(screen, (0,0,0), [x1, yPrev], [x1, y], 2)
            pygame.draw.line(screen, (0,0,0), [x1, y], [x2, y], 2)
            yPrev=y
        for i in range(3*self.n//7, 4*self.n//7):
            self.heights[i]=150
    def getPts(self):
        pts=[]
        dx=(self.x1-self.x0)/self.n
        for i in range(self.n):
            y = self.y0 - self.heights[i]
            x = self.x0 + i * dx
            pts.append([x, y])
        return pts

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    terrain=Terrain(500, 0, 800, 50)
    lm=LunarModule(200, 100, 0)

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w:
                    lm.gas=[0.5, 0.5, 0.5, 0.5]
                if ev.key == pygame.K_d:
                    lm.gas=[0, 0, 0.1, 0.1]
                if ev.key == pygame.K_a:
                    lm.gas=[0.1, 0.1, 0, 0]

        dt=1/fps

        lm.sim(dt)
        lm.checkCollision(terrain)

        lm.gas=0.9*np.array(lm.gas)

        screen.fill((255, 255, 255))
        terrain.draw(screen)
        lm.draw(screen)

        drawText(screen, f"Test = {1}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024