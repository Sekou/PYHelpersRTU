#2026, S. Diane, particle swarm optimization
import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, c=(255, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2)) #расстояние между точками
def rot(v, ang): return np.dot([[-v[1], v[0]], v],[math.sin(ang), math.cos(ang)]) # поворот вектора на угол

sz = (800, 600)

def func(x,y):# целевая функция (с многими локальными минимумами)
    return 1-math.sin(y/30)*math.sin(x/30)/(200+x+y)

class Particle: #класс частицы-гипотезы о решении оптимизационной задачи
    def __init__(self, p):
        self.val, self.val_best=100500,100500
        self.p, self.p_best, self.v=[*p],[*p],[0,0]
    def sim(self, g_best, func, dt):
        self.val=func(self.p[0],self.p[1])
        if self.val<self.val_best: self.val_best, self.p_best = self.val, [*self.p]
        self.v+=0.15*(self.p_best - np.array(self.p)) + 0.1*(g_best - np.array(self.p)) +\
        np.random.multivariate_normal([0,0], 50*np.eye(2)) #небольшое случайное отклонение
        self.p+=self.v*dt
    def draw(self, screen): pygame.draw.circle(screen, (255,0,0), self.p, 3, 2)

# генерируем растр по заданной функции
arr=np.zeros([sz[0], sz[1], 3]) #x and y are swapped for pygame compatibility
for x in range(arr.shape[0]):
    for y in range(arr.shape[1]):
        arr[x,y,:]=func(x,y)
arr=(arr-np.min(arr))*255/(np.max(arr)-np.min(arr))
func_surf = pygame.surfarray.make_surface(np.array(arr, dtype=int))

if __name__=="__main__":
    screen, timer, fps =  pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    dt = 1 / fps

    goal, v_best=[400,300], 100500
    pts=[Particle(np.random.multivariate_normal([400,300], 2500*np.eye(2))) for i in range(20)]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r: print("Hi")

        for p in pts: p.sim(goal, func, dt)
        i=np.argmin([p.val for p in pts])
        if pts[i].val<v_best:
            v_best, goal=pts[i].val, [*pts[i].p]

        screen.blit(func_surf, (0, 0))
        for p in pts: p.draw(screen) #рисуем частицы
        pygame.draw.circle(screen, (0,0,255), goal, 4, 3) #рисуем точку-решение
        draw_text(screen, f"Test = {1}", 5, 5)
        pygame.display.flip(), timer.tick(fps)
