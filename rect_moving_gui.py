import pygame
import sys
import tkinter as tk
from tkinter import simpledialog

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RECT_COLOR = (0, 128, 255)
RECT_WIDTH, RECT_HEIGHT = 100, 50

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Перемещение прямоугольников")

# Класс для прямоугольника
class Rect:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, RECT_WIDTH, RECT_HEIGHT)
        self.text = ""

    def draw(self, surface):
        pygame.draw.rect(surface, RECT_COLOR, self.rect)
        if self.text:
            font = pygame.font.Font(None, 30)
            text_surface = font.render(self.text, True, WHITE)
            surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

# Функция для запроса текста
def ask_for_text():
    root = tk.Tk()
    root.withdraw()  # Скрыть главное окно
    text = simpledialog.askstring("Введите текст", "Текст для прямоугольника:")
    root.destroy()
    return text

clock = pygame.time.Clock()
fps=20

def draw_all(rectangles):
    # Очистка экрана
    screen.fill(WHITE)
    # Рисование прямоугольников
    for rect in rectangles:
        rect.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

# Основная функция
if __name__ == "__main__":
    # Создание списка прямоугольников
    rectangles = [Rect(100, 100), Rect(300, 200), Rect(500, 300)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    for rect in rectangles:
                        if rect.rect.collidepoint(event.pos):
                            mouse_x, mouse_y = event.pos
                            offset_x = rect.rect.x - mouse_x
                            offset_y = rect.rect.y - mouse_y
                            dragging = True

                            # Перемещение прямоугольника
                            while dragging:
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEMOTION:
                                        rect.rect.x = event.pos[0] + offset_x
                                        rect.rect.y = event.pos[1] + offset_y
                                        draw_all(rectangles)
                                    if event.type == pygame.MOUSEBUTTONUP:
                                        if event.button == 1:
                                            dragging = False

                elif event.button == 3:  # Правая кнопка мыши
                    for rect in rectangles:
                        if rect.rect.collidepoint(event.pos):
                            rect.text = ask_for_text()

        draw_all(rectangles)

    pygame.quit()
    sys.exit()
