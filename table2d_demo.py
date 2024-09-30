#2024, S. Diane, table class example for pygame

import sys, pygame
from pygame.locals import*

from table2d import *

def main():
    sz=(800, 600)
    screen = pygame.display.set_mode(sz)
    timer = pygame.time.Clock()
    fps = 20

    width = 400  # ширина таблицы
    height = 300  # высота таблицы
    nx = 7  # число столбцов
    ny = 5  # число строк

    tb=Table(100,100, width,height, nx,ny)
    tb.cells[1*nx+2].text="aaa"
    selCell=None

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                ix, iy=tb.getIxIy(x, y)
                for c in tb.cells: c.selected=False
                selCell=tb.getCell(ix, iy)
                selCell.selected=True
            if event.type == KEYDOWN:
                selCell.text+=event.unicode

        screen.fill((255, 255, 255))
        tb.draw(screen)

        pygame.display.flip()
        timer.tick(fps)

main()