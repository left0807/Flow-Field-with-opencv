import mediapipe as mp
import numpy as np
import cv2 

fingerPos = [[2,3,4],
             [5,6,7,8],
             [9,10,11,12],
             [13,14,15,16],
             [17,18,19,20]]

class Detector():
    def __init__(self, width, height):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.width = width
        self.height = height

    def getLandmarks(self, frame):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(imgRGB)
        return result.multi_hand_landmarks
    
    def findFinger(self, frame):
        result = self.getLandmarks(frame)
        self.handpos = []

        if result:
            for handLms in result:
                lms = handLms.landmark
                rock = True
                paper = True
                for i in range(1, 5):
                    x1 = lms[fingerPos[i][1]].x-lms[fingerPos[i][0]].x
                    y1 = lms[fingerPos[i][1]].y-lms[fingerPos[i][0]].y
                    x2 = lms[fingerPos[i][2]].x-lms[fingerPos[i][0]].x
                    y2 = lms[fingerPos[i][2]].y-lms[fingerPos[i][0]].y
                    
                    x3 = lms[fingerPos[i][3]].x-lms[fingerPos[i][2]].x
                    y3 = lms[fingerPos[i][3]].y-lms[fingerPos[i][2]].y
                    
                    if x1*x3 + y1*y3 > 0 and x1*x2 + y1*y2 > 0:
                        rock = False
                    else:
                        paper = False

                self.handpos.append([rock*1 + paper*-1, np.array([lms[0].x*self.width, lms[0].y*self.height])])

        # if self.handpos:
        #     for id, pos in self.handpos:
        #         print(pos)

    def drawHand(self, frame, landmarks = None):
        if landmarks:
            result = landmarks
        else:
            result = self.getLandmarks(frame)

        if result:
            for handLms in result:
                self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS,
                                           self.mpDraw.DrawingSpec(color=(255, 255, 255), thickness = 1, circle_radius=1),
                                           self.mpDraw.DrawingSpec(color=(255, 255, 255), thickness = 1, circle_radius=1))
                
    