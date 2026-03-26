import sys, pygame

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, c=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))

sz = (800, 600)

class Button:
    def __init__(self, name, x, y, w=60, h=30, action=None):
        self.x, self.y, self.w, self.h=x, y, w, h
        self.pressed, self.name, self.action=False, name, action
    def run(self):
        if self.action is not None: self.action()
    def contains(self, x, y):
        return self.x-self.w/2 < x < self.x+self.w/2 and self.y-self.h/2 < y < self.y+self.h/2
    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), [self.x-self.w/2, self.y-self.h/2, self.w, self.h], 2)
        if self.pressed:
            pygame.draw.rect(screen, (200,200,200), [self.x-self.w/2, self.y-self.h/2, self.w, self.h])
        draw_text(screen, self.name, self.x-8*len(self.name)/2, self.y-14/2)

if __name__=="__main__":
    screen, timer, fps =  pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    dt = 1 / fps

    bw = Button("W", 400,200, action=lambda: print("W"))
    bs = Button("S", 400,260, action=lambda: print("S"))
    ba = Button("A", 350,230, action=lambda: print("A"))
    bd = Button("D", 450,230, action=lambda: print("D"))

    bb=[ba, bw, bs, bd]

    while True:
        for b in bb: b.pressed = False
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for b in bb:
                    if b.contains(*ev.pos):
                        b.pressed=not b.pressed
                        b.run()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w: bw.run()
                if ev.key == pygame.K_s: bs.run()
                if ev.key == pygame.K_a: ba.run()
                if ev.key == pygame.K_d: bd.run()

        screen.fill((255, 255, 255))

        for b in bb: b.draw(screen)

        draw_text(screen, f"Test = {1}", 5, 5)
        pygame.display.flip(), timer.tick(fps)

#template file by S. Diane, RTU MIREA, 2026
