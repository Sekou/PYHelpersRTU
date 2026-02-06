#Various helper functions (author: Sekou Diane, 2024-2026)

def flatten(lst): # разглаживание вложенного списка в линейный вид
    return [e for l in filter(lambda v:type(v)==list,lst) for e in flatten(l)]+[*filter(lambda v:type(v)!=list,lst)]
    
def draw_text(screen, s, x, y, sz=15, с=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, с), (x, y))

def draw_multiline_text(screen, text, pos, sz=25, color=(0,0,0), transf=False, sep="\n"):
    for i,t in enumerate(text.split(sep)): # отрисовка многострочного текста
        draw_text(screen, t, [pos[0], pos[1]+sz*i], sz, color, transf)
    
def arr_to_str(arr, sep="\t"): # конвертирует одномерный массив в строку
    return sep.join([f"{v:.3f}" for v in arr])
    
# разбивка длинной строки на более маленькие для компактной отрисовки
def insert_str_breaks(s, max_w_len=15, sep="\\"): 
    n, n2=len(s), int(len(s)**0.5)+1
    lst, shift, cnt, trigger=list(s), 0, 0, False
    for i in range(n):
        if i>0 and any([j%n2==0 for j in [i, i+1, i+2]]): trigger=True
        if ((cnt:=cnt+1)>=max_w_len or s[i].isspace()) and trigger:
            if s[i].isspace(): lst[i + shift] = sep
            else: lst.insert(i - 1 + (shift:=shift+1), sep)
            cnt, trigger=0, False
    return "".join(lst)
    
def prob_sel(probs): # вероятностный выбор индекса элемента
    m, s, r=sum(probs), 0, np.random.rand()
    if m==0: return np.random.randint(len(probs))
    for i in range(len(probs)):
        s+=probs[i]/m
        if s>=r: return i
    return -1

def read_pts(filename): # чтение массива целочисленных точек
    with open(filename, "r") as f:
        return [[int(v) for v in l.split()] for l in f.readlines()]

def rot(v, ang): return np.dot([[-v[1], v[0]], v],[math.sin(ang), math.cos(ang)]) # поворот вектора на угол
    
def rot2(v, ang): # поворот вектора на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def rot_around(v, ang, c): # поворот вектора на угол вокруг точки
    return list(np.add(c, rot([v[0]-c[0], v[1]-c[1]], ang)))

def rot_arr(vv, ang): # функция для поворота массива на угол
    return [rot(v, ang) for v in vv]

def rot_arr_around(vv, ang, c): # функция для поворота массива на угол вокруг точки
    return list(np.add(c, [rot([v[0]-c[0], v[1]-c[1]], ang) for v in vv]))

def draw_rot_rect(screen, color, pc, w, h, ang): #рисует повернутый прямоугольник (по точке центра, ширине, высоте и углу)
    pygame.draw.polygon(screen, color, np.add(rot_arr([[-w/2, -h/2], [+w/2, -h/2], [+w/2, +h/2], [-w/2, +h/2]], ang), pc), 2)
    
def lim_ang(ang, arc=3.141592653589793): # ограничение угла в пределах +/-pi
    ang=ang%(2*arc); return ang + (2*arc if ang<-arc else -2*arc if ang>arc else 0)
    
def lim_ang2(ang): # ограничение угла в пределах +/-pi
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def check_ccw(A, B, C): #triangle direction: CCW for Y-axis up, but CW for Y-axis down
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
def lim_abs(val, amp): # ограничение значения по абсолютной величине
    return min(amp, max(-amp, val))

def round_pt(p, stepx, stepy): #округление координат точки (для снэппинга)
    p = [p[0] + stepx / 2, p[1] + stepy / 2]
    return [p[0] - p[0] % stepx, p[1] - p[1] % stepy]

def nonlin(a, b, nominal=1): # нелинейная функция (степенная)
    return math.pow(abs(a/nominal), b-1) * a
    
def lin_nonlin(a, gamma, nominal=1): # линейно-нелинейная функция
    return a if abs(a)<nominal else math.pow(abs(a/nominal), gamma-1) * a
    
def lin_nonlin_sat(v, gamma, th1, th2): # линейно-нелинейная функция с насыщением
    return lim_abs(lin_nonlin(v, gamma, th1), th2)

