from random import random
import numpy
import cv2
from PIL import Image
import os

def color_transfer(sourcePath,targetPath, destinationPath):
    print(sourcePath)
    print(destinationPath)
    debugSrcPath = ''
    debugTargPath = ''
    debugDestPath = ''

    sourceImagePath = sourcePath if sourcePath != None else debugSrcPath
    targetImagePath = targetPath if targetPath != None else debugTargPath
    destomationImagePath = destinationPath if destinationPath != None else debugDestPath

    sourceImage = Image.open(sourceImagePath).convert('RGB') # look into converting this directly to lab 
    targetImage = Image.open(targetImagePath).convert('RGB')

    sourceRGB = numpy.array(sourceImage)
    targetRGB = numpy.array(targetImage)

    sourceBGR = sourceRGB[:, :, ::-1].copy() #again why do I need to convert to bgr?
    targetBGR = targetRGB[:, :, ::-1].copy()

    source = cv2.cvtColor(sourceBGR, cv2.COLOR_BGR2LAB)
    target = cv2.cvtColor(targetBGR, cv2.COLOR_BGR2LAB)

    source2 = cv2.cvtColor(sourceBGR, cv2.COLOR_BGR2LAB)
    target2 = cv2.cvtColor(targetBGR, cv2.COLOR_BGR2LAB)

    source = source.astype(numpy.float32)
    target = target.astype(numpy.float32)

    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_statifier(source)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_statifier(target)

    (l, a, b) = cv2.split(target) #could try swapping target / source to see different resoults
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar

     # scale by the standard deviations
    l = (lStdSrc / lStdTar) * l
    a = (aStdSrc / aStdTar) * a
    b = (bStdSrc / bStdTar) * b
   
     
    # add in the source mean
    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc

    # clip the pixel intensities to [0, 255] if they fall outside
    # this range
    l = numpy.clip(l, 0, 255)
    a = numpy.clip(a, 0, 255)
    b = numpy.clip(b, 0, 255)

    # merge the channels together and convert back to the RGB color
    # space, being sure to utilize the 8-bit unsigned integer data
    # type
    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    cv2.imshow('Transfered',transfer)
    cv2.imwrite(os.path.join(destomationImagePath,(int)(random() * 1000) + '.png'), transfer)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def image_statifier(image):
    #this function takes an inputted image and returns the mean and std deviation for each dimension in a lab img
    (l, a, b) = cv2.split(image)
    #L
    (lMean, lStd) = (l.mean(), l.std())
    #a
    (aMean, aStd) = (a.mean(), a.std())
    #b
    (bMean, bStd) = (b.mean(), b.std())

    return (lMean, lStd, aMean, aStd, bMean, bStd)
