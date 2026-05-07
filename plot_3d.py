# 2026, S. Diane, 3D plot
# pip install pygame PyOpenGL
import pygame, numpy as np, math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_point(p):
    glColor3f(1, 1, 1), glPointSize(5.0), glBegin(GL_POINTS), glVertex3f(*p), glEnd()

def draw_segment(p0, p1):
    glColor3f(1, 1, 1), glBegin(GL_LINES), glVertex3fv(p0), glVertex3fv(p1), glEnd()

def draw_axes():
    glBegin(GL_LINES)  # Specify we are drawing lines
    for v in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        glColor3f(*v), glVertex3fv((0, 0, 0)), glVertex3fv(v)
    glEnd()

def draw_surface(func, step = 0.1, domain = [[-1, -1], [1,1]]): # Создаем сетку по x и y
    xx = [x for x in np.arange(domain[0][0], domain[1][0], step)]
    yy = [y for y in np.arange(domain[0][1], domain[1][1], step)]
    glColor3f(0.0, 1.0, 1.0)  # Цвет поверхности
    for i in range(len(xx) - 1):
        for j in range(len(yy) - 1): # Берем четыре точки квадрата
            pp=[[xx[i], yy[j]], [xx[i + 1], yy[j]],
                [xx[i + 1], yy[j + 1]], [xx[i], yy[j + 1]]]
            glBegin(GL_LINE_LOOP)
            for x,y in pp: glVertex3f(x, y, func(x,y))
            glEnd()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    zIsUp = np.array([  # разворачиваем систему координат чтоб было похоже на X0Y0Z0
        -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
    glMultMatrixf(zIsUp)

    glTranslatef(0, -5.0, -0.5)  # Move the camera back
    fps = 10
    dt, time = 1 / fps, 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(0.1, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_axes()

        #рисуем график
        draw_surface(func = lambda x,y: math.sin(x)*math.sin(y))

        pygame.display.flip(), pygame.time.wait(fps)
        time += dt

main()