def lin_interp(xx, yy, x): # линейная интерполяция по точечным данным
    i=1 if x<xx[0] else 0
    while i<len(xx)-1 and x>xx[i]: i+=1
    return yy[i-1]+(x-xx[i-1])/(xx[i]-xx[i-1])*(yy[i]-yy[i-1])

# подбор значения по монотонной нелинейной функции 
def find_inv_x(f, y, xmin, xmax, step=0.1):
    xx=np.arange(xmin, xmax, step)
    return xx[np.argmin([abs(y-f(x)) for x in xx])]
    
def shift_to_zero(v, delta): # уменьшение значения по абсолютной величине
    return max(0, v-delta) if v>0 else min(0, v+delta)

def shift_to(v, target, delta): # сдвиг значения к целевой переменной
    return max(target, v-delta) if v>target else min(target, v+delta)

def ang_to(p1, p2): # угол от 1 точки на 2 точку
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    
def dist(p1, p2): # расстояние между точками
    return np.linalg.norm(np.subtract(p2, p1))

def path_len(pts): # длина ломанной линии
    return sum(np.linalg.norm(np.subtract(p1,p2)) for p1,p2 in zip(pts[1:], pts[:-1]))

def greedy_tsp(pts, ind): # жадное разомкнутое решение задачи коммивояжера (поиск в глубину)
    buf, res = [np.array(pts[i]) for i in range(len(pts)) if i!=ind], [np.array(pts[ind])]
    while len(buf): res+=[buf.pop(np.argmin([np.hypot(*(res[-1] - p)) for p in buf]))]
    return res

def greedy_tsp_fast(pts, ind): # ускоренное жадное разомкнутое решение задачи коммивояжера (поиск в глубину)
    n, buf, res = len(pts), [i for i in range(len(pts)) if i!=ind], [ind]
    G2 = [[0] * n for _ in range(n)] # создаем матрицу квадратов расстояний
    for i,p in enumerate(pts):
        for j,q in enumerate(pts):
            if i<=j: G2[j][i] = G2[i][j] = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
    while len(buf): res += [buf.pop(np.argmin([G2[res[-1]][i] for i in buf]))]
    return [np.array(pts[i]) for i in res]

def best_greedy_tsp(pts): # лучшее из частных жадных разомкнутых решений задачи коммивояжера
    ss = [greedy_tsp_fast(pts, i) for i in range(len(pts))]
    return ss[np.argmin([path_len(s) for s in ss])]

#@njit()
def get_permutations(A, k): #вектор индексов перестановки из A по k
    r = [[_ for _ in range(0)]]
    for i in range(k): r = [[a] + b for a in A for b in r if not a in b]
    return r

#@njit
def find_euler_path(pts: NDArray[np.float64]): #поиск кратчайшего пути через n точек
    n = len(pts)  # print("Num permutations: ",math.factorial(n))
    graph = [[0] * n for _ in range(n)] # создаем матрицу расстояний
    for i,p in enumerate(pts):
        for j,q in enumerate(pts):
            if i<=j: graph[j][i] = graph[i][j] = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
    best_path, min_len=None, np.inf
    for perm in get_permutations(range(n), n): # генерируем все перестановки узлов
        path = [pts[i] for i in perm]
        l=path_len(path)
        if l<min_len: best_path, min_len = path, l
    return best_path # возвращаем найденный путь Эйлера

def calc_integral(pts, calc_moment=False): 
    integral = 0 # интеграл функции под ломанной линией
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        v = (y0 + y1) / 2 * (x1 - x0)
        integral += v*(x0+x1)/2 if calc_moment else v
    return integral
    
def rot_segm(segm, ang): # центральный поворот отрезка на угол
    c=np.mean(segm, axis=0)
    v1,v2=np.subtract(segm[0], c), np.subtract(segm[1], c)
    return list(np.add([rot(v1, ang), rot(v2, ang)], c))
    
def pt_segm_dist(p, p1, p2): # расстояние от точки до прямой (заданной отрезком)
    k = (p2[1]-p1[1]) / (0.0000001 if p2[0]==p1[0] else (p2[0]-p1[0]))
    return np.abs(k * (p1[0]-p[0]) - p1[1] + p[1]) / (k * k + 1)**0.5 # числитель: p[1]-(k*p[0]+b)

