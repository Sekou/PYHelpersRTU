import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, c=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))

sz = (800, 600)

class Cell:  # ячейка
    def __init__(self, id, ix, iy, x, y, w, h):
        self.id, self.ix, self.iy, self.x, self.y, self.w, self.h = id, ix, iy, x, y, w, h
        self.text, self.val, self.selected = "", 0, False
    def get_pos(self): return [self.x, self.y]
    def get_bb(self): return [self.x, self.y, self.w, self.h] # рамка ячейки
    def get_center(self): return [self.x + 0.5 * self.w, self.y + 0.5 * self.h] # центр ячейки
    def draw(self, screen):
        color = (255, 0, 0) if self.selected else (50, 0, 0)  # контур ячейки
        pygame.draw.rect(screen, color, self.get_bb(), (3 if self.selected else 1))
        p = self.get_center()  # точка для вывода текста ячейки
        if len(self.text): draw_text(screen, self.text, p[0] - 4*len(self.text), p[1] - 20, sz=12)
        draw_text(screen, f"{self.val:.2f}", p[0] - 20, p[1] - 10, sz=12, c=(255, 0, 0))

class Table: # таблица
    def __init__(self, x0, y0, width, height, nx, ny):
        self.x0,self.y0,self.width,self.height,self.nx,self.ny =  x0, y0,width, height,nx, ny
        n, w, h = nx*ny, self.width / self.nx, self.height / self.ny
        self.cells=[Cell(i, i%nx, i//nx, self.x0+(i%nx)*w, self.y0+(i//nx)*h, w, h) for i in range(n)]
    def get_ix_iy(self, x_px, y_px):
        return math.floor((x_px - self.x0) / (self.width / self.nx)), math.floor((y_px - self.y0) / (self.height / self.ny))
    def get_cell(self, ix, iy): #объект ячейки
        return None if (ix<0 or ix>=self.nx or iy<0 or iy>=self.ny) else self.cells[iy*self.nx+ix]
    def draw(self, screen):
        return [self.cells[iy*self.nx+ix].draw(screen) for iy in range(self.ny) for ix in range(self.nx)]
    def get_neighbourhood(self, ix, iy):
        for dy,dx in zip([-1,-1,-1,0,0,0,1,1,1],[-1,0,1]*3):
            if dy==0 and dx==0: continue
            if (c2:=self.get_cell(ix+dx, iy+dy)) is not None: yield c2

if __name__=="__main__":
    screen, timer, fps =  pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Table 2D')
    dt = 1 / fps

    tb=Table(x0=100,y0=100, width=400, height=300, nx=7, ny=5)
    tb.get_cell(2,2).text="x"
    sel_cell=None

    for i,c in enumerate(tb.get_neighbourhood(2,2)):
        c.text=f"text {i}"
        c.val=i

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1: print("test")
                else: sel_cell.text += ev.unicode
            if ev.type == pygame.MOUSEBUTTONDOWN:
                ix, iy = tb.get_ix_iy(*ev.pos)
                for c in tb.cells: c.selected = False
                sel_cell = tb.get_cell(ix, iy)
                if sel_cell is not None: sel_cell.selected = True

        screen.fill((255, 255, 255))
        tb.draw(screen)

        draw_text(screen, f"Test = {1}", 5, 5)
        pygame.display.flip(), timer.tick(fps)

#template file by S. Diane, RTU MIREA, 2024-2026
