import cv2
import numpy as np
import sketch
import cv2Window
import mphand
import time

width = 720
height = 1280

capture = cv2.VideoCapture(0)
canvas = sketch.flowFeild(capture.read()[1].shape[0], capture.read()[1].shape[1], 50)
detector = mphand.Detector()

webcam_win = cv2Window.Window('webcam_win',
                            ['L - H',
                            'L - V',
                            'L - S',
                            'U - H',
                            'U - V',
                            'U - S'],
                            [(0, 255),
                            (0, 255),
                            (0, 255),
                            (0, 255),
                            (0, 255),
                            (0, 255)],
                            new_win = True,
                            default_value=
                            [39, 177, 0, 255, 255, 255])

feild_win =  cv2Window.Window('feild_win',
                                ['scale',
                                'inc',
                                'oct',
                                'no.Praticles',
                                'force',
                                'max.speed'],
                                [(1, 70),
                                (1, 100),
                                (1, 24),
                                (0, 6000),
                                (0, 100),
                                (0, 500)],
                                new_win = True,
                                default_value=
                                [50, 5, 1, 3000, 50, 50],
                                func_list =
                                [canvas.changeScl,
                                 canvas.changeInc,
                                 canvas.changeNoise,
                                 canvas.changeNumParticles,
                                 canvas.changeFeildStrengthForce,
                                 canvas.changeMaxspeed])

def replace_background(frame, backgorund,lh,lv,ls,uh,uv,us):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (lh, ls, lv), (uh, us, uv))
    res = cv2.bitwise_and(frame, frame, mask=mask)
    f = frame-res
    proj = np.where(f==0, backgorund, f)
    return proj

def main():

    pretime = time.time()
    while True:
        ret, frame = capture.read()
        hands = detector.findFinger(frame)
        for p, hand in hands:
            cv2.circle(frame, hand[0].astype(int), 10,  (255, 255, 255), 2)
        canvas.update(hands)

        lh,lv,ls,uh,uv,us = webcam_win.getAllTrackbarPos()
        cv2.imshow('feild', canvas.canvas)
        cv2.imshow('webcam', replace_background(frame, canvas.canvas,lh,lv,ls,uh,uv,us))
        cv2.imshow('hand', detector.drawHand(frame))

        pretime = time.time()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()