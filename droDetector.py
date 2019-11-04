import sys
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np

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
    imagePath = ''
    dro = None
    image = None
    
    def __init__(self, image):
        self.setUpRootWindow()        
        self.setUpWidgets()
        self.rootWindow.mainloop()

    def setUpRootWindow(self):
        self.rootWindow = tk.Tk()
        self.rootWindow.title("Dro-Detector")
        self.rootWindow.iconbitmap('icon.ico')

    def setUpWidgets(self):
        self.theImage = tk.Label(text = "Please select an image!")
        self.theImage.grid(row = 0, column = 0, columnspan = 4)

        self.selectImageButton = tk.Button(self.rootWindow, text = 'Select image', command = self.selectImageButton)
        self.selectImageButton.grid(row = 3, column = 0, columnspan = 1)

        self.findFaceButton = tk.Button(self.rootWindow, text = 'Find face', command = self.findFaceButton)
        self.findFaceButton.grid(row = 3, column = 1, columnspan = 1)

        self.droifyButton = tk.Button(self.rootWindow, text = 'Droify!', command = self.droifyButton)
        self.droifyButton.grid(row = 3, column = 2, columnspan = 1)

        self.saveButton = tk.Button(self.rootWindow, text = 'Save image', command = self.saveImageButton)
        self.saveButton.grid(row = 3, column = 3, columnspan = 1)


    def selectImageButton(self):
        imageFileName = filedialog.askopenfilename(title = "Select an image", filetypes = (("png", "*.png"), ("all files", "*.*")))
        if(imageFileName != ''):
            self.imagePath = imageFileName
            self.imageReset()
            acquiredImage = ImageTk.PhotoImage(image = Image.open(imageFileName))
            self.theImage.config(image = acquiredImage)
            self.theImage.image = acquiredImage

    def imageReset(self):
        return

    def findFaceButton(self):
        #Get dro from file
        image = cv2.imread(self.imagePath)
        self.dro = DroDetector.getDroCoords(image)
        faceInImage = image[self.dro.pointA[1]:self.dro.pointB[1] , self.dro.pointA[0]:self.dro.pointB[0]]

        #save in temp
        self.image = faceInImage
        self.storeImage(faceInImage)

        #load image in temp
        acquiredImage = ImageTk.PhotoImage(image = Image.open('temp/temp.png'))
        self.theImage.config(image = acquiredImage)
        self.theImage.image = acquiredImage

        #Disable this button

        #Activate droify button
        return

    def droifyButton(self):
        image = cv2.imread(self.imagePath)
        droImage = self.getDroImage(self.dro, image)

        #save in temp
        self.storeImage(droImage)

        #load image in temp
        acquiredImage = ImageTk.PhotoImage(image = Image.open('temp/temp.png'))
        self.theImage.config(image = acquiredImage)
        self.theImage.image = acquiredImage
        return

    def saveImageButton(self):
        savedImagePath = filedialog.asksaveasfile(mode='w', defaultextension=".png")
        if savedImagePath != None:
            self.saveDroImage(self.image, savedImagePath.name)
            

        return 
    @staticmethod
    def storeDroImage(dro, image):
        droImage = image[dro.pointA[1]:dro.pointB[1] , dro.pointA[0]:dro.pointB[0]]
        lineColour = (0, 255, 0)
        lineThickness = 1
        cv2.rectangle(droImage, dro.pointA, dro.pointB, (0, 255, 0), lineThickness)
        DroViewer.showImage('Dro found', droImage)

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
        droImage = DroDetector.grayscaleImage(droImage)

        #Invert for the algorithm
        invertedDroImage = 255 - droImage

        #Blur the invert for the algorithm
        blurredInvertedDroImage = cv2.GaussianBlur(invertedDroImage, (11, 11), cv2.BORDER_DEFAULT)

        #Dodge blend for the algorithm
        finalImage = DroViewer.dodge(blurredInvertedDroImage, droImage)
        return finalImage
    
    @staticmethod
    def dodge(front,back):
        # The formula comes from http://www.adobe.com/devnet/pdf/pdfs/blend_modes.pdf
        result = back * 256.0 / (256.0 - front) 
        result[result > 255] = 255
        result[front == 255] = 255
        return result.astype('uint8')

    @staticmethod
    def storeImage(image):
        cv2.imwrite('temp/' + 'temp.png', image)

    @staticmethod
    def saveDroImage(image, imagePath):
        cv2.imwrite(imagePath, image)