import mediapipe as mp
import cvzone.HandTrackingModule as htm
import numpy as np
import cv2 

fingerPos = [[2,3,4],
             [5,6,8],
             [9,10,12],
             [13,14,16],
             [17,18,20]]

class Detector():
    def __init__(self, width, height):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.htmDetector = htm.HandDetector(detectionCon=0.75)
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
                v = 0
                for i in range(1, 5):
                    x1 = lms[fingerPos[i][1]].x-lms[fingerPos[i][0]].x
                    y1 = lms[fingerPos[i][1]].y-lms[fingerPos[i][0]].y
                    x2 = lms[fingerPos[i][2]].x-lms[fingerPos[i][1]].x
                    y2 = lms[fingerPos[i][2]].y-lms[fingerPos[i][1]].y
                    
                    if x1*x2 + y1*y2 > 0:
                        rock = False
                    else:
                        paper = False

                self.handpos.append([rock*1 + paper*-1, np.array([lms[0].x*self.width, lms[0].y*self.height])])

        # if self.handpos:
        #     for id, pos in self.handpos:
        #         print(pos)

    def drawHand(self, frame):
        result = self.getLandmarks(frame)
        cp = frame.copy()
        if result:
            for handLms in result:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    cv2.putText(cp, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)
            
            self.mpDraw.draw_landmarks(cp, handLms, self.mpHands.HAND_CONNECTIONS)

        return cp
    