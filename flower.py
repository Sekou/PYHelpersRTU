#S. Diane, flower draw function, 2024

import pygame
import sys
import math

def draw_flower(surface, x, y, petal_color, center_color):
    # Количество лепестков
    num_petals = 7
    petal_r=10

    # Рисуем лепестки
    for i in range(num_petals):
        angle = i * (360 / num_petals)  # Угол лепестка
        rad = math.radians(angle)  # Переводим в радианы
        # Вычисляем позицию лепестка
        petal_x = x + petal_r * math.cos(rad)  # x-координата
        petal_y = y + petal_r * math.sin(rad)  # y-координата
        # Рисуем лепесток
        pygame.draw.circle(surface, petal_color,
                           [petal_x, petal_y], petal_r/2)
    # Рисуем центр цветка (круг)
    pygame.draw.circle(surface, center_color, (x, y), petal_r*0.7)

if __name__ == "__main__":
    # Инициализация Pygame
    pygame.init()

    # Установим размеры окна
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        WHITE = (255, 255, 255)
        YELLOW = (255, 255, 0)
        PINK = (255, 182, 193)

        # Заполняем экран белым цветом
        screen.fill(WHITE)

        # Рисуем цветок в центре экрана
        draw_flower(screen, width // 2, height // 2, PINK, YELLOW)

        # Обновляем экран
        pygame.display.flip()


