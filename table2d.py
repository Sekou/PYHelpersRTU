#2024, S. Diane, table class for pygame

import pygame

class Cell: #ячейка
    def __init__(self, id):
        self.id=id
        self.text = ""
        self.selected = False

class Table: #таблица
    def __init__(self, x0, y0, width, height, nx, ny):
        self.x0,self.y0 =  x0, y0
        self.width,self.height = width, height
        self.nx,self.ny = nx, ny
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 25)
        numCells=nx*ny
        self.cells=[Cell(i) for i in range(numCells)]
    def getIxIy(self, mouseX, mouseY):
        w, h = self.width / self.nx, self.height / self.ny
        iy = (mouseY - self.y0) / h
        ix = (mouseX - self.x0) / w
        return int(ix), int(iy)
    def getCell(self, ix, iy): #объект ячейки
        return self.cells[iy*self.nx+ix]
    def getCellBB(self, ix, iy): #рамка ячейки
        y = round(self.y0 + iy * self.height / self.ny)
        y_ = round(self.y0 + (iy + 1) * self.height / self.ny)
        x = round(self.x0 + ix * self.width / self.nx)
        x_ = round(self.x0 + (ix + 1) * self.width / self.nx)
        return [x, y, x_ - x, y_ - y]
    def getCellCenter(self, ix, iy): #центр ячейки
        bb=self.getCellBB(ix, iy)
        return [bb[0]+0.5*bb[2], bb[1]+0.5*bb[3]]
    def draw(self, screen):
        for iy in range(self.ny):
            for ix in range(self.nx):
                #контур ячейки
                bb = self.getCellBB(ix, iy)
                c=self.cells[iy*self.nx+ix]
                color=(255, 0, 0) if c.selected else (50, 0, 0)
                w=3 if c.selected else 1
                pygame.draw.rect(screen, color, bb, w)
                # текст ячейки
                img = self.font.render(c.text, True, (0, 0, 0))
                r = img.get_rect()
                fsz = self.font.get_linesize()
                r[0] += bb[0] + 0.5*(bb[2]-0.5*fsz*len(c.text))
                r[1] += bb[1] + fsz
                screen.blit(img, r)
