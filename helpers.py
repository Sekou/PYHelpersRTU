def prob_sel(probs): #вероятностный выбор индекса элемента
    m, s, r=sum(probs), 0, np.random.rand()
    if m==0: return np.random.randint(len(probs))
    for i in range(len(probs)):
        s+=probs[i]/m
        if s>=r: return i
    return -1

def read_pts(filename): #чтение массива целочисленных точек
    with open(filename, "r") as f:
        return [[int(v) for v in l.split()] for l in f.readlines()]

def rot_segm(segm, ang): #центральный поворот отрезка на угол
    c=np.mean(segm, axis=0)
    v1=np.subtract(segm[0], c)
    v2=np.subtract(segm[1], c)
    return list(np.add([rot(v1, ang), rot(v2, ang)], c))

def pt_segm_dist(p, p1, p2): #расстояние от точки до отрезка
    dx, dy = np.subtract(p2, p1)
    k = dy / (0.0000001 if dx==0 else dx)
    b = p1[1] - k * p1[0]
    return np.abs(-k * p[0] + p[1] - b) / math.sqrt(k * k + 1)

def project_pt(segm, pt): #точка-проекция точки на отрезок
    v2=np.subtract(pt, segm[0], dtype=float)
    v1=np.subtract(segm[1], segm[0], dtype=float)
    v1_=v1/np.linalg.norm(v1)
    L2=np.dot(v1_, v2)
    return segm[0] + L2*v1_

def check_proj(segm, pt): #проверка попадания проецирцемой точки внетрь отрезка
    v2=np.subtract(pt, segm[0], dtype=float)
    v1=np.subtract(segm[1], segm[0], dtype=float)
    L1=np.linalg.norm(v1)
    return 0<=np.dot(v1/L1, v2)<=L1

def check_intersection(A,B,C,D): #проверка пересечения двух отрезков
    ccw = lambda A, B, C: (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def get_segm_intersection(A, B, C, D): #поиск точки пересечения двух отрезков
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = A, B, C, D
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0: return None  # отрезки параллельны или совпадают
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    if 0 <= t <= 1 and 0 <= u <= 1:
        intersection_x = x1 + t * (x2 - x1)
        intersection_y = y1 + t * (y2 - y1)
        return (intersection_x, intersection_y)
    return None

#проверяем, находится ли точка внутри многоугольника
def point_inside_polygon(point, vertices):
    (x, y), c = point, 0
    for i in range(len(vertices)):
        (x1, y1), (x2, y2) = vertices[i-1], vertices[i]
        if min(y1,y2) <= y < max(y1, y2):
            ratio = (y - y1) / (y2 - y1)
            c ^= (x - x1 < ratio*(x2 - x1))
    return c

#определяем точки, лежащие внутри многоугольника
def get_points_inside_ngon(ngon_pts, xmin, xmax, ymin, ymax, step=20):
    pts=[]
    for x in range(xmin, xmax, step):
        for y in range(ymin, ymax, step):
            check = point_inside_polygon([x, y], ngon_pts)
            if check: pts.append([x,y])
    return pts

#отрисовка стрелки по точке и углу
def arrow(screen, color, p0, angle, lenpx, w):
    p1 = [p0[0] + lenpx * math.cos(angle), p0[1] + lenpx * math.sin(angle)]
    p2 = [p1[0] - 10 * math.cos(angle + 0.5), p1[1] - 10 * math.sin(angle + 0.5)]
    p3 = [p1[0] - 10 * math.cos(angle - 0.5), p1[1] - 10 * math.sin(angle - 0.5)]
    pygame.draw.line(screen, color, p0, p1, w)
    pygame.draw.line(screen, color, p1, p2, w)
    pygame.draw.line(screen, color, p1, p3, w)
    
#отрисовка стрелки по 2 точкам
def arrow2(screen, color, p0, p1, w):
    angle=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
    p2 = [p1[0] - 10 * math.cos(angle + 0.5), p1[1] - 10 * math.sin(angle + 0.5)]
    p3 = [p1[0] - 10 * math.cos(angle - 0.5), p1[1] - 10 * math.sin(angle - 0.5)]
    pygame.draw.line(screen, color, p0, p1, w)
    pygame.draw.line(screen, color, p1, p2, w)
    pygame.draw.line(screen, color, p1, p3, w)
