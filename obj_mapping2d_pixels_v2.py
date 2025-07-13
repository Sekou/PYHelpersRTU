#2025, S. Diane
#пример движения двухколесного робота с зоной видимости, разбитой на пиксели
#контуры объектов наносятся на карту в виде облака точек

import sys, pygame
import pygame_ext
import numpy as np
import math
from numba import jit

pygame.font.init()
def draw_text(screen, s, x, y, sz=20, color=(0,0,0)): #отрисовка текста
    font = pygame.font.SysFont('Comic Sans MS', sz)
    screen.blit(font.render(s, True, (0,0,0)), (x,y))

def rot(v, ang): #поворот вектора на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def lim_ang(ang): #ограничение угла в пределах +/-pi
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def rot_arr(vv, ang): # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]

@jit
def dist(p1, p2): #расстояние между точками
    dx,dy=p1[0]-p2[0],p1[1]-p2[1]
    return math.sqrt(dx*dx+dy*dy)

#проверяем, находится ли точка внутри многоугольника
@jit
def pt_inside_ngon(point, vertices):
    (x, y), c = point, 0
    for i in range(len(vertices)):
        (x1, y1), (x2, y2) = vertices[i-1], vertices[i]
        if min(y1,y2) <= y < max(y1, y2):
            ratio = (y - y1) / (y2 - y1)
            c ^= (x - x1 < ratio*(x2 - x1))
    return c

@jit
def get_segm_intersection(A, B, C, D, lines=False): #поиск точки пересечения двух отрезков
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = A, B, C, D
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0: return None  # отрезки параллельны или совпадают
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    if lines or (0 <= t <= 1 and 0 <= u <= 1):
        intersection_x = x1 + t * (x2 - x1)
        intersection_y = y1 + t * (y2 - y1)
        return (intersection_x, intersection_y)
    return None

@jit
def pt_segm_dist(p, p1, p2): #расстояние от точки до отрезка
    dx, dy = np.subtract(p2, p1)
    k = dy / (0.0000001 if dx==0 else dx)
    b = p1[1] - k * p1[0]
    return np.abs(-k * p[0] + p[1] - b) / math.sqrt(k * k + 1)

@jit
def pt_on_edge(pt, pts_, eps=0.1): #лежит ли точка на границе многоугольника
    for i in range(len(pts_)):
        p1, p2 = pts_[i - 1], pts_[i]
        pc = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2]
        if dist(pt, pc) < dist(p1, p2) / 2:
            if pt_segm_dist(pt, pts_[i - 1], pts_[i]) < eps:
                return True
    return False

@jit
def find_nearest_pt(pt, pts): #поиск индекса и расстояния до ближайшей точки
    dd,m,ind = [dist(p, pt) for p in pts],100500,-1
    for i,d in enumerate(dd):
        if d<m: m,ind=d,i
    return ind,m

sz = (800, 600)

class Ngon:
    #ngon=Ngon(2, 3, [[-0.5, -0.3], [-0.4, 0.4], [0.7,0.9], [0.3, -0.5]])
    def __init__(self, id, x=0, y=0, ang=0, pts=None):
        self.id, self.x, self.y, self.ang, self.pts = id, x, y, ang, pts
        self.avg_r=self.get_avg_radius()
        self.max_r=self.get_max_radius()
        self.real_pts=self.get_real_points()
    def get_avg_radius(self):
        return np.mean([np.linalg.norm(p) for p in self.pts])
    def get_max_radius(self):
        return max([np.linalg.norm(p) for p in self.pts])
    def get_pos(self):
        return [self.x, self.y]
    def get_real_points(self):
        pp=[rot(p, self.ang) for p in self.pts]
        return np.array(pp)+self.get_pos()
    def draw(self, screen):
        pts_=self.real_pts
        pygame_ext.draw.lines(screen, (0, 0, 0), True, pts_, 1)
        pygame_ext.draw.circle(screen, (0,0,0), self.get_pos(), 3/pygame_ext.scale, 0)
    def get_inner_pts(self, step=0.1):
        pts_=self.real_pts
        (ax,ay), (bx,by) = np.min(pts_, axis=0), np.max(pts_, axis=0)
        for y in np.arange(ay, by, step):
            for x in np.arange(ax, bx, step):
                if not pt_inside_ngon((x,y), pts_): continue
                yield (x,y)
    def is_crossed(self, p1, p2):
        pc = np.mean([p1, p2], axis=0)
        if dist(self.get_pos(), pc) < dist(p1, p2) / 2 + self.max_r:
            pts_ = self.real_pts
            for i in range(len(pts_)):
                if get_segm_intersection(p1, p2, pts_[i - 1], pts_[i]):
                    return True
        return False
    def collides(self, ngon2):
        if dist(self.get_pos(), ngon2.get_pos())<self.max_r+ngon2.max_r:
            pts_ = self.real_pts
            pts__ = ngon2.real_pts
            if pt_inside_ngon(ngon2.get_pos(), pts_): return True
            if pt_inside_ngon(self.get_pos(), pts__): return True
            for i in range(len(pts_)):
                if ngon2.is_crossed(pts_[i - 1], pts_[i]):
                    return True
        return False
    def contains(self, ngon2):
        return all([pt_inside_ngon(p, self.real_pts) for p in ngon2.real_pts])
    def has_edge_pt(self, pt, eps=0.1):
        if dist(pt, self.get_pos())<self.max_r:
            return pt_on_edge(pt, self.real_pts, eps)
        return False

