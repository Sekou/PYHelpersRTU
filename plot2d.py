#2024, S. Diane, plotting functions for pygame

import pygame
import numpy as np
import math

def dist(p1, p2): #расстояние между точками
    return np.linalg.norm(np.subtract(p1, p2))

def rot(v, ang): #поворот вектора на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]
    
pygame.font.init()
def draw_text(screen, s, x, y, sz=20, color=(0,0,0)):
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, (0,0,0)), (x,y))

def draw_arrow(screen, color, p1, p2, w, sz):
    v=sz*np.subtract(p1, p2)/dist(p2, p1)
    p3, p4=np.add(rot(v, 0.3),p2), np.add(rot(v, -0.3),p2)
    for p in [p1, p3, p4]: pygame.draw.line(screen, color, p, p2, w)

def draw_plot_mini(screen, p1, width, height, valsx, valsy, sx=1, sy=1):
    draw_arrow(screen, (0,0,0), p1, np.add(p1, [0, -height]), 2, 15)
    draw_arrow(screen, (0,0,0), p1, np.add(p1, [width, 0]), 2, 15)
    draw_text(screen, f"{width*sx}", width, 0)
    pp=list(zip(p1[0]+np.array(valsx)*sx, p1[1]-np.array(valsy)*sy))
    for pa, pb in zip(pp[1:], pp[:-1]):
        pygame.draw.line(screen, (0,0,255), pa, pb, 2)

def draw_plot(screen, p1, width, height, valsx, valsy, scale_x=1, scale_y=1, signed_x=False, signed_y=False):
    p1=np.array(p1)
    a, b, c, d = 0, width, 0, -height
    if signed_x: a, b = -width/2, width/2
    if signed_y: c, d = height/2, -height/2
    draw_arrow(screen, (0,0,0), p1+[a,0], p1+[b,0], 2, 15)
    draw_arrow(screen, (0,0,0), p1+[0,c], p1+[0,d], 2, 15)
    a1, a2=max(abs(a), abs(b))/scale_x, max(abs(c), abs(d))/scale_y
    s1, s2=f"{a1:.3f}".rstrip('0').rstrip('.'), f"{a2:.3f}".rstrip('0').rstrip('.')
    draw_text(screen, s1, *(p1+[b - 5*(2+len(s1)), 10]), 10)
    draw_text(screen, s2, *(p1+[-5*(2+len(s2)), d]), 10)
    for l in [[a,c,b,c], [a,d,b,d], [a,c,a,d], [b,c,b,d]]:
        pygame.draw.line(screen, (150,150,150), p1+l[:2], p1+l[2:])
    pp=list(zip(p1[0]+np.array(valsx)*scale_x, p1[1]-np.array(valsy)*scale_y))
    for pa, pb in zip(pp[1:], pp[:-1]):
        dx,dy=pb[0]-p1[0],pb[1]-p1[1]
        if dx>b or dx<a or dy>c or dy<d: continue
        else: pygame.draw.line(screen, (0,0,255), pa, pb, 2)

# Example
# wpx, hpx, wreal, hreal=750, 500, 100, 30*2
# sc1, sc2 = wpx/wreal, hpx/hreal
# xx,yy=[0,50,100], [5,7,6]
# draw_plot(screen, (25,300), wpx, hpx, xx, yy, sc1, sc2, signed_y=True

