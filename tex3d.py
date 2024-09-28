#S. Diane, 2024
#Drawing text and color textures in PyGame+OpenGL simulation

import pygame
from OpenGL.GL import *

texTable={}
colorTable={}
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

def enableTex(WH):
    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WH[0], WH[1], 0, -100, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, WH[0],  WH[1])

def genTextureForText(text):
    if text in texTable.keys(): return texTable[text][0]
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
    return i

def genColorTexture(color):
    sc=str(color)
    if sc in colorTable.keys(): return colorTable[sc][0]
    szx, szy = 4, 4
    textSurface = pygame.Surface([szx, szy], pygame.SRCALPHA)
    textSurface.fill(color)
    image = pygame.image.tostring(textSurface, "RGBA", True)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    i = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, i)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, szx, szy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    colorTable[sc] = (i, color)
    return i

def drawTextInner(displayWH, text, sz, x, y):
    i=genTextureForText(text)
    k=displayWH[0]/displayWH[1]
    w,h=len(text)*sz/k, sz*k
    x,y=-1+2*x,1-2*y
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, i)
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

#draws face with color texture
def drawFace(vertices, inds, color):
    i=genColorTexture(color)
    glEnable(GL_TEXTURE_2D)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D, i)
    glBegin(GL_POLYGON)
    for i in range(len(inds)):
        ix, iy = [[0, 0], [1, 0], [1, 1]][i%3]
        glTexCoord2f(ix, iy)
        glVertex3f(*vertices[inds[i]])
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
