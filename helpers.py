#Various helper functions (author: Sekou Diane, 2024-2025)

def draw_text(screen, s, x, y, sz=15, с=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, с), (x, y))

def draw_multiline_text(screen, text, pos, sz=25, color=(0,0,0), transf=False):
    for i,t in enumerate(text.split("\n")): # отрисовка многострочного текста
        draw_text(screen, t, [pos[0], pos[1]+sz*i], sz, color, transf)
    
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

def rot(v, ang): #поворот вектора на угол
    s, c = math.sin(ang), math.cos(ang)
    return [v[0] * c - v[1] * s, v[0] * s + v[1] * c]

def lim_ang(ang): #ограничение угла в пределах +/-pi
    while ang > math.pi: ang -= 2 * math.pi
    while ang <= -math.pi: ang += 2 * math.pi
    return ang

def ang_to(p1, p2): # Угол от 1 точки на 2 точку
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    
def dist(p1, p2): #расстояние между точками
    return np.linalg.norm(np.subtract(p2, p1))

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
    if 0 <= t <= 1 and 0 <= u <= 1: return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    return None

#пересечения отрезка с прямоугольником
def get_segm_intersection_rect(A, B, x, y, w, h):
    res, pp=[], [[x,y], [x+w,y], [x+w,y+h], [x,y+h]]
    for i in range(4):
        p1, p2 = pp[i-1], pp[i]
        p=get_segm_intersection(A, B, p1, p2)
        if p: res.append(p)
    return res
    
#пересечения отрезка с окружностью
def get_segm_intersection_circle(A, B, pos, R, full_line=False, tangent_tol=1e-9):
    (p1x, p1y), (p2x, p2y), (cx, cy) = A, B, pos
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** .5
    big_d = x1 * y2 - x2 * y1
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

#проверяем, находится ли точка внутри многоугольника
def pt_inside_ngon(point, vertices):
    (x, y), c = point, 0
    for i in range(len(vertices)):
        (x1, y1), (x2, y2) = vertices[i-1], vertices[i]
        if min(y1,y2) <= y < max(y1, y2):
            ratio = (y - y1) / (y2 - y1)
            c ^= (x - x1 < ratio*(x2 - x1))
    return c

#определяем точки, лежащие внутри многоугольника
def get_pts_inside_ngon(ngon_pts, xmin, xmax, ymin, ymax, step=20):
    pts=[]
    for x in range(xmin, xmax, step):
        for y in range(ymin, ymax, step):
            check = pt_inside_ngon([x, y], ngon_pts)
            if check: pts.append([x,y])
    return pts
    
#определяем периметр многоугольника
def polygon_perimeter(points):
    res=0
    for i in range(len(points)):
        A, B=points[i], points[(i+1)%len(points)]
        res+=dist(A, B)
    return res
    
#определяем площадь многоугольника
def polygon_area(coords):
    x, y = [p[0] for p in coords], [p[1] for p in coords] # get x and y in vectors
    x_, y_ = x - np.mean(x), y - np.mean(y) # shift coordinates
    main_area = np.dot(x_[:-1], y_[1:]) - np.dot(y_[:-1], x_[1:]) # calculate area
    correction = x_[-1] * y_[0] - y_[-1] * x_[0]
    return 0.5 * np.abs(main_area + correction)

#отрисовка стрелки по точке и углу
def arrow(screen, color, p0, angle, lenpx, w):
    p1 = [p0[0] + lenpx * math.cos(angle), p0[1] + lenpx * math.sin(angle)]
    p2 = [p1[0] - 10 * math.cos(angle + 0.5), p1[1] - 10 * math.sin(angle + 0.5)]
    p3 = [p1[0] - 10 * math.cos(angle - 0.5), p1[1] - 10 * math.sin(angle - 0.5)]
    for a,b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)
    
#отрисовка стрелки по 2 точкам
def arrow2(screen, color, p0, p1, w):
    angle=math.atan2(p1[1]-p0[1],p1[0]-p0[0])
    p2 = [p1[0] - 10 * math.cos(angle + 0.5), p1[1] - 10 * math.sin(angle + 0.5)]
    p3 = [p1[0] - 10 * math.cos(angle - 0.5), p1[1] - 10 * math.sin(angle - 0.5)]
    for a,b in [[p0, p1], [p1, p2], [p1, p3]]: pygame.draw.line(screen, color, a, b, w)

#формирование нескольких различных цветов
def get_some_colors():
    return [(220, 0, 0), (0, 220, 0), (0, 0, 220),
     (150, 150, 0), (0, 150, 150), (150, 0, 150),
     (120, 50, 50), (50, 120, 50), (50, 50, 120),
     (100, 100, 50), (50, 100, 100), (100, 50, 100)]

#сохранение скриншота в pygame
def save_screenshot(screen):
    import time, datetime as dt
    frmt_date = dt.datetime.fromtimestamp(
        time.time()).strftime("%Y-%m-%d(%H-%M-%S)")
    pygame.image.save(screen, frmt_date+".png")

#функция для запроса текста
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
    
#функция для запроса многострочного текста
def ask_multiline_string(text="", cap="Введите текст", tit="Текст объекта:"):
    (root := tk.Tk()).title(cap)
    ttk.Label(root, text=tit, font=("Bold", 12)).grid(column=0, row=1)
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=8, font=("Times New Roman", 15))
    text_area.insert(tk.INSERT, text)
    text_area.grid(column=0, row=2,  columnspan=2, pady=10, padx=10)
    result=""
    def read_text():
        nonlocal result, root
        result = text_area.get("1.0", tk.END).strip()
        root.quit()
    def cancel():
        nonlocal result, root
        result = None
        root.quit()
    text_area.focus()
    btn = ttk.Button(root, text="OK", command=read_text)
    btn.grid(column=0, row=3, pady=10, padx=0)
    btn2 = ttk.Button(root, text="Cancel", command=cancel)
    btn2.grid(column=1, row=3, pady=10, padx=0)
    root.mainloop()
    root.destroy()
    return result
