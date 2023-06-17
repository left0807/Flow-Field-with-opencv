import cv2
import numpy as np
import sketch
import cv2Window
import mphand
import time

width = 720
height = 1280

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
canvas = sketch.flowFeild(width, height, 50)
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

def replace_background(frame, front, backgorund,lh,lv,ls,uh,uv,us):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (lh, ls, lv), (uh, us, uv))
    res = cv2.bitwise_or(front, front, mask=mask)
    f = front-res
    proj = np.where(f==0, backgorund, f)
    return proj

def main():

    pretime = time.time()
    while True:
        ret, frame = capture.read()
        canvas.update(hands = detector.findFinger(frame))
        front = np.bitwise_not(np.zeros(frame.shape, dtype='uint8'))

        lh,lv,ls,uh,uv,us = webcam_win.getAllTrackbarPos()
        cv2.imshow('feild', canvas.canvas)
        cv2.imshow('webcam', replace_background(frame, front, canvas.canvas,lh,lv,ls,uh,uv,us))
        cv2.imshow('hand', detector.drawHand(frame))
        pretime = time.time()


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()