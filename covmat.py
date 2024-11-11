#S. Diane, 2023-2024
import math
import numpy as np
import sys, pygame

#оценка матрицы ковариации
def estimateCovMat(pts, weights):
    sx, sy, sxy, M = 0, 0, 0, 0
    pavg=np.zeros(2)
    for i in range(len(pts)):
        pavg+=pts[i].pos*weights[i]
        M+=weights[i]
    pavg/=M
    for i in range(len(pts)):
        d=(pts[i].pos-pavg)
        sx+=d[0]*d[0]*weights[i]
        sy+=d[1]*d[1]*weights[i]
        sxy+=d[0]*d[1]*weights[i]
    sx/=M;sy/=M;sxy/=M
    return pavg, np.array([[sx, sxy],[sxy, sy]])

#оценка геометрических параметров распределения
def getCovParams(mat, eps=1e-12):
    a, c = mat[0,0], mat[1,1]
    b=(mat[0,1]+mat[1,0])/2
    hs, hd =(a+c)/2, (a-c)/2
    D=np.sqrt(hd*hd+b*b)
    lam1, lam2 = hs+D+eps, hs-D+eps
    if(b==0 and a>=c): theta = 0
    elif(b==0 and a<c): theta = np.pi/2
    else: theta=math.atan2(lam1-a, b)
    r1, r2=np.sqrt(lam1),np.sqrt(lam2)
    sth, cth=np.sin(theta),np.cos(theta)
    return [r1, r2, sth, cth]

#отрисовка распределения вероятностей в виде эллипса
def drawEllipse(screen, pcov, p0, scale, color, w, N=50):
    k = np.pi * 2 / N
    def pt(t):
        stime, ctime = np.sin(t), np.cos(t)
        x = pcov[0] * pcov[3] * ctime - pcov[1] * pcov[2] * stime
        y = pcov[0] * pcov[2] * ctime + pcov[1] * pcov[3] * stime
        return (x * scale + p0[0], y * scale + p0[1])
    for i in range(N):
        pygame.draw.line(screen, color, pt(k*(i-1)), pt(k*i), w)

#формирование повернутой матрицы ковариации
def getRotCovMat(sigma1, sigma2, theta):
    CovMat=np.array([[sigma1**2, 0],[0, sigma2**2]])
    Scale=np.sqrt(CovMat)
    s,c=np.sin(theta),np.cos(theta)
    R=np.array([[c, -s],[s, c]])
    T=np.matmul(R,Scale)
    Lr=np.matmul(T,np.transpose(T))
    return Lr
