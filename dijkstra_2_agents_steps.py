# Finding route on a lattice graph with excluded edges for obstacles
# S. Diane, 2026
import sys, pygame, numpy as np, math

pygame.font.init()
DEBUG=True

def draw_text(screen, s, x, y, sz=20, color=(0, 0, 0)): # отрисовка текста
    screen.blit(pygame.font.SysFont('Comic Sans MS', sz).render(s, True, (0, 0, 0)), (x, y))
def check_intersection(A, B, C, D):  # проверка пересечения двух отрезков
    ccw = lambda A, B, C: (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
def rot(v, ang): return np.dot([[-v[1], v[0]], v], [math.sin(ang), math.cos(ang)])  # поворот вектора на угол
def rot_arr(vv, ang): return [rot(v, ang) for v in vv]  # функция для поворота массива на угол
def dist(p1, p2): return np.linalg.norm(np.subtract(p2, p1))  # расстояние между точками

class Obstacle:  # препятствие
    def __init__(self, x, y, ang, L, W):
        self.x, self.y, self.ang, self.L, self.W = x, y, ang, L, W
    def get_all_pts(self):
        pp = [[i * self.L / 2, j * self.W / 2] for i, j in [[-1, -1], [1, -1], [1, 1], [-1, 1]]]
        return np.add(rot_arr(pp, self.ang), self.get_pos())
    def intersects(self, segment):
        pts = self.get_all_pts()
        for a, b in zip(pts, list(pts[1:]) + list(pts[:1])):
            if check_intersection(a, b, *segment): return True
        return False
    def draw(self, screen): pygame.draw.lines(screen, (0, 0, 0), True, self.get_all_pts(), 2)
    def get_pos(self): return [self.x, self.y]

class Node:
    def __init__(self, x, y):
        self.x, self.y, self.edges, self.vA, self.vB = x, y, [], None, None
        self.visited, heuristic=False, 0
    def get_pos(self): return [self.x, self.y]
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.get_pos(), 7, 1)
        for e in self.edges: pygame.draw.line(screen, (255, 0, 0), e.n1.get_pos(), e.n2.get_pos(), 1)
    def draw_highlight(self, screen, color, r):
        pygame.draw.circle(screen, color, self.get_pos(), r, 3)

class Edge:
    def __init__(self, n1, n2): self.n1, self.n2, self.w = n1, n2, dist(n1.get_pos(), n2.get_pos())

class Graph:
    def __init__(self, objs, step):
        self.step,self.wave,self.show_heuristic = step, [], False
        pts = [[[x, y] for x in range(0, sz[0], step)] for y in range(0, sz[1], step)]
        self.nodes = [[Node(*p) for p in line] for line in pts]
        def get_nbrs(ix, iy, nodes):
            inds = [[x + ix, y + iy] for x, y in [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]]
            inds = [[x, y] for x, y in inds if 0 <= y < len(nodes) and 0 <= x < len(nodes[y])]
            p1 = self.nodes[iy][ix].get_pos()
            collisions = [objs[0].intersects([p1, self.nodes[i][j].get_pos()]) for j, i in inds]
            inds = [i for i, c in zip(inds, collisions) if not c]
            return [nodes[y][x] for x, y in inds]
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[0])):
                nbrs = get_nbrs(j, i, self.nodes)
                for nb in nbrs:
                    self.nodes[i][j].edges.append(Edge(self.nodes[i][j], nb))
                    nb.edges.append(Edge(nb, self.nodes[i][j]))
    def get_all_nodes(self):
        return [n for row in self.nodes for n in row]
    def draw(self, screen):
        for n in self.get_all_nodes():
            n.draw(screen)
            if DEBUG:
                if n.visited: n.draw_highlight(screen, (0,0,0), 5)
                if graph.show_heuristic: draw_text(screen, f"{n.heuristic:.1f}", *n.get_pos(), 8)
        if DEBUG:
            for n in self.wave: n.draw_highlight(screen, (0,200,200), 4)
    def find_nearest_node(self, pos):
        all_nodes = self.get_all_nodes()
        dd = [dist(n.get_pos(), pos) for n in all_nodes]
        return all_nodes[np.argmin(dd)]

    # MASTER ROUTE
    def H1(self, node, obstacle, n2a, n2b): #эвристика 1
        L = dist(n2a.get_pos(), n2b.get_pos())
        res = dist(node.get_pos(), n2a.get_pos())
        nn = [n for n in self.get_all_nodes() if abs(L - dist(n.get_pos(), node.get_pos())) < L / 10]
        collision = [obstacle.intersects([node.get_pos(), n.get_pos()]) for n in nn]
        return res * (1 + 100 * sum(collision) / len(nn))
    def calc_heuristic1(self, obstacle, n2a, n2b):
        for node in self.get_all_nodes():
            node.heuristic = self.H1(node, obstacle, n2a, n2b)
    def find_route_step1(self, obstacle, n1a, n1b, n2a, n2b, iter):
        if iter==0:
            all_nodes = self.get_all_nodes()
            for n in all_nodes: n.visited, n.D, n.route = False, 100500, []
            n1a.D, n1a.route, self.wave = 0, [n1a], [n1a]
        # elif (not use_heuristic and not n2.visited) or (use_heuristic and len(self.wave)):
        elif not n2a.visited:
            v = self.wave.pop(np.argmin([n.D + self.H1(n, obstacle, n2a, n2b) for n in self.wave]))
            v.visited, next = True, [e for e in v.edges if not e.n2.visited]
            for e in next: # если текущ. вершина лучше соседа, то обновл. соседа
                if e.n2.D > v.D + e.w: e.n2.D, e.n2.route = v.D + e.w, v.route + [e.n2]
                if not e.n2 in self.wave: self.wave.append(e.n2) # берем соседа в фронт поиска
        else: return list(reversed(n2a.route))
        return None

    # SLAVE ROUTE
    def H2(self, node, obstacle, n2a, n2b, path1): #эвристика 2
        L = dist(n2a.get_pos(), n2b.get_pos())
        res = dist(node.get_pos(), n2a.get_pos())
        res+= 5*min([abs(dist(node.get_pos(), n.get_pos())-L) for n in path1]) # учет жесткости балки
        res+= -min([L]+[dist(node.get_pos(), n.get_pos()) for n in path1]) # учет расстояния до 1-го маршрута
        nn = [n for n in self.get_all_nodes() if abs(L - dist(n.get_pos(), node.get_pos())) < L / 10]
        return res
    def calc_heuristic2(self, obstacle, n2a, n2b, path1):
        for node in self.get_all_nodes():
            node.heuristic = self.H2(node, obstacle, n2a, n2b, path1)
    def find_route_step2(self, obstacle, path1, n1a, n1b, n2a, n2b, iter):
        if iter == 0:
            all_nodes = self.get_all_nodes()
            for n in all_nodes: n.visited, n.D, n.route = False, 100500, []
            n1b.D, n1b.route, self.wave = 0, [n1b], [n1b]
        # elif (not use_heuristic and not n2.visited) or (use_heuristic and len(self.wave)):
        elif not n2b.visited:
            v = self.wave.pop(np.argmin([n.D + self.H2(n, obstacle, n2a, n2b, path1) for n in self.wave]))
            v.visited, next = True, [e for e in v.edges if not e.n2.visited]
            for e in next:  # если текущ. вершина лучше соседа, то обновл. соседа
                if e.n2.D > v.D + e.w: e.n2.D, e.n2.route = v.D + e.w, v.route + [e.n2]
                if not e.n2 in self.wave: self.wave.append(e.n2)  # берем соседа в фронт поиска
        else: return list(reversed(n2b.route))
        return None

