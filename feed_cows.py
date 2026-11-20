#2026, S. Diane, drawing robot and cows in pygame

import sys, pygame, numpy as np, math

def rot(v, ang): return np.dot([[-v[1], v[0]], v],[math.sin(ang), math.cos(ang)]) # поворот вектора на угол
def lim_ang(ang, arc=3.141592653589793): # ограничение угла в пределах +/-pi
    return ang%(2*arc)+2*arc*(int(ang%(2*arc)<-arc)-int(ang%(2*arc)>arc))
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2))
def rot_arr(vv, ang): return [rot(v, ang) for v in vv] # функция для поворота массива на угол
def draw_rot_rect(screen, color, pc, w, h, ang): #рисует повернутый прямоугольник (по точке центра, ширине, высоте и углу)
    pygame.draw.polygon(screen, color, np.add(rot_arr([[-w/2, -h/2], [+w/2, -h/2], [+w/2, +h/2], [-w/2, +h/2]], ang), pc), 2)

# Инициализация Pygame
pygame.init()
# Настройки окна и таймера
WIDTH, HEIGHT = 800, 600
screen, timer, fps = pygame.display.set_mode((WIDTH, HEIGHT)), pygame.time.Clock(), 20
pygame.display.set_caption("Корова на Pygame")

class Robot:
    def __init__(self, x, y, alpha):
        self.x, self.y, self.alpha = x, y, alpha
        self.L, self.W = 70, 40
        self.speed, self.vsteer, self.steer = 0, 0, 0
        self.last_da=0
        self.cargo_pts=[[self.L/4,0], [0,-self.W/4], [0,self.W/4]]
        self.traj=[] #точки траектории
    def get_pos(self): return [self.x, self.y]
    def get_cargo_pts(self): return [np.add(rot(p, self.alpha),self.get_pos()) for p in self.cargo_pts]
    def draw(self, screen, color=(0,0,0)):
        p, dx, dy=np.array(self.get_pos()), self.L/3, self.W/3
        draw_rot_rect(screen, color, p, self.L, self.W, self.alpha)
        dd=rot_arr([[-dx,-dy], [-dx,dy], [dx,-dy], [dx,dy]], self.alpha)
        for d, k in zip(dd, [0,0,1,1]): draw_rot_rect(screen, color, p+d, self.L/5, self.W/5, self.alpha+k*self.steer)
        for i in range(len(self.traj)-1): pygame.draw.line(screen, (0,0,255), self.traj[i], self.traj[i+1], 1)
    def sim(self, dt):
        delta=rot([self.speed*dt, 0], self.alpha)
        self.x, self.y=np.add(self.get_pos(), rot([self.speed*dt, 0], self.alpha))
        self.steer=self.steer+self.vsteer*dt
        self.steer=min(max(-0.7, self.steer), 0.7)
        if self.steer!=0: #велосипедная кинематика
            da = self.speed*dt/(self.L / math.tan(self.steer))
            self.alpha=lim_ang(self.alpha+da)
        if len(self.traj)==0 or dist(self.get_pos(), self.traj[-1])>10:
            self.traj.append(self.get_pos())
    def goto(self, pos, dt, max_steer=1):
        v=np.subtract(pos, self.get_pos())
        da=lim_ang(math.atan2(v[1], v[0]) - self.alpha)
        self.steer += 3 * da * dt - 1.5*self.last_da*dt
        self.last_da=da
        self.steer = min(max_steer, max(-max_steer, self.steer))
        self.speed = 50
    def get_traj_len(self):
        return sum([dist(a,b) for a, b in zip(self.traj[:-1], self.traj[1:])])

def draw_food(screen, x0,y0, sz=35):
    lnln=[
        [[x0-sz/2,y0-sz/2],[x0+sz/2,y0+sz/2]],
        [[x0-sz/2,y0+sz/2],[x0+sz/2,y0-sz/2]],
        [[x0-sz/2,y0-sz/4],[x0+sz/2,y0+sz/4]],
        [[x0-sz/2,y0+sz/4],[x0+sz/2,y0-sz/4]],
        [[x0-sz/3,y0-sz/3],[x0+sz/3,y0-sz/5]],
        [[x0-sz/2,y0+sz/5],[x0+sz/2,y0+sz/3]],
        [[x0-sz/2,y0+sz/10],[x0+sz/2,y0+sz/9]],
        [[x0-sz/10,y0-sz/2],[x0+sz/10,y0+sz/2]]
    ]
    for p1,p2 in lnln: pygame.draw.line(screen, (150,150,0), p1,p2,2)

