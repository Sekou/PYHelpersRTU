import math
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos

kpi=np.pi/180

def drawPoints(pts):
    glPointSize(3)
    glBegin(GL_POINTS)
    for p in pts:
        glVertex3fv(p)
    glEnd()

def drawAxes():
    for v in np.array(((1,0,0),(0,1,0),(0,0,1))):
        glColor(v)
        glBegin(GL_LINES)
        glVertex3fv((0,0,0))
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

pts=[
    [0.5,0.3,0.4],
    [0.2,0.3,0.4],
    [0.5,0.7,0.4],
    [0.5,0.3,0.6],
    [0.5,0.5,0.5]
]

pts2 = rotate(pts, 45*kpi, 0, 0)
pts2 = pts2 + [0.5,0.3,0.1]

def main():
    pygame.init()
    display=(800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0,0,-3)

    #разворот системы координат, чтоб ось Z была направлена вверх
    glMultMatrixf([ [0,0,-1,0],[-1,0,0,0],[0,1,0,0],[0,0,0,1] ])
    glTranslatef(0,0,-0.5)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key==K_1:
                    print("Test") 

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(1, 1, 1, 1)

        glRotate(1, 0,0,1) #поворот на 1 градус вокруг оси Z
        drawAxes()

        glColor((1,0,0))
        drawPoints(pts)
        glColor((0,0,1))
        drawPoints(pts2)

        pygame.display.flip()
        pygame.time.wait(50)

main()

#template file by S. Diane, RTU MIREA, 2024
