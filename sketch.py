import numpy as np
import cv2
import math
import particles
import mphand
from perlin_noise import PerlinNoise

class flowFeild():
    def __init__(self, width, height, scl):
        self.canvas = np.zeros((height, width, 3), dtype = 'uint8')
        self.background = np.zeros((height, width, 3), dtype = 'uint8')
        self.width = width
        self.height = height
        self.scl = scl
        self.col = width//scl
        self.row = height//scl
        self.inc = 0.005
        self.noise = PerlinNoise()
        self.zoff = 0
        self.numParticles = 600
        self.feildStrengthForceMag = 0.4
        self.attractiveForceMag = 5
        self.maxspeed = 5/(5+0.4)
        self.field = []
        self.particlesList = []
        self.radius = 1
        self.trijectory = 20
        self.theme = 0
        self.curlAngle = math.pi/3

        self.rotation_matrix = np.array([[math.cos(self.curlAngle), -math.sin(self.curlAngle)],
                                         [math.sin(self.curlAngle), math.cos(self.curlAngle)]])

        for i in range(self.col*self.row):
            self.field.append(np.array([1, 0]))

        for i in range(self.numParticles):
            self.particlesList.append(particles.Particles(width, height, scl, self.maxspeed, self.theme, self.radius))
    
    def changeScl(self, scl):
        if scl <= 10:
            print("Scl too small")
            return 
        
        self.scl = scl
        self.col = self.width//scl
        self.row = self.height//scl
        self.field = []
        for i in range((self.col+1)*(self.row+1)):
            self.field.append(np.array([1, 0]))

    def changeInc(self, inc):
        self.inc = inc/1000

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
                self.particlesList.append(particles.Particles(self.width, self.height, self.scl, self.maxspeed, self.theme, self.radius))

        self.numParticles = numParticles

    def changeFeildStrengthForce(self, feildStrengthForce):
        self.feildStrengthForce = feildStrengthForce/100

    def changeMaxspeed(self, maxspeed):
        for particle in self.particlesList:
            particle.maxspeed = maxspeed/(maxspeed+self.feildStrengthForce*10)

    def changeRadius(self, radius):
        if(radius == 0):
            print("radius can't be zero")
            return
        self.radius = radius
        for particle in self.particlesList:
            particle.radius = radius

    def changeTrajectory(self, trajectory):
        self.trajectory = trajectory

    def changeTheme(self, theme):
        self.theme = theme
        for particle in self.particlesList:
            particle.setColour(theme)
    
    def drawVectors(self, x, y):
        id = y*self.col+x
        pt1 = np.array([x*self.scl, y*self.scl])
        pt2 = pt1 + self.field[id]/(self.field[id]**2).sum()**0.5*self.scl

        cv2.line(self.canvas, pt1.astype(int), pt2.astype(int), (255,255,255), 1)

    def update(self, hands = None):
        self.canvas = cv2.addWeighted(self.canvas, (100-self.trijectory)/100, self.background, 1, 0)
        if hands:
            for hand, handpos in hands:
                cv2.circle(self.canvas, handpos.astype(int), 5, (255, 255, 255), 2)
        
        yoff = 1
        for y in range(self.row+1):
            xoff = 100
            for x in range(self.col+1):
                deg = self.noise([xoff, yoff, self.zoff])*4*math.pi
                self.field[y*self.col + x] = np.array([self.feildStrengthForce*math.cos(deg), self.feildStrengthForce*math.sin(deg)])

                if hands:
                    for hand, handpos in hands:
                        attractiveForce = handpos - np.array([x*self.scl, y*self.scl])
                        attractiveForce = self.attractiveForceMag*hand*attractiveForce/(attractiveForce**2).sum()**0.5
                        self.field[x+y*self.col] = self.field[x+y*self.col] + np.matmul(self.rotation_matrix, attractiveForce)

                #self.drawVectors(x, y)
                xoff += self.inc
            yoff += self.inc
        self.zoff += self.inc

        for particle in self.particlesList:
            x, y = particle.pos
            x = math.floor(x/self.scl)
            y = math.floor(y/self.scl)
            particle.update(self.field[x+y*self.col])
            particle.show(self.canvas)


