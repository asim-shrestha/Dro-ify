import sys
import cv2
import tkinter as tk
import numpy as np
import os

class Dro:
    def __init__(self, droCoords):
        #Ensure that the dro image is a square
        self.distanceBetweenPoints = min(droCoords[2], droCoords[3])
        self.pointA = (droCoords[0], droCoords[1])
        self.pointB = (droCoords[0] + self.distanceBetweenPoints, droCoords[1] + self.distanceBetweenPoints)

class DroDetector:
    @staticmethod
    def getDroCoords(image):
        grayscaledImage = DroDetector.grayscaleImage(image)
        droCoordsList = DroDetector.__findDroCoords(grayscaledImage)
        dro = Dro(droCoordsList)
        return dro
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
    def __init__(self, image):
        #Create window and window items
        self.rootWindow = tk.Tk()
        self.rootWindow.title("Dro-Detector")
        self.rootWindow.iconbitmap(os.getcwd() + '\icon.ico')

        selectImageButton = tk.Button(self.rootWindow, text = 'Select image', command = self.selectImageButton)
        selectImageButton.grid(row = 3, column = 0)

        setFileNameButton = tk.Button(self.rootWindow, text = 'Set file name', command = self.setFileNameButton)
        setFileNameButton.grid(row = 3, column = 1)

        droifyButton = tk.Button(self.rootWindow, text = 'Droify!', state = tk.DISABLED)
        droifyButton.grid(row = 3, column = 2)

        #Start window
        self.rootWindow.mainloop()

    def setFileNameButton(self):
        nameEntry = tk.Entry(self.rootWindow, width = 50)
        nameEntry.grid(row = 2, column = 1) 
        return

    def selectImageButton(self):
        myLabel = tk.Label(self.rootWindow, text = 'Clicked!')
        myLabel.grid(row = 1, column = 0) 
        return

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
    def saveDroImage(image, imageName):
        cv2.imwrite('dros/' + imageName+ '.png', image)