def pt_segm_dist2(p, p1, p2):  # расстояние от точки до ограниченного отрезка
    k = (p2[1]-p1[1]) / (0.0000001 if p2[0]==p1[0] else (p2[0]-p1[0]))
    d = np.abs(k * (p1[0] - p[0]) - p1[1] + p[1]) /(k * k + 1)**0.5  # числитель: p[1]-(k*p[0]+b)
    v1,v12,v2=np.subtract(p, p1), np.subtract(p2, p1), np.subtract(p, p2)
    return d if 0 < v1 @ v12 / (v12@v12) < 1 else min(v1@v1, v2@v2)**0.5

def get_insert_ind(points_, mouse_pos): # поиск отрезка для вставки новой точки
    dd=[100500, dist(mouse_pos, points_[0]), dist(mouse_pos, points_[-1])]
    ii, nmax=[0,-1,len(points_)], len(points_)-2
    for i, (p1, p2) in enumerate(zip(points_[:-1], points_[1:])):
        d,f=pt_segm_dist2(mouse_pos, p1, p2)
        b = (f==0 or 0<i<nmax) or (d<dd[1] and i==0 and f<0 or d<dd[2] and i==nmax and f>0)
        if b and d<dd[0]: dd[0], ii[0]=d,i
    return ii[np.argmin(dd)]

def project_pt(segm, pt): # точка-проекция точки на отрезок
    v1, v2=np.subtract(segm[1], segm[0], dtype=float), np.subtract(pt, segm[0], dtype=float)
    return segm[0] + np.dot(v1, v2)*v1/np.dot(v1,v1)

def project_pt_along(segm, pt, vec): # точка-проекция точки на отрезок в направлении прямой, заданной вектором
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = segm[0], segm[1], pt, np.add(pt, vec)
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0: return None  # отрезки параллельны или совпадают
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1)) if 0 <= t <= 1 else None

def check_proj(segm, pt): # проверка попадания проецирцемой точки внетрь отрезка
    v2=np.subtract(pt, segm[0], dtype=float)
    v1=np.subtract(segm[1], segm[0], dtype=float)
    L1=np.linalg.norm(v1)
    return 0<=np.dot(v1/L1, v2)<=L1

def check_intersection(A,B,C,D): # проверка пересечения двух отрезков
    ccw = lambda A, B, C: (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def get_segm_intersection(A, B, C, D): # поиск точки пересечения двух отрезков
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = A, B, C, D
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0: return None  # отрезки параллельны или совпадают
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    if 0 <= t <= 1 and 0 <= u <= 1: return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None

# пересечения отрезка с прямоугольником
def get_segm_intersection_rect(A, B, x, y, w, h):
    res, pp=[], [[x,y], [x+w,y], [x+w,y+h], [x,y+h]]
    for i in range(4):
        p1, p2 = pp[i-1], pp[i]
        p=get_segm_intersection(A, B, p1, p2)
        if p: res.append(p)
    return res
    
# пересечения отрезка с окружностью
def get_segm_intersection_circle(A, B, pos, R, full_line=False, tangent_tol=1e-9):
    (p1x, p1y), (p2x, p2y), (cx, cy) = A, B, pos
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr, big_d = (dx ** 2 + dy ** 2) ** .5, big_d = x1 * y2 - x2 * y1
    discriminant = R ** 2 * dr ** 2 - big_d ** 2
    if discriminant < 0: return [] # No intersection between circle and line
    else:  # There may be 0, 1, or 2 pts with the segment
        pts = [ (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant ** .5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant ** .5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out pts that do not fall within the segment
            fraction = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in pts]
            pts = [pt for pt, frac in zip(pts, fraction) if 0 <= frac <= 1]
        if len(pts) == 2 and abs(discriminant) <= tangent_tol: return [pts[0]] # If line is tangent to circle, return just one point
        else: return pts

# проверяем, находится ли точка внутри многоугольника
def pt_inside_ngon(point, vertices):
    (x, y), c = point, 0
    for i in range(len(vertices)):
        (x1, y1), (x2, y2) = vertices[i-1], vertices[i]
        if min(y1,y2) <= y < max(y1, y2):
            ratio = (y - y1) / (y2 - y1)
            c ^= (x - x1 < ratio*(x2 - x1))
    return c

# определяем точки, лежащие внутри многоугольника
def get_pts_inside_ngon(ngon_pts, xmin, xmax, ymin, ymax, step=20):
    pts=[]
    for x in range(xmin, xmax, step):
        for y in range(ymin, ymax, step):
            check = pt_inside_ngon([x, y], ngon_pts)
            if check: pts.append([x,y])
    return pts

def ngon_len(pts): # периметр многоугольника
    return sum(np.linalg.norm(np.subtract(p1,p2)) for p1,p2 in zip(pts, pts[1:]+[pts[0]]))
    
def ngon_len2(pts): # периметр многоугольника 2
    return sum(np.linalg.norm(np.subtract(pts[i], pts[(i + 1) % len(pts)])) for i in range(len(pts)))
    
#определяем площадь многоугольника
def ngon_area(coords):
    x, y = [p[0] for p in coords], [p[1] for p in coords] # get x and y in vectors
    x_, y_ = x - np.mean(x), y - np.mean(y) # shift coordinates
    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:]) # calculate area
    return 0.5 * np.abs(main_area + x_[-1] * y_[0] - y_[-1] * x_[0]) # correction added

