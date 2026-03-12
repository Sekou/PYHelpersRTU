#S.Diane, 2025-2026
#info: developed to alter visualization from pixel space to metric space
#usage: just import this file and use 'draw' object
import pygame, numpy as np, math

shift, scale, eps, T = [0,0], 20, 0.0000001, np.zeros((3,3))
def getT(): global T; T=np.array([[scale,0,0],[0,scale,0],[shift[0],shift[1],1]]); return T
def EXT(v): return [*v,1]
def tr(p): return (getT() @ EXT(p))[:-1]
def trtr(pp): getT(); return [(T@EXT(p))[:-1] for p in pp]

class Draw:
    def __init__(self): self.first_time=True
    def circle(self, screen, color, pos, r, w=1): pygame.draw.circle(screen, color, tr(pos), r * scale, w)
    def rect(self, screen, color, xywh, w=1):
        pos,(szx, szy)= tr(xywh[:2]), xywh[2:]
        pygame.draw.rect(screen, color, [*pos, szx * scale, szy * scale], w)
    def cell(self, screen, color, pos, sz, w=1):  # отрисовка квадратной дискреты
        self.rect(screen, color, (pos[0] - sz / 2, pos[1] - sz / 2, sz+w/scale, sz+w/scale), w)
    def cross(self, screen, color, pos, r, w=1):
        (x,y),sz,dl = tr(pos), r*scale, pygame.draw.line
        dl(screen, color, [x, y-sz], [x,y+sz], w), dl(screen, color, [x-sz, y], [x+sz,y], w)
    def asterisk(self, screen, color, pos, r, w=1):
        (x,y),sz,a = tr(pos), r*scale,math.pi/4
        for i in range(4):
            s,c=math.sin(i*a), math.cos(i*a)
            pygame.draw.line(screen, color, [x-c*sz, y-s*sz], [x+c*sz, y+s*sz], w)
    def arrow(self, screen, color, p0, angle, lenpx, w):
        p0=tr(p0)
        p1=[p0[0]+lenpx*math.cos(angle), p0[1]+lenpx*math.sin(angle)]
        p2=[p1[0]-10*math.cos(angle+0.5), p1[1]-10*math.sin(angle+0.5)]
        p3=[p1[0]-10*math.cos(angle-0.5), p1[1]-10*math.sin(angle-0.5)]
        for a,b in [[p0,p1],[p1,p2],[p1,p3]]: pygame.draw.line(screen, color, a, b, w)
    def coordinate_system(self, screen, axes_len_meters, w=2):
        self.arrow(screen, (255,0,0), (0,0), 0, axes_len_meters * scale, w)
        self.arrow(screen, (0,255,0), (0,0), math.pi / 2, axes_len_meters * scale, w)
    def line(self, screen, color, p1, p2, w): pygame.draw.line(screen, color, tr(p1), tr(p2), w)
    def lines(self, screen, color, closed, pp, w=1):
        pp=trtr(pp)
        for i in range(0 if closed else 1, len(pp)): pygame.draw.line(screen, color, pp[i-1], pp[i], w)
    def grid(self, screen, color, step, x0, y0, xmax, ymax, w=1):
        for x in np.arange(x0, xmax+eps, step): self.line(screen, color, [x, y0], [x, ymax], w)
        for y in np.arange(y0, ymax+eps, step): self.line(screen, color, [x0, y], [xmax, y], w)
    def text(self, screen, s, x, y, sz=12, color=(0, 0, 0), px=True): # отрисовка текста
        if self.first_time: pygame.font.init(); self.first_time=False
        screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, color), (x, y) if px else tr((x, y)))
draw=Draw()
