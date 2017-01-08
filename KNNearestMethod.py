import cv2
import numpy as np
import contours as ctr
from string import ascii_lowercase

def KNOCR():
    samples, responses, ls, sp = ctr.CreateBase('BaseminFinal.png')

    # we use the same method for the other document we want to test.
    samplesTest, r, linesIndices, spaces = ctr.CreateBase('lorem.png')

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

    finalString = ''
    print (linesIndices)
    for res in range(len(results)):
        if res in spaces:
            finalString = finalString+' '
        if res in linesIndices:
            finalString = finalString+'\n'
        finalString = finalString+indResponses[int(results[res][0])]

    print (finalString)

KNOCR()

