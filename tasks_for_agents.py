#2026, S. Diane
import sys, pygame, numpy as np, math
pygame.font.init()
def draw_text(screen, s, x, y, sz=20, color=(0,0,0)): #отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, (0,0,0)), (x,y))
def lim_ang(ang, arc=3.141592653589793): # ограничение угла в пределах +/-pi
    ang=ang%(2*arc); return ang + (2*arc if ang<-arc else -2*arc if ang>arc else 0)
def ang_to(p1, p2): return math.atan2(p2[1] - p1[1], p2[0] - p1[0]) # угол от 1 точки на 2 точку
def dist(p1, p2): return np.linalg.norm(np.subtract(p2, p1)) # расстояние между точками

class Task: #задача, выполняемая в течение некоторого времени
    def __init__(self, x, y):
        self.name, self.finished=self.__class__.__name__, False
        self.x, self.y=x, y
    def get_pos(self): return [self.x, self.y]
    def run(self, agent, dt):
        agent.vlin=20
        agent.vrot=lim_ang(ang_to(agent.get_pos(), self.get_pos())-agent.a)
        if dist(self.get_pos(), agent.get_pos())<10: self.finished=True
    def draw(self, agent, screen):
        pygame.draw.circle(screen, (200, 200, 0), self.get_pos(), 3, 2)
        pygame.draw.line(screen, (200, 200, 0), agent.get_pos(), self.get_pos(), 1)

class Agent:
    def __init__(self, x, y):
        self.radius, self.color=20, (0,0,0)
        self.x, self.y, self.a, self.vlin, self.vrot=x,y,0, 0,0
        self.task=None
    def get_pos(self): return [self.x, self.y]
    def draw(self, screen):
        p1=np.array(self.get_pos())
        pygame.draw.circle(screen, self.color, p1, self.radius, 2)
        s,c=math.sin(self.a), math.cos(self.a)
        pygame.draw.line(screen, self.color, p1, p1+[self.radius*c, self.radius*s],2)
        if self.task: self.task.draw(self, screen)
    def sim(self, dt):
        if self.task: self.task.run(self, dt)
        s,c=math.sin(self.a), math.cos(self.a)
        self.x, self.y=self.x+c*self.vlin*dt, self.y+s*self.vlin*dt
        self.a=lim_ang(self.a+self.vrot*dt)

if __name__=="__main__":
    sz, timer, fps = (800, 600), pygame.time.Clock(), 20
    screen, dt = pygame.display.set_mode(sz), 1 / fps
    agents = [Agent(200, 200), Agent(300, 400), Agent(400, 250), Agent(350, 300), Agent(450, 250)]
    agent=agents[0]

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                agent.vlin = 50 if ev.key == pygame.K_w else -50 if ev.key == pygame.K_s else agent.vlin
                agent.vrot = -1 if ev.key == pygame.K_a else 1 if ev.key == pygame.K_d else agent.vrot

        for i in range(0, len(agents)):
            if agents[i].task and agents[i].task.finished:
                agents[i].task=None
            if not agents[i].task:
                agents[i].task = Task(np.random.randint(sz[0]), np.random.randint(sz[1]))

        for a in agents: a.sim(dt)

        screen.fill((255, 255, 255))
        for a in agents: a.draw(screen)

        draw_text(screen, f"Test = {1}", 5, 5)
        pygame.display.flip(), timer.tick(fps)

#template file by S. Diane, RTU MIREA, 2024-2026
