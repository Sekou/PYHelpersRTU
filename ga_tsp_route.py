#2025, S. Diane
#Solving traveling salesman problem with evolutionary approach

import sys, pygame
import numpy as np
from pygame.locals import*

rint=np.random.randint

def dist(p1, p2): #расстояние между точками
    return np.linalg.norm((p2[0] - p1[0], p2[1] - p1[1]))

class Creature: #существо/особь/траектория/решение задачи
    def __init__(self, ga, inds=None):
        self.ga=ga
        self.vec_len=len(ga.pts)
        self.inds=list(range(self.vec_len)) if inds is None else inds
        self.fitness=0
        self.mutate(0.5)

    def mutate(self, k_mut):
        n=len(self.inds)
        for i in range(n):
            if np.random.rand()<k_mut:
                j=i+rint(1, n)
                self.inds[i], self.inds[j%n] = self.inds[j%n], self.inds[i]

    def eval(self):
        ii, pp = self.inds, self.ga.pts
        l=sum([dist(pp[i1], pp[i2]) for i1, i2 in zip(ii[:-1], ii[1:])])
        self.fitness=1/(1+l)

    def cross(self, other):
        i0 = rint(self.vec_len-1)
        i1, j = rint(i0+1,self.vec_len), i0
        inds = self.inds[:] # методом прямого копирования берем крайнюю часть индексов
        taken = inds[:i0]+inds[i1:]
        for ind in other.inds: # методом добора формируем центральную часть индексов
            if j>=i1: break
            if not ind in taken:
                inds[j], j = ind, j+1
        return Creature(self.ga, inds)

class GA: # генетический алгоритм
    #1 создание рандомной популяции
    def __init__(self, pts, num_creatures):
        self.k_mut=0.1 #сила мутаций
        self.f_mut=0.1 #частота мутаций
        self.pts=pts
        self.num_creatures=num_creatures
        self.num_elite=max(1, num_creatures//3)
        self.creatures=[] #особи
        for i in range(num_creatures):
            cr=Creature(self)
            self.creatures.append(cr)
        self.eval()
        self.sort()

    #2 оценка особей
    def eval(self):
        for cr in self.creatures:
            cr.eval()
    #3 сортировка особей
    def sort(self):
        self.creatures.sort(key=lambda x: -x.fitness)
    #4 скрещивание лучших
    def cross(self):
        childs=[]
        while self.num_elite+len(childs) < len(self.creatures):
            #индексы особей
            if self.num_elite==1:
                i1,i2=0, rint(1, self.num_creatures)
            else:
                i1,i2=rint(self.num_elite-1), rint(i1+1, self.num_elite)
            #особи
            cr1=self.creatures[i1]
            cr2=self.creatures[i2]
            ch=cr1.cross(cr2)
            childs.append(ch)
        self.creatures[self.num_elite:]=childs
    #5 мутация особей
    def mutate(self):
        N=max(1, int(self.num_creatures * self.f_mut))
        for i in range(N):
            i_ = rint(self.num_elite, self.num_creatures)
            cr = self.creatures[i_].mutate(self.k_mut)
    #6 выдача решения
    def get_solution(self):
        return self.creatures[0]
    #7 полный цикл
    def epoch(self, num_iters):
        for i in range(num_iters):
            self.cross()
            self.mutate()
            self.eval()
            self.sort()
        return self.creatures[0]
    def draw(self, screen):
        colors=[(255,0,0), (0,255,0), (0,0,255), (150,150,0), (0,150,150), (150,0,150),
                (150, 0, 0), (0, 150, 0), (0, 0, 150), (90, 90, 0), (0, 90, 90), (90, 0, 90)]
        for j,cr in enumerate(self.creatures):
            for i in range(1, len(cr.inds)):
                i1, i2=cr.inds[i-1], cr.inds[i]
                p1, p2=self.pts[i1], self.pts[i2]
                w=5 if j==0 else 1
                pygame.draw.line(screen, colors[j], p1, p2, w)

def main():
    sz=(800, 600)
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    r = 5
    fps = 30

    pts=[
        [100,100], [200,150], [150,300], [250,200], [350,300],
        [450,200], [250,400], [350,400], [150,400], [250,100]
    ]

    ga=GA(pts, 5)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: #одна итерация
                    cr=ga.epoch(1)
                    print(f"f={cr.fitness}")
                if event.key == pygame.K_2: #много итераций
                    cr=ga.epoch(500)
                    print(f"f={cr.fitness}")

        screen.fill((255, 255, 255))
        for p in pts:
            pygame.draw.circle(screen, (255, 0, 0), p, r, 2)
        ga.draw(screen)

        pygame.display.flip()
        timer.tick(fps)

main()
