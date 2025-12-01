import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y, sz=20, color=(0,0,0)): #отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, (0,0,0)), (x,y))
def lim_ang(ang, arc=3.141592653589793): # ограничение угла в пределах +/-pi
    ang=ang%(2*arc); return ang + (2*arc if ang<-arc else -2*arc if ang>arc else 0)

class Robot:
    def __init__(self, x, y):
        self.radius, self.color=20, (0,0,0)
        self.x, self.y, self.a, self.vlin, self.vrot=x,y,0, 0,0
    def get_pos(self): return [self.x, self.y]
    def draw(self, screen):
        p1=np.array(self.get_pos())
        pygame.draw.circle(screen, self.color, p1, self.radius, 2)
        s,c=math.sin(self.a), math.cos(self.a)
        pygame.draw.line(screen, self.color, p1, p1+[self.radius*c, self.radius*s],2)
    def sim(self, dt):
        s,c=math.sin(self.a), math.cos(self.a)
        self.x, self.y=self.x+c*self.vlin*dt, self.y+s*self.vlin*dt
        self.a=lim_ang(self.a+self.vrot*dt)

if __name__=="__main__":
    sz, timer, fps = (800, 600), pygame.time.Clock(), 20
    screen, dt = pygame.display.set_mode(sz), 1 / fps
    robot = Robot(200, 200)

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                robot.vlin = 50 if ev.key == pygame.K_w else -50 if ev.key == pygame.K_s else robot.vlin
                robot.vrot = -1 if ev.key == pygame.K_a else 1 if ev.key == pygame.K_d else robot.vrot

        robot.sim(dt)

        screen.fill((255, 255, 255))
        robot.draw(screen)

        draw_text(screen, f"Test = {1}", 5, 5)
        pygame.display.flip(), timer.tick(fps)

#template file by S. Diane, RTU MIREA, 2024-2025
