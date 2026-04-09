# 2026, S. Diane, Manipulator model based on Denavit-Hartenberg approach (DH-scheme)
import sys, pygame, numpy as np, math

WIDTH, HEIGHT, CAM_SCALE=800, 600, 250
MAX_TRAJ_LEN=1000
CHECK_LIMITS=False

# матрица 4x4 поворота трехмерного вектора или объекта (3д-модели, камеры, дрона, датчика...)
def get_R_mat_4x4(roll, pitch, yaw, S=math.sin, C=math.cos): #например, (x2,y2,z2)=(get_mat()@[x, y, z, 1])[:3]
    cp, sp, cy, sy, cr, sr = C(pitch), S(pitch), C(yaw), S(yaw), C(roll), S(roll)
    mrol = [[1, 0, 0, 0], [0, cr, -sr, 0], [0, sr, cr, 0], [0, 0, 0, 1]] # x
    mpit = [[cp, 0, sp, 0], [0, 1, 0, 0], [-sp, 0, cp, 0], [0, 0, 0, 1]] # y
    myaw = [[cy, -sy, 0, 0], [sy, cy, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]] # z
    return np.array(mrol) @ mpit @ myaw
def get_R_mat_3x3(roll, pitch, yaw, S=math.sin, C=math.cos): #матрица 3x3 поворота: mrol @ mpit @ myaw
    cp, sp, cy, sy, cr, sr = C(pitch), S(pitch), C(yaw), S(yaw), C(roll), S(roll)
    return np.array([[cp*cy,-cp*sy,sp], [cr*sy+cy*sp*sr,cy*cr-sr*sp*sy,-cp*sr],
                     [sr*sy-cr*cy*sp,cr*sp*sy+cy*sr,cp*cr]])
def get_T_mat_4x4(x,y,z): #матрица смещения
    return np.array([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])
def transform_pt_3d(x, y, z, roll, pitch, yaw, S=math.sin, C=math.cos): # трансформация 3D точки
    cp, sp, cy, sy, cr, sr = C(pitch), S(pitch), C(yaw), S(yaw), C(roll), S(roll)
    return (x*cp*cy-y*cp*sy+z*sp, x*(cr*sy+cy*sp*sr)+y*(cy*cr-sr*sp*sy)-z*cp*sr,
            x*(sr*sy-cr*cy*sp) + y*(cr*sp*sy+cy*sr) + z*cp*cr) #mrol @ mpit @ myaw
