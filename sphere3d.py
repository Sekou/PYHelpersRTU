import math
import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos

kpi = np.pi / 180

# from tex3d import *

def drawPoints(pts, sz=3):
    glPointSize(sz)
    glBegin(GL_POINTS)
    for p in pts:
        glVertex3fv(p)
    glEnd()

def drawAxes():
    for v in np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1))):
        glColor(v)
        glBegin(GL_LINES)
        glVertex3fv((0, 0, 0))
        glVertex3fv(v)
        glEnd()

def rotate(pts, r, p, y):
    cr, cp, cy = cos(r), cos(p), cos(y)
    sr, sp, sy = sin(r), sin(p), sin(y)
    myaw = [[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]]  # z
    mpit = [[cp, 0, sp], [0, 1, 0], [-sp, 0, cp]]  # y
    mrol = [[1, 0, 0], [0, cr, -sr], [0, sr, cr]]  # x
    mat = np.array(myaw) @ mpit @ mrol
    res = mat.dot(np.transpose(pts))
    res = np.transpose(res)
    return res

pts=[]

for i in range(100):
    r=[1,0,0]
    a=np.random.random()*math.pi*2
    b=np.random.random()*math.pi*2
    r=rotate([r], 0, a, b)[0]
    pts.append(r)

ptMarker=[0,0,0]

def drawScene():
    glRotate(1, 0, 0, 1)  # поворот на 1 градус вокруг оси Z
    drawAxes()
    glColor((1, 0, 0))
    drawPoints(pts)
    glColor((0, 0, 1))
    drawPoints([ptMarker], 5)

def main():
    global pts

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0, 0, -3)

    # разворот системы координат, чтоб ось Z была направлена вверх
    glMultMatrixf([[0, 0, -1, 0], [-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    glTranslatef(0, 0, -0.1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_w: ptMarker[0]+=0.1
                if event.key == K_s: ptMarker[0]-=0.1
                if event.key == K_d: ptMarker[1]+=0.1
                if event.key == K_a: ptMarker[1]-=0.1
                if event.key == K_e: ptMarker[2]+=0.1
                if event.key == K_q: ptMarker[2]-=0.1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glClearColor(1, 1, 1, 1)
        drawScene()

        # x,y,z=ptMarker
        # drawText(display, f"Pos: {x:.3f}, {y:.3f}, {z:.3f}", 12, 5, 5)

        pygame.display.flip()
        pygame.time.wait(50)


main()

# template file by S. Diane, RTU MIREA, 2024
