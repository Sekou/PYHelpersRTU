#2026, S.Diane, drawing a cow in pygame

import sys
import pygame

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Корова на Pygame")

def draw_cow(screen, x0,y0, sz=200):
    WHITE,BLACK,GRAY = (255, 255, 255), (0, 0, 0), (180, 180, 180)
    E, L, R, w0=pygame.draw.ellipse, pygame.draw.line, pygame.Rect, round(sz/100)+2
    a,b,c,d,e,f=x0-sz*0.3,x0-sz*0.22,x0+sz*0.22,x0+sz*0.3,y0+sz*0.3,y0+sz*0.6
    for v in [a,b,c,d]: L(screen, BLACK, (v, e), (v, f), w0)# 1. Ноги
    L(screen, BLACK, (x0+sz*0.5, y0), (x0+sz*0.6, y0+sz*0.3), w0)# 2. Хвост
    for w, c in zip([0, w0], [GRAY, BLACK]): # 3. Тело
        E(screen, c, R(x0-sz*0.5, y0-sz*0.3, sz, sz*0.7), width=w)
    L(screen, BLACK, (x0-sz*0.61, y0-sz*0.45), (x0-sz*0.57, y0-sz*0.35), w0) # 4. Рога
    L(screen, BLACK, (x0-sz*0.49, y0-sz*0.45), (x0-sz*0.52, y0-sz*0.35), w0)
    head_rect = R(x0-sz*0.76, y0-sz*0.38, sz*0.42, sz*0.32)# 5. Голова
    for w, c in zip([0, w0], [GRAY, BLACK]):# Контур головы
        E(screen, c, R(x0-sz*0.76, y0-sz*0.38, sz*0.42, sz*0.32), width=w)
    E(screen, BLACK, R(x0-sz*0.58, y0-sz*0.3, sz*0.07, sz*0.07)) # 6. Глаз
    for w,c in zip([0,w0],[GRAY, BLACK]): # 7. Ухо
        E(screen, c, R(x0-sz*0.48, y0-sz*0.36, sz*0.13, sz*0.1), width=w)
    for w,c in zip([0,w0],[GRAY, BLACK]):# 8. Нос
        E(screen, c, R(x0-sz*0.78, y0-sz*0.27, sz*0.09, sz*0.14), width=w)
    szsz=[(x0 - sz * 0.2, y0 - sz * 0.2, sz * 0.2, sz * 0.15),# 9. Пятна (овалы)
    (x0 - sz * 0.3, y0 + sz * 0.1, sz * 0.25, sz * 0.2),
    (x0 + sz * 0.2, y0 - sz * 0.1, sz * 0.23, sz * 0.25)]
    for sz in szsz: E(screen, WHITE, R(*sz))

# Основной цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Заливка фона белым цветом
    screen.fill((255,255,255))
    draw_cow(screen, 300,200, 50)

    # Обновление экрана
    pygame.display.flip()

pygame.quit()
sys.exit()

#исходная версия сгенерированная Google-AI
def draw_cow0(screen):
    # Цвета (RGB)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (180, 180, 180)
    # 1. Ноги (4 линии) - рисуем первыми, чтобы они были "за" телом
    pygame.draw.line(screen, BLACK, (220, 230), (220, 310), 6)  # Передняя левая
    pygame.draw.line(screen, BLACK, (250, 230), (250, 310), 6)  # Передняя правая
    pygame.draw.line(screen, BLACK, (350, 230), (350, 310), 6)  # Задняя левая
    pygame.draw.line(screen, BLACK, (380, 230), (380, 310), 6)  # Задняя правая
    # 2. Хвост (1 линия)
    pygame.draw.line(screen, BLACK, (395, 180), (440, 240), 4)
    # 3. Тело (1-й овал: x, y, ширина, высота)
    body_rect = pygame.Rect(200, 150, 200, 100)
    pygame.draw.ellipse(screen, GRAY, body_rect)
    pygame.draw.ellipse(screen, BLACK, body_rect, 3)  # Контур тела
    # 4. Рога (2 линии) - рисуем до головы, чтобы крепились к ней
    pygame.draw.line(screen, BROWN, (190, 135), (185, 115), 5)  # Левый рог
    pygame.draw.line(screen, BROWN, (195, 135), (210, 115), 5)  # Правый рог
    # 5. Голова (2-й овал: x, y, ширина, высота)
    head_rect = pygame.Rect(150, 130, 75, 55)
    pygame.draw.ellipse(screen, GRAY, head_rect)
    pygame.draw.ellipse(screen, BLACK, head_rect, 3)  # Контур головы
    # 6. Глаз (1 овал)
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(180, 145, 15, 15))
    # 7. Ухо (1 овал)
    pygame.draw.ellipse(screen, GRAY, pygame.Rect(200, 125, 25, 20))
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(200, 125, 25, 20), 3)
    # 8. Нос (1 овал)
    pygame.draw.ellipse(screen, GRAY, pygame.Rect(145, 150, 20, 20))
    pygame.draw.ellipse(screen, BLACK, pygame.Rect(145, 150, 20, 20), 3)
    # 9. Пятна (овалы)
    pygame.draw.ellipse(screen, WHITE, pygame.Rect(245, 200, 50, 30))
    pygame.draw.ellipse(screen, WHITE, pygame.Rect(275, 160, 40, 25))
    pygame.draw.ellipse(screen, WHITE, pygame.Rect(335, 180, 30, 35))