def pt_ngon_dist(pt, ngon): # расстояние от точки до многоугольника
    return min(pt_segm_dist(pt, p1, p2) for p1, p2 in zip(ngon, [*ngon[1:],ngon[0]]))
    
# отрисовка стрелки по точке и углу
def draw_arrow(screen, color, p0, ang, lenpx, w):
    p1 = [p0[0] + lenpx * math.cos(ang), p0[1] + lenpx * math.sin(ang)]
    p2 = [p1[0] - 10 * math.cos(angle + 0.5), p1[1] - 10 * math.sin(angle + 0.5)]
    p3 = [p1[0] - 10 * math.cos(angle - 0.5), p1[1] - 10 * math.sin(angle - 0.5)]
    for a,b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)
    
# отрисовка стрелки по 2 точкам
def draw_arrow2(screen, color, p0, p1, w):
    angle=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
    p2 = [p1[0] - 10 * math.cos(angle + 0.5), p1[1] - 10 * math.sin(angle + 0.5)]
    p3 = [p1[0] - 10 * math.cos(angle - 0.5), p1[1] - 10 * math.sin(angle - 0.5)]
    for a,b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)
        
# отрисовка сетки
def draw_grid(screen, szx=600, szy=400, stepx=50, stepy=50, c = (200,200,200)): #отрисовка сетки
    for iy in np.arange(0, szy+stepy/2, stepy): pygame.draw.line(screen, c, r2i(0, 0+iy), r2i(0+szx, 0+iy), 1)
    for ix in np.arange(0, szx+stepx/2, stepx): pygame.draw.line(screen, c, r2i(0+ix, 0), r2i(0+ix, 0+szy), 1)

# формирование нескольких различных цветов
def get_some_colors():
    return [(220, 0, 0), (0, 220, 0), (0, 0, 220), (150, 150, 0), (0, 150, 150), (150, 0, 150),
     (120, 50, 50), (50, 120, 50), (50, 50, 120), (100, 100, 50), (50, 100, 100), (100, 50, 100)]

# сохранение скриншота в pygame
def save_screenshot(screen):
    import time, datetime as dt
    frmt_date = dt.datetime.fromtimestamp(
        time.time()).strftime("%Y-%m-%d(%H-%M-%S)")
    pygame.image.save(screen, frmt_date+".png")

# функция для запроса текста
def ask_for_text(text="", cap="Введите текст", tit="Текст объекта:"):
    (root := tk.Tk()).withdraw()  # Скрыть главное окно
    def activate():
        time.sleep(0.25)
        try: pyautogui.getWindowsWithTitle("Введите текст")[0].activate()
        except: pass
    threading.Thread(target=activate).start()
    text = simpledialog.askstring(cap, tit, initialvalue=text)
    root.destroy()
    return text
    
# функция для запроса многострочного текста
def open_trackbar_dialog(params, names): # диалог с трекбарами для задания параметров
    root, tracks, result = tk.Tk(), [], None
    root.title("Задать параметры"), root.geometry("300x450"), root.resizable(False, False)
    def to_scale_value(val): return int((val + 1) * 50) # Конвертация параметров из диапазона (-1, 1) к (0, 100)
    def from_scale_value(val): return (val / 50) - 1 # Конвертация параметров из диапазона (0, 100) к (-1, 1)
    for prm, name in zip(params, names):# Создание трекбаров
        ttk.Label(root, text=name).pack()
        tracks.append(ttk.Scale(root, from_=0, to=100, orient='horizontal'))
        tracks[-1].set(to_scale_value(prm)), tracks[-1].pack()
    def on_ok(): # Получение значений с трекбаров и преобразование в диапазон (-1, 1)
        nonlocal result
        result = [from_scale_value(tr.get()) for tr in tracks]
        root.quit()
    def on_cancel(): root.quit()
    root.protocol("WM_DELETE_WINDOW", on_cancel)
    ttk.Button(root, text="OK", command=on_ok).pack(pady=5) # Кнопка OK
    ttk.Button(root, text="Отмена", command=on_cancel).pack() # Кнопка Cancel
    root.mainloop(); root.destroy()
    return result

