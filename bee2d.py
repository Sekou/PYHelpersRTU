#A function to draw a 2d bee, S. Diane, 2024
import pygame
import math

def draw_bee(screen, x_global, y_global, angle, wing_flap_angle):
    k=180/3.1415926
    wing1_flap_angle=k*(2.2+wing_flap_angle)
    wing2_flap_angle=k*(-2.2-wing_flap_angle)
    # Цвета
    head_color = (230, 180, 0)  # Темно-желтый цвет для головы
    body_color = (255, 220, 0)  # Желтый цвет для тела
    wing_color = (150, 150, 150)  # Светло-серый цвет для крыльев
    detail_color = (0, 0, 0)  # Черный цвет для полос, глаз, хоботка и жала

    # Параметры пчелы
    eye_r = 2
    head_r = 5
    body_width = 30
    body_height = 20
    wing_length = 20
    wing_height = 8
    stripe_width = 3

    sf = pygame.Surface((body_width * 2, body_width*2), pygame.SRCALPHA)
    x,y=body_width, body_width

    # Отрисовка тела пчелы
    pygame.draw.line(sf, detail_color, (x - 1.2*body_width / 2, y), (x + 1.2*(body_width / 2)+head_r, y), 2)
    body_rect = pygame.Rect(x - body_width / 2, y - body_height / 2, body_width, body_height)
    pygame.draw.ellipse(sf, body_color, body_rect)

    # Отрисовка головы пчелы
    head_rect = pygame.Rect(x + body_width / 2 - head_r, y - head_r, head_r*2, head_r*2)
    pygame.draw.ellipse(sf, head_color, head_rect)
    eye_rect1 = pygame.Rect(x + body_width / 2 - eye_r, y - eye_r - head_r/2, eye_r*2, eye_r*2)
    pygame.draw.ellipse(sf, detail_color, eye_rect1)
    eye_rect2 = pygame.Rect(x + body_width / 2 - eye_r, y - eye_r + head_r/2, eye_r*2, eye_r*2)
    pygame.draw.ellipse(sf, detail_color, eye_rect2)

    # Рисуем полосы на теле пчелы
    n_stripes=3
    for i in range(n_stripes):
        stripe_rect = pygame.Rect(
            x - body_width / 2 + ((i+0.8) * (body_width / (n_stripes+1))),
            y - body_height / 2,
            stripe_width,
            body_height
        )
        pygame.draw.rect(sf, detail_color, stripe_rect)

    # Вычисляем координаты крыльев для взмаха
    wing1_center = (x + body_width / 4, y - body_height / 2)
    wing2_center = (x + body_width / 4, y + body_height / 2)

    sf1=pygame.Surface((wing_length*2, wing_height), pygame.SRCALPHA)
    sf2=pygame.Surface((wing_length*2, wing_height), pygame.SRCALPHA)

    # Отрисовка крыльев в виде эллипсов
    pygame.draw.ellipse(sf1, wing_color, (wing_length,0, wing_length, wing_height))
    pygame.draw.ellipse(sf2, wing_color, (wing_length,0, wing_length, wing_height))

    # Поворот крыльев
    wing1 = pygame.transform.rotate(sf1, wing1_flap_angle)
    wing2 = pygame.transform.rotate(sf2, wing2_flap_angle)

    # Отрисовка крыльев с учетом поворота
    sf.blit(wing1, (wing1_center[0] - wing1.get_width() / 2, wing1_center[1] - wing1.get_height() / 2))
    sf.blit(wing2, (wing2_center[0] - wing2.get_width() / 2, wing2_center[1] - wing2.get_height() / 2))

    sf = pygame.transform.rotate(sf, k*angle)
    dx, dy=sf.get_width()/2, sf.get_height()/2

    screen.blit(sf, (x_global-dx, y_global-dy))


# Пример использования
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Отрисовка пчелы")
    clock = pygame.time.Clock()

    running = True
    x, y, a=400, 300, 1
    beta=0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Очистка экрана
        draw_bee(screen, x, y, a, beta)  # Рисуем пчелу
        x+=0.1
        y+=0.1
        a+=0.1
        beta=1-beta
        pygame.display.flip()  # Обновление экрана
        clock.tick(10)  # Ограничение FPS

    pygame.quit()
