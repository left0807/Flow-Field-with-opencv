from random import random
import numpy as np
import cv2

colors = [
    [(255, 238, 0),
    (255, 250, 184),
    (255, 255, 255),
    (255, 250, 184),
    (255, 240, 199),
    (232, 132, 245)],
    [    
    (0, 0, 51),      # Dark navy blue
    (0, 0, 102),     # Dark blue
    (0, 0, 128),     # Navy blue
    (0, 0, 153),     # Dark blue (X11)
    (0, 0, 205),     # Medium blue
    (25, 25, 112),   # Midnight blue
    (46, 49, 146),   # Ultramarine blue
    (65, 105, 225),  # Royal blue
    (70, 130, 180),  # Steel blue
    (72, 61, 139),   # Dark slate blue
    (79, 148, 205),  # Light slate blue
    (100, 149, 237), # Cornflower blue
    (106, 90, 205),  # Slate blue
    (119, 136, 153), # Light slate gray
    (123, 104, 238)
    ],
    [    
    (255, 36, 0),    # Bright red
    (255, 99, 71),   # Tomato
    (255, 140, 0),   # Dark orange
    (255, 165, 0),   # Orange
    (255, 215, 0),   # Gold
    (255, 246, 143), # Banana yellow
    (255, 255, 255), # White
    (255, 99, 0),    # Orange-red
    (255, 0, 0),     # Red
    (218, 165, 32),  # Goldenrod
    (184, 134, 11),  # Dark goldenrod
    (255, 192, 203), # Pink
    (255, 105, 180), # Hot pink
    (255, 69, 0),    # Red-orange
    (210, 105, 30),  # Chocolate
    (139, 0, 0),     # Dark red
    (128, 0, 0) ]
    ]

class Particles():
    def __init__(self, width, height, scl, maxspeed, theme, radius):
        self.width = width
        self.height = height
        self.scl = scl
        self.pos = np.array([random()*width, random()*height])
        self.prepos = self.pos.copy()
        self.vel = np.array([0.0, 0.0])
        self.maxspeed = maxspeed
        self.radius = radius
        self.setColour(theme)

    def setColour(self, theme):
        self.color = colors[theme][int(random()*len(colors[theme]))][::-1]

    def update(self, force):   
        self.vel = (self.vel + force)*self.maxspeed
        self.pos += self.vel
    
    def show(self, canvas):
        cv2.line(canvas, self.pos.astype(int), self.prepos.astype(int),
                 self.color, self.radius)
        self.edges()
        self.prepos = self.pos.copy()

    def edges(self):
        self.pos = np.remainder(self.pos, [self.width, self.height]);

        # if self.pos[1] > self.width or self.pos[1] < 0 or self.pos[0] > self.height or self.pos[0] < 0:
        #     self.__init__(self.width, self.height, self.scl)