import cv2
import numpy as np
import contours as ctr
from string import ascii_lowercase

def KNOCR():
    samples, responses = ctr.CreateBase('BaseFinal.png')

    # we use the same method for the other document we want to test.
    samplesTest, r = ctr.CreateBase('text1.JPG')

    for s in samples:
        s = s/255
    for st in samplesTest:
        st = st/255

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)
    ret, results, neighbours, dist = model.findNearest(samplesTest, 20)

    print (len(samplesTest))
    print (len(neighbours))

    indResponses = np.empty((0, 36))
    indResponses = np.append(indResponses, [i for i in ascii_lowercase])
    indResponses = np.append(indResponses, [str(i) for i in range(0, 10)])

    finalString = ''
    for res in results:
        finalString = finalString+indResponses[int(res[0])]

    print (finalString)

KNOCR()

