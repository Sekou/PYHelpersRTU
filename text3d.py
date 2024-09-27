#S. Diane, 2024
#Drawing text in PyGame+OpenGL simulation

import pygame
from OpenGL.GL import *

texTable={}
PM, MVM = None, None #projection and modelview matrices
def pushGL():
    global PM, MVM
    PM = glGetDoublev(GL_PROJECTION_MATRIX)
    MVM = glGetDoublev(GL_MODELVIEW_MATRIX)

def popGL():
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixf(PM)
    glMatrixMode(GL_MODELVIEW)
    glLoadMatrixf(MVM)

def enableTex(display):
    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, display[0], display[1], 0, -100, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, display[0],  display[1])

def genTextureForText(text):
    if text in texTable.keys(): return
    font = pygame.font.Font(None, 64)
    textSurface = font.render(text, True, (0,0,0, 255))
    szx, szy = textSurface.get_width(), textSurface.get_height()
    image = pygame.image.tostring(textSurface, "RGBA", True)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    i = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, i)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, szx, szy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    texTable[text] = (i, text)

def drawTextInner(displayWH, text, sz, x, y):
    genTextureForText(text)
    k=displayWH[0]/displayWH[1]
    w,h=len(text)*sz/k, sz*k
    x,y=-1+2*x,1-2*y
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, texTable[text][0])
    glBegin(GL_QUADS)
    for ix,iy in [[0,0], [1,0], [1,1], [0,1]]:
        glTexCoord2f(ix,iy)
        glVertex3f(x+w*ix, -y + h*(1-iy), -1)
    glEnd()

#draws text in specified position
def drawText(displayWH, text, sz, x, y):
    pushGL()
    enableTex(displayWH)
    drawTextInner(displayWH, text, sz, x, y)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    popGL()