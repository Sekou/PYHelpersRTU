#S.Diane, 2025
#info: developed to alter visualization from pixel space to metric space
#usage: just import this file and use 'draw' object

import pygame
import numpy as np
import math

shift=[0,0]
scale=50
eps=0.0000001

def getT():
    return np.array([[scale,0,0],[0,scale,0],[shift[0],shift[1],1]])
def EXT(v): return [*v,1]
def CUT(v): return v[:-1]
# def trP(p): return CUT(getT()@EXT(p))

class Draw:
    def circle(self, screen, color, pos, r, w=1):
        pos=CUT(getT()@EXT(pos))
        pygame.draw.circle(screen, color, pos, r*scale, w)
    def rect(self, screen, color, xywh, w=1):
        pos,(szx, szy)= CUT(getT() @ EXT(xywh[:2])), xywh[2:]
        pygame.draw.rect(screen, color, [*pos, szx * scale, szy * scale], w)
    def cell(self, screen, color, pos, sz, w=1):  # отрисовка квадратной дискреты
        eps = w/scale
        bb = (pos[0] - sz / 2, pos[1] - sz / 2, sz+eps, sz+eps)
        self.rect(screen, color, bb, w)
    def cross(self, screen, color, pos, r, w=1):
        pos=CUT(getT()@EXT(pos))
        x,y,sz=pos[0], pos[1], r*scale
        pygame.draw.line(screen, color, [x, y-sz], [x,y+sz], w)
        pygame.draw.line(screen, color, [x-sz, y], [x+sz,y], w)
    def asterisk(self, screen, color, pos, r, w=1):
        pos=CUT(getT()@EXT(pos))
        x,y,sz,a=pos[0], pos[1], r*scale,math.pi/4
        for i in range(4):
            s,c=math.sin(i*a), math.cos(i*a)
            pygame.draw.line(screen, color, [x-c*sz, y-s*sz], [x+c*sz, y+s*sz], w)
    def arrow(self, screen, color, p0, angle, lenpx, w):
        T=getT(); p0=CUT(T@EXT(p0))
        p1=[p0[0]+lenpx*math.cos(angle), p0[1]+lenpx*math.sin(angle)]
        p2=[p1[0]-10*math.cos(angle+0.5), p1[1]-10*math.sin(angle+0.5)]
        p3=[p1[0]-10*math.cos(angle-0.5), p1[1]-10*math.sin(angle-0.5)]
        for a,b in [[p0, p1],[p1, p2],[p1, p3]]:
            pygame.draw.line(screen, color, a, b, w)
    def coordinate_system(self, screen, axes_len_meters, w=2):
        self.arrow(screen, (255,0,0), (0,0), 0, axes_len_meters * scale, w)
        self.arrow(screen, (0,255,0), (0,0), math.pi / 2, axes_len_meters * scale, w)
    def line(self, screen, color, p1, p2, w):
        T=getT(); p1, p2=CUT(T@EXT(p1)), CUT(T@EXT(p2))
        pygame.draw.line(screen, color, p1, p2, w)
    def lines(self, screen, color, closed, pp, w=1):
        T=getT(); pp=[CUT(T@EXT(p)) for p in pp]
        start=0 if closed else 1
        for i in range(start, len(pp)):
            pygame.draw.line(screen, color, pp[i-1], pp[i], w)
    def grid(self, screen, color, step, x0, y0, xmax, ymax, w=1):
        x,y=x0,y0
        while x<=xmax+eps:
            self.line(screen, color, [x, y0], [x, ymax], w)
            x+=step
        while y<=ymax+eps:
            self.line(screen, color, [x0, y], [xmax, y], w)
            y+=step

draw=Draw()
