#S. Diane 2026, пример задания параметров с помощью диалогового окна

import pygame
import tkinter as tk
from tkinter import ttk, simpledialog

# Инициализация pygame
pygame.init()

# Размер окна pygame
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Объекты с параметрами")

NAMES = ["A / B", "C / D", "E / F"]

objects = [# Объекты (прямоугольники)
    {'rect': pygame.Rect(100, 100, 80, 50), 'params': [0]*len(NAMES)},
    {'rect': pygame.Rect(300, 200, 100, 60), 'params': [0]*len(NAMES)},
    {'rect': pygame.Rect(500, 350, 120, 70), 'params': [0]*len(NAMES)},
]

def open_trackbar_dialog(params, names): # диалог с трекбарами для задания параметров
    root, tracks, result = tk.Tk(), [], None 
    root.title("Задать параметры"), root.geometry("300x250"), root.resizable(False, False)
    def to_scale_value(val): return int((val + 1) * 50) # Конвертация параметров из диапазона (-1, 1) к (0, 100)
    def from_scale_value(val): return (val / 50) - 1 # Конвертация параметров из диапазона (0, 100) к (-1, 1)
    for prm, name in zip(params, names):# Создание трекбаров
        ttk.Label(root, text=name).pack()
        tracks.append(ttk.Scale(root, from_=0, to=100, orient='horizontal'))
        tracks[-1].set(to_scale_value(prm)), tracks[-1].pack()
    def on_ok(): # Получение значений с трекбаров и преобразование в диапазон (-1, 1)
        nonlocal result
        result = [from_scale_value(tr.get()) for tr in tracks]
        root.destroy()
    def on_cancel(): root.destroy()
    ttk.Button(root, text="OK", command=on_ok).pack(pady=5) # Кнопка OK
    ttk.Button(root, text="Отмена", command=on_cancel).pack() # Кнопка Cancel
    root.mainloop()
    return result

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                # Проверка клика по объектам
                for obj in objects:
                    if obj['rect'].collidepoint(mouse_pos):# Открытие диалога и обновление параметров
                        new_params = open_trackbar_dialog(obj['params'], NAMES)
                        if new_params is not None:
                            obj['params'] = new_params
                        break

        # Отрисовка объектов и их параметров (например, с цветом, основанным на параметрах)
        for obj in objects:
            rect = obj['rect']
            params = obj['params']
            # Можно сделать цвет зависимым от параметров, например
            color = (
                int(127 + 127 * params[0]),  # по оси "A/B"
                int(127 + 127 * params[1]),  # по оси "C/D"
                int(127 + 127 * params[2])   # по оси "E/F"
            )
            pygame.draw.rect(screen, color, rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()



