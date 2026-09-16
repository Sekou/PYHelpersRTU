#2026, S. Diane, cubes demo 
import pygame, sys  

pygame.init()  
  
def draw_text(screen, s, x, y, sz=15, с=(0, 0, 0)): # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, с), (x, y))

def draw_square(screen, x, y, sz, id):
    pygame.draw.rect(screen, colors[id], [x-sz//2, y-sz//2, sz, sz], 0)
    draw_text(screen, str(ind), x-5, y-5, 20)

screen_width, screen_height = 800, 600  
screen = pygame.display.set_mode((screen_width, screen_height))  
pygame.display.set_caption("Cubes")  
  
running = True  

colors=[(255,0,0),(0,255,0),(0,0,255),
    (130,0,130),(130,130,0),(0,130,130),
    (130,50,50),(50,130,50),(50,50,130)]

cube_inds=[0,1,2,3,4,5,6,7,8]
# inds=[0,2,1,3,4,5]

while running:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()  
            sys.exit()  
  
    screen.fill((255,255, 255))  
    for i, ind in enumerate(cube_inds):
        draw_square(screen, 100+60*i, 300, 50, ind)
    pygame.display.flip()
