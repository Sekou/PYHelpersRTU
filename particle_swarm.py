#2026, S. Diane, particle swarm optimization

import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, c=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2)) #расстояние между точками
def rot(v, ang): return np.dot([[-v[1], v[0]], v],[math.sin(ang), math.cos(ang)]) # поворот вектора на угол

sz = (800, 600)

class Particle:
    def __init__(self, p):
        self.p, self.v=p,[0,0]
    def sim(self, goal, dt):
        self.v+=0.05*(goal - np.array(self.p))
        self.p+=self.v*dt
    def draw(self, screen):
        pygame.draw.circle(screen, (255,0,0), self.p, 3, 2)

if __name__=="__main__":
    screen, timer, fps =  pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    dt = 1 / fps

    goal=[300,200]
    pts=[Particle(np.random.multivariate_normal([400,300], 100*np.eye(2))) for i in range(20)]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    print("Hi")     

        screen.fill((255, 255, 255))     

        for p in pts: p.sim(goal, dt)
        for p in pts: p.draw(screen)
        pygame.draw.circle(screen, (0,0,255), goal, 3, 2)

        draw_text(screen, f"Test = {1}", 5, 5)
        pygame.display.flip(), timer.tick(fps)

#template file by S. Diane, RTU MIREA, 2024-2026
