from pygame import font
from pygame import Surface
from pygame.draw import circle as draw_circle
from pygame.draw import line as draw_line
from pygame.draw import rect as draw_rect
from pygame import Rect
import pygame
import sys
font.init()

def update_on_call(fn):
    def wrapper(*args, **kwargs):
        resp = fn(*args, **kwargs)
        Visual.update()
        return resp


    return wrapper

class Visual:
    instances = []
    def __init__(self, window, clock, bg, graph) -> None:
        self.window = window
        self.clock = clock
        self.bg = bg
        self.graph = graph
        Visual.instances += [self]

        self.previously_pressed = False
        self.pass_pause = False

    def update(self=None):
        if self != None:
            self.graph.draw(self.window)
            return
        for vi in Visual.instances:
            vi.graph.draw(vi.window)

    def pause(self):
        while(1):
            self.main()
            if self.pass_pause:
                self.pass_pause = False
                return

    def main(self):
        self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and not self.previously_pressed:
            self.pass_pause = True
            self.previously_pressed = True
        if not keys[pygame.K_RETURN] and self.previously_pressed:
            self.pass_pause = False
            self.previously_pressed = False

        self.window.fill(self.bg)
        self.update()
        pygame.display.update()

class Point:
    def __init__(self,x,y):
        self.x,self.y = x,y

    def __add__(self, _o):
        if isinstance(_o, Point):
            x = self.x + _o.x
            y = self.y + _o.y
            return Point(x,y)
        if isinstance(_o, int):
            x = self.x + _o
            y = self.y + _o
            return Point(x,y)

    def __sub__(self, _o):
        if isinstance(_o, Point):
            x = self.x - _o.x
            y = self.y - _o.y
            return Point(x,y)
        if isinstance(_o, int):
            x = self.x - _o
            y = self.y - _o
            return Point(x,y)

    def __truediv__(self, _o):
        if isinstance(_o, int):
            x = self.x / _o
            y = self.y / _o
            return Point(x,y)


    def __getitem__(self, key: int):
        return [self.x,self.y][key]

    def tuple(self):
        return (self.x, self.y)

class Graph:
    global_font = font.SysFont('Aerial', 30)
    def __init__(self, points, edges, adjacency_matrix=[]) -> None:
        self.points = points
        self.edges = edges
        self.adj_matrix = adjacency_matrix

    def draw(self, surface: Surface, rx=0, ry=0):
        for obj in self.edges + self.points:
            obj.draw(surface, rx, ry)

        

class Vertex:
    v_id = 1
    vs = []
    radius = 20
    color = (0,0,0)
    border_radius = 2
    border_color = (255,255,255)
    font_color = (255,255,255)

    def __init__(self,x,y,label=None,radius=radius, color=color, border_radius=border_radius, border_color=border_color, font_color=font_color):
        if label == None:
            label = Vertex.v_id
            Vertex.v_id += 1
        self.id = label
        self.x,self.y = x,y
        self.label = label
        self.radius = radius
        self.color = color
        self.border_radius = border_radius
        self.border_color = border_color
        self.font_color = font_color

        self.edges = []
        

        self.hide = 0
        Vertex.vs.append(self)

    def get(id):
        return Vertex.vs[id-1]

    def add_edges(self, edges):
        if edges != []:
            self.edges.append(edges)
            return
        self.edges += edges

    def draw(self, surface: Surface, _rx=0, _ry=0):
        draw_circle(surface, self.border_color, (self.x + _rx, self.y + _ry), self.radius + self.border_radius)
        draw_circle(surface, self.color, (self.x + _rx, self.y + _ry), self.radius)
        txt = Graph.global_font.render(str(self.label), False, self.font_color)
        w,h = txt.get_size()
        surface.blit(txt, (self.x - w/2,self.y - h/2))

    @property
    def center(self) -> Point:
        return Point(self.x, self.y)

    @update_on_call
    def __setattr__(self, __name: str, __value) -> None:
        super().__setattr__(__name, __value)

class Edge:
    e_id = 1
    es = []
    width = 3
    color = (255,255,255)
    font_color = (255,255,255)

    def __init__(self,p1: Point ,p2: Point, color=color, width=width, dotted=0, weight:int=None, font_color=font_color, v1: Vertex=None,v2: Vertex=None, show_w=False):
        self.id = Edge.e_id
        Edge.e_id += 1

        self._p1 = p1
        self._p2 = p2
        self.v1 = v1
        self.v2 = v2
        self.width = width
        self.color = color
        self.dotted = dotted
        self.weight = weight
        self.font_color = font_color

        self.show_w = show_w

        Edge.es.append(self)

    def get(id):
        return Edge.es[id-1]

    @update_on_call
    def __setattr__(self, __name: str, __value) -> None:
        super().__setattr__(__name, __value)

    @property
    def p1(self):
        return self._p1.tuple()
    @property
    def p2(self):
        return  self._p2.tuple()

    def draw(self, surface: Surface, _rx=0 , ry=0):
        draw_line(surface, self.color, self.p1, self.p2, self.width)
        if self.weight != None and self.show_w:
            rxy = self._p1/2 + self._p2/2
            txt = Graph.global_font.render(str(self.weight), False, self.font_color)
            w,h = txt.get_size()
            draw_rect(surface, (0,0,0), Rect((rxy - (Point(w,h)+10)/2).tuple(),(Point(w,h)+10).tuple()))
            surface.blit(txt, (rxy - Point(w,h)/2).tuple())


