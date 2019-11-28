import sys
import cv2
import os
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
        droCoordsList, result = DroDetector.__findDroCoords(grayscaledImage)
        if(result == False):
            return None
        dro = Dro(droCoordsList)
        return dro

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
        if(len(faces) > 0):
            return faces[0], True
        else:
            return None, False

class DroViewer:
    imagePath = ''
    dro = None
    image = None
    
    def __init__(self):
        self.setUpRootWindow()        
        self.setUpWidgets()
        self.rootWindow.mainloop()
        return

    def setUpRootWindow(self):
        self.rootWindow = tk.Tk()
        self.rootWindow.title("Dro-Detector")
        self.rootWindow.iconbitmap('icon.ico')
        self.rootWindow.resizable(False, False)
        return 

    def setUpWidgets(self):
        self.theImage = tk.Label(text = "Please select an image!")
        self.theImage.grid(row = 1, column = 0, columnspan = 5)

        self.selectImageButton = tk.Button(self.rootWindow, text = 'Select image', command = self.selectImageButton)
        self.selectImageButton.grid(row = 0, column = 0, columnspan = 1)

        self.findFaceButton = tk.Button(self.rootWindow, text = 'Find face', command = self.findFaceButton, state = tk.DISABLED)
        self.findFaceButton.grid(row = 0, column = 1, columnspan = 1)

        self.droifyButton = tk.Button(self.rootWindow, text = 'Droify!', command = self.droifyButton, state = tk.DISABLED)
        self.droifyButton.grid(row = 0, column = 2, columnspan = 1)

        self.save1x1Button = tk.Button(self.rootWindow, text = 'Save image', command = self.save1x1Button, state = tk.DISABLED)
        self.save1x1Button.grid(row = 0, column = 3, columnspan = 1)

        self.save2x2Button = tk.Button(self.rootWindow, text = 'Save multi-image', command = self.save2x2Button, state = tk.DISABLED)
        self.save2x2Button.grid(row = 0, column = 4, columnspan = 1)
        return


    def selectImageButton(self):
        self.imagePath = filedialog.askopenfilename(title = "Select an image", filetypes = (("All files", "*.*"), ("png", "*.png")))
        if(self.imagePath != ''):
            self.updateTheImage(cv2.imread(self.imagePath))
            self.imageReset()

    def imageReset(self):
        self.findFaceButton.config(state = tk.NORMAL)
        self.droifyButton.config(state = tk.DISABLED)
        self.save1x1Button.config(state = tk.DISABLED)
        self.save2x2Button.config(state = tk.NORMAL)
        return

    def findFaceButton(self):
        #Get dro from file
        image = cv2.imread(self.imagePath)
        self.dro = DroDetector.getDroCoords(image)
        if(self.dro == None):
            return

        faceInImage = image[self.dro.pointA[1]:self.dro.pointB[1] , self.dro.pointA[0]:self.dro.pointB[0]]
        self.updateTheImage(faceInImage)

        #Change button states
        self.findFaceButton.config(state = tk.DISABLED)
        self.droifyButton.config(state = tk.NORMAL)
        self.save1x1Button.config(state = tk.NORMAL)
        self.save2x2Button.config(state = tk.NORMAL)
        return

    def droifyButton(self):
        image = cv2.imread(self.imagePath)
        print(self.imagePath)
        droImage = self.getDroImage(self.dro, image)
        self.updateTheImage(droImage)
        self.droifyButton.config(state = tk.DISABLED)
        return

    def updateTheImage(self, image):      
        #save in temp
        self.tempSaveImage(image)

        #load image in temp
        acquiredImage = ImageTk.PhotoImage(image = Image.open('temp/temp.png'))
        self.image = self.getTempImage()
        self.theImage.config(image = acquiredImage)
        self.theImage.image = acquiredImage
        return

    def getTempImage(self):
        tempImagePath = (os.getcwd() + '\\temp\\temp.png').replace('\\', '/')
        print(tempImagePath)
        print(self.imagePath)
        return cv2.imread(tempImagePath)

    def save1x1Button(self):
        savedImagePath = filedialog.asksaveasfile(mode='w', defaultextension=".png")
        if savedImagePath != None:
            self.saveDroImage(self.image, savedImagePath.name)
        return

    def save2x2Button(self):
        savedImagePath = filedialog.asksaveasfile(mode='w', defaultextension=".png")
        if savedImagePath != None:
            dimensions = self.image.shape
            height = dimensions[0]
            width = dimensions[1]
            emojiLength = 5
            emojiHeight = int(height/emojiLength)
            emojiWidth = int(width/emojiLength)
            for row in range(0, emojiLength):
                startY = int(row * emojiHeight)
                for column in range(0, emojiLength):
                    startX = int(column * emojiHeight)
                    image = self.image[startY : startY + emojiHeight, startX : startX + emojiHeight]
                    self.saveDroImage(image, savedImagePath.name[0:-4] + str((row * emojiLength) + column) + '.png') 
            self.saveDroImage(self.image, savedImagePath.name)
            return
    
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
        result = back * 256.0 / (256.0 - front) 
        result[result > 255] = 255
        result[front == 255] = 255
        return result.astype('uint8')

    @staticmethod
    def tempSaveImage(image):
        DroViewer.saveDroImage(image, 'temp/temp.png')

    @staticmethod
    def saveDroImage(image, imagePath):
        cv2.imwrite(imagePath, image)