import pygame, sys, math, numpy as np
pygame.init()

WIDTH, HEIGHT = 800, 600 # Размеры окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Интерактивный график f(x)")

# Цвета и смещение осей
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
POINT_COLOR, LINE_COLOR = (255, 0, 0), (0, 0, 255)
X0_PIX, Y0_PIX, SCALEX, SCALEY, DW, DH, STEP, CX, CY=400, 300, 0.5, 0.5, 700, 500, 50, True, True
def r2i(x,y): return [X0_PIX + x*SCALEX, Y0_PIX - y*SCALEY]
def i2r(x,y): return [(x-X0_PIX)/SCALEX, (Y0_PIX - y)/SCALEY]

# Начальные точки (пример)
points = [[100, 500], [200, 300], [300, 400], [400, 200], [500, 350], [600, 250], [700, 400]]

def adjust_scale(k=1):
    global SCALEX, SCALEY, DW, DH
    pp = np.array(points)
    DW, DH=max([abs(x) for x in pp[:,0]]), max([abs(y) for y in pp[:,1]])
    SCALEX, SCALEY=WIDTH/DW*0.45*k, HEIGHT/DH*0.45*k

# Параметры выделения точки
pt = None
pt_radius = 8 # расстояние для выбора точки мышью

def draw_text(screen, s, x, y, sz=15, с=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, с), (x, y))

def draw_grid(screen, szx=600, szy=400, stepx=50, stepy=50, c = (200,200,200)): #отрисовка сетки
    for iy in np.arange(0, szy+stepy/2, stepy): pygame.draw.line(screen, c, r2i(0, 0+iy), r2i(0+szx, 0+iy), 1)
    for ix in np.arange(0, szx+stepx/2, stepx): pygame.draw.line(screen, c, r2i(0+ix, 0), r2i(0+ix, 0+szy), 1)

def draw_arrow2(screen, color, p0, p1, w): #отрисовка стрелки по 2 точкам
    angle=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
    p2 = [p1[0] - 10 * math.cos(angle + 0.5), p1[1] - 10 * math.sin(angle + 0.5)]
    p3 = [p1[0] - 10 * math.cos(angle - 0.5), p1[1] - 10 * math.sin(angle - 0.5)]
    for a,b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)

mouse_pos=[0,0]
def draw(points_):
    screen.fill(WHITE)
    for A, B in ([r2i(-DW*int(CX), 0),r2i(DW, 0)], [r2i(0, -DH*int(CY)), r2i(0, DH)]):
        draw_arrow2(screen, (0, 0, 0), A, B, 2) #оси
    for b,(d1,d2) in zip([True, CY, CX, CX and CY], [[1,1],[1,-1],[-1,1],[-1,-1]]):
        if b: draw_grid(screen, d1*DW, d2*DH, d1*STEP, d2*STEP) #сетка
    if len(points_) > 1: pygame.draw.lines(screen, LINE_COLOR, False, points_, 2) #линия
    for p in points_: pygame.draw.circle(screen, POINT_COLOR, p, pt_radius) #точки
    pygame.draw.circle(screen, (200,200,200), mouse_pos, pt_radius) #мышь
    m1, m2=mouse_pos, i2r(*mouse_pos)
    strings=[f"Ranges = {DW:.2f}, {DH:.2f}",
             f"Mouse = {m1[0]:.0f}, {m1[1]:.0f} px",
             f"Point = {m2[0]:.2f}, {m2[1]:.2f}"]
    draw_text(screen, "; ".join(strings), 5, 5)
    pygame.display.flip()
    clock.tick(fps)

def get_ind_point_under(points_, mouse_pos):
    for i, point in enumerate(points_):
        dx, dy = point[0] - mouse_pos[0], point[1] - mouse_pos[1]
        if (dx ** 2 + dy ** 2) ** 0.5 <= pt_radius: return i
    return -1

def dist(p1, p2): #расстояние между точками
    return np.linalg.norm(np.subtract(p2, p1))

def pt_segm_dist2(p, p1, p2): #расстояние от точки до ограниченного отрезка
    dx, dy = np.subtract(p2, p1); k = dy / (0.0000001 if dx==0 else dx)
    d = np.abs(k * (p1[0]-p[0]) - p1[1] + p[1]) / math.sqrt(k * k + 1) # числитель: p[1]-(k*p[0]+b)
    pr=np.subtract(p,p1)@np.subtract(p2,p1)/((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    return (d, 0) if 0<pr<1 else (min(dist(p, p1), dist(p, p2)), np.sign(pr))

def get_insert_ind(points_, mouse_pos): #поиск отрезка для вставки новой точки
    dd=[100500, dist(mouse_pos, points_[0]), dist(mouse_pos, points_[-1])]
    ii, nmax=[0,-1,len(points_)], len(points_)-2
    for i, (p1, p2) in enumerate(zip(points_[:-1], points_[1:])):
        d,f=pt_segm_dist2(mouse_pos, p1, p2)
        b = (f==0 or 0<i<nmax) or (d<dd[1] and i==0 and f<0 or d<dd[2] and i==nmax and f>0)
        if b and d<dd[0]: dd[0], ii[0]=d,i
    return ii[np.argmin(dd)]

if __name__ == "__main__":
    clock = pygame.time.Clock()
    fps = 20

    while True:
        points_ = [r2i(*p) for p in points]
        draw(points_)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    X0_PIX, Y0_PIX, STEP, CX, CY=25, 570, 50, False, False
                    adjust_scale(2)
                if ev.key == pygame.K_2:
                    X0_PIX, Y0_PIX, STEP, CX, CY=400, 300, 50, True, True
                    adjust_scale()
                if ev.key == pygame.K_s:
                    with open("points.txt", "w") as f: f.write(str(points))
                if ev.key == pygame.K_l:
                    with open("points.txt", "r") as f: points=eval(f.read())
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:  # ЛКМ
                mouse_pos = pygame.mouse.get_pos()
                i = get_ind_point_under(points_, mouse_pos)
                pt=points[i] if i>=0 else None
                while pt is not None:
                    for ev in pygame.event.get():
                        if ev.type == pygame.MOUSEMOTION:# Перетаскиваем выбранную точку
                            mouse_pos = pygame.mouse.get_pos()
                            points_[i], points[i] = mouse_pos, i2r(*mouse_pos)
                            draw(points_)
                        elif ev.type == pygame.MOUSEBUTTONUP:
                            if ev.button == 1: pt = None
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 3:  # ПКМ
                mouse_pos = pygame.mouse.get_pos()
                i = get_ind_point_under(points_, mouse_pos)
                if pygame.key.get_pressed()[pygame.K_LSHIFT] and i >= 0: points=points[:i]+points[i+1:]
                else:
                    i=get_insert_ind(points_, mouse_pos)
                    i2=min(i+1, len(points_)) if i>=0 else 0
                    points=points[:i2]+[i2r(*mouse_pos)]+points[i2:]

#template file by S. Diane, RTU MIREA, 2025
