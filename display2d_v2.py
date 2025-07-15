# 2024-2025, S. Diane
# класс для отрисовки точек (в соседнем с симуляцией робота окне)

import math
import sys, pygame
import numpy as np
import time, datetime as dt

WIDTH, HEIGHT = 800, 600
SCALE=75

KEY = None # to read from external scripts
INFO = None # to set from external scripts
INFO_TEXT_SZ=25

points=[]
points_ext=[]
curves=[]
agents=[]

pygame.font.init()
def draw_text(screen, s, x, y, sz=14, color=(0,0,0)): # drawing text
    font = pygame.font.SysFont('Comic Sans MS', sz)
    screen.blit(font.render(s, True, (0,0,0)), (x,y))

def dist(p1, p2): #расстояние между точками
    dx,dy=p1[0]-p2[0],p1[1]-p2[1]
    return math.sqrt(dx*dx+dy*dy)

def get_some_colors():
    return [(220, 0, 0), (0, 220, 0), (0, 0, 220),
     (150, 150, 0), (0, 150, 150), (150, 0, 150),
     (120, 50, 50), (50, 120, 50), (50, 50, 120),
     (100, 100, 50), (50, 100, 100), (100, 50, 100)]

def save_screenshot(screen):
    frmt_date = dt.datetime.fromtimestamp(
        time.time()).strftime("%Y-%m-%d(%H-%M-%S)")
    pygame.image.save(screen, frmt_date+".png")

def save_data():
    res= {}
    res["points"]=[list(p) for p in points]
    res["points_ext"]=[p.as_dict() for p in points_ext]
    res["curves"]=curves
    res["agents"]=agents
    frmt_date = dt.datetime.fromtimestamp(
        time.time()).strftime("%Y-%m-%d(%H-%M-%S)")
    with open(frmt_date+".txt", "w") as f:
        f.write(str(res))

COLORS=get_some_colors()
Y_AXIS_UP=True
k=(-1 if Y_AXIS_UP else 1)
R_POINT=15

