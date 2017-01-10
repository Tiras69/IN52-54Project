import cv2
import numpy as np
import imageProcessing as imPro
import Binarization as bina
from string import ascii_lowercase

def computeKNN(basePath, testPath, cameraMode):
    baseSamples, baseResponses, baseLineStarts, baseSpaces, baseRectangles = imPro.computeProcessing(basePath) 

    if cameraMode:
        bina.binarization2(testPath)
        
    # we use the same method for the other document we want to test.
    testSamples, testResponses, testLineIndices, testSpaces, testRectangles = imPro.computeProcessing(testPath)

    for sample in baseSamples:
        sample = sample / 255

    for sampleTest in testSamples:
        sampleTest = sampleTest / 255

    model = cv2.ml.KNearest_create()
    model.train(baseSamples, cv2.ml.ROW_SAMPLE, baseResponses)
    ret, results, neighbours, dist = model.findNearest(testSamples, 20)

    # print (len(testSamples))
    # print (len(neighbours))

    indResponses = np.empty((0, 36))
    indResponses = np.append(indResponses, [i for i in ascii_lowercase])

    resultKNN = ""
    # print (testLineIndices)
    for res in range(len(results)):
        if res in testSpaces:
            resultKNN = resultKNN + " "
        if res in testLineIndices:
            if resultKNN != "":
                resultKNN = resultKNN + "\n"
        resultKNN = resultKNN + indResponses[int(results[res][0])]

    # print ("FINAL STRING :\n" + resultKNN)

    return resultKNN

