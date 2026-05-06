import sys, pygame, numpy as np
pygame.font.init()
def draw_text(screen, s, x, y, sz=15, c=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))

SIM_SPEED=5

class Cell: #ячейка
    def __init__(self, ix,iy,x, y, val, sz):
        self.acc, self.vel, self.nbrs_val=0,0,0
        self.ix,self.iy,self.x,self.y,self.sz,self.val,self.new_val = ix, iy, x, y, sz, val, val
        self.color, self.flag, self.str =(255,100,100),False,""
    def get_center(self): return [self.x+self.sz/2,self.y+self.sz/2]
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.sz,self.sz))
        pygame.draw.rect(screen, (0,0,0), (self.x,self.y,self.sz,self.sz), 1)
        draw_text(screen, self.str, self.x, self.y-2, sz=10)
    def sim(self, dt, grid): #CHANGE AS NEEDED
        self.acc=-0.5*(self.val-self.nbrs_val)
        self.vel+=self.acc*dt
        self.val+=self.vel*dt
        v,i=abs(self.val), 0 if self.val>=0 else 2
        self.color=[int(min(255,max(0,v))) for v in np.array((255-v*255,255-v*255,255-v*255))]
        self.color[i]=255

arr=[0.71, 1, 0.71, 1, 0.71, 1, 0.71, 1]
kk = np.array(arr) / sum(arr)

class Grid: #сетка
    def __init__(self, x, y, nx, ny, sz):
        self.x,self.y,self.nx,self.ny = x,y,nx,ny
        self.cells=[[Cell(j,i,x+j*sz, y+i*sz, 0, sz) for j in range(nx)] for i in range(ny)]
        self.nbrhd=[[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
    def draw(self, screen): foo=[c.draw(screen) for row in self. cells for c in row]
    def get_cell(self,ix,iy): return self.cells[iy % self.ny][ix % self.nx]
    def get_val(self,ix,iy): return self.get_cell(ix, iy).val
    def set_val(self,ix,iy,val): self.cells[iy][ix].val=val
    def set_new_val(self,ix,iy,val): self.cells[iy][ix].new_val=val
    def sync(self,ix,iy): self.cells[iy][ix].val=self.cells[iy][ix].new_val
    def get_all_cells(self):
        for row in self.cells:
            for c in row: yield c
    def get_k_nbrs(self, ix, iy):
        for k,(dx,dy) in zip(kk,self.nbrhd):
            if 0<=ix+dx<self.nx and 0<=iy+dy<self.ny:
                yield (k,self.cells[iy+dy][ix+dx])
    def sim(self, dt):#CHANGE AS NEEDED
        for row in self.cells:
            for c in row:
                nbrs=[nb.val*k for k,nb in self.get_k_nbrs(c.ix, c.iy)]
                c.nbrs_val=np.sum(nbrs)
        for row in self.cells:
            for c in row: c.sim(dt, self)

sz = (800, 600)

if __name__ == "__main__":
    screen, timer, fps = pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    dt = 1 / fps

    gr=Grid(50,50,35,35,15)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1: gr.cells[1][2].val=5

        for i in range(SIM_SPEED):
            gr.sim(dt)

        screen.fill((255, 255, 255))
        gr.draw(screen)

        draw_text(screen, f"Press {1}", 5, 5)
        pygame.display.flip(), timer.tick(fps)


# template file by S. Diane, RTU MIREA, 2026