def trP(p):
    return (p[0] * SCALE + WIDTH // 2, p[1] * SCALE * k + HEIGHT // 2)

def arrow(screen, color, p0, angle, lenpx, w):
    angle, d = k*angle, 6
    c,s=math.cos(angle),math.sin(angle)
    p0 = [p0[0] + s/4, p0[1] - c/4] # small visual fix
    p1 = [p0[0] + lenpx * c, p0[1] + lenpx * s]
    p2 = [p1[0] - d * math.cos(angle + 0.5), p1[1] - d * math.sin(angle + 0.5)]
    p3 = [p1[0] - d * math.cos(angle - 0.5), p1[1] - d * math.sin(angle - 0.5)]
    for a, b in [[p0, p1], [p1, p2], [p1, p3]]:
        pygame.draw.line(screen, color, a, b, w)

class ExtPt: # extended point
    def __init__(self, x=0, y=0, radius=0, angle=None, color=(0,0,0), name=None):
        self.x, self.y = x, y
        self.radius = radius
        self.name = name
        self.angle = angle
        self.color = color
    def get_pos(self):
        return (self.x, self.y)
    def as_dict(self):
        return {'x': self.x, 'y': self.y, 'radius': self.radius,
                'name': self.name, 'angle': self.angle, 'color': self.color}
    def from_dict(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)
    def draw(self, screen):
        p, r = trP(self.get_pos()), self.radius * SCALE if self.radius else R_POINT
        pygame.draw.circle(screen, self.color, p, 3, 0)
        if self.radius: pygame.draw.circle(screen, self.color, p, max(10, r), 1)
        if self.angle: arrow(screen, self.color, p, self.angle, max(10, r), 2)
        if self.name: draw_text(screen, self.name, *p)

def drawGrid(screen, dx, dy):
    nx=int(WIDTH / abs(dx * SCALE) / 2 + 1)
    ny=int(HEIGHT / abs(dy * SCALE) / 2 + 1)
    dx*=SCALE; dy*=SCALE
    hw= WIDTH // 2; hh= HEIGHT // 2
    c=(200, 200, 200)
    for i in range(nx):
        pygame.draw.line(screen, c, (i*dx+hw, 0), (i*dx+hw, HEIGHT))
        if i>0: pygame.draw.line(screen, c, (-i * dx + hw, 0), (-i * dx + hw, HEIGHT))
    for i in range(ny):
        pygame.draw.line(screen, c, (0,i*dy+hh), (WIDTH, i * dy + hh))
        if i>0: pygame.draw.line(screen, c, (0,-i*dy+hh), (WIDTH, -i * dy + hh))

def try_add_pt(pt, eps=0.01):
    dd = [dist(p, pt) for p in points]
    if len(dd) > 0:
        i = np.argmin(dd)
        if dd[i] < eps:
            points[i] = 0.5 * np.add(points[i], pt)
            return
    points.append(pt)

def add_ext_pt(pt, eps=0.01):
    points_ext.append(pt)

def rot(p, ang):
    s,c=math.sin(ang), math.cos(ang)
    x=p[0]*c-p[1]*s
    y=p[0]*s+p[1]*c
    return [x,y]

def displayLoop():
    global screen, KEY
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Points 2D')
    timer = pygame.time.Clock()
    fps, R0 = 10, 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                KEY=event.key
                if KEY==pygame.K_s: save_screenshot(screen)
                if KEY==pygame.K_d: save_data()
                if KEY==pygame.K_a: save_data() or save_screenshot(screen)
            if event.type == pygame.QUIT:
                sys.exit(0)
        screen.fill((255, 255, 255))
        drawGrid(screen, 1, 1)
        for p in points:
            pygame.draw.circle(screen, (255, 0, 0), trP(p), R0, 0)
        for pe in points_ext:
            pe.draw(screen)
        for ind, cr in enumerate(curves):
            for i in range(1,len(cr)):
                c=COLORS[ind%len(COLORS)]
                pygame.draw.line(screen, c, trP(cr[i-1]), trP(cr[i]), 1)
        for ind, a in enumerate(agents):
            q = trP(a[:2])
            c = COLORS[ind % len(COLORS)]
            pygame.draw.circle(screen, c, q, R0, 0)
            pygame.draw.circle(screen, (0,0,0), q, R0, 1)
            arrow(screen, c, q, a[2], 15, 2)
            draw_text(screen, str(ind), *q)

        # coordinate system axes
        arrow(screen, (255,0,0), trP((0,0)), 0, 30, 2)
        arrow(screen, (0,255,0), trP((0,0)), math.pi/2, 30, 2)

        if INFO:
            draw_text(screen, INFO, 5, 5, sz=INFO_TEXT_SZ)

        pygame.display.flip()
        timer.tick(fps)

def start():
    import threading
    thr = threading.Thread(target=displayLoop, args=[])
    thr.start()

if __name__=="__main__":
    start()

#USAGE:
# import display2d_v2 as display2d
# from display2d_v2 import ExtPt
#
# display2d.start()
# display2d.points=[[1,1], [2,2], [-1,2]] # ordinary points
# display2d.try_add_pt([2.5,2.2],eps=0.1)
# display2d.agents=[[1, -1, 0.5], [1.5, -2, 1]] # robot positions
#
# display2d.points_ext=[ # points / objects with direction and color
#     ExtPt(1.5, 1.5, 0.1, 1, (100,100,0), "Pt1"),
#     ExtPt(2.5, 0.5, 0.5, 1, (100,100,0), "Pt2"),
#     ExtPt(-1.5, 1.5, 0.5, 1, (100,100,0), "Pt3") ]
# display2d.add_ext_pt(ExtPt(-2.5, 0.5, None, 1, (50,240,0), "Pt4"))
#
# # curves (trajectories, zones, ...)
# display2d.curves=[[(0,0), (1,1), (2,1), (3,0.5)]]
