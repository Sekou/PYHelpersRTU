#by S. Diane, 2024
import sys, pygame
import numpy as np
import math

class Edge:
    def __init__(self, n1, n2, w):
        self.n1=n1
        self.n2=n2
        self.w=w
    def draw(self, screen):
        pygame.draw.line(screen, (0,0,0), self.n1.getPos(), self.n2.getPos())

class Node:
    def __init__(self, x, y):
        self.x, self.y=x, y
        self.nextEdges=[]
    def getPos(self):
        return [self.x, self.y]
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), self.getPos(), 4, 0)
        for e in self.nextEdges:
            e.draw(screen)

class Graph:
    def __init__(self, pts):
        self.nodes=[Node(*p) for p in pts]
    def draw(self, screen):
        for n in self.nodes:
            n.draw(screen)
    def connect(self):
        for n1 in self.nodes:
            for n2 in self.nodes:
                if n1==n2: continue
                w=np.linalg.norm(np.subtract(n1.getPos(), n2.getPos()))
                n1.nextEdges.append(Edge(n1, n2, w))

# import simple_graph
# graph=simple_graph.Graph(pts)
# graph.connect()