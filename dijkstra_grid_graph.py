import sys, pygame, numpy as np, math

pygame.font.init()
def draw_text(screen, s, x, y, sz=20, color=(0, 0, 0)):  # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, (0, 0, 0)), (x, y))
def dist(p1, p2): return np.linalg.norm(np.subtract(p1, p2))  # расстояние между точками
def lim_ang(ang, arc=3.141592653589793):  # ограничение угла в пределах +/-pi
    ang = ang % (2 * arc);
    return ang + (2 * arc if ang < -arc else -2 * arc if ang > arc else 0)
def rot(v, ang): return np.dot([[-v[1], v[0]], v], [math.sin(ang), math.cos(ang)])  # поворот вектора на угол
def rot_arr(vv, ang): return [rot(v, ang) for v in vv]  # функция для поворота массива на угол

class Obj:  # объект
    def __init__(self, x, y, ang, L, W):
        self.x, self.y, self.ang, self.L, self.W = x, y, ang, L, W
    def get_pos(self): return [self.x, self.y]
    def get_all_pts(self, r_inflate=0):
        a, b=self.L / 2+r_inflate, self.W / 2+r_inflate
        pp = [[i * a, j * b] for i, j in [[-1, -1], [1, -1], [1, 1], [-1, 1]]]
        return np.add(rot_arr(pp, self.ang), self.get_pos())
    def set_pos(self, p): self.x, self.y = p
    def draw(self, screen):
        pp = self.get_all_pts(0)
        pygame.draw.lines(screen, (0, 0, 0), True, pp, 2)

# проверяем, находится ли точка внутри многоугольника
def pt_inside_ngon(pt, points, foo=0): #ngon_contains_pt
    for (A, B), (C, D) in zip([*points[-1:], *points[:-1]], points):
        if min(B, D) <= pt[1] < max(B, D): foo ^= (pt[0] - A < (pt[1] - B) / (D - B) * (C - A))
    return foo

class Node:
    def __init__(self, x, y, cell_sz=0): self.x, self.y, self.edges, self.cell_sz = x, y, [], cell_sz
    def get_pos(self): return [self.x, self.y]
    def get_bb(self): return [self.x-self.cell_sz/2, self.y-self.cell_sz/2, self.cell_sz, self.cell_sz]
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.get_pos(), 4, 1)
        if self.cell_sz: pygame.draw.rect(screen, (200, 200, 200), [a+b for a,b in zip(self.get_bb(), [0,0,1,1])], 1)
        for e in self.edges: pygame.draw.line(screen, (255, 0, 0), e.n1.get_pos(), e.n2.get_pos(), 1)
class Edge:
    def __init__(self, n1, n2): self.n1, self.n2, self.w = n1, n2, np.linalg.norm(((n1.x-n2.x), (n1.y-n2.y)))
class Graph:
    def __init__(self, objs, x0, y0, W, H, step):
        pts = [[[x+x0, y+y0] for x in range(0, W, step)] for y in range(0, H, step)]
        self.nodes = [[Node(*p, step) for p in line] for line in pts]
        def get_nbrs(ix, iy, nodes):
            inds = [ix,iy]+np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])
            return [nodes[y][x] for x, y in inds if 0 <= y < len(nodes) and 0 <= x < len(nodes[y])]
        for i,j in [[a,b] for a in range(len(self.nodes)) for b in range(len(self.nodes[a]))]:
            if any(pt_inside_ngon(self.nodes[i][j].get_pos(), o) for o in objs): continue
            for nb in [_ for _ in get_nbrs(j, i, self.nodes) if all(not pt_inside_ngon(_.get_pos(), o) for o in objs)]:
                self.nodes[i][j].edges.append(Edge(self.nodes[i][j], nb))
                nb.edges.append(Edge(nb, self.nodes[i][j]))
    def draw(self, screen):
        for i in range(len(self.nodes)):
            for n in self.nodes[i]: n.draw(screen)
    def all_nodes(self): return [self.nodes[a][b] for a in range(len(self.nodes)) for b in range(len(self.nodes[a]))]
    def find_route(self, n1, n2):
        for n in self.all_nodes(): n.visited, n.D, n.route = False, 100500, []
        n1.D, n1.route, wave = 0, [n1], [n1]
        while len(wave):
            v = wave.pop(np.argmin([n.D for n in wave]))
            v.visited, next = True, [e for e in v.edges if not e.n2.visited]
            for e in next:  # если текущ. вершина лучше соседа, то обновл. соседа
                if e.n2.D > v.D + e.w: e.n2.D, e.n2.route = v.D + e.w, v.route + [e.n2]
                if not e.n2 in wave: wave.append(e.n2) # берем соседа в фронт поиска
        return list(reversed(n2.route))

if __name__ == "__main__":
    sz, timer, fps = (800, 600), pygame.time.Clock(), 20
    screen, dt = pygame.display.set_mode(sz), 1 / fps

    objs = [Obj(390, 300, 1, 200, 150)]

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1: print("Test")

        objs[0].ang+=0.05
        graph = Graph([o.get_all_pts(r_inflate=10) for o in objs], 15, 15, sz[0], sz[1], 25)
        route = graph.find_route(graph.nodes[3][3], graph.nodes[-3][-3])

        screen.fill((255, 255, 255))
        for o in objs: o.draw(screen)
        graph.draw(screen)

        for p1,p2 in zip(route[:-1],route[1:]):
            pygame.draw.line(screen, (0,0,0), p1.get_pos(), p2.get_pos(), 2)

        L=sum([dist(p1.get_pos(), p2.get_pos()) for p1, p2 in zip(route[:-1], route[1:])])

        draw_text(screen, f"L = {L:.2f}", 5, 5)

        pygame.display.flip(), timer.tick(fps)

# template file by S. Diane, RTU MIREA, 2024-2025