# функция для проекции 3D точки в 2D #WIDTH, HEIGHT, CAM_SCALE=800, 600, 150
def project_pt_3d_to_2d(x, y, z, roll, pitch, yaw, tilt=0.1):
    xs, ys, zs = transform_pt_3d(x, y, z, roll, pitch, yaw)
    xs, ys, zs = transform_pt_3d(xs, ys, zs, math.pi / 2 + tilt, 0, 0)
    return int(xs * CAM_SCALE + WIDTH // 2), int(ys * CAM_SCALE + int(HEIGHT // 2 + 100))
# функция отрисовки осей #draw_axes(screen, roll, pitch, yaw, 1)
def draw_axes(screen, roll, pitch, yaw, size=1, p0=(0,0,0), M0=[[1,0,0],[0,1,0],[0,0,1]], w=1):
    base_dirs = [(size, 0, 0), (0, size, 0), (0, 0, size)]
    colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
    start_2d = project_pt_3d_to_2d(*p0, roll, pitch, yaw)
    for (rx, ry, rz), c in zip(base_dirs, colors): # Проецируем точки на экран
        end_2d = project_pt_3d_to_2d(*(p0+M0@np.array((rx, ry, rz))), roll, pitch, yaw)
        pygame.draw.line(screen, c, start_2d, end_2d, w)

class Link:
    def __init__(self, ind, thZ, alX, aX, dZ): #углы: alpha вокруг X, theta вокруг Z
        self.ind, self.p1, self.p2, self.mat = ind, [0,0,0], [0,0,0], np.eye(4)
        self.p2_, self.mat_ = None, None #точка и  матрица контраксиального (радиального) смещения для отрисовки звена в виде "кочерги"
        self.q, self.q_min, self.q_max = 0, -math.pi, math.pi
        self.thetaZ, self.alphaX, self.aX, self.dZ = thZ, alX, aX, dZ
    def get_config_mat(self, kx=1, kz=1, C=math.cos, S = math.sin):
        aX, dZ, alX, thZ = self.aX, self.dZ, self.alphaX, self.thetaZ
        ct,st,ca,sa=C(thZ), S(thZ), C(alX), S(alX) # ...далее рассчитаем матрицу по (2.2-29) из "Ли, Гонсалес, Фу, 1973"
        return np.array([[ct,-ca*st,sa*st,aX*ct*kx],[st,ca*ct,-sa*ct,aX*st*kx],[0,sa,ca,dZ*kz],[0,0,0,1]])
    def get_motion_mat(self):
        c, s = math.cos(self.q), math.sin(self.q) #Z
        return np.array([[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]])
    def calc(self):
        if CHECK_LIMITS:
            if self.q<self.q_min or self.q>self.q_max: print(f"Limit reached: {self.ind} axis")
            self.q=min(self.q_max, max(self.q_min, self.q))
        self.p2=(self.mat@[0, 0, 0, 1])[:3]
        if self.mat_ is not None: self.p2_=(self.mat_@[0, 0, 0, 1])[:3] # для "кочерги"
        assert self.aX**2+self.dZ**2-dist(self.p1, self.p2)**2<0.01, f"Link {self.ind}: L0!=L1"
    def draw(self, screen, roll, pitch, yaw):
        A=project_pt_3d_to_2d(*self.p1, roll, pitch, yaw)
        B=B_=project_pt_3d_to_2d(*self.p2, roll, pitch, yaw)
        if self.p2_ is not None: # для "кочерги"
            B_=project_pt_3d_to_2d(*self.p2_, roll, pitch, yaw)
            pygame.draw.line(screen, (200,0,200), A, B_, 4) #dZ
        pygame.draw.line(screen, (200,200,0), B_, B, 4) #dA
        pygame.draw.circle(screen, (0,0,0), B, 4, 2)
    def draw_axes(self, screen, roll, pitch, yaw):
        draw_axes(screen, roll, pitch, yaw, 0.1, self.p2, self.mat[:3,:3], 3)
        B = project_pt_3d_to_2d(*self.p2, roll, pitch, yaw)
        draw_text(screen, f"{self.ind}", int(B[0]), int(B[1]))

class Manipulator:
    def __init__(self): self.traj, self.links, self.author=[], [], "S. Diane, 2026"
    def add_link(self, thZ, alX, aX, dZ):
        self.links.append(Link(len(self.links)+1, thZ, alX, aX, dZ))
    def get_start_pos(self): return self.links[0].p1
    def get_end_pos(self): return self.links[-1].p2
    def calc(self, add_traj=False):
        for i, l in enumerate(self.links):
            local_mat, local_mat_=l.get_motion_mat()@l.get_config_mat(1, 1), None
            if l.aX!=0 or l.dZ!=0: local_mat_=l.get_motion_mat()@l.get_config_mat(0, 1) # для "кочерги"
            if i==0:
                T0=get_T_mat_4x4(*l.p1)
                l.mat = T0 @ local_mat # для конца звена
                if local_mat_ is not None: l.mat_ = T0 @ local_mat_ # для "кочерги"
            if i>0:
                l.p1 = self.links[i-1].p2
                l.mat=self.links[i-1].mat@local_mat # для конца звена
                if local_mat_ is not None: l.mat_=self.links[i-1].mat@local_mat_  # для "кочерги"
            l.calc() #calculate self.links[i].p2
        if add_traj: self.traj.append(self.get_end_pos())
        if len(self.traj)>MAX_TRAJ_LEN: self.traj=self.traj[-MAX_TRAJ_LEN:]
    def draw(self, screen, roll, pitch, yaw):
        A = project_pt_3d_to_2d(*self.get_start_pos(), roll, pitch, yaw)
        pygame.draw.circle(screen, (255,0,0), A, 5, 2)
        for i in range(len(self.links)): self.links[i].draw(screen, roll, pitch, yaw)
        for i in range(len(self.links)): self.links[i].draw_axes(screen, roll, pitch, yaw)
        for i in range(len(self.traj)-1):
            A = project_pt_3d_to_2d(*self.traj[i], roll, pitch, yaw)
            B = project_pt_3d_to_2d(*self.traj[i+1], roll, pitch, yaw)
            pygame.draw.line(screen, (0,200,200), A, B, 1)
        mat0 = get_T_mat_4x4(*self.links[0].p1)
        draw_axes(screen, roll, pitch, yaw, 0.3, self.links[0].p1, mat0[:3, :3])
    def get_coords(self): return [l.q for l in self.links]
    def solve_fk(self): # решение ПЗК
        self.calc()
        return self.get_end_pos()
    def solve_ik(self, target, step=0.1, iters=1): # решение ОЗК
        ll=self.links[::-1]
        tg, E = np.array(target), np.linalg.norm  # подготовка к покоординатному спуску
        for i,l in enumerate(ll): # легче вращ. последн. звено - начинаем с него
            e0, e_last, e_min, a_best, dir = E(self.solve_fk() - tg), 0, np.inf, ll[i].q, 1
            while dir != 0: # пробегаемся сначала в плюс; если ошибка растет, то в минус
                ll[i].q, e = min(ll[i].q_max, max(ll[i].q_min, ll[i].q + dir * step)), E(self.solve_fk() - tg)
                if e < e_min: e_min, a_best = e, ll[i].q
                if e > e0 or e == e_last: ll[i].q, dir = ll[i].q - (1.5 + 0.5 * dir) * step, (-1 if dir == 1 else 0)
                e_last = e
            ll[i].q = a_best
            self.solve_fk()
        return True if iters <= 1 else self.solve_ik(target, step / 2, iters - 1) # рекурсия

pygame.font.init()

def draw_text(screen, s, x, y, sz=15, c=(0, 0, 0)): # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))

def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2)) # расстояние между точками

