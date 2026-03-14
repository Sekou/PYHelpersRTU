import pygame, numpy as np

def flatten(l): return [item for sublist in l for item in sublist]

class Cell:
    def __init__(self, x, y, val, sz):
        self.x,self.y,self.sz,self.val,self.new_val= x, y, sz, val, val
        self.color, self.flag, self.str =(255,100,100),False,""
    def get_center(self): return [self.x+self.sz/2,self.y+self.sz/2]
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.sz,self.sz))
        pygame.draw.rect(screen, (0,0,0), (self.x,self.y,self.sz,self.sz), 1)

class Grid:
    def __init__(self, x, y, nx, ny, sz):
        self.x,self.y,self.nx,self.ny = x,y,nx,ny
        self.cells=[[Cell(x+j*sz, y+i*sz, 0, sz) for j in range(nx)] for i in range(ny)]
    def draw(self, screen): foo=[c.draw(screen) for c in flatten(self.cells)]
    def get_cell(self,x,y): return self.cells[y % self.ny][x % self.nx]
    def get_val(self,x,y): return self.get_cell(x, y).val
    def set_val(self,x,y,val): self.cells[y][x].val=val
    def set_new_val(self,x,y,val): self.cells[y][x].new_val=val
    def sync(self,x,y): self.cells[y][x].val=self.cells[y][x].new_val

# template file by S. Diane, RTU MIREA, 2026
