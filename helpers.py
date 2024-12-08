def probSel(probs): #вероятностный выбор индекса элемента
    m, s, r=sum(probs), 0, np.random.rand()
    if m==0: return np.random.randint(len(probs))
    for i in range(len(probs)):
        s+=probs[i]/m
        if s>=r: return i
    return -1

def readPts(filename): #чтение массива целочисленных точек
    with open(filename, "r") as f:
        return [[int(v) for v in l.split()] for l in f.readlines()]

def rotSegm(segm, ang): #центральный поворот отрезка на угол
    c=np.mean(segm, axis=0)
    v1=np.subtract(segm[0], c)
    v2=np.subtract(segm[1], c)
    return list(np.add([rot(v1, ang), rot(v2, ang)], c))

def ptSegmDist(p, p1, p2): #расстояние от точки до отрезка
    dx, dy = np.subtract(p2, p1)
    k = dy / (0.0000001 if dx==0 else dx)
    b = p1[1] - k * p1[0]
    return np.abs(-k * p[0] + p[1] - b) / math.sqrt(k * k + 1)

def proj(segm, pt): #точка-проекция точки на отрезок
    v2=np.subtract(pt, segm[0], dtype=float)
    v1=np.subtract(segm[1], segm[0], dtype=float)
    v1_=v1/np.linalg.norm(v1)
    L2=np.dot(v1_, v2)
    return segm[0] + L2*v1_

def projCheck(segm, pt): #проверка попадания проецирцемой точки внетрь отрезка
    v2=np.subtract(pt, segm[0], dtype=float)
    v1=np.subtract(segm[1], segm[0], dtype=float)
    L1=np.linalg.norm(v1)
    return 0<=np.dot(v1/L1, v2)<=L1
