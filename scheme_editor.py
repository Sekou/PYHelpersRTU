#2025, S. Diane
#Scheme editor 2d

import pygame
pygame.init()

import sys
import tkinter as tk
from tkinter import simpledialog
import numpy as np
import math
import json

# Константы
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RECT_COLOR = (0, 0, 0)
CIRCLE_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 0)
RECT_WIDTH, RECT_HEIGHT = 100, 50
CIRCLE_RAD = 50

def dist(p1, p2): #расстояние между точками
    return np.linalg.norm(np.subtract(p2, p1))

def get_segm_intersection(A, B, C, D): #поиск точки пересечения двух отрезков
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = A, B, C, D
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0: return None  # отрезки параллельны или совпадают
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    if 0 <= t <= 1 and 0 <= u <= 1: return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None

def get_segm_intersection_rect(A, B, x, y, w, h):
    res, pp=[], [[x,y], [x+w,y], [x+w,y+h], [x,y+h]]
    for i in range(4):
        p1, p2 = pp[i-1], pp[i]
        p=get_segm_intersection(A, B, p1, p2)
        if p: res.append(p)
    return res

#https://stackoverflow.com/questions/30844482/what-is-most-efficient-way-to-find-the-intersection-of-a-line-and-a-circle-in-py
def get_segm_intersection_circle(A, B, pos, R, full_line=False, tangent_tol=1e-9):
    (p1x, p1y), (p2x, p2y), (cx, cy) = A, B, pos
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** .5
    big_d = x1 * y2 - x2 * y1
    discriminant = R ** 2 * dr ** 2 - big_d ** 2
    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 pts with the segment
        pts = [ (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant ** .5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant ** .5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out pts that do not fall within the segment
            fraction = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in pts]
            pts = [pt for pt, frac in zip(pts, fraction) if 0 <= frac <= 1]
        if len(pts) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both pts have same location)
            return [pts[0]]
        else: return pts

def pt_segm_dist(p, p1, p2): #расстояние от точки до отрезка
    dx, dy = np.subtract(p2, p1)
    k = dy / (0.0000001 if dx==0 else dx)
    b = p1[1] - k * p1[0]
    return np.abs(-k * p[0] + p[1] - b) / math.sqrt(k * k + 1)

id=0
def get_next_id():
    global id
    return (id:=id+1)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Перемещение прямоугольников")

def draw_text(screen, text, pos, sz=25, color=(0,0,0)):
    screen.blit(pygame.font.Font(None, sz).render(text, True, color), pos)

def arrow2(screen, color, p0, p1, w):
    angle=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
    p2 = [p1[0] - 10 * math.cos(angle + 0.5), p1[1] - 10 * math.sin(angle + 0.5)]
    p3 = [p1[0] - 10 * math.cos(angle - 0.5), p1[1] - 10 * math.sin(angle - 0.5)]
    for a,b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)

# Класс для объекта
class Obj:
    def __init__(self, x=0, y=0):
        self.id=get_next_id()
        self.x, self.y = x, y
        self.arrows=[]
        self.text = ""
    def get_pos(self): return (self.x, self.y)
    def set_pos(self, x, y): self.x, self.y=x, y
    def contains_point(self, pt): return False
    def draw(self, surface, objs): pass
    def get_intersections(self, p1, p2):
        if np.linalg.norm(np.subtract(p1, p2))<0.0001: return []
        if type(self) is Rect: return get_segm_intersection_rect(p1, p2, *self.get_xywh())
        elif type(self) is Circle: return get_segm_intersection_circle(p1, p2, self.get_pos(), self.r)
        return []
    def draw_arrows(self, surface, objs):
        if not type(self) in [Rect, Circle]: return
        for a in self.arrows:
            pp=[a.obj1.get_pos(), a.obj2.get_pos()]
            for i, obj, p1, p2 in [[0, a.obj1, *pp], [1, a.obj2, *pp[::-1]]]:
                if len(pi:=obj.get_intersections(p1, p2))>0:
                    pp[i]=pi[0]
                    pygame.draw.circle(surface, (255,0,0), pi[0], 3)
            a.p0, a.p1 = pp[0], pp[1]
            a.draw(surface, objs)
    def to_dict(self):
        D = {"id":self.id, "x":self.x, "y":self.y, "arrows":[[a.obj2.id, a.text] for a in self.arrows],
             "text":self.text, "type":self.__class__.__name__}
        return D
    def update_type(self, D):
        self.__class__=getattr(sys.modules[__name__], D["type"])
    def from_dict(self, D):
        self.id, self.x, self.y, self.text, self.arrows = D["id"], D["x"], D["y"], D["text"], D["arrows"]

