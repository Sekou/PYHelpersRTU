import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y):
    screen.blit(pygame.font.SysFont('Comic Sans MS', 20).render(s, True, (0,0,0)), (x,y))

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

def draw_rot_rect(screen, color, pc, w, h, ang): #точка центра, ширина высота прямоуг и угол поворота прямогуольника
    pts = [[- w/2, - h/2],[+ w/2, - h/2],[+ w/2, + h/2],[- w/2, + h/2]]
    pygame.draw.polygon(screen, color, np.add(rotArr(pts, ang), pc), 2)

class Robot:
    def __init__(self, x, y, alpha):
        self.x, self.y = x, y
        self.alpha=alpha
        self.L, self.W = 70, 40
        self.speed, self.steer = 0, 0
        self.traj=[] #точки траектории
        
    def get_pos(self): return [self.x, self.y]
    def clear(self):
        self.traj, self.vals1, self.vals2  = [], [], []

    def draw(self, screen):
        p=np.array(self.get_pos())
        draw_rot_rect(screen, (0,0,0), p, self.L, self.W, self.alpha)
        dx, dy=self.L/3, self.W/3
        dd=rotArr([[-dx,-dy], [-dx,dy], [dx,-dy], [dx,dy]], self.alpha)
        for d, k in zip(dd, [0,0,1,1]):
            draw_rot_rect(screen, (0, 0, 0), p+d,
                        self.L/5, self.W/5, self.alpha+k*self.steer)
        for i in range(len(self.traj)-1):
            pygame.draw.line(screen, (0,0,255), self.traj[i], self.traj[i+1], 1)
    def sim(self, dt):
        self.added_traj_pt = False
        delta=rot([self.speed*dt, 0], self.alpha)
        self.x+=delta[0]
        self.y+=delta[1]
        if self.steer!=0:
            R = self.L/self.steer
            da = self.speed*dt/R
            self.alpha+=da
        if len(self.traj)==0 or dist(self.get_pos(), self.traj[-1])>10:
            self.traj.append(self.get_pos())
            self.added_traj_pt=True

    def goto(self, pos, dt):
        v=np.subtract(pos, self.get_pos())
        aGoal=math.atan2(v[1], v[0])
        da=limAng(aGoal-self.alpha)
        self.steer += 0.5 * da * dt
        maxSteer=1
        if self.steer > maxSteer: self.steer = maxSteer
        if self.steer < -maxSteer: self.steer = -maxSteer
        self.speed = 50

if __name__=="__main__":
    screen, timer, fps = pygame.display.set_mode(sz), pygame.time.Clock(), 20

    robot=Robot(100, 100, 1)

    time=0
    goal = [600,400]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
        dt=1/fps
        screen.fill((255, 255, 255))
        robot.goto(goal, dt)
        robot.sim(dt)
        robot.draw(screen)
        pygame.draw.circle(screen, (255,0,0), goal, 5, 2)
        draw_text(screen, f"Time = {time:.3f}", 5, 5)
       
        pygame.display.flip(), timer.tick(fps)
        time+=dt

#template file by S. Diane, RTU MIREA, 2026
