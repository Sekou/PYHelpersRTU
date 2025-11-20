#S. Diane, flowers and trees draw functions, 2024 - 2025

import pygame, sys, math, numpy as np

class Tree: #Ель
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color=(0,125,0)
    def get_pos(self):
        return [self.x, self.y]
    def draw(self, screen):
        p1 = np.array(self.get_pos())
        p2 = p1+[0,-35]
        pygame.draw.line(screen, self.color, p1, p2, 2)
        self.draw_branch(screen, p2, 10, 0.7, 0)
        self.draw_branch(screen, p2, 15, 0.7, 8)
        self.draw_branch(screen, p2, 20, 0.7, 16)
        self.draw_branch(screen, p2, 10, -0.7+math.pi, 0)
        self.draw_branch(screen, p2, 15, -0.7+math.pi, 8)
        self.draw_branch(screen, p2, 20, -0.7+math.pi, 16)
    def draw_branch(self, screen, p2, l, a, dy):
        s, c = math.sin(a), math.cos(a)
        pygame.draw.line(screen, self.color, p2+[0,dy], p2+[l*c, l*s+dy], 2)

class Tree2: #Дуб
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color=(0,125,0)
    def get_pos(self):
        return [self.x, self.y]
    def draw(self, screen):
        p1 = np.array(self.get_pos())
        p2 = p1 + [0, -35]
        pygame.draw.line(screen, self.color, p1, p2, 2)
        pp = [[0,-14], [-6,-12], [-7,-9], [-10,-7], [-12,-2], [-9,2], [-12,6], [-13,11],
              [-6,15], [6,16], [12,13], [13,7], [9,4], [11,0], [10,-7], [7,-9], [6,-12]]
        pygame.draw.polygon(screen, (0, 150, 0), p1*0.2+p2*0.8+pp, 2)

class Tree3: #Береза
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color=(0,125,0)
    def get_pos(self):
        return [self.x, self.y]
    def draw(self, screen):
        p1 = np.array(self.get_pos())
        p2 = p1+[0,-25]
        p3 = p1+[0,-35]
        pygame.draw.line(screen, self.color, p1, p3, 2)
        pygame.draw.circle(screen, self.color, p3, 3, 2)
        self.draw_branch(screen, p2, 10, -0.7, 0)
        self.draw_branch(screen, p2, 15, -0.7, 8)
        self.draw_branch(screen, p2, 15, -0.7, 16)
        self.draw_branch(screen, p2, 10, 0.7+math.pi, 0)
        self.draw_branch(screen, p2, 15, 0.7+math.pi, 8)
        self.draw_branch(screen, p2, 15, 0.7+math.pi, 16)
    def draw_branch(self, screen, p2, l, a, dy):
        s, c = math.sin(a), math.cos(a)
        p3 = p2+[0,dy]
        p4 = p3+[l/2*c, l/2*s]
        p5 = p3+[l*c, l*s]
        pygame.draw.line(screen, self.color, p3, p5, 2)
        pygame.draw.circle(screen, self.color, p4, 3, 2)
        pygame.draw.circle(screen, self.color, p5, 3, 2)

class House:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color=(50,50,0)
        self.sz=45
    def get_pos(self):
        return [self.x, self.y]
    def draw_sq(self, screen, p, sz):
        pp=[[-sz/2, 0],[+sz/2, 0],[+sz/2, -sz], [-sz/2, -sz]]
        pygame.draw.polygon(screen, (0, 150, 0), p+pp, 2)
    def draw_roof(self, screen, p, sz):
        pp = [[+sz / 2, -sz], [-sz / 2, -sz], [0, -1.5 * sz]]
        pygame.draw.polygon(screen, (0, 150, 0), p+pp, 2)
    def draw(self, screen):
        p=np.array(self.get_pos())
        self.draw_sq(screen, p, self.sz)
        self.draw_sq(screen, p+[0,-self.sz//4], self.sz//2)
        self.draw_roof(screen, p, self.sz)
        pygame.draw.line(screen, (0, 150, 0), p+[0, -self.sz//4], p+[0, -3*self.sz//4], 2)
        pygame.draw.line(screen, (0, 150, 0), p+[-self.sz//4, -self.sz//2], p+[self.sz//4, -self.sz//2], 2)

class Flower:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.petal_color = (255, 182, 193)
        self.center_color = (255, 255, 0)
        self.num_petals = 7
        self.petal_r = 10
    def get_pos(self):
        return [self.x, self.y]
    def draw(self, screen):
        # Рисуем лепестки
        for i in range(self.num_petals):
            angle = i * (360 / self.num_petals)  # Угол лепестка
            rad = math.radians(angle)  # Переводим в радианы
            # Вычисляем позицию лепестка
            petal_x = self.x + self.petal_r * math.cos(rad)  # x-координата
            petal_y = self.y + self.petal_r * math.sin(rad)  # y-координата
            # Рисуем лепесток
            pygame.draw.circle(screen, self.petal_color,
                               [petal_x, petal_y], self.petal_r / 2)
        # Рисуем центр цветка (круг)
        pygame.draw.circle(screen, self.center_color, (self.x, self.y), self.petal_r * 0.7)

if __name__ == "__main__":
    # Инициализация Pygame
    pygame.init()

    # Установим размеры окна
    screen = pygame.display.set_mode((800, 600))

    f=Flower(200, 200)
    t=Tree(300, 250)
    t2=Tree2(400, 350)
    h=House(400, 200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Заполняем экран белым цветом
        screen.fill((255, 255, 255))

        # Рисуем объекты
        f.draw(screen)
        t.draw(screen)
        t2.draw(screen)
        h.draw(screen)

        # Обновляем экран
        pygame.display.flip()



