import pygame
import os
import sys

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Menu Example")

# Цвета
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Папка с файлами
FILES_FOLDER = "files"

# Получение списка файлов
def get_files():
    try:
        return [f for f in os.listdir(FILES_FOLDER) if os.path.isfile(os.path.join(FILES_FOLDER, f))]
    except FileNotFoundError:
        return []

# Отрисовка текста
font = pygame.font.SysFont(None, 24)

def draw_text(text, position, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, position)

# Меню
class Menu:
    def __init__(self, options, position):
        self.options = options
        self.position = position  # (x, y)
        self.item_height = 30
        self.width = 200
        self.visible = True

    def draw(self):
        if not self.visible:
            return
        x, y = self.position
        # Рисуем фон меню
        pygame.draw.rect(screen, GRAY, (x, y, self.width, self.item_height * len(self.options)))
        # Рисуем пункты меню
        for i, option in enumerate(self.options):
            option_rect = pygame.Rect(x, y + i * self.item_height, self.width, self.item_height)
            pygame.draw.rect(screen, WHITE, option_rect, 1)
            draw_text(option, (x + 5, y + i * self.item_height + 5))
        # Можно добавить выделение выбранного пункта при наведении мышью

    def get_option_at_pos(self, pos):
        x, y = self.position
        px, py = pos
        if (x <= px <= x + self.width) and (y <= py <= y + self.item_height * len(self.options)):
            index = (py - y) // self.item_height
            return self.options[int(index)]
        return None

# Основной цикл
clock = pygame.time.Clock()
menu = None
file_content = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Правая кнопка мыши
                # Открываем меню по позиции мыши
                files = get_files()
                if files:
                    menu = Menu(files, event.pos)
                else:
                    menu = None

            elif event.button == 1:  # Левый клик для выбора пункта меню
                if menu and menu.visible:
                    option = menu.get_option_at_pos(event.pos)
                    if option:
                        # Обработка выбора файла
                        filepath = os.path.join(FILES_FOLDER, option)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        print(f"Загружен файл: {option}")
                        # Можно обработать содержимое файла по своему усмотрению
                    # Скрываем меню после выбора
                    menu.visible = False

    # Очистка экрана
    screen.fill(WHITE)

    # Можно вывести содержимое файла на экран
    if file_content:
        lines = file_content.splitlines()
        for i, line in enumerate(lines[:20]):  # Ограничение по количеству строк
            draw_text(line, (10, 10 + i * 25))

    # Отрисовка меню
    if menu and menu.visible:
        menu.draw()

    pygame.display.flip()
    clock.tick(60)
