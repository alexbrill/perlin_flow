import pygame
from pygame import *
from sys import exit
from PERLIN import *
from math import sin, cos, pi, floor, sqrt
from random import random

SIZE  = W, H = (600, 600)
NAME  = "PERLIN FLOW"
FPS   = 30
WHITE = (255, 255, 255)
BLACK = (0  , 0  , 0  )
GREY  = (51 , 51 , 51 )

scl = 25
cols = floor(W / scl)
rows = floor(H / scl)
inc = 0.1
z_inc = 0.000075
quan = 150
max_speed = 2

def randcol():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def dist(x0, y0, x1 = 0, y1 = 0):
    return sqrt((x1 - x0)**2 + (y1 - y0)**2)

def rotate(x, y, a, off_x = 0, off_y = 0):
    rx = x * cos(a) - y * sin(a) + off_x
    ry = x * sin(a) + y * cos(a) + off_y
    return [rx, ry]

def fromAngle(a, l = 1):
    return rotate(0, -l, a)

class vect:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def get(self):
        return [self.x, self.y]

    def get_r(self):
        return [round(self.x), round(self.y)]

    def add(self, vect2):
        self.x = self.x + vect2.x
        self.y = self.y + vect2.y

    def sum(self, added):
        return vect(self.x + added.x, self.y + added.y)

    def mult(self, scl):
        self.x = self.x * scl
        self.y = self.y * scl

    def limit(self, const):
        d = dist(self.x, self.y)
        if d > const:
            scl = const / d
            self.mult(scl)


class Particle:
    def __init__(self):
        self.pos = vect(randint(0, W-1), randint(0, H-1))
        self.vel = vect()
        self.acc = vect()
        self.r = 4
        self.col = randcol()

    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(max_speed)
        self.pos.add(self.vel)
        self.acc.mult(0)
        self.edges()

    def applyForce(self, force):
        self.acc.add(force)

    def show(self, screen1, screen2):
        draw.circle(screen2, self.col, self.pos.get_r(), 1)
        draw.circle(screen1, self.col, self.pos.get_r(), self.r)

    def edges(self):
        if self.pos.x < 0:
            self.pos.x = W - 1
        if self.pos.x >= W:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = H - 1
        if self.pos.y >= H:
            self.pos.y = 0

    def follow(self, vectors):
        x = floor(self.pos.x / scl)
        y = floor(self.pos.y / scl)
        index = x + y * cols
        #print(self.pos.x, x, self.pos.y, y, index)
        force = vectors[index]
        force.mult(0.1)
        self.applyForce(force)
        
        

def run():
    pygame.init()
    display.set_caption(NAME)
    screen = display.set_mode(SIZE)
    fig = pygame.Surface(SIZE)
    clock = time.Clock()
    noise = SimplexNoise()
    noise.randomize(randint(1, 100))
    xoff = 0
    yoff = 0
    zoff = 0
    particles = []
    flowfield = []

    for i in range(quan):
        particles.append(Particle())
    
    while 1:
        #clock.tick(FPS)
        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
                
        screen.fill(WHITE)
        
        flowfield.clear()
        yoff = 0
        for i in range(cols):
            xoff = 0
            for j in range(rows):
                a = (noise.noise3(xoff, yoff, zoff) + 1) / 2 * 2 * pi
                temp_v = fromAngle(a, scl)
                v = vect(temp_v[0], temp_v[1])
                flowfield.append(v)
                #v_st = vect(i*scl, j*scl)
                #v_end = v_st.sum(v)
                #draw.line(screen, GREY, v_st.get(), v_end.get(), 2)
                xoff = xoff + inc
            yoff = yoff + inc
            zoff = zoff + z_inc

        for el in particles:
            el.follow(flowfield)
            el.update()
            el.show(screen, fig)
            
        fig.set_alpha(100)
        screen.blit(fig, (0, 0))
        display.update()
    

if __name__ == "__main__":
    run()