# Класс для стрелки
class Arrow:
    def __init__(self, p0, p1):
        self.p0, self.p1=p0, p1
        self.obj1, self.obj2=None, None
        self.text=""
    def draw(self, surface, objs):
        arrow2(surface, (0,0,0), self.p0, self.p1, 2)
        if self.text:
            c=np.mean((self.p0, self.p1), axis=0)
            draw_text(surface, self.text, c, 25, TEXT_COLOR)
    def contains_point(self, pt):
        d_pt=pt_segm_dist(pt, self.p0, self.p1)
        d0=dist(self.p0, self.p1)
        d1, d2 = dist(self.p0, pt), dist(self.p1, pt)
        va=np.subtract(self.p1, self.p0)/d0
        vb=np.subtract(pt, self.p0)
        proj = np.dot(va, vb)
        d=d_pt if 0<proj<d0 else min(d1, d2)
        return d<5

# Класс для окружности
class Circle(Obj):
    def __init__(self, x, y, text=""):
        super().__init__(x, y)
        self.r = CIRCLE_RAD
        self.text=text
    def draw(self, surface, objs):
        super().draw(surface, objs)
        pygame.draw.circle(surface, CIRCLE_COLOR, (self.x, self.y), self.r, 2)
        if self.text: draw_text(surface, self.text, (self.x - 20, self.y - 5), 25, TEXT_COLOR)
    def contains_point(self, pt):
        return np.linalg.norm(np.subtract(pt, self.get_pos()))<self.r
    def to_dict(self):
        return {**super().to_dict(), "r":self.r}
    def from_dict(self, D):
        super().from_dict(D)
        self.r=D["r"]

# Класс для прямоугольника
class Rect(Obj):
    def __init__(self, x, y, text=""):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, RECT_WIDTH, RECT_HEIGHT)
        self.text=text
    def get_pos(self):
        return (self.rect.x+self.rect.width/2, self.rect.y+self.rect.height/2)
    def get_xywh(self):
        return [self.rect.x, self.rect.y, self.rect.w, self.rect.h]
    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x-self.rect.width/2, y-self.rect.height/2
    def draw(self, surface, objs):
        super().draw(surface, objs)
        pygame.draw.rect(surface, RECT_COLOR, self.rect, 2)
        if self.text: draw_text(surface, self.text, (self.rect.x + 5, self.rect.y + 5), 25, TEXT_COLOR)
    def contains_point(self, pt):
        return self.rect.collidepoint(pt)
    def to_dict(self):
        r=self.rect
        return {**super().to_dict(), "rect":[r.x,r.y,r.w,r.h]}
    def from_dict(self, D):
        super().from_dict(D)
        self.rect=self.rect = pygame.Rect(*D["rect"])

#класс холста
class Canvas:
    def __init__(self):
        self.objs=[]
    def draw(self, screen):
        for o in self.objs:
            o.draw_arrows(screen, self.objs)
        for o in self.objs:
            o.draw(screen, self.objs)
    def find_object(self, pos):
        for o in self.objs:
            if o.contains_point(pos): return o
        return None
    def get_object(self, id):
        for o in self.objs:
            if o.id==id: return o
        return None
    def find_arrow(self, pos):
        for o in self.objs:
            for a in o.arrows:
                if a.contains_point(ev.pos): return a
        return None
    def to_dict(self):
        return [o.to_dict() for o in self.objs]
    def from_dict(self, D):
        self.objs=[]
        for val in D: #загрузка объектов
            (o:=Obj()).update_type(val)
            o.from_dict(val)
            self.objs.append(o)
        for o in self.objs: #загрузка стрелок
            for i, (a, txt) in enumerate(o.arrows):
                o2=self.get_object(a)
                a2=Arrow(o.get_pos(), o2.get_pos())
                a2.obj1, a2.obj2, a2.text = o, o2, txt
                o.arrows[i]=a2