# матрица поворота трехмерного вектора или объекта (3д-модели, камеры, дрона, датчика...)
def get_mat(roll, pitch, yaw): #например, (x2,y2,z2)=(get_mat()@[x, y, z, 1])[:3]
    cr, cp, cy = math.cos(roll), math.cos(pitch), math.cos(yaw)
    sr, sp, sy = math.sin(roll), math.sin(pitch), math.sin(yaw)
    mrol = [[1, 0, 0, 0], [0, cr, -sr, 0], [0, sr, cr, 0], [0, 0, 0, 1]]  # x
    mpit = [[cp, 0, sp, 0], [0, 1, 0, 0], [-sp, 0, cp, 0], [0, 0, 0, 1]]  # y
    myaw = [[cy, -sy, 0, 0], [sy, cy, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]  # z
    return np.array(mrol) @ mpit @ myaw

# функция для проекции 3D точки в 2D
CAM_SCALE=150 #pixels per meter
CAM_DIST=5 #distance from camera to scene origin
def project_point(x, y, z, roll, pitch, yaw):
    cp,sp,cy,sy,cr,sr=math.cos(pitch), math.sin(pitch), \
                      math.cos(yaw), math.sin(yaw), math.cos(roll), math.sin(roll)
    z, x = z*cp - x*sp, x*cp + z*sp
    xs, ys, zs = x*cy - y*sy, -z*cr - y*sr, y*cr - z*sr
    factor = CAM_DIST / (CAM_DIST + zs)
    x_proj = xs * factor * CAM_SCALE + WIDTH // 2
    y_proj = ys * factor * CAM_SCALE + int(HEIGHT *2/3)
    return int(x_proj), int(y_proj)
    
# функция отрисовки осей
def draw_axes(screen, size, roll, pitch, yaw):
    base_dirs = [(size, 0, 0), (0, size, 0), (0, 0, size)]
    colors=[(255,100,100), (100,255,100), (100,100,255)]
    for (rx, ry, rz), c in zip(base_dirs, colors):
        # Проецируем точки на экран
        start_2d = project_point(0,0,0, roll, pitch, yaw)
        end_2d = project_point(rx, ry, rz, roll, pitch, yaw)
        pygame.draw.line(screen, c, start_2d, end_2d, 2)

# загрузка изображений из папки
def load_images_from_folder(dir):
    return list(filter(lambda v: v is not None, [cv2.imread(os.path.join(dir,f)) for f in os.listdir(dir)]))

def show_traj_3d(traj): # график трехмерной линии 
    import matplotlib.pyplot as plt
    ax = plt.figure().add_subplot(projection='3d')
    ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    # ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.plot(*np.swapaxes(traj, 0, 1), label='trajectory')  
    ax.legend(); plt.show()

def euler_angles_to_rotation_matrix(phi, theta, psi): # матрица из углов: Z-Y-X (Yaw-Pitch-Roll)
    R_x = np.array([[1, 0, 0], [0, np.cos(phi), -np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])
    R_y = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    R_z = np.array([[np.cos(psi), -np.sin(psi), 0], [np.sin(psi), np.cos(psi), 0], [0, 0, 1]])
    return R_z @ R_y @ R_x

def read_txyz_from_csv(file, sep = ',' ): # 1 строка — заголовки
    with open(file, "r", encoding="utf-8") as f: lines = f.readlines()
    return [[float(p) for p in l.strip().split(sep)] for l in lines[1:]]

def convex_hull(points): # выпуклая оболочка набора точек
    points, lower, upper = sorted(points), [], []
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    for p in points: # Строим нижнюю оболочку
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: lower.pop()
        lower.append(p)
    for p in reversed(points):# Строим верхнюю оболочку
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0: upper.pop()
        upper.append(p)
    return lower + [p for p in upper if not p in lower]

def project_pt_lim(segm, pt): # ограниченная проекция точки на отрезок
    v1, v2=np.subtract(segm[1], segm[0], dtype=float), np.subtract(pt, segm[0], dtype=float)
    denom, nom=np.dot(v1,v1), np.dot(v1, v2)
    return segm[0] + max(0,min(denom, nom))*v1/denom

def project_ngon_pt(ngon, pt): # проекция точки на многоугольник
    p,dmin=None, np.inf
    for i in range(len(ngon)):
        p2=project_pt_lim([ngon[i-1], ngon[i]], pt)
        if (d:=dist(pt, p2)) < dmin: p, dmin = p2, d
    return p

def place_pts_into_ngon(pts, ngon, k0=0.5): # перенос и масштабирование точек внутри многоугольника
    c1, c2 = np.mean(pts, axis=0), np.mean(ngon, axis=0)
    approx_r1=max(dist(p, c1) for p in pts)
    approx_r2=sum(dist(p1, p2) for p1, p2 in zip(ngon, [*ngon[1:],ngon[0]]))/2/np.pi
    k=k0*approx_r2/approx_r1
    return [(p-c1)*k+c2 for p in pts]

def repell_pts_from_ngon(pts, ngon, target_dist=100):  #отталкивание точек друг от краев многоугольника
    res = [[*p] for p in pts]
    for i in range(len(pts)):
        v=np.subtract(pts[i], project_ngon_pt(ngon, pts[i]))
        d=np.linalg.norm(v)
        res[i] += v * min(target_dist * 0.1, target_dist / d ** 3)
    return res

def repell_pts(pts, target_dist=100): #отталкивание точек друг от друга
    res=[[*p] for p in pts]
    for i in range(len(pts)):
        for j in list(range(i))+list(range(i+1, len(res))):
            v=np.subtract(pts[j], pts[i])
            d=np.linalg.norm(v)
            res[j] +=  v * min(target_dist * 0.1, target_dist / d ** 3)
    return res

def fill_ngon_with_pts_triangular(num_pts, ngon, k=0.95): #заполнение многоугольника по треугольной сетке требуемым числом точек
    area = ngon_area(ngon) #WARN: DEPENDENCY
    r, h = k * (area / num_pts) ** 0.5, k * np.sqrt(3)/2 * (area / num_pts) ** 0.5
    (x0, y0), (x1, y1) = np.min(ngon, axis=0), np.max(ngon, axis=0)
    pp, delta_x, delta_s, s_sum = [], h / 2, r * h / 2, 0
    for i, y in enumerate(np.arange(y0 + h / 2, y1, h)):
        d = delta_x/2 if i % 2 == 0 else -delta_x/2
        for x in np.arange(x0 + d, x1, r):
            if (s_sum:=s_sum + delta_s) > area: break
            if pt_inside_ngon([x, y], ngon): pp.append([x, y]) #WARN: DEPENDENCY
    if (z := len(pp) - num_pts) > 0:
        for d, p in sorted([pt_ngon_dist(p, ngon), p] for p in pp)[:z]: pp.remove(p) #WARN: DEPENDENCY
    return pp

def fill_ngon_with_pts_square_auto(step, ngon): #заполнение многоугольника точками по квадратной сетке с нужным шагом
    (x0, y0), (x1, y1), pp = np.min(ngon, axis=0), np.max(ngon, axis=0), []
    for i, y in enumerate(np.arange(y0 + step / 2, y1, step)):
        for x in np.arange(x0 + step / 2, x1, step):
            if pt_inside_ngon([x, y], ngon): pp.append([x, y]) #WARN: DEPENDENCY
    return pp

#SHORTER VERSIONS
# отрисовка стрелки по точке и углу
def draw_arrow(screen, color, p0, ang, lenpx, w):
    p1 = [p0[0] + lenpx * math.cos(ang), p0[1] + lenpx * math.sin(ang)]
    p2, p3 = np.subtract(p1, rot([10,0], ang + 0.5)), np.subtract(p1, rot([10,0], ang - 0.5))
    for a,b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)
    
# отрисовка стрелки по 2 точкам
def draw_arrow2(screen, color, p0, p1, w): # отрисовка стрелки по 2 точкам
    ang=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
    p2, p3 = np.subtract(p1, rot([10,0], ang + 0.5)), np.subtract(p1, rot([10,0], ang - 0.5))
    for a,b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)

