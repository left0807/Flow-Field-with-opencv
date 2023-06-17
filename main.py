import cv2
import numpy as np
import sketch
import cv2Window

width = 720
height = 1280

capture = cv2.VideoCapture(0)
canvas = sketch.flowFeild(capture.read()[1].shape[0], capture.read()[1].shape[1], 50)

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
                                ['vector scale',
                                'incremental value of noise',
                                'noise octave',
                                'Particles number',
                                'feild strength force',
                                'particels max speed'],
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



def main():

    while True:
        canvas.update()
        ret, frame = capture.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        lh,lv,ls,uh,uv,us = webcam_win.getAllTrackbarPos()
        mask = cv2.inRange(hsv, (lh, ls, lv), (uh, us, uv))
        res = cv2.bitwise_and(frame, frame, mask=mask)
        f = frame-res

        proj = np.where(f==0, canvas.canvas, f)
        cv2.imshow('feild', canvas.canvas)
        cv2.imshow('webcam', proj)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()