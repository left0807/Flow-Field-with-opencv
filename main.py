import cv2
import numpy as np
import sketch
import cv2Window
import mphand
import time

width = 1280
height = 720

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
canvas = sketch.flowFeild(width, height, 100)
detector = mphand.Detector(width, height)
detectFreq = 5

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
                                'force'],
                                [(1, 200),
                                (1, 100),
                                (1, 24),
                                (0, 6000),
                                (0, 100)],
                                new_win = True,
                                default_value=
                                [100, 5, 1, 600, 50],
                                func_list =
                                [canvas.changeScl,
                                 canvas.changeInc,
                                 canvas.changeNoise,
                                 canvas.changeNumParticles,
                                 canvas.changeFeildStrengthForce])

particle_win = cv2Window.Window('particle_win',
                                ['max.speed',
                                 'radius',
                                 'trajectory',
                                 'theme'],
                                 [(0, 500),
                                  (1, 5),
                                  (0, 100),
                                  (0, 0)],
                                  new_win = True,
                                  default_value=
                                  [50, 1, 20, 0],
                                  func_list=
                                  [canvas.changeMaxspeed,
                                   canvas.changeRadius,
                                   canvas.changeTrajectory,
                                   canvas.changeTheme])

def replace_background(frame, front, backgorund,lh,lv,ls,uh,uv,us):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (lh, ls, lv), (uh, us, uv))
    res = cv2.bitwise_or(front, front, mask=mask)
    f = front-res
    proj = np.where(f==0, backgorund, f)
    return proj

def main():
    pretime = time.time()
    front = np.bitwise_not(np.zeros((width, height), dtype='uint8'))

    t = 0
    while True:
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)

        if t%detectFreq == 0:
            detector.findFinger(frame)

        canvas.update(hands = detector.handpos)
        lh,lv,ls,uh,uv,us = webcam_win.getAllTrackbarPos()
        #proj = replace_background(frame, front, canvas.canvas,lh,lv,ls,uh,uv,us)
        #cv2.putText(proj, str(int(1/(time.time()-pretime))), (100, 100), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 2)

        cv2.imshow('feild', canvas.canvas)
        #cv2.imshow('webcam', proj)

        pretime = time.time()
        t = t+1
    



        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()