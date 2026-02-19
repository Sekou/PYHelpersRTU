import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, с=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, с), (x, y))
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2)) #расстояние между точками
def rot(v, ang): return np.dot([[-v[1], v[0]], v],[math.sin(ang), math.cos(ang)]) # поворот вектора на угол
def rot_arr(vv, ang): return [rot(v, ang) for v in vv] # функция для поворота массива на угол
def lim_ang(ang, arc=3.141592653589793): # ограничение угла в пределах +/-pi
    ang=ang%(2*arc); return ang + (2*arc if ang<-arc else -2*arc if ang>arc else 0)
def draw_rot_rect(screen, color, pc, w, h, ang): #точка центра, ширина, высота и угол поворота прямогуольника
    pts = [[- w/2, - h/2],[+ w/2, - h/2],[+ w/2, + h/2],[- w/2, + h/2]]
    pygame.draw.polygon(screen, color, np.add(rot_arr(pts, ang), pc), 2)

sz = (800, 600)

if __name__=="__main__":
    screen, timer, fps =  pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    dt = 1 / fps

    while True:
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    print("Hi")     

        screen.fill((255, 255, 255))     

        draw_text(screen, f"Test = {1}", 5, 5)
        pygame.display.flip(), timer.tick(fps)

#template file by S. Diane, RTU MIREA, 2024-2026
