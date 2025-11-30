# Camera class for 3D algorithms, S. Diane, 2023-2025
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
    kPI = np.pi / 180
    swapCS = np.array([[0, -1, 0, 0], [0, 0, 1, 0], [-1, 0, 0, 0], [0, 0, 0, 1]])

    def save_pos(self): self.coords = self.x, self.y, self.z, self.yaw, self.pitch, self.roll

    def restore_pos(self): self.x, self.y, self.z, self.yaw, self.pitch, self.roll = self.coords

    def move_local(self, dx, dy, dz):
        M = self.calc_view_matrix()[:3, :3]
        M_ = np.linalg.inv(M)
        dx, dy, dz = M_ @ [dx, dy, dz]
        self.x, self.y, self.z = self.x+dx, self.y+dy, self.z+dz

    def calc_proj_matrix(self):
        ar = self.hRes / self.vRes
        tn = tan(self.hFOV * self.kPI / 2)
        d1 = self.nearZ - self.farZ
        d2 = self.nearZ + self.farZ
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
        if swap_axes: camMatrix = self.swapCS @ camMatrix
        return camMatrix

    def calc_screen_matrix(self, swap_y=True):
        k = -1 if swap_y else 1
        return np.array([[0.5 * self.hRes, 0, 0, 0.5 * self.hRes],
                         [0, 0.5 * self.vRes, 0, k * 0.5 * self.vRes],
                         [0, 0, 1, 0], [0, 0, 0, 1]])

    def transf_DC_to_screen(self, pDC):
        pNDC = pDC / pDC[-1]
        S = self.calc_screen_matrix()
        return (S @ pNDC)[:2]  # x, y for a pixel

    def transf_pts_from_world_to_screen(self, pts, M=None):
        res = []
        if M is None: M = self.calc_proj_matrix() @ self.calc_view_matrix()
        for p in pts:
            pDC = M @ [p[0], p[1], p[2], 1]
            pScreen = self.transf_DC_to_screen(pDC)
            res.append(tuple(pScreen))
        return res

    def get_info(self):
        return f"x {self.x:.2f}, y {self.y:.2f}, z {self.z:.2f}," \
               f" rl {self.roll:.2f}, pt {self.pitch:.2f}, yw {self.yaw:.2f}"

    def draw_world_axes(self):
        for v in np.array([(1, 0, 0), (0, 1, 0), (0, 0, 1)]):
            glColor(v), glBegin(GL_LINES)
            glVertex3fv((0, 0, 0))
            glVertex3fv(v)
            glEnd()

    def draw_world_axes_ortho_2d(self, sz=20, x0y0=(30,30)): #requires: glOrtho(0, display[0], 0, display[1], -1, 1)
        vv_global=cc=[(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        MV=self.calc_view_matrix()[:3,:3]
        pp, p0=[(MV@v)[:2] for v in vv_global], (MV@[0, 0, 0])[:2]
        for c, p in zip(cc, pp):
            glColor(c), glBegin(GL_LINES)
            glVertex2fv(x0y0), glVertex2fv(sz*p+x0y0)
            glEnd()

    def draw_cam_axes_ortho_2d(self, sz=20, x0y0=(30,30)): #requires: glOrtho(0, display[0], 0, display[1], -1, 1)
        vv_local=cc=[(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        vv_global = self.swapCS[:3,:3]@vv_local
        MV=self.calc_view_matrix()[:3,:3]
        pp, p0=[(MV@v)[:2] for v in vv_global], (MV@[0, 0, 0])[:2]
        for c, p in zip(cc, pp):
            glColor(c), glBegin(GL_LINES)
            glVertex2fv(x0y0), glVertex2fv(sz*p+x0y0)
            glEnd()

#Camera navigation in simple 3D scene, 2023-2025, S. Diane
import pygame

@np.vectorize
def F(x,y): return 0.03*np.sin(5*x)*np.sin(5*y)
def gen_surface_points(n):
    r = 2*np.arange(n) / (n-1) - 1
    inps=np.meshgrid(r, r)
    res=np.moveaxis(np.array([*inps, F(*inps)]), 0, -1)
    return res.reshape((n*n,3))

def show_mat(mat, prec=5):
    res=[[round(x, prec) for x in r] for r in mat]
    return str(res)

def draw_pts(points):
    start = glColor((1, 1, 1)), glBegin(GL_POINTS)
    for v in points: glVertex3fv(v)
    glEnd()

points = gen_surface_points(10)
display = (800, 600)

def main():
    pygame.init()
    screen = pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)

    cam=Camera()
    cam.x, cam.y, cam.z = -5,0,1
    cam.save_pos()

    ind_frame=0
    last_key=0
    last_info=""

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

        keys = pygame.key.get_pressed()  # get the state of all keys

        # camera motion
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

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION), glLoadIdentity()
        glMatrixMode(GL_MODELVIEW), glLoadIdentity()

        ci=cam.get_info()
        if ci!=last_info: print(f"i={ind_frame}: ", last_info:=ci)

        glPointSize(5.0)

        #1 projection matrix
        MP = np.transpose(cam.calc_proj_matrix()) #column-major order
        glMultMatrixf(MP)

        #2 view matrix
        MV = np.transpose(cam.calc_view_matrix()) #column-major order
        glMultMatrixf(MV)

        # drawing points
        draw_pts(points)
        cam.draw_world_axes()
        if ind_frame == 0: print(f"MP={MP}\n", f"MV={MV}\n")

        glMatrixMode(GL_MODELVIEW), glLoadIdentity()
        glOrtho(0, display[0], 0, display[1], -1, 1)
        cam.draw_world_axes_ortho_2d()
        cam.draw_cam_axes_ortho_2d(x0y0=(display[0]-30, 30))

        pygame.display.flip()
        pygame.time.wait(20)
        ind_frame+=1

if __name__=="__main__": main()
