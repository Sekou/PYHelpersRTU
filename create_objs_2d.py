import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, c=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2)) #расстояние между точками

sz = (800, 600)

OBJ_SZ=20
class Obj: #небольшой объект на экране
    def __init__(self, id, x, y): self.id, self.x, self.y, self.sz = id, x, y, OBJ_SZ
    def get_pos(self): return [self.x, self.y]
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), self.get_pos(), self.sz/2, 2)
        draw_text(screen, f"{self.id}", self.x, self.y+OBJ_SZ//2, 10)

if __name__=="__main__":
    screen, timer, fps =  pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    sim_time, dt = 0, 1 / fps

    objs = []

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_s:
                    pp=[o.get_pos() for o in objs]
                    with open("scene.txt", "w") as f:
                        f.write(str(pp))
                if ev.key == pygame.K_l:
                    with open("scene.txt", "r") as f:
                        pp=eval(f.read())
                        objs = [Obj(i, *p) for i, p in enumerate(pp)]
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    oo = [o for o in objs if dist(o.get_pos(), ev.pos)<OBJ_SZ]
                    if len(oo)==0: objs.append(Obj(len(objs), *ev.pos))

        screen.fill((255, 255, 255))
        for o in objs: o.draw(screen)

        draw_text(screen, f"Num objs = {len(objs)}", 5, 5)
        pygame.display.flip(), timer.tick(fps)
        sim_time+=dt

#template file by S. Diane, RTU MIREA, 2026
