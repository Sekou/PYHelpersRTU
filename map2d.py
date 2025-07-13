#2025, S. Diane
#An in-window 2d-map for pygame robots

import math
import pygame

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
        #usage: # map = Map(12, 10, 300, 250, 450, 110)
        #usage: # for o in oo: map.try_add_pt(o.get_pos()) #map.try_add_circle(o.get_pos(), o.get_avg_radius(), 0.2)
        #usage: # map.draw(screen)
