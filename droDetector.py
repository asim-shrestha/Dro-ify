import sys
import cv2
import numpy as np

class Dro:
    def __init__(self, droCoords):
        #Ensure that the dro image is a square
        self.pointA = (droCoords[0], droCoords[1])
        self.pointB = (droCoords[0] + droCoords[2], droCoords[1] + droCoords[3])

class DroDetector:
    @staticmethod
    def getDroCoords(image):
        try:
            grayscaledImage = DroDetector.grayscaleImage(image)
            droCoordsList = DroDetector.__findDroCoords(grayscaledImage)
            dro = Dro(droCoordsList)
            return dro
        except:
            print('Something is wrong with your image')

    @staticmethod
    def grayscaleImage(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def __findDroCoords(grayscaledImage):
        # Create the haar cascade
        faceClassifier = cv2.CascadeClassifier(filename = "haarcascade_frontalface_default.xml")

        # Detect faces in the image
        faces = faceClassifier.detectMultiScale(
            grayscaledImage,
            scaleFactor=1.1,
            minNeighbors=5,
        minSize=(30, 30)
        )

        #Ensure only one dro exists
        if(len(faces) > 100):
            print('Too many dros!')
            return None
        else:
            return faces[0]

class DroViewer:
    @staticmethod
    def viewDroInImage(dro, image):
        droImage = image.copy()
        lineColour = (0, 255, 0)
        lineThickness = 1
        cv2.rectangle(droImage, dro.pointA, dro.pointB, (0, 255, 0), lineThickness)
        DroViewer.showImage('Dro found', droImage)

    @staticmethod
    def showImage(headerText, image):
        cv2.imshow(headerText, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def getDroImage(dro, image):
        #Greyscale dro closeup
        droImage = image[dro.pointA[1]:dro.pointB[1] , dro.pointA[0]:dro.pointB[0]]
        DroViewer.showImage('Initial image', droImage)
        droImage = DroDetector.grayscaleImage(droImage)

        #Invert for the algorithm
        invertedDroImage = 255 - droImage

        #Blur the invert for the algorithm
        blurredInvertedDroImage = cv2.GaussianBlur(invertedDroImage, (11, 11), cv2.BORDER_DEFAULT)

        #Dodge blend for the algorithm
        finalImage = DroViewer.dodge(blurredInvertedDroImage, droImage)
        DroViewer.showImage('Final dro', finalImage)
        return finalImage
    
    @staticmethod
    def dodge(front,back):
        # The formula comes from http://www.adobe.com/devnet/pdf/pdfs/blend_modes.pdf
        result = back * 256.0 / (256.0 - front) 
        result[result > 255] = 255
        result[front == 255] = 255
        return result.astype('uint8')

    @staticmethod
    def saveDroImage(image):
        cv2.imwrite('dros/dro1.jpg', image)