def draw_cow(screen, x0,y0, sz=200):
    WHITE,BLACK,GRAY = (255, 255, 255), (0, 0, 0), (180, 180, 180)
    E, L, R, w0=pygame.draw.ellipse, pygame.draw.line, pygame.Rect, round(sz/100)+2
    a,b,c,d,e,f=x0-sz*0.3,x0-sz*0.22,x0+sz*0.22,x0+sz*0.3,y0+sz*0.3,y0+sz*0.6
    for v in [a,b,c,d]: L(screen, BLACK, (v, e), (v, f), w0) # 1. Ноги
    L(screen, BLACK, (x0+sz*0.5, y0), (x0+sz*0.6, y0+sz*0.3), w0) # 2. Хвост
    for w, c in zip([0, w0], [GRAY, BLACK]): # 3. Тело
        E(screen, c, R(x0-sz*0.5, y0-sz*0.3, sz, sz*0.7), width=w)
    L(screen, BLACK, (x0-sz*0.61, y0-sz*0.45), (x0-sz*0.57, y0-sz*0.35), w0) # 4. Рога
    L(screen, BLACK, (x0-sz*0.49, y0-sz*0.45), (x0-sz*0.52, y0-sz*0.35), w0)
    head_rect = R(x0-sz*0.76, y0-sz*0.38, sz*0.42, sz*0.32)# 5. Голова
    for w, c in zip([0, w0], [GRAY, BLACK]):# Контур головы
        E(screen, c, R(x0-sz*0.76, y0-sz*0.38, sz*0.42, sz*0.32), width=w)
    E(screen, BLACK, R(x0-sz*0.58, y0-sz*0.3, sz*0.07, sz*0.07)) # 6. Глаз
    for w,c in zip([0,w0],[GRAY, BLACK]): # 7. Ухо
        E(screen, c, R(x0-sz*0.48, y0-sz*0.36, sz*0.13, sz*0.1), width=w)
    for w,c in zip([0,w0],[GRAY, BLACK]):# 8. Нос
        E(screen, c, R(x0-sz*0.78, y0-sz*0.27, sz*0.09, sz*0.14), width=w)
    szsz=[(x0 - sz * 0.2, y0 - sz * 0.2, sz * 0.2, sz * 0.15), # 9. Пятна (овалы)
    (x0 - sz * 0.3, y0 + sz * 0.1, sz * 0.25, sz * 0.2),
    (x0 + sz * 0.2, y0 - sz * 0.1, sz * 0.23, sz * 0.25)]
    for sz in szsz: E(screen, WHITE, R(*sz))

# Основной цикл программы
running = True

robot=Robot(100, 100, 1) # Робот
sim_time, dt = 0, 1 / fps # Время симуляции
cows = [[200, 350], [400, 350], [600, 350]] # Положения коров
food = robot.get_cargo_pts() # Положения порций еды
goals = [[x, y-50] for x,y in cows] + [[700,200]] # Цели движения
ind_goal=-1 # Индекс цели
goal = None # Точка цели

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if goal is not None: robot.goto(goal, dt) # Движение к цели

    if goal is None or dist(robot.get_pos(), goal)<50:
        ind_goal+=1 # Переключение на следующую цель
        if ind_goal<len(goals):goal=goals[ind_goal]
        else: robot.vsteer=robot.speed=0

    if ind_goal < len(goals): # Сброс корма вблизи цели
        for i,(a,b) in enumerate(zip(food, robot.get_cargo_pts())):
            if i>=ind_goal: a[:]=b[:]

    robot.sim(dt) # Симуляция движения робота

    # Заливка фона белым цветом
    screen.fill((255,255,255))
    # Отрисовка коров
    for c in cows: draw_cow(screen, *c, 50)
    robot.draw(screen)

    # Отрисовка целевых точек
    for g in goals: pygame.draw.circle(screen, (0,0,255), g, 3)
    pygame.draw.circle(screen, (0,0,255), goal, 10, 3)

    # Отрисовка порций сена
    for p in food:
        draw_food(screen, *p, 24)

    # Обновление экрана и таймера
    pygame.display.flip(), timer.tick(fps)
    sim_time += dt

pygame.quit()
sys.exit()