class Robot:
    def __init__(self, x, y):
        self.radius=0.4
        self.color=(200,200,200)
        self.x, self.y, self.ang=x,y,0
        self.vlin, self.vrot=0,0
        self.vision_area=Ngon(-1, self.x, self.y, self.ang, [[self.radius, -0.1], [self.radius, 0.1], [3, 1.5], [3, -1.5]])
        self.traj=[]
    def get_pos(self):
        return [self.x, self.y]
    def draw(self, screen):
        p1=np.array(self.get_pos())
        pygame_ext.draw.circle(screen, self.color, p1, self.radius, 0)
        pygame_ext.draw.circle(screen, (0,0,0), p1, self.radius, 1)
        s,c=math.sin(self.ang), math.cos(self.ang)
        pygame_ext.draw.line(screen, self.color, p1, p1+[self.radius*c, self.radius*s],2)
        self.vision_area.draw(screen)
        pygame_ext.draw.lines(screen, self.color, False, self.traj, 1)
    def sim(self, dt):
        s,c=math.sin(self.ang), math.cos(self.ang)
        self.x+=c*self.vlin*dt
        self.y+=s*self.vlin*dt
        self.ang+= self.vrot * dt
        self.vision_area.x=self.x
        self.vision_area.y=self.y
        self.vision_area.ang=self.ang
        self.vision_area.real_pts=self.vision_area.get_real_points()
        if len(self.traj)==0 or dist(self.traj[-1], self.get_pos())>0.1:
            self.traj.append(self.get_pos())
    def get_visible_objs(self, objs):
        pp=self.vision_area.real_pts
        return [o for o in objs if pt_inside_ngon(o.get_pos(), pp)]

class Pt:
    def __init__(self, pos, color=(0,0,0)):
        self.x, self.y = pos[0], pos[1]
        self.color = color
        self.state = False
    def get_pos(self):
        return [self.x, self.y]
class Map:
    def __init__(self, w_real, h_real, w_px, h_px, x0_px, y0_px):
        self.w_real, self.h_real = w_real, h_real
        self.w_px, self.h_px = w_px, h_px
        self.x0_px, self.y0_px = x0_px, y0_px
        self.pts=[]
        self.raw_pts=[]
    def try_add_pt(self, pt, eps=0.1):
        pt_=pt.get_pos()
        # dd=[dist(p, pt_) for p in self.raw_pts]
        if len(self.raw_pts)>0:
            i,d = find_nearest_pt(pt_, self.raw_pts)
            if d<eps:
                self.pts[i]=Pt(0.5*np.add(self.pts[i].get_pos(), pt_), pt.color)
                return
        self.pts.append(pt)
        self.raw_pts = np.array([p.get_pos() for p in self.pts])
    def try_add_circle(self, pt, r, eps=0.1):
        n=int(2*np.pi*r/eps)
        da=2*np.pi/n
        for i in range(n):
            s,c=math.sin(i*da),math.cos(i*da)
            self.try_add_pt(Pt([pt[0]+c*r,pt[1]+s*r]), eps)
    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), (self.x0_px, self.y0_px, self.w_px, self.h_px), 0)
        pygame.draw.rect(screen, (200,200,200), (self.x0_px, self.y0_px, self.w_px, self.h_px), 1)
        sx,sy=self.w_px/self.w_real, self.h_px/self.h_real
        for pt in self.pts:
            p=pt.get_pos()
            p_=[p[0] * sx + self.x0_px, p[1] * sy + self.y0_px]
            w = 0 if pt.state else 2
            pygame.draw.circle(screen, pt.color, p_, 3, 2)
        for i in range(int(self.w_real)):
            p1, p2 = [self.x0_px + i* sx, self.y0_px], [self.x0_px + i* sx, self.y0_px + self.h_px]
            pygame.draw.line(screen, (200,200,200), p1, p2, 1)
        for i in range(int(self.h_real)):
            p1, p2 = [self.x0_px, self.y0_px + i * sy], [self.x0_px + self.w_px, self.y0_px + i * sy]
            pygame.draw.line(screen, (200,200,200), p1, p2, 1)