# Функция для запроса текста
def ask_for_text(text):
    (root := tk.Tk()).withdraw()  # Скрыть главное окно
    text = simpledialog.askstring("Введите текст", "Текст объекта:", initialvalue=text)
    root.destroy()
    return text

# Отрисовка всех объектов
def draw_all(screen, canvas):
    screen.fill(WHITE)
    canvas.draw(screen)
    draw_text(screen, "Use 'r' and 'c' to create rects and circles", (5, 5))
    draw_text(screen, "Use 'Ctrl' + mouse to create arrows", (5, 25))
    pygame.display.flip()
    clock.tick(fps)

clock = pygame.time.Clock()
fps=20

# Основная функция
if __name__ == "__main__":
    canvas=Canvas()

    mode="paint"
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    with open("tmp/scheme1.json", "w") as f:
                        json.dump(canvas.to_dict(), f)
                if ev.key == pygame.K_2:
                    with open("tmp/scheme1.json", "r") as f:
                        canvas.from_dict(json.load(f))
                if ev.key == pygame.K_n:
                    canvas.objs=[]
                if ev.key == pygame.K_c:
                    o=Circle(200,200, "circle")
                    canvas.objs.append(o)
                if ev.key == pygame.K_r:
                    o=Rect(200,300, "rect")
                    canvas.objs.append(o)
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1: # Левая кнопка мыши
                    if obj_under := canvas.find_object(ev.pos):
                        (mouse_x, mouse_y), p = ev.pos, obj_under.get_pos()
                        offset_x, offset_y = p[0] - ev.pos[0], p[1] - ev.pos[1]
                        if pygame.key.get_mods() & pygame.KMOD_LCTRL: mode = "arrow"
                        else: mode = "dragging"
                        # Перемещение объектов
                        while mode == "dragging":
                            for ev in pygame.event.get():
                                if ev.type == pygame.MOUSEMOTION:
                                    obj_under.set_pos(ev.pos[0] + offset_x, ev.pos[1] + offset_y)
                                    draw_all(screen, canvas)
                                if ev.type == pygame.MOUSEBUTTONUP:
                                    if ev.button == 1:
                                        mode = "paint"
                        # Протягивание стрелки
                        if mode == "arrow":
                            tmp_obj = Obj(*ev.pos) #создание кончика стрелки
                            obj_under.arrows.append(new_arrow:=Arrow(p, tmp_obj.get_pos()))
                            new_arrow.obj1, new_arrow.obj2 = obj_under, tmp_obj
                        while mode == "arrow":
                            for ev in pygame.event.get():
                                if ev.type == pygame.MOUSEMOTION:
                                    if tmp_obj:
                                        tmp_obj.set_pos(*ev.pos) #движение кончика стрелки
                                        new_arrow.p1=ev.pos
                                    draw_all(screen, canvas)
                                if ev.type == pygame.MOUSEBUTTONUP:
                                    if ev.button == 1:
                                        obj_next= canvas.find_object(ev.pos)
                                        if obj_next and obj_under!=obj_next: #закрепление кончика стрелки на выбранном объекте
                                            new_arrow.obj1, new_arrow.obj2=obj_under, obj_next
                                            new_arrow.text="arrow"
                                        else: obj_under.arrows.remove(new_arrow)
                                    mode = "paint"
                elif ev.button == 3:  # Правая кнопка мыши
                    if obj := canvas.find_object(ev.pos):
                        text = ask_for_text(obj.text)
                        if text: obj.text = text
                    if a := canvas.find_arrow(ev.pos):
                        text = ask_for_text(a.text)
                        if text: a.text = text

        draw_all(screen, canvas)

    pygame.quit()
    sys.exit()
