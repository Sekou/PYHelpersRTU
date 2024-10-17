#2024, S. Diane, trackbar class example for pygame

import pygame
import sys
import trackbar

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 20)
def drawText(screen, s, x, y):
    surf=font.render(s, True, (0,0,0))
    screen.blit(surf, (x,y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    timer = pygame.time.Clock()

    # Создаем экземпляр Trackbar
    tb = trackbar.Trackbar(x=100, y=100, width=200, height=20,
                           min_value=0, max_value=100, initial_value=50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            tb.handle_event(event)

        screen.fill((255, 255, 255))
        tb.draw(screen)        # Рисуем ползунок
        drawText(screen, f"Value = {tb.value}", 5, 5)


        pygame.display.flip()
        timer.tick(60)

if __name__ == "__main__":
    main()