def main():
    PIXEL_SZ=0.1
    screen = pygame.display.set_mode(sz)
    pygame.display.set_caption('Polygon mapping, S. Diane, 2025')
    timer = pygame.time.Clock()
    fps = 20
    robot = Robot(2, 3)
    map = Map(12, 10, 300, 250, 450, 110)

    ngon=Ngon(0, 4, 4, 0, [[-0.5, -0.3], [-0.4, 0.4], [0.7,0.9], [0.3, -0.5]])
    ngon2=Ngon(1, 7, 5, 1, [[-0.2, -0.6], [-0.3, 0.3], [0.5,0.5]])
    ngon3=Ngon(2, 2, 6, 1, [[-0.6, -0.5], [-0.5, 0.8], [0.8,0.3], [0.6, -0.7], [-0.3, -0.8]])
    ngon4=Ngon(3, 0.5, 1.5, 0, [[0, 0], [8, 0], [8,7], [0, 7]])
    objs=[ngon, ngon2, ngon3, ngon4]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w: robot.vlin=1
                if ev.key == pygame.K_s: robot.vlin=-1
                if ev.key == pygame.K_a: robot.vrot=-1
                if ev.key == pygame.K_d: robot.vrot=+1
                if ev.key == pygame.K_z: robot.vrot=robot.vlin=0

        dt=1/fps
        robot.sim(dt)
        oo=robot.get_visible_objs(objs)
        #
        # for o in oo:
        #     # map.try_add_pt(o.get_pos())
        #     map.try_add_circle(o.get_pos(), o.get_avg_radius(), 0.2)

        screen.fill((255, 255, 255))
        robot.draw(screen)
        for o in objs:
            o.draw(screen)
        map.draw(screen)

        pp=robot.vision_area.get_inner_pts(PIXEL_SZ)
        vv=robot.vision_area.real_pts
        focal_pt=get_segm_intersection(vv[0], vv[3], vv[1], vv[2], True)
        pygame_ext.draw.circle(screen, (0, 0, 255), focal_pt, 0.05)

        colors=[(255,0,0),(0,255,0),(0,0,255),(125,125,0),(0,125,125),(125,0,125)]

        pixels=[]
        objs_=[o for o in objs if robot.vision_area.collides(o) and not o.contains(robot.vision_area)]
        for p in pp:
            if not any([o.is_crossed(focal_pt, p) for o in objs_]):
                color=(200,200,200)
                for o in objs_:
                    if o.has_edge_pt(p, PIXEL_SZ):
                        pixels.append([p,colors[o.id]])
                        break
                pygame_ext.draw.cell(screen, color, p, PIXEL_SZ)

        for pos,color in pixels:
            map.try_add_pt(Pt(pos, color), 2*PIXEL_SZ)

        for pos,color in pixels:
            pygame_ext.draw.cell(screen, color, pos, PIXEL_SZ)

        pygame_ext.draw.coordinate_system(screen, 1)
        # pygame_ext.draw.cross(screen, (255,0,0), (2,2), 0.5, 1)
        # pygame_ext.draw.asterisk(screen, (255,0,0), (3,2), 0.5, 1)

        draw_text(screen, f"Test = {1}", 5, 5)
        str_objs=f"objs: {', '.join(str(o.id) for o in oo)}"
        draw_text(screen, str_objs, 5, 25)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2024
