#2026, S. Diane, implementation of Dijkstra algorithm for area visibility graph
import math, sys, pygame, numpy as np

pygame.font.init()
def draw_text(screen, s, x, y, sz=15, c=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, c), (x, y))

sz = (800, 600)

def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2)) #расстояние между точками
def rot(v, ang): return np.dot([[-v[1], v[0]], v],[math.sin(ang), math.cos(ang)]) # поворот вектора на угол
def lim_ang(ang, arc=3.141592653589793): return (ang - 2 * arc) if ang > arc else (ang + 2 * arc) if ang <= -arc else ang
def get_corner(p1, p, p2): return lim_ang(math.atan2(p1[1]-p[1], p1[0]-p[0])-math.atan2(p2[1]-p[1], p2[0]-p[0])) #угол
def get_normal(p1, p2): #единичный вектор, повернутый по часовой стрелке (в экранной СК)
    return np.array([[0,1],[-1,0]])@np.subtract(p2, p1)/((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)**0.5
def inc_segment(p1, p2, eps=1): #увеличение или сокращение отрезка
    u = np.array(np.subtract(p2, p1), dtype=np.float64)
    return list([p1, p2]+np.array((u, -u))*eps/np.linalg.norm(u))
def pt_segm_dist2(p, p1, p2): # расстояние от точки до ограниченного отрезка
    k = (p2[1]-p1[1]) / (0.0000001 if p2[0]==p1[0] else (p2[0]-p1[0]))
    d = np.abs(k * (p1[0] - p[0]) - p1[1] + p[1]) /(k * k + 1)**0.5  # числитель: p[1]-(k*p[0]+b)
    v1,v12,v2=np.subtract(p, p1), np.subtract(p2, p1), np.subtract(p, p2)
    return d if 0 < v1 @ v12 / (v12@v12) < 1 else min(v1@v1, v2@v2)**0.5
def check_intersection(A,B,C,D): # проверка пересечения двух отрезков
    ccw = lambda A, B, C: (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

class Ngon:
    def __init__(self, pts):
        self.pts=pts
        self.inflated=[]
    def draw(self, screen):
        for i in range(len(self.pts)): # for p1,p2 in zip(self.pts, self.pts[1:]+self.pts[:1]):
            pygame.draw.line(screen, (0,0,0), self.pts[i-1], self.pts[i], 2)
        if len(self.inflated):
            for i in range(len(self.inflated)):
                pygame.draw.line(screen, (0, 0, 255), self.inflated[i - 1], self.inflated[i], 1)
    def inflate(self, r):
        vv=[]
        for i in range(len(self.pts)):
            p1, p2 = self.pts[i-1], self.pts[i]
            n=get_normal(p1, p2)
            vv.extend([p1+n*r, p2+n*r, [0,0]])
        for i in range(len(self.pts)):
            p0, p1, p2 = self.pts[i-1], self.pts[i], self.pts[(i+1)%len(self.pts)]
            c, d=get_corner(p0, p1, p2), np.subtract(p1, p0)
            p=p1+rot(r*d/np.linalg.norm(d), -c/2)
            vv[i*3+2]=p
        self.inflated=vv
        return vv
    def check_collision(self, p1, p2, r):
        p1, p2= inc_segment(p1, p2, 1)
        for i in range(len(self.pts)):
            if check_intersection(self.pts[i - 1], self.pts[i], p1, p2): return True
            if pt_segm_dist2(self.pts[i], p1, p2)<r: return True
        return False

class Node:
    def __init__(self, x, y): self.x, self.y, self.edges=x, y, []
    def get_pos(self): return [self.x, self.y]
    def draw(self, screen):
        pygame.draw.circle(screen, (255,0,0), self.get_pos(), 7, 1)
        for e in self.edges: pygame.draw.line(screen, (255,0,0), e.n1.get_pos(), e.n2.get_pos(), 1)
class Edge:
    def __init__(self, n1, n2): self.n1,self.n2,self.w=n1, n2, dist(n1.get_pos(), n2.get_pos())
class Graph:
    def __init__(self, start, goal, objs, r):
        pts = [p for ng in objs for p in ng.inflated]
        self.nodes=[Node(*start)] + [Node(x,y) for x,y in pts] + [Node(*goal)]
        for i in range(len(self.nodes)):
            for j in range(i+1, len(self.nodes)):
                if not any([o.check_collision(self.nodes[j].get_pos(), self.nodes[i].get_pos(), r) for o in objs]):
                    self.nodes[i].edges.append(Edge(self.nodes[i], self.nodes[j]))
                    self.nodes[j].edges.append(Edge(self.nodes[j], self.nodes[i]))
    def draw(self, screen):
        for n in self.nodes: n.draw(screen)
    def find_route(self, n1, n2):
        for n in self.nodes: n.visited, n.D, n.route = False, 100500, []
        n1.D, n1.route, wave = 0, [n1], [n1]
        while len(wave):
            v=wave.pop(np.argmin([n.D for n in wave]))
            v.visited, next = True, [e for e in v.edges if not e.n2.visited]
            for e in next: #если текущ. вершина лучше соседа, то обновл. соседа
                if e.n2.D > v.D+e.w: e.n2.D, e.n2.route=v.D+e.w, v.route+[e.n2]
                wave.append(e.n2) #берем соседа в фронт поиска
        return list(reversed(n2.route))

if __name__ == "__main__":
    screen, timer, fps = pygame.display.set_mode(sz), pygame.time.Clock(), 20
    pygame.display.set_caption('Animation 2D')
    dt = 1 / fps

    ngons=[Ngon([[200,200],[300,300],[150,300]]),
           Ngon([[500,400],[650,400],[650,500],[500,500]])]

    r=20
    for n in ngons: n.inflate(r)

    g=Graph([50,50], [750, 550], ngons, r*0.8)

    route=[]
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    route=g.find_route(g.nodes[0], g.nodes[-1])

        screen.fill((255, 255, 255))
        for n in ngons: n.draw(screen)
        g.draw(screen)
        for i in range(1, len(route)):
            pygame.draw.line(screen, (100,100,255), route[i - 1].get_pos(), route[i].get_pos(), 4)

        L=sum([dist(p1.get_pos(), p2.get_pos()) for p1, p2 in zip(route[:-1], route[1:])])

        draw_text(screen, f"L = {L:.2f}", 5, 5)
        pygame.display.flip(), timer.tick(fps)
