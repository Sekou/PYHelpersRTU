import sys, pygame
import numpy as np
from pygame.locals import*

def dist(p1, p2):
    return np.linalg.norm(np.subtract(p1, p2))

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

def draw_radio(screen, x, y, sz=60, n=3):
    (p1,p2,p3),rn=np.array([(x-sz/3-1, y),(x+sz/3, y),(x, y-sz)]),range(n)
    pp1,pp2=[p1+i*(p3-p1)/n for i in rn],[p2+i*(p3-p2)/n for i in rn]
    for l,r in [[pp1, pp2],[pp2, pp1]]:
        for a,b in zip(l[:-1], r[1:]):
            pygame.draw.line(screen, (0,0,0), a, b, 2)
    for p in [p1,p2]: pygame.draw.line(screen, (0,0,0), p, p3, 2)
    pygame.draw.circle(screen, (0,0,0), p3, sz/8, 2)

if __name__=="__main__":
    sz=(800, 600)
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
        screen.fill((255, 255, 255))
        draw_radio(screen, 200, 200)
        pygame.display.flip()
        timer.tick(fps)
