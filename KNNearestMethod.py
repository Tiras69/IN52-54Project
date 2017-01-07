import cv2
import numpy as np
import contours as ctr

def KNOCR():
    samples, responses = ctr.CreateBase('BaseFinal.png')

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)


KNOCR()

