import cv2
import numpy as np 
from numpy.linalg import norm

import contours as ctr
from string import ascii_lowercase

SIZE = 20
numberOfBins = 16

NUMBER_OF_CLASS = 26

class StatModel(object):
    def load(self, fn):
        self.model.load(fn) 
    def save(self, fn):
        self.model.save(fn)

class SVM(StatModel):
    def __init__(self, C = 1, gamma = 0.5):
        self.model = cv2.ml.SVM_create()
        self.model.setGamma(gamma)
        self.model.setC(C)
        self.model.setKernel(cv2.ml.SVM_RBF)
        self.model.setType(cv2.ml.SVM_C_SVC)

    def train(self, samples, responses):
        self.model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    def predict(self, samples):
        return self.model.predict(samples)



#Pour écriture manuscrite
def straighten(sourceImg):
    imgMoments = cv2.moments(sourceImg)
    if abs(imgMoments['mu02']) < 1e-2:
        return sourceImg.copy()
    skew = imgMoments['mu11']/imgMoments['mu02']
    M = np.float32([[1, skew, -0.5*SIZE*skew], [0, 1, 0]])
    sourceImg = cv2.warpAffine(sourceImg,M,(SIZE, SIZE),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR)
    return sourceImg

def histOfGradient(chars):
    
    samples = []
    for img in chars:
        gradientX = cv2.Sobel(img, cv2.CV_32F, 1, 0)
        gradientY = cv2.Sobel(img, cv2.CV_32F, 0, 1)
        magnitude, angle = cv2.cartToPolar(gradientX, gradientY)
        
        #print(angle)

        bins = np.int32(numberOfBins * angle/(2*np.pi))
        #print (magnitude)
        
        #dividing in 4 zones the letter
        binZones = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
        magnitudeZones = magnitude[:10,:10], magnitude[10:,:10], magnitude[:10,10:], magnitude[10:,10:]
        #print (binZones)
        hists = [np.bincount(b.ravel(), m.ravel(), numberOfBins) for b, m in zip(binZones, magnitudeZones)]
        hist = np.hstack(hists)     # hist is a 64 bit vector (16 + 16 + 16 + 16)

        # transform to Hellinger kernel
        eps = 1e-7
        hist /= hist.sum() + eps
        hist = np.sqrt(hist)
        hist /= norm(hist) + eps

        samples.append(hist)
    return np.float32(samples)




img1 = cv2.imread('digits.png',0) 
cells = [np.hsplit(row,100) for row in np.vsplit(img1,50)]
train_cells = [ i[:50] for i in cells ]
#print(len(train_cells[0][0][0]))
hogdata = [list(map(histOfGradient,row))for row in train_cells]
#print(hogdata)
print(len(hogdata[0][0]))
trainData = np.float32(hogdata).reshape(-1,64)
print(type(trainData))
print(type(trainData[0]))
print(type(trainData[0][0]))

#responses = np.array([i for i in range(0, 26)]).astype(np.float32)
#print(responses)
#responses = np.repeat(responses, 20)
#print(responses)
#svm = cv2.ml.SVM()

#responses = np.float32(np.repeat(np.arange(26), 20)[:,np.newaxis])
#responses = np.float32(np.repeat(np.arange(10),250)[:,np.newaxis])



#svm = cv2.ml.SVM_create()
#svm.setKernel(cv2.ml.SVM_LINEAR)
#svm.setType(cv2.ml.SVM_C_SVC)
#svm.setC(2.67)
#svm.setGamma(5.383)


model = SVM(C=2.67, gamma=5.383)



samples, responses, ls, space, rectangles = ctr.CreateBase('BaseminFinal.png')

im = cv2.imread('BaseminFinal.png')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, imGrayTresh = cv2.threshold(imgray,150,255,cv2.THRESH_BINARY)

chars = []
print(len(rectangles))
for rect in rectangles:
    number = imGrayTresh[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    number = cv2.resize(number, (20, 20))
    #number = straighten(number)
    #hists  = histOfGradient(number)
    #data.append(hists)
    chars.append(number)

chars = np.array(chars)
print(type(chars))
print(type(chars[0]))
print(type(chars[0][0]))
print(type(chars[0][0][0]))
print(len(chars))

labels = np.repeat(np.arange(NUMBER_OF_CLASS), len(chars)/NUMBER_OF_CLASS)
#print(len(responses))

chars2 = list(map(straighten, chars))
print(len(chars2))
print(type(chars2))
samplesTrain = histOfGradient(chars)
print(str(type(samplesTrain)) + 'sample type')

model.train(samplesTrain, labels)

#data = np.float32(data)
#data = np.array(data)
#print(type(data))
#print(type(data[0]))
#print(type(data[0][0]))

#model.train(data, responses)
#svm.train(, cv2.ml.ROW_SAMPLE, responses)


samples, responses, ls, space, rectangles = ctr.CreateBase('BaseminFinal.png')

im = cv2.imread('lorem.png')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, imGrayTresh = cv2.threshold(imgray,150,255,cv2.THRESH_BINARY)

chars = []
print(len(rectangles))
for rect in rectangles:
    number = imGrayTresh[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    number = cv2.resize(number, (20, 20))
    #number = straighten(number)
    #hists  = histOfGradient(number)
    #data.append(hists)
    chars.append(number)

chars = np.array(chars)
print(type(chars))
print(type(chars[0]))
print(type(chars[0][0]))
print(type(chars[0][0][0]))
print(len(chars))

#labels = np.repeat(np.arange(NUMBER_OF_CLASS), len(chars)/NUMBER_OF_CLASS)
#print(len(responses))
chars2 = []
chars2 = list(map(straighten, chars))
print(len(chars2))
print(type(chars2))
samplesTest = histOfGradient(chars)

res = model.predict(samplesTest)

print(len(res))
print(res)