def lim_ang(ang, arc=3.141592653589793): # ограничение угла в пределах +/-pi
    return ang%(2*arc)+2*arc*(int(ang%(2*arc)<-arc)-int(ang%(2*arc)>arc))

sz = (800, 600)

if __name__ == "__main__":
    screen, timer, fps = pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    tsim, dt = 0, 1 / fps

    manip=Manipulator()

    a90, a180=math.pi/2, math.pi

    # Planar 2-link manipulator (straight)
    # manip.add_link(0,0, 0.7, 0)
    # manip.add_link(0, 0, 0.4, 0)

    # Planar 2-link manipulator (bent)
    # manip.add_link(0,-a90, 0.7, 0)
    # manip.add_link(0, 0, 0, 0.4)

    #Puma maniulator (6-axis)
    # manip.add_link(a90,-a90, 0, 0)
    # manip.add_link(0, 0, 0.432, 0.149)
    # manip.add_link(a90, a90, -0.020, 0)
    # manip.add_link(0, -a90, 0, 0.433)
    # manip.add_link(0, a90, 0, 0)
    # manip.add_link(0, 0, 0, 0.056)

    #KULA LBR iiwa 7 R800 maniulator (7-axis)
    manip.add_link(0,-a90, 0, 0.34)
    manip.add_link(0, a90, 0, 0)
    manip.add_link(0, -a90, 0, 0.4)
    manip.add_link(a180, -a90, 0, 0)
    manip.add_link(0, -a90, 0, 0.4)
    manip.add_link(a180, -a90, 0, 0)
    manip.add_link(0, 0, 0, 0.126)

    # manip.links[0].p1=[0,0,0.66]

    roll, pitch, yaw=0,0,0
    need_axes=True
    fk_motion_mode=False

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_0:
                    manip.traj.clear()
                    for i, l in enumerate(manip.links): l.q = 0
                if ev.key == pygame.K_1: need_axes=not need_axes
                if ev.key == pygame.K_2: fk_motion_mode=not fk_motion_mode
                if ev.key == pygame.K_3:
                    manip.traj.clear() #for KULA LBR iiwa 7 R800 maniulator (7-axis)
                    fk_motion_mode = False
                    qq = [1.570796, 1.570796, 2.96706, -1.570796, 1.570796, 1.570796, 0]
                    ss=[1,1,1,-1,1,-1,1]
                    for i, l in enumerate(manip.links): l.q = qq[i]*ss[i]
                if ev.key == pygame.K_4:
                    manip.traj.clear()
                    manip.solve_ik([0.5,0.5,0.5], 0.1, 10)
                    manip.solve_fk()
                    print(manip.get_coords())
        if fk_motion_mode:
            for i, l in enumerate(manip.links):
                l.q = 2/(i+1)*math.sin(tsim*(i+1) + i)

        manip.calc(True)

        screen.fill((255, 255, 255))
        if need_axes: draw_axes(screen, roll, pitch, yaw, 1)
        manip.draw(screen, roll, pitch, yaw)

        yaw+=-0.05

        draw_text(screen, f"Start pos = {[round(v,2) for v in manip.get_start_pos()]}", 5, 5)
        draw_text(screen, f"End pos = {[round(v,2) for v in manip.get_end_pos()]}", 5, 25)
        draw_text(screen, f"0 - zero coords", 5, 45)
        draw_text(screen, f"1 - toggle axes", 5, 65)
        draw_text(screen, f"2 - move in FK mode", 5, 85)
        draw_text(screen, f"3 - set FK coords", 5, 105)
        draw_text(screen, f"4 - solve IK for (0.5,0.5,0.5)", 5, 125)

        pygame.display.flip(), timer.tick(fps)
        tsim+=dt

# template file by S. Diane, RTU MIREA, 2024-2026
