import numpy as np
import cv2
import math
import particles
from perlin_noise import PerlinNoise

class flowFeild():
    def __init__(self, width, height, scl):
        self.canvas = np.zeros((width, height, 3), dtype = 'uint8')
        self.background = np.zeros((width, height, 3), dtype = 'uint8')
        self.width = width
        self.height = height
        self.scl = scl
        self.col = width//scl
        self.row = height//scl
        self.inc = 0.05
        self.noise = PerlinNoise()
        self.zoff = 0
        self.numParticles = 3000
        self.feildStrengthForce = 0.4
        self.maxspeed = 5/(5+0.4)
        self.field = []
        self.particlesList = []

        for i in range(self.col*self.row):
            self.field.append(np.array([1, 0]))

        for i in range(self.numParticles):
            self.particlesList.append(particles.Particles(width, height, scl, self.maxspeed))
    
    def changeScl(self, scl):
        if scl <= 10:
            print("Scl too small")
            return 
        
        self.scl = scl
        self.col = self.width//scl
        self.row = self.height//scl
        self.field = []
        for i in range(self.col*self.row):
            self.field.append(np.array([1, 0]))

    def changeInc(self, inc):
        self.inc = inc/100

    def changeNoise(self, oct):
        if oct == 0:
            print("Oct cannot be zero")
            return
        self.noise = PerlinNoise(octaves=oct)

    def changeNumParticles(self, numParticles):
        if numParticles < self.numParticles:
            self.particlesList = self.particlesList[0:numParticles]
        else:
            for _ in range(numParticles-self.numParticles):
                self.particlesList.append(particles.Particles(self.width, self.height, self.scl, self.maxspeed))

        self.numParticles = numParticles

    def changeFeildStrengthForce(self, feildStrengthForce):
        self.feildStrengthForce = feildStrengthForce/100

    def changeMaxspeed(self, maxspeed):
        for particle in self.particlesList:
            particle.maxspeed = maxspeed/(maxspeed+self.feildStrengthForce*10)

    
    def drawVectors(self, x, y):
        id = y*self.col+x
        pt1 = np.array([x*self.scl, y*self.scl])
        pt2 = pt1 + self.field[id]/(self.field[id]**2).sum()**0.5*self.scl

        cv2.line(self.canvas, pt1.astype(int), pt2.astype(int), (255,255,255), 1)

    def update(self):
        self.canvas = cv2.addWeighted(self.canvas, 0.8, self.background, 1, 0)
        
        xoff = 1
        for x in range(self.row+1):
            yoff = 100
            for y in range(self.col+1):
                deg = self.noise([xoff, yoff, self.zoff])*2*math.pi
                self.field[x+y*self.col] = np.array([self.feildStrengthForce*math.cos(deg), self.feildStrengthForce*math.sin(deg)])
                #self.drawVectors(x, y)
                yoff += self.inc
            xoff += self.inc

        self.zoff += self.inc

        for particle in self.particlesList:
            x, y = particle.pos
            x = int(x/self.scl)
            y = int(y/self.scl)
            particle.update(self.field[x+y*self.col])
            particle.show(self.canvas)

