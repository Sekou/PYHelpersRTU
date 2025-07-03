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
    def arrow(self, screen, color, p0, angle, lenpx, w):
        T=getT(); p0=CUT(T@EXT(p0))
        p1=[p0[0]+lenpx*math.cos(angle), p0[1]+lenpx*math.sin(angle)]
        p2=[p1[0]-10*math.cos(angle+0.5), p1[1]-10*math.sin(angle+0.5)]
        p3=[p1[0]-10*math.cos(angle-0.5), p1[1]-10*math.sin(angle-0.5)]
        pygame.draw.line(screen, color, p0, p1, w)
        pygame.draw.line(screen, color, p1, p2, w)
        pygame.draw.line(screen, color, p1, p3, w)
    def line(self, screen, color, p1, p2, w):
        T=getT(); p1, p2=CUT(T@EXT(p1)), CUT(T@EXT(p2))
        pygame.draw.line(screen, color, p1, p2, w)
    def lines(self, screen, color, closed, pp, w=1):
        T=getT(); pp=[CUT(T@EXT(p)) for p in pp]
        for i in range(len(pp)):
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
