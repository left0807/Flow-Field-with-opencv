from random import random
import math
import numpy as np
import cv2

star_colors = [
    (255, 238, 0),
    (255, 250, 184),
    (255, 255, 255),
    (255, 250, 184),
    (255, 240, 199),
    (232, 132, 245)
]

class Particles():
    def __init__(self, width, height, scl, maxspeed):
        self.width = width
        self.height = height
        self.scl = scl
        self.pos = np.array([random()*height, random()*width])
        self.prepos = self.pos.copy()
        self.vel = np.array([0.0, 0.0])
        self.maxspeed = maxspeed
        self.color = star_colors[int(random()*len(star_colors))][::-1]

    def update(self, force, canvas = None, hands = None, attractiveForceMag = None):   
        self.vel = (self.vel + force)*self.maxspeed

        for hand, handpos in hands:
            handpos = np.multiply(handpos, [self.height, self.width])
            v = handpos - self.pos
            v = v/(v**2).sum()**0.5
            self.vel = (self.vel + hand*attractiveForceMag*v)*self.maxspeed
            cv2.circle(canvas, handpos.astype(int), 10,  (255, 255, 255), 2)

        self.pos += self.vel
    
    def show(self, canvas):
        cv2.line(canvas, self.pos.astype(int), self.prepos.astype(int),
                 self.color, 1)
        self.edges()
        self.prepos = self.pos.copy()

    def edges(self):
        self.pos = np.remainder(self.pos, [self.height, self.width]);

        # if self.pos[1] > self.width or self.pos[1] < 0 or self.pos[0] > self.height or self.pos[0] < 0:
        #     self.__init__(self.width, self.height, self.scl)