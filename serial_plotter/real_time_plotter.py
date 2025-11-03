#2025, S.Diane, plotter script for displaying real-time data

import serial, pygame, math, numpy as np
import sys, threading

pygame.font.init()
def draw_text(screen, s, x, y, sz=20, color=(0, 0, 0)):
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, (0, 0, 0)), (x, y))

def dist(p1, p2): #расстояние между точками
    return np.linalg.norm(np.subtract(p1, p2))

def rot(v, ang): #поворот вектора на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def draw_arrow(screen, color, p1, p2, w, sz):
    v = sz * np.subtract(p1, p2) / dist(p2, p1)
    p3, p4 = np.add(rot(v, 0.3), p2), np.add(rot(v, -0.3), p2)
    for p in [p1, p3, p4]: pygame.draw.line(screen, color, p, p2, w)

def draw_plot(screen, p1, w, h, valsx, valsy, scale_x=1, scale_y=1, sign_x=False, sign_y=False, color=(0,0,255)):
    p1, a, b, c, d = np.array(p1), 0, w, 0, -h
    if sign_x: a, b = -w / 2, w / 2
    if sign_y: c, d = h / 2, -h / 2
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
        else: pygame.draw.line(screen, color, pa, pb, 2)

sz = (800, 600)

colors1 = [(220, 0, 0), (0, 220, 0), (0, 0, 220), (150, 150, 0), (0, 150, 150), (150, 0, 150),
     (120, 50, 50), (50, 120, 50), (50, 50, 120), (100, 100, 50), (50, 100, 100), (100, 50, 100)]
colors2=[(r//2, g//2, b//2) for r,g,b in colors1]
colors=colors1+colors2

plots = []
def add_plot(xx, yy): plots.append((xx, yy))
def clear_plots(): plots.clear()

info=""
user_key_callback=None
user_exit_callback=None
wpx, hpx, wreal, hreal = 750, 500, 100, 30 * 2

def draw():
    screen = pygame.display.set_mode(sz)
    pygame.display.set_caption('Animation 2D')
    timer = pygame.time.Clock()
    fps = 20; dt = 1 / fps

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                if user_exit_callback: user_exit_callback()
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if user_key_callback: user_key_callback(ev.key)

        screen.fill((255, 255, 255))
        draw_text(screen, info, 5, 5)
        scx, scy = wpx / wreal, hpx / hreal
        for i, (xx, yy) in enumerate(plots):
            draw_plot(screen, (25, 300), wpx, hpx, xx, yy, scx, scy, sign_y=True, color=colors[i])

        pygame.display.flip()
        timer.tick(fps)

threading.Thread(target=draw).start()

#USAGE:
#1. adjust wreal, hreal
#real_time_plotter.hreal = 10
#with lock:
#    real_time_plotter.clear_plots()
#    for i, (d, v) in enumerate(zip(datas, vals)):
#        d.add_val(t, v)
#        real_time_plotter.add_plot(d.get_x_inds(), d.y_data)
