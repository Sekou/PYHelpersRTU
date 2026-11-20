#2026, S. Diane, clustering points near objects

import math, pygame, sys, numpy as np
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2)) # расстояние между точками

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
fps=20
timer = pygame.time.Clock()
colors=[[255,0,0], [0,255,0], [0,0,255], [180,180,0], [0,180,180], [180,0,180],
        [150,0,0], [0,150,0], [0,0,150], [90,90,0], [0,90,90], [90,0,90], [180,180,180]]

objs=[[200,150], [430,230], [600,140], [310,400], [510,420]]
NUM_OBJS=len((objs))

def rnd_pt(i, objs): return [np.random.normal(objs[i][0], 50),np.random.normal(objs[i][1], 30)] #случайная точка некоторой особи
pts = [[*rnd_pt(np.random.randint(NUM_OBJS), objs), -1] for i in range(200)]

centers = [[np.random.randint(0, width), np.random.randint(0, height), i] for i in range(NUM_OBJS)]

#шаг 1
def find_nearest_clusters():
    for p in pts:
        D=[dist(p[:2], c[:2]) for c in centers]
        p[2]=np.argmin(D)

#шаг 2
def shift_centers():
    for i in range(len(centers)):
        #рассчитываем геометрический центр подмножества
        cm = np.mean([p for p in pts if p[2]==i], axis=0, dtype=int)
        if cm is not None: #обновляем центроид
            centers[i][:2]=cm

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: find_nearest_clusters()
            if event.key == pygame.K_2: shift_centers()

    screen.fill((255, 255, 255)) #очистка экрана
    for i,p in enumerate(pts):
        pygame.draw.circle(screen, colors[p[2]], p[:2], 5)
    for i,p in enumerate(centers):
        pygame.draw.rect(screen, colors[p[2]], (p[0]-5, p[1]-5, 10, 10), 3)

    pygame.display.flip(), timer.tick(fps)
