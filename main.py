from graph import *
from config import Config
import pygame
import sys
from random import randint as rng
from queue import PriorityQueue

## Config
configuration = Config('config.txt',default={
    'bg-color':(0,0,0),
    "width":600,
    "height":600
}
).config

## Pygame
bg = [int(x) for x in configuration['bg-color']] # green screen
pygame.init()
clock = pygame.time.Clock()
height = int(configuration["height"])
width = int(configuration["width"])

window = pygame.display.set_mode((width,height))#, pygame.NOFRAME)
pygame.display.set_caption('Graph visualization')
#######


v = [Vertex(x%5*100 + 80, int(x/5) * 400 + 100) for x in range(10)]
e = []

a = [
    [0,0,2,0,9],
    [3,1,0,3,4],
    [0,0,10,9,0],
    [0,4,0,0,0],
    [1,0,0,0,0]
]

for x in range(5):
    for y in range(5):
        if a[x][y] != 0:
            s = Edge(v[x].center, v[y+5].center, v1=v[x],v2=v[y+5], weight=a[x][y])
            e.append(s)
            v[x].add_edges(s)
            v[y+5].add_edges(s)

visual = Visual(window, clock, bg,graph=Graph(v,e))


def prim(graph: Graph):
    soma = 0
    v_count = len(graph.points)
    root = graph.points[rng(0,9)]
    selected = set([root.id])
    edges_selected = []
    q = PriorityQueue()
    for e in root.edges:
        if e.v1 == root:
            q.put((e.weight, e.v2.id, e.id))
        else:
            q.put((e.weight, e.v1.id, e.id))


    while(len(selected) < v_count):
        visual.pause()
        if q.empty():
            return soma
        w, v_id, e_id = q.get()
        v, e = Vertex.get(v_id), Edge.get(e_id)
        while(v.id in selected):
            if q.empty():
                return soma
            w, v_id, e_id = q.get()
            v, e = Vertex.get(v_id), Edge.get(e_id)


        e.color = [200,100,40]
        edges_selected.append(e)
        selected.add(v.id)
        soma += w
        for new_edge in v.edges:
            if new_edge.v1.id == v_id:
                q.put((new_edge.weight, new_edge.v2.id, new_edge.id))
            else:
                q.put((new_edge.weight, new_edge.v1.id, new_edge.id))
    return soma, edges_selected


prim(visual.graph)
while(1):
    visual.main()