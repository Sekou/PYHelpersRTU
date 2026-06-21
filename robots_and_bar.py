import sys, pygame, numpy as np, math

pygame.font.init()

def draw_text(screen, s, x, y, sz=20, color=(0, 0, 0)): # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, (0, 0, 0)), (x, y))
def lim_ang(ang, arc=3.141592653589793): # ограничение угла в пределах +/-pi
    ang = ang % (2 * arc);
    return ang + (2 * arc if ang < -arc else -2 * arc if ang > arc else 0)
def rot(v, ang): return np.dot([[-v[1], v[0]], v], [math.sin(ang), math.cos(ang)]) # поворот вектора на угол
def rot_arr(vv, ang): return [rot(v, ang) for v in vv] # функция для поворота массива на угол
def dist(p1, p2): return np.linalg.norm(np.subtract(p2, p1))  # расстояние между точками

# отрисовка стрелки по точке и углу
def draw_arrow(screen, color, p0, ang, lenpx, w):
    p1 = [p0[0] + lenpx * math.cos(ang), p0[1] + lenpx * math.sin(ang)]
    p2 = [p1[0] - 10 * math.cos(ang + 0.5), p1[1] - 10 * math.sin(ang + 0.5)]
    p3 = [p1[0] - 10 * math.cos(ang - 0.5), p1[1] - 10 * math.sin(ang - 0.5)]
    for a, b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)

class Robot:
    def __init__(self, x, y):
        self.radius, self.color = 20, (0, 0, 0)
        self.x, self.y, self.a, self.vlin, self.vrot = x, y, 0, 0, 0
    def get_pos(self): return [self.x, self.y]
    def draw(self, screen):
        p1 = np.array(self.get_pos())
        pygame.draw.circle(screen, self.color, p1, self.radius, 2)
        s, c = math.sin(self.a), math.cos(self.a)
        pygame.draw.line(screen, self.color, p1, p1 + [self.radius * c, self.radius * s], 2)
    def sim(self, dt):
        s, c = math.sin(self.a), math.cos(self.a)
        self.x, self.y = self.x + c * self.vlin * dt, self.y + s * self.vlin * dt
        self.a = lim_ang(self.a + self.vrot * dt)

class Bar:  # балка
    def __init__(self, x, y, ang, L, W):
        self.x, self.y, self.ang, self.L, self.W = x, y, ang, L, W
        self.a, self.v, self.m = np.zeros(2), np.zeros(2), 1
        self.eps, self.w, self.J = 0, 0, 500
        self.F, self.M = np.zeros(2), 0
    def reset(self): self.F, self.M = np.zeros(2), 0
    def get_pos(self): return [self.x, self.y]
    def get_all_pts(self):
        pp = [[i * self.L / 2, j * self.W / 2] for i, j in [[-1, -1], [1, -1], [1, 1], [-1, 1]]]
        return np.add(rot_arr(pp, self.ang), self.get_pos())
    def local_to_global_pt(self, pt):
        return np.array(rot(pt, self.ang)) + self.get_pos()
    def set_pos(self, p): self.x, self.y = p
    def draw(self, screen):
        pp = self.get_all_pts()
        pygame.draw.lines(screen, (0, 0, 0), True, pp, 2)
        draw_arrow(screen, (255, 0, 0), self.get_pos(), math.atan2(*self.F[::-1]), 20, 2) #сила
        c, m = ((0, 255, 0), self.M) if self.M >= 0 else ((255, 0, 0), -self.M)
        pygame.draw.circle(screen, c, self.get_pos(), m / 100, 2) #момент
    def apply_force(self, local_pt, global_F):
        self.F += global_F
        lF = np.linalg.norm(local_pt)
        vec = np.array(local_pt) / np.linalg.norm(local_pt)
        vec = rot(vec, self.ang)
        vec2 = rot(vec, np.pi / 2)
        F = np.dot(vec2, global_F)
        self.M += F * lF
    def sim(self, dt):
        self.a = np.array(self.F) / self.m
        self.v += self.a * dt
        self.v *= (0.001**dt)
        self.x, self.y = self.x + self.v[0] * dt, self.y + self.v[1] * dt
        self.eps = self.M / self.J
        self.w += self.eps * dt
        self.w *= (0.001**dt)
        self.ang = self.ang + self.w * dt

if __name__ == "__main__":
    sz, timer, fps = (800, 600), pygame.time.Clock(), 20
    screen, dt = pygame.display.set_mode(sz), 1 / fps
    robot, robot2 = Robot(200, 200), Robot(200, 400)

    obstacle = Bar(400, 300, 0, 200, 150)
    objs = [obstacle]
    bar = Bar(400, 250, 1, 200, 30)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    print("Test")

                robot2.vlin = robot.vlin = 50 if ev.key == pygame.K_w else -50 if ev.key == pygame.K_s else robot.vlin
                robot2.vrot = robot.vrot = -1 if ev.key == pygame.K_a else 1 if ev.key == pygame.K_d else robot.vrot

        for r in [robot, robot2]: r.sim(dt)

        bar.reset()
        for r,k in [[robot,1],[robot2,-1]]:
            pF = bar.local_to_global_pt((k*bar.L / 2, 0))
            delta = np.subtract(r.get_pos(), pF)
            bar.apply_force((k*bar.L / 2, 0), delta * 30)
        bar.sim(dt)

        screen.fill((255, 255, 255))
        for r in [robot, robot2]: r.draw(screen)
        bar.draw(screen)

        draw_text(screen, f"Test = {1}", 5, 5)
        pygame.display.flip(), timer.tick(fps)

# template file by S. Diane, RTU MIREA, 2026