if __name__ == "__main__":
    sz, timer, fps = (800, 600), pygame.time.Clock(), 20
    screen, dt = pygame.display.set_mode(sz), 1 / fps

    obstacle = Obstacle(400, 300, 0, 180, 130)
    graph = Graph([obstacle], 50)

    route_a, route_b = None, None
    debug_node = None

    #Start
    n1a = graph.find_nearest_node((200, 200))
    n1b = graph.find_nearest_node((200, 400))

    #Finish
    n2a = graph.find_nearest_node([600, 200])
    n2b = graph.find_nearest_node([600, 400])

    iter, iter_found, iter2, iter2_found=0,0, 0,0
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: sys.exit(0)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    route_a = graph.find_route_step1(obstacle, n1a, n1b, n2a, n2b, iter)
                    if iter_found==0 and route_a is not None: iter_found=iter
                    iter=iter+1
                if ev.key == pygame.K_2:
                    if not graph.show_heuristic: graph.calc_heuristic1(obstacle, n2a, n2b)
                    graph.show_heuristic=not graph.show_heuristic
                if ev.key == pygame.K_3:
                    route_b = graph.find_route_step2(obstacle, route_a, n1a, n1b, n2a, n2b, iter2)
                    if iter2_found==0 and route_b is not None: iter2_found=iter2
                    iter2=iter2+1
                if ev.key == pygame.K_4:
                    if not graph.show_heuristic: graph.calc_heuristic2(obstacle, n2a, n2b, route_a)
                    graph.show_heuristic=not graph.show_heuristic
                if ev.key == pygame.K_5:
                    route_a, route_b = None, None
                    iter, iter_found, iter2, iter2_found = 0, 0, 0, 0
                    while route_a==None:
                        route_a=graph.find_route_step1(obstacle, n1a, n1b, n2a, n2b, iter)
                        if iter_found == 0 and route_a is not None: iter_found = iter
                        iter = iter + 1
                    while route_b==None:
                        route_b=graph.find_route_step2(obstacle, route_a, n1a, n1b, n2a, n2b, iter2)
                        if iter2_found == 0 and route_b is not None: iter2_found = iter2
                        iter2 = iter2 + 1
                if ev.key == pygame.K_0: DEBUG=not DEBUG

            if ev.type == pygame.MOUSEBUTTONDOWN:
                debug_node = graph.find_nearest_node(ev.pos)
                print(debug_node.get_pos())

        screen.fill((255, 255, 255))
        graph.draw(screen), obstacle.draw(screen)
        if debug_node is not None: pygame.draw.circle(screen, (200, 200, 0), debug_node.get_pos(), 20, 3)

        pygame.draw.circle(screen, (220, 100, 100), n1a.get_pos(), 15, 3)
        pygame.draw.circle(screen, (220, 100, 100), n1b.get_pos(), 15, 3)
        pygame.draw.circle(screen, (220, 100, 100), n2a.get_pos(), 7, 3)
        pygame.draw.circle(screen, (220, 100, 100), n2b.get_pos(), 7, 3)

        for route in [route_a, route_b]:
            if route is not None:
                for i in range(1, len(route)):
                    pygame.draw.line(screen, (0, 0, 255), route[i - 1].get_pos(), route[i].get_pos(), 2)

        if DEBUG:
            draw_text(screen, f"Iter = {iter} / {iter_found}", 5, 5)
            draw_text(screen, f"Iter2 = {iter2} / {iter2_found}", 5, 25)
        pygame.display.flip(), timer.tick(fps)

# template file by S. Diane, RTU MIREA, 2026
