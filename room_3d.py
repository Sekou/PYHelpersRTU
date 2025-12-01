# Demonstration of a camera flying in a 3D room, S. Diane, 2023-2025
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from math import sin, cos, tan

class Camera:
    x, y, z = 0, 0, 0  # pose params
    yaw, pitch, roll = 0, 0, 0
    coords = [0] * 6
    hFOV = 45  # inner params
    hRes, vRes = 800, 600
    nearZ, farZ = 0.1, 50
    kPI, author = np.pi / 180, "S. Diane, 2025"
    swapCS = np.array([[0, -1, 0, 0], [0, 0, 1, 0], [-1, 0, 0, 0], [0, 0, 0, 1]])
    def save_pos(self): self.coords = self.x, self.y, self.z, self.yaw, self.pitch, self.roll
    def restore_pos(self): self.x, self.y, self.z, self.yaw, self.pitch, self.roll = self.coords
    def move_local(self, dx, dy, dz):
        M = self.calc_view_matrix()[:3, :3]
        M_ = np.linalg.inv(M)
        dx, dy, dz = M_ @ [dx, dy, dz]
        self.x, self.y, self.z = self.x+dx, self.y+dy, self.z+dz
    def calc_proj_matrix(self):
        ar, tn = self.hRes / self.vRes, tan(self.hFOV * self.kPI / 2)
        d1, d2 = self.nearZ - self.farZ, self.nearZ + self.farZ
        A, B, C, D = 1 / ar / tn, 1 / tn, d2 / d1, 2 * self.farZ * self.nearZ / d1
        mproj = np.array([[A, 0, 0, 0], [0, B, 0, 0], [0, 0, C, D], [0, 0, -1, 0]])
        return mproj
    def calc_view_matrix(self, swap_axes=True):
        # positive world shift -> negative camera shift
        X, Y, Z = -self.x, -self.y, -self.z
        y, p, r = -self.yaw * self.kPI, -self.pitch * self.kPI, -self.roll * self.kPI
        # calc rotation matricies
        cr, cp, cy = cos(r), cos(p), cos(y)
        sr, sp, sy = sin(r), sin(p), sin(y)
        myaw = [[cy, -sy, 0, 0], [sy, cy, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # z
        mpit = [[cp, 0, sp, 0], [0, 1, 0, 0], [-sp, 0, cp, 0], [0, 0, 0, 1]]  # y
        mrol = [[1, 0, 0, 0], [0, cr, -sr, 0], [0, sr, cr, 0], [0, 0, 0, 1]]  # x
        # calc full view transformation
        mshift = [[1, 0, 0, X], [0, 1, 0, Y], [0, 0, 1, Z], [0, 0, 0, 1]]
        camMatrix = np.array(mpit) @ mrol @ myaw @ mshift
        return self.swapCS @ camMatrix if swap_axes else camMatrix
    def calc_screen_matrix(self, swap_y=True):
        k = -1 if swap_y else 1
        return np.array([[0.5 * self.hRes, 0, 0, 0.5 * self.hRes],
                         [0, 0.5 * self.vRes, 0, k * 0.5 * self.vRes],
                         [0, 0, 1, 0], [0, 0, 0, 1]])
    def transf_DC_to_screen(self, pDC):
        return (self.calc_screen_matrix() @ (pDC / pDC[-1]))[:2]  # x, y for a pixel
    def transf_pts_from_world_to_screen(self, pts, M=None):
        if M is None: M = self.calc_proj_matrix() @ self.calc_view_matrix()
        return [tuple(self.transf_DC_to_screen(M @ [p[0], p[1], p[2], 1])) for p in pts]
    def get_info(self):
        return f"x {self.x:.2f}, y {self.y:.2f}, z {self.z:.2f}," \
               f" rl {self.roll:.2f}, pt {self.pitch:.2f}, yw {self.yaw:.2f}"
    def draw_world_axes(self):
        for v in np.array([(1, 0, 0), (0, 1, 0), (0, 0, 1)]):
            glColor(v), glBegin(GL_LINES), glVertex3fv((0, 0, 0)), glVertex3fv(v), glEnd()
    def draw_world_axes_ortho_2d(self, sz=20, x0y0=(30,30)): #requires: glOrtho(0, display[0], 0, display[1], -1, 1)
        vv_global=cc=[(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        MV=self.calc_view_matrix()[:3,:3]
        pp, p0=[(MV@v)[:2] for v in vv_global], (MV@[0, 0, 0])[:2]
        for c, p in zip(cc, pp):
            glColor(c), glBegin(GL_LINES), glVertex2fv(x0y0), glVertex2fv(sz*p+x0y0), glEnd()
    def draw_cam_axes_ortho_2d(self, sz=20, x0y0=(30,30)): #requires: glOrtho(0, display[0], 0, display[1], -1, 1)
        vv_local=cc=[(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        vv_global = self.swapCS[:3,:3]@vv_local
        MV=self.calc_view_matrix()[:3,:3]
        pp, p0=[(MV@v)[:2] for v in vv_global], (MV@[0, 0, 0])[:2]
        for c, p in zip(cc, pp):
            glColor(c), glBegin(GL_LINES), glVertex2fv(x0y0), glVertex2fv(sz*p+x0y0), glEnd()

#Camera navigation in simple 3D scene, 2023-2025, S. Diane
import pygame

def show_mat(mat, prec=5): return str([[round(x, prec) for x in r] for r in mat])

LIGHT_POS=[0, 0, 2.5]
def enable_light():
    glEnable(GL_LIGHTING), glEnable(GL_LIGHT0), glEnable(GL_COLOR_MATERIAL)
    glLight(GL_LIGHT0, GL_POSITION, (*LIGHT_POS, 1))  # point light from the left, top, front
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1))

def disable_light():
    glDisable(GL_LIGHTING), glDisable(GL_LIGHT0), glDisable(GL_COLOR_MATERIAL)

def set_material(diffuse, specular, shininess):
    # Установка материала
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

# Функция для рисования 4-угольника по индексам вершин
def draw_quad(verts, verts_idx):
    glBegin(GL_QUADS)
    for idx in verts_idx: glVertex3fv(verts[idx])
    glEnd()

# Функция для рисования полигона по индексам вершин
def draw_polygon(verts, verts_idx):
    glBegin(GL_POLYGON)
    for idx in verts_idx: glVertex3fv(verts[idx])
    glEnd()

ROOM_SZ=5

def convex_hull(points):
    points, lower, upper = sorted(points), [], []
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    for p in points: # Строим нижнюю оболочку
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    for p in reversed(points):# Строим верхнюю оболочку
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower + [p for p in upper if not p in lower]

def draw_shadow_polygon(projected_verts, inner=True):
    vv=[v[:2] for v in projected_verts]
    verts=[[*v, 0.01] for v in convex_hull(vv)]
    draw_polygon(verts, list(range(len(verts))))

def draw_parallepiped(verts, inner=True):
    iii=[[0, 1, 2, 3], [7, 6, 5, 4], [0, 3, 7, 4], [1, 5, 6, 2], [0, 4, 5, 1], [2, 6, 7, 3]]
    for ii in iii: draw_quad(verts, ii if inner else ii[::-1])  # низ; верх; лево; право; зад; перед

def draw_room_and_cube():
    # Координаты стен комнаты (параллелепипед)
    room_vertices = [
        [-ROOM_SZ, -ROOM_SZ, 0], [ROOM_SZ, -ROOM_SZ, 0], [ROOM_SZ, ROOM_SZ, 0], [-ROOM_SZ, ROOM_SZ, 0], # пол
        [-ROOM_SZ, -ROOM_SZ, 3], [ROOM_SZ, -ROOM_SZ, 3], [ROOM_SZ, ROOM_SZ, 3], [-ROOM_SZ, ROOM_SZ, 3] # потолок
    ]
    # Материал для комнаты (мягкий, матовый)
    set_material(diffuse=[0.9, 0.9, 0.9, 1], specular=[0.2, 0.2, 0.2, 1], shininess=20)
    # Рисуем комнату
    glColor3f(0.7, 0.7, 0.7) # цвет стен
    draw_parallepiped(room_vertices, True)
    # Координаты куба внутри комнаты
    cube_size = 0.7
    cube_center = [0, 0, cube_size/2]  # чуть выше центра комнаты
    cx, cy, cz = cube_center
    s = cube_size / 2
    cube_vertices = [
        [cx - s, cy - s, cz - s], [cx + s, cy - s, cz - s], [cx + s, cy + s, cz - s], [cx - s, cy + s, cz - s], # низ
        [cx - s, cy - s, cz + s], [cx + s, cy - s, cz + s], [cx + s, cy + s, cz + s], [cx - s, cy + s, cz + s]] # верх
    # Материал для куба (глянцевый/блестящий)
    set_material(diffuse=[1, 1, 1, 1], specular=[1, 1, 1, 1], shininess=100)
    # Рисуем куб
    glColor3f(1.0, 0.0, 0.0)  # красный цвет для куба
    draw_parallepiped(cube_vertices, False)
    draw_shadow_for_cube(cube_vertices, LIGHT_POS)

display = (800, 600)

def draw_shadow_for_cube(cube_vertices, light_pos):
    # Включаем stencil buffer
    glEnable(GL_STENCIL_TEST), glClear(GL_STENCIL_BUFFER_BIT)
    # Устанавливаем режим заполнения stencil-буфера при рендеринге теней
    glColorMask(False, False, False, False)  # цвет не рисуем
    glDepthMask(False)  # глубину отключаем
    glStencilFunc(GL_ALWAYS, 1, 0xFF)  # всегда обновляем stencil
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)  # обновление при рисовании тени
    # Для тени проецируем вершины объекта на плоскость z=0
    projected_vertices = []
    for v in cube_vertices:
        denom = (light_pos[2] - v[2])
        t = 0 if denom == 0 else (-v[2] / denom)
        x_proj, y_proj = v[0] + t * (light_pos[0] - v[0]), v[1] + t * (light_pos[1] - v[1])
        projected_vertices.append([x_proj, y_proj, 0.01])  # z близко к 0 для тени
    glColorMask(True, True, True, True), glDepthMask(True) # Восстановление режима
    # Рисуем тень цветом — где stencil == 1
    glStencilFunc(GL_EQUAL, 1, 0xFF), glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
    glEnable(GL_BLEND), glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.0, 0.0, 0.0, 0.2)  # полупрозрачная тень
    draw_shadow_polygon(projected_vertices) #повторная отрисовка объекта в проекции
    glDisable(GL_BLEND), glDisable(GL_STENCIL_TEST)

if __name__=="__main__":
    DEBUG=True
    pygame.init()
    screen = pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
    cam=Camera()
    cam.x, cam.y, cam.z = -5,0,1
    cam.save_pos()
    ind_frame, last_key, last_info = 0, 0, ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(), quit()
            if event.type == pygame.KEYUP: last_key = 0
            if event.type == pygame.KEYDOWN:
                last_key=event.key
                if event.key==pygame.K_1: # print matricies
                    MP = cam.calc_proj_matrix()
                    print("PROJ: ", show_mat(MP))
                    MV = cam.calc_view_matrix(False)
                    print("VIEW: ", show_mat(MV))
                    print("FULL: ", show_mat(MP @ MV))
                    print("SCREEN: ", show_mat(cam.calc_screen_matrix()))
                if event.key==pygame.K_2: # print points
                    points2d = []
                    M=MP@cam.swapCS@MV
                    for p in points:
                        q=M@[*p, 1]; q=q[:2]/q[-1]
                        points2d.append(list(q))
                    print("PTS 3d: ", points)
                    print("PTS 2d: ", points2d)
                if event.key==pygame.K_0: DEBUG=not DEBUG

        # camera motion
        keys = pygame.key.get_pressed()  # get the state of all keys
        if keys[pygame.K_UP]: cam.move_local(0, 0, -0.1)
        if keys[pygame.K_DOWN]: cam.move_local(0, -0, 0.1)
        if keys[pygame.K_RIGHT]: cam.yaw-=1
        if keys[pygame.K_LEFT]: cam.yaw+=1
        if keys[pygame.K_r]: cam.move_local(0, 0.1, 0)
        if keys[pygame.K_f]: cam.move_local(0, -0.1, 0)
        if keys[pygame.K_a]: cam.move_local(-0.1, 0, 0)
        if keys[pygame.K_d]: cam.move_local(0.1, 0, 0)
        if keys[pygame.K_w]: cam.pitch-=1
        if keys[pygame.K_s]: cam.pitch+=1
        if keys[pygame.K_q]: cam.roll-=1
        if keys[pygame.K_e]: cam.roll+=1
        if keys[pygame.K_z]: cam.restore_pos()

        cam.x, cam.y=min(max(-ROOM_SZ, cam.x), ROOM_SZ), min(max(-ROOM_SZ, cam.y), ROOM_SZ)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION), glLoadIdentity()
        glMatrixMode(GL_MODELVIEW), glLoadIdentity()

        ci=cam.get_info()
        if ci!=last_info: print(f"i={ind_frame}: ", last_info:=ci)

        glMultMatrixf(np.transpose(cam.calc_proj_matrix())) # 1 projection matrix (column-major order)
        glMultMatrixf(np.transpose(cam.calc_view_matrix())) # 2 view matrix (column-major order)

        enable_light()
        glEnable(GL_DEPTH_TEST)

        draw_room_and_cube()  # drawing objects

        LIGHT_POS[:2]=1*np.sin(ind_frame/10), 1*np.cos(ind_frame/10)

        if DEBUG:
            disable_light(), glColor((1, 1, 1)), glPointSize(10.0), glBegin(GL_POINTS), glVertex3fv(LIGHT_POS), glEnd()
            glDisable(GL_DEPTH_TEST)
            cam.draw_world_axes()
            glMatrixMode(GL_MODELVIEW), glLoadIdentity()
            glOrtho(0, display[0], 0, display[1], -1, 1)
            cam.draw_world_axes_ortho_2d()
            cam.draw_cam_axes_ortho_2d(x0y0=(display[0]-30, 30))

        pygame.display.flip()
        pygame.time.wait(20)
        if ind_frame == 0: print(f"MP={MP}\n", f"MV={MV}\n")
        ind_frame+=1
