import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y, sz=20):
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, (0,0,0)), (x,y))

sz = (800, 600)

def rot(v, ang): return np.dot([[-v[1], v[0]], v],[math.sin(ang), math.cos(ang)]) # поворот вектора на угол
def lim_ang(ang, arc=3.141592653589793): # ограничение угла в пределах +/-pi
    return ang%(2*arc)+2*arc*(int(ang%(2*arc)<-arc)-int(ang%(2*arc)>arc))
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2))
def rot_arr(vv, ang): return [rot(v, ang) for v in vv] # функция для поворота массива на угол
def draw_rot_rect(screen, color, pc, w, h, ang): #рисует повернутый прямоугольник (по точке центра, ширине, высоте и углу)
    pygame.draw.polygon(screen, color, np.add(rot_arr([[-w/2, -h/2], [+w/2, -h/2], [+w/2, +h/2], [-w/2, +h/2]], ang), pc), 2)

class Robot:
    def __init__(self, x, y, alpha):
        self.x, self.y, self.alpha = x, y, alpha
        self.L, self.W = 70, 40
        self.speed, self.vsteer, self.steer = 0, 0, 0
        self.traj=[] #точки траектории
        self.info, self.info2="", ""
    def get_pos(self): return [self.x, self.y]
    def clear(self): self.traj, self.info, self.info2  = [], "", ""
    def draw(self, screen, color=(0,0,0)):
        p, dx, dy=np.array(self.get_pos()), self.L/3, self.W/3
        draw_rot_rect(screen, color, p, self.L, self.W, self.alpha)
        dd=rot_arr([[-dx,-dy], [-dx,dy], [dx,-dy], [dx,dy]], self.alpha)
        for d, k in zip(dd, [0,0,1,1]): draw_rot_rect(screen, color, p+d, self.L/5, self.W/5, self.alpha+k*self.steer)
        for i in range(len(self.traj)-1): pygame.draw.line(screen, (0,0,255), self.traj[i], self.traj[i+1], 1)
        for i,s in enumerate([self.info, self.info2]): draw_text(screen, s, self.x, self.y-50+100*i, 12)
    def sim(self, dt):
        delta=rot([self.speed*dt, 0], self.alpha)
        self.x, self.y=self.x+delta[0], self.y+delta[1]
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
        self.steer += 0.5 * da * dt
        self.steer = min(max_steer, max(-max_steer, self.steer))
        self.speed = 50
    def get_traj_len(self):
        return sum([dist(a,b) for a, b in zip(self.traj[:-1], self.traj[1:])])

if __name__=="__main__":
    screen, timer, fps = pygame.display.set_mode(sz), pygame.time.Clock(), 20

    robot=Robot(100, 100, 1)

    sim_time, dt=0,1/fps
    goal = [600,400]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
        screen.fill((255, 255, 255))
        robot.goto(goal, dt)
        robot.sim(dt)
        robot.draw(screen)
        pygame.draw.circle(screen, (255,0,0), goal, 5, 2)
        draw_text(screen, f"Time = {sim_time:.3f}", 5, 5)
       
        pygame.display.flip(), timer.tick(fps)
        sim_time+=dt

#template file by S. Diane, RTU MIREA, 2024-2026
