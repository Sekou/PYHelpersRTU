#2025, S. Diane
#пример движения двухколесного робота с зоной видимости
#объекты наносятся на карту в виде приближенного облака точек

import sys, pygame
import pygame_ext
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

#проверяем, находится ли точка внутри многоугольника
def pt_inside_ngon(point, vertices):
    (x, y), c = point, 0
    for i in range(len(vertices)):
        (x1, y1), (x2, y2) = vertices[i-1], vertices[i]
        if min(y1,y2) <= y < max(y1, y2):
            ratio = (y - y1) / (y2 - y1)
            c ^= (x - x1 < ratio*(x2 - x1))
    return c

sz = (800, 600)

class Ngon:
    #ngon=Ngon(2, 3, [[-0.5, -0.3], [-0.4, 0.4], [0.7,0.9], [0.3, -0.5]])
    def __init__(self, id, x=0, y=0, ang=0, pts=None):
        self.id, self.x, self.y, self.ang, self.pts = id, x, y, ang, pts
    def get_avg_radius(self):
        return np.mean([np.linalg.norm(p) for p in self.pts])
    def get_pos(self):
        return [self.x, self.y]
    def get_real_points(self):
        pp=[rot(p, self.ang) for p in self.pts]
        return np.array(pp)+self.get_pos()
    def draw(self, screen):
        pts_=self.get_real_points()
        for i in range(len(pts_)):
            pygame_ext.draw.line(screen, (0,0,0), pts_[i-1], pts_[i], 2)
        pygame_ext.draw.circle(screen, (0,0,0), self.get_pos(), 3/pygame_ext.scale, 0)

class Robot:
    def __init__(self, x, y):
        self.radius=0.5
        self.color=(0,0,0)
        self.x, self.y, self.ang=x,y,0
        self.vlin, self.vrot=0,0
        self.vision_area=Ngon(-1, self.x, self.y, self.ang, [[self.radius, -0.1], [self.radius, 0.1], [3, 1.5], [3, -1.5]])
    def get_pos(self):
        return [self.x, self.y]
    def draw(self, screen):
        p1=np.array(self.get_pos())
        pygame_ext.draw.circle(screen, self.color, p1, self.radius, 2)
        s,c=math.sin(self.ang), math.cos(self.ang)
        pygame_ext.draw.line(screen, self.color, p1, p1+[self.radius*c, self.radius*s],2)
        self.vision_area.draw(screen)
    def sim(self, dt):
        s,c=math.sin(self.ang), math.cos(self.ang)
        self.x+=c*self.vlin*dt
        self.y+=s*self.vlin*dt
        self.ang+= self.vrot * dt
        self.vision_area.x=self.x
        self.vision_area.y=self.y
        self.vision_area.ang=self.ang
    def get_visible_objs(self, objs):
        pp=self.vision_area.get_real_points()
        return [o for o in objs if pt_inside_ngon(o.get_pos(), pp)]

class Map:
    def __init__(self, w_real, h_real, w_px, h_px, x0_px, y0_px):
        self.w_real, self.h_real = w_real, h_real
        self.w_px, self.h_px = w_px, h_px
        self.x0_px, self.y0_px = x0_px, y0_px
        self.pts=[]
    def try_add_pt(self, pt, eps=0.1):
        dd=[dist(p, pt) for p in self.pts]
        if len(dd)>0:
            i=np.argmin(dd)
            if dd[i]>eps: self.pts.append(pt)
            else: self.pts[i]=0.5*np.add(self.pts[i], pt)
        else: self.pts.append(pt)
    def try_add_circle(self, pt, r, eps=0.1):
        n=int(2*np.pi*r/eps)
        da=2*np.pi/n
        for i in range(n):
            s,c=math.sin(i*da),math.cos(i*da)
            self.try_add_pt([pt[0]+c*r,pt[1]+s*r], eps)
    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), (self.x0_px, self.y0_px, self.w_px, self.h_px), 0)
        pygame.draw.rect(screen, (200,200,200), (self.x0_px, self.y0_px, self.w_px, self.h_px), 1)
        sx,sy=self.w_px/self.w_real, self.h_px/self.h_real
        for p in self.pts:
            p_=[p[0] * sx + self.x0_px, p[1] * sy + self.y0_px]
            pygame.draw.circle(screen, (255,0,0), p_, 3, 2)
        for i in range(int(self.w_real)):
            p1, p2 = [self.x0_px + i* sx, self.y0_px], [self.x0_px + i* sx, self.y0_px + self.h_px]
            pygame.draw.line(screen, (200,200,200), p1, p2, 1)
        for i in range(int(self.h_real)):
            p1, p2 = [self.x0_px, self.y0_px + i * sy], [self.x0_px + self.w_px, self.y0_px + i * sy]
            pygame.draw.line(screen, (200,200,200), p1, p2, 1)

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20
    robot = Robot(2, 2)
    map = Map(12, 8, 300, 200, 450, 10)

    ngon=Ngon(0, 4, 4, 0, [[-0.5, -0.3], [-0.4, 0.4], [0.7,0.9], [0.3, -0.5]])
    ngon2=Ngon(1, 7, 5, 1, [[-0.2, -0.6], [-0.3, 0.3], [0.5,0.5]])
    ngon3=Ngon(2, 2, 6, 1, [[-0.6, -0.5], [-0.5, 0.8], [0.8,0.3], [0.6, -0.7], [-0.3, -0.8]])
    objs=[ngon, ngon2, ngon3]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w: robot.vlin=1
                if ev.key == pygame.K_s: robot.vlin=-1
                if ev.key == pygame.K_a: robot.vrot=-1
                if ev.key == pygame.K_d: robot.vrot=+1

        dt=1/fps
        robot.sim(dt)
        oo=robot.get_visible_objs(objs)

        for o in oo:
            # map.try_add_pt(o.get_pos())
            map.try_add_circle(o.get_pos(), o.get_avg_radius(), 0.2)

        screen.fill((255, 255, 255))
        robot.draw(screen)
        for o in objs:
            o.draw(screen)
        map.draw(screen)

        drawText(screen, f"Test = {1}", 5, 5)
        str_objs=f"objs: {', '.join(str(o.id) for o in oo)}"
        drawText(screen, str_objs, 5, 25)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024
