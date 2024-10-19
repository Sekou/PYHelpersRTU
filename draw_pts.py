import sys, pygame
from pygame.locals import*
import numpy as np
import sys

width=800
height=600
file=sys.path[0]+'\\pts.txt'
print(file)

def main():
    screen=pygame.display.set_mode((width,height))
    timer = pygame.time.Clock()
    fps = 20
    pts = [] #[[200, 200], [300, 300], [200, 300]]
    r = 4
    MODE=0 #0-pts, 1-ngons

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONUP:
                p, d = None, 100500
                thr=10
                pos = pygame.mouse.get_pos()
                dd=[np.linalg.norm(np.subtract(pos, p)) for p in pts]
                if len(dd)>0:
                    i=np.argmin(dd)
                    p, d = pts[i], dd[i]
                if event.button == 1 and d>thr:
                    pts.append(pos)
                if event.button == 3 and d<=thr:
                    pts.remove(p)
            if event.type == pygame.KEYDOWN:
                if event.key == K_m:
                    MODE=1-MODE
                if event.key == K_c:
                    pts=[]
                if event.key == K_s:
                    np.savetxt(file, pts, fmt='%3.0d')
                    pygame.image.save(screen, file.replace(".txt", ".png"))
                if event.key == K_l:
                    pts=np.loadtxt(file)

        screen.fill((255, 255, 255))

        for pt in pts:
            pygame.draw.circle(screen, (0,255,0), pt, r, 0)
        if MODE==1 and len(pts)>1:
            pts_=[*pts, pts[0]]
            for a, b in zip(pts_[:-1], pts_[1:]):
                pygame.draw.line(screen, (0,255,0), a, b, 2)

        pygame.display.flip()
        timer.tick(fps)

main()
