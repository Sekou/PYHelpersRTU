import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, c=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2)) #расстояние между точками

sz = (800, 600)

OBJ_SZ=20
class Obj: #небольшой объект на экране
    def __init__(self, id, x, y):
        self.id, self.x, self.y, self.sz = id, x, y, OBJ_SZ
        self.sel=False
        self.next=[]
    def get_pos(self): return [self.x, self.y]
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0) if not self.sel else (255,0,0), self.get_pos(), self.sz/2, 2)
        for o in self.next: pygame.draw.line(screen, (0,0,255), self.get_pos(), o.get_pos(), 2)
        draw_text(screen, f"{self.id}", self.x, self.y+OBJ_SZ//2, 10)

if __name__=="__main__":
    screen, timer, fps =  pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    sim_time, dt = 0, 1 / fps

    objs = []
    sel_objs = []

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_s:
                    pp=[o.get_pos() for o in objs] #координаты узлов
                    ii_lst=[[o.id for o in o.next] for o in objs] #индексы соединений
                    with open("scene.txt", "w") as f:
                        f.write(str([pp,ii_lst]))
                if ev.key == pygame.K_l:
                    with open("scene.txt", "r") as f:
                        pp,ii_lst=eval(f.read()) #координаты узлов, индексы соединений
                        objs = [Obj(i, *p) for i, p in enumerate(pp)]
                        for o,ii in zip(objs,ii_lst): o.next=[objs[i] for i in ii]
            if ev.type == pygame.MOUSEBUTTONDOWN:
                def unsel_all():
                    for o in objs: o.sel=False

                oo = [o for o in objs if dist(o.get_pos(), ev.pos) < OBJ_SZ]
                if pygame.key.get_pressed()[pygame.K_LCTRL] and ev.button == 1:
                    if len(oo):
                        oo[0].sel=True
                        if not oo[0] in sel_objs:
                            sel_objs.append(oo[0])
                            if len(sel_objs)==2 and not sel_objs[1] in sel_objs[0].next:
                                sel_objs[0].next.append(sel_objs[1])
                                unsel_all(), sel_objs.clear()
                elif ev.button == 1:
                    unsel_all()
                    if len(oo)==0: objs.append(Obj(len(objs), *ev.pos))

        screen.fill((255, 255, 255))
        for o in objs: o.draw(screen)

        draw_text(screen, f"Num objs = {len(objs)}", 5, 5)
        pygame.display.flip(), timer.tick(fps)
        sim_time+=dt

#template file by S. Diane, RTU MIREA, 2026
