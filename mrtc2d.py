#Модель мобильного робототехнического комплекса, автор: С.А.К. Диане, 2026
import sys, pygame, numpy as np, math

sz = (800, 600)

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, с=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, с), (x, y))
def rot(v, ang): return np.dot([[-v[1], v[0]], v],[math.sin(ang), math.cos(ang)]) # поворот вектора на угол
def lim_ang(ang): # ограничение угла в пределах +/-pi
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang
def rot_arr(vv, ang): return [rot(v, ang) for v in vv]  # функция для поворота массива на угол
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2))
def draw_rot_rect(screen, color, pc, w, h, ang):  # точка центра, ширина высота прямоуг и угол поворота прямогуольника
    pts = [[- w / 2, - h / 2], [+ w / 2, - h / 2], [+ w / 2, + h / 2], [- w / 2, + h / 2]]
    pygame.draw.polygon(screen, color, np.add(rot_arr(pts, ang), pc), 2)

def mainp_ik_2_link(target, l1, l2, p0, a0, sign=1):
    v=target-np.array(p0) #применяем формулу для решения треугольника
    a2=sign*(math.pi-math.acos( min(1, max(-1, (l1**2+l2**2 - v@v)/2/l1/l2)) ))
    ep=np.add([l1, 0],[l2*math.cos(a2), l2*math.sin(a2)])
    amanip, agoal=math.atan2(ep[1], ep[0])+a0, math.atan2(v[1], v[0])
    return [lim_ang(agoal-amanip), a2]

def ang_to(p1, p2): return math.atan2(p2[1] - p1[1], p2[0] - p1[0]) # угол от 1 точки на 2 точку

class Link:
    def __init__(self, L=20, ang=0, pos=[0, 0]):
        self.pos = pos
        self.L, self.ang = L, ang
        self.min_ang, self.max_ang = -math.pi/2, math.pi/2
        self.global_ang, self.ext_ang = 0, 0
        self.vrot = 1
    def get_end_pos(self):
        a = self.global_ang
        return np.array(self.pos) + [self.L * math.cos(a), self.L * math.sin(a)]
    def sim(self, dt): self.ang = min(self.max_ang, max(self.min_ang, lim_ang(self.ang + self.vrot * dt))) # NEW
    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), self.pos, self.get_end_pos(), 2)
        pygame.draw.circle(screen, (0, 0, 0), self.pos, 2, 2)

class TwoLinkManipulator:
    def __init__(self, pos0, num_links, L0):
        self.pos0 = pos0
        self.links = [Link(L0 / (1 + 0.5*i), 0, pos0) for i in range(2)]
    def sim(self, dt):
        for l in self.links: l.sim(dt)
        self.upd_poses()
    def set_angs(self, aa): #мгновенное движение манипулятора
        for a, l in zip(aa, self.links): l.ang=a
    def goto_angs(self, aa): #плавное движение манипулятора
        for a, l in zip(aa, self.links): l.vrot=10*(a-l.ang)
    def upd_poses(self):
        self.links[0].pos = self.pos0
        self.links[0].global_ang = self.links[0].ext_ang + self.links[0].ang # NEW ext_ang
        for i in range(1, len(self.links)):
            self.links[i].global_ang = lim_ang(self.links[i - 1].global_ang + self.links[i].ang)
            self.links[i].pos = self.links[i - 1].get_end_pos()
    def draw(self, screen):
        for l in self.links: l.draw(screen)
        pygame.draw.circle(screen, (0, 0, 0), self.links[-1].get_end_pos(), 2, 2)
    def get_end_pos(self):
        return self.links[-1].get_end_pos()
    def solve_ik(self, goal, ang0=0):
        sign = 1 if lim_ang(ang_to(self.pos0, goal)-ang0)>0 else -1
        aa=mainp_ik_2_link(goal, *[l.L for l in self.links][:2], self.links[0].pos, self.links[0].ext_ang, sign)
        self.goto_angs(aa)

class Robot:
    def __init__(self, x, y, alpha):
        self.x, self.y = x, y
        self.alpha, self.steer = alpha, 0
        self.L, self.W = 70, 40
        self.speed, self.vsteer = 0, 0
        self.traj = []  # точки траектории
        self.last_da = 0
        self.manip = TwoLinkManipulator(self.get_pos(), 2, 45)
    def get_pos(self): return [self.x, self.y]
    def clear(self): self.traj = []
    def draw(self, screen):
        p = np.array(self.get_pos())
        draw_rot_rect(screen, (0, 0, 0), p, self.L, self.W, self.alpha)
        dx, dy = self.L / 3, self.W / 3
        dd = [[-dx, -dy], [-dx, dy], [dx, -dy], [dx, dy]]
        dd = rot_arr(dd, self.alpha)
        for d, k in zip(dd, [0, 0, 1, 1]):
            draw_rot_rect(screen, (0, 0, 0), p + d, self.L / 5, self.W / 5, self.alpha + k * self.steer)
        for p1,p2 in zip(self.traj[:-1], self.traj[1:]): pygame.draw.line(screen, (0, 0, 255), p1, p2, 1)
        self.manip.draw(screen)
    def sim(self, dt):
        self.addedTrajPt = False
        delta = rot([self.speed * dt, 0], self.alpha)
        self.x, self.y = self.x+delta[0], self.y+delta[1]
        if self.steer != 0:
            R = self.L / self.steer
            da = self.speed * dt / R
            self.alpha += da
        self.steer = min(1, max(-1,self.steer+self.vsteer*dt))
        self.manip.pos0 = self.get_pos()
        self.manip.links[0].ext_ang = self.alpha   # NEW ext_ang !!!
        self.manip.sim(dt)
        if len(self.traj) == 0 or dist(self.get_pos(), self.traj[-1]) > 10:
            self.traj.append(self.get_pos())
            self.addedTrajPt = True
    def goto(self, pos, dt):
        v = np.subtract(pos, self.get_pos())
        da = lim_ang(math.atan2(v[1], v[0]) - self.alpha)
        self.speed, self.vsteer = 50, 10*da + 10*(da-self.last_da)/dt #ПД-регулятор
        self.last_da=da
    def stretch_manip(self, goal): self.manip.solve_ik(goal, self.alpha)
    def stop(self):
        self.speed=self.vsteer=0
        for l in self.manip.links: l.vrot=0

if __name__ == "__main__":
    screen, timer, fps = pygame.display.set_mode(sz), pygame.time.Clock(), 20

    robot = Robot(100, 100, 1)

    time = 0
    goal = [600, 400]

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                goal = ev.pos
        dt = 1 / fps
        screen.fill((255, 255, 255))

        robot.goto(goal, dt)
        robot.stretch_manip(goal)
        robot.sim(dt)

        robot.draw(screen)
        pygame.draw.circle(screen, (255, 0, 0), goal, 5, 2)
        draw_text(screen, f"Time = {time:.3f}", 5, 5)

        pygame.display.flip(), timer.tick(fps)
        time += dt

# template file by S. Diane, RTU MIREA, 2026
