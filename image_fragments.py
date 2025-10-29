import sys, pygame
import numpy as np

pygame.font.init()
def draw_text(screen, s, x, y, sz=12, с=(100, 200, 100)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, с), (x, y))

W, H = sz = (800, 600)

class Frame:
    def __init__(self, x0, y0, w, h):
        self.x0, self.y0, self.w, self.h=x0, y0, w, h
        self.brightness=0
    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,0), (self.x0, self.y0, self.w, self.h), 2)
    def calc_brightness(self, img):
        self.brightness=0
        iw,ih=img.shape[1],img.shape[0]
        for iy in range(min(self.h, ih-self.y0)):
            for ix in range(min(self.w, iw-self.x0)):
                self.brightness+= np.mean(img[self.y0+iy,self.x0+ix,:])
        self.brightness/=(self.w*self.h*255)
        return self.brightness

def main():
    screen = pygame.display.set_mode(sz)
    pygame.display.set_caption('Histogram Detector')
    timer = pygame.time.Clock()
    fps = 20; dt=1/fps

    surf = pygame.image.load('img.jpg')
    img = pygame.surfarray.array3d(surf)
    img=img.swapaxes(0, 1) #y (1st), x (2nd)
    img_rect = surf.get_rect(topleft=(0, 0))

    frame=Frame(100, 100, 45, 45)

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1: print("test")
            if ev.type == pygame.MOUSEBUTTONDOWN:
                frame.x0, frame.y0 = ev.pos
                frame.calc_brightness(img)

        screen.fill((200, 200, 200))
        screen.blit(surf, img_rect)

        frame.draw(screen)

        draw_text(screen, f"W*H = {W}*{H}", 5, 5)
        draw_text(screen, f"Brightness = {frame.brightness:.2f}", 5, 25)

        pygame.display.flip()
        timer.tick(fps)

main()

#template file by S. Diane, RTU MIREA, 2025
