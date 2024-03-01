import sys, pygame
import numpy as np
import math

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

sz = (800, 600)

def rot(v, ang): #функция для поворота на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def limAng(ang):
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def rotArr(vv, ang): # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]

def dist(p1, p2):
    return np.linalg.norm(np.subtract(p1, p2))

def drawRotRect(screen, color, pc, w, h, ang): #точка центра, ширина высота прямоуг и угол поворота прямогуольника
    pts = [
        [- w/2, - h/2],
        [+ w/2, - h/2],
        [+ w/2, + h/2],
        [- w/2, + h/2],
    ]
    pts = rotArr(pts, ang)
    pts = np.add(pts, pc)
    pygame.draw.polygon(screen, color, pts, 2)
    # for i in range(len(pts)):
    #    pygame.draw.line(screen, (0,0,255),pts[i-1], pts[i], 2)

def main():
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 30
    b, team1, team2 = None, None, None

    a = Area((25, 25), sz[1]-50, sz[0]-50)
    def initScene():
        nonlocal b, team1, team2
        p1 = a.getGlobalPt((200,0))
        p2 = a.getGlobalPt((-200, 0))
        team1 = Team(a, 3, 100, True)
        team2 = Team(a, 3, 100, False)
        ptRndx = np.random.randint(-10, 11)
        ptRndy = np.random.randint(-10, 11)
        b = Ball(*a.getGlobalPt((ptRndx, ptRndy)),70)
        b.vx = 0
        b.vy = 0
    initScene()
    score1, score2 = 0, 0

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    initScene()

        dt=1/fps
        b.sim(dt)
        team1.sim(dt, b)
        team2.sim(dt, b)

        screen.fill((255, 255, 255))
        team1.draw(screen)
        team2.draw(screen)
        b.draw(screen)
        a.draw(screen)

        outside = a.isPtOutside(b.getPos())
        if outside:
            ptLocal=a.getLocalPt(b.getPos())
            initScene()
            if ptLocal[0] < 0: score1 += 1
            else: score2 += 1

        drawText(screen, f"Score = {score1} : {score2}", 5, 5)

        pygame.display.flip()
        timer.tick(fps)

main()
