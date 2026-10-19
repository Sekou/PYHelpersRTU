import sys, pygame, numpy as np
pygame.font.init()

def draw_text(screen, s, x, y, sz=15, c=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))

sz = (800, 600)

class Mode:
    def __init__(self): self.active, self.finished = False, False
    def on_down(self, p): self.active, self.p0, self.p = True, p, p
    def on_up(self, p): self.active, self.finished, self.p = False, True, p
    def on_move(self, p): self.p = p
    def draw(self, screen): pass

class ModeFree (Mode):
    def __init__(self):
        super().__init__()
        self.active=True
    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), self.p, 3, 2)

class ModeFrameSel (Mode):
    def __init__(self): super().__init__()
    def on_move(self, p): self.p = p
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (0,0,0), [*self.p0, self.p[0]-self.p0[0], self.p[1]-self.p0[1]], 2)

ind=0
mouse_modes=[ModeFree(), ModeFrameSel()]
mouse_mode=mouse_modes[ind]

if __name__ == "__main__":
    screen, timer, fps = pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    dt = 1 / fps

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    ind=(ind+1)%len(mouse_modes)
                    mouse_mode = mouse_modes[ind]
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_mode.on_down(ev.pos)
            if ev.type == pygame.MOUSEBUTTONUP:
                mouse_mode.on_up(ev.pos)
            if ev.type == pygame.MOUSEMOTION:
                mouse_mode.on_move(ev.pos)

        screen.fill((255, 255, 255))
        mouse_mode.draw(screen)

        draw_text(screen, f"Mode = {mouse_mode.__class__.__name__}", 5, 5)
        pygame.display.flip(), timer.tick(fps)

# template file by S. Diane, RTU MIREA, 2026
