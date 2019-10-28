import sys
import cv2

class Dro:
    def __init__(self, droCoords):
        self.pointA = (droCoords[0], droCoords[1])
        self.pointB = (droCoords[0] + droCoords[2], droCoords[1] + droCoords[3])

class DroDetector:
    @staticmethod
    def getDroCoords(image):
        grayscaledImage = DroDetector.grayscaleImage(image)
        droCoordsList = DroDetector.__findDroCoords(grayscaledImage)
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
        if(len(faces) > 100):
            print('Too many dros!')
            return None
        else:
            return faces[0]

class DroViewer:
    @staticmethod
    def viewDroInImage(dro, image):
        lineColour = (0, 255, 0)
        lineThickness = 1
        cv2.rectangle(image, dro.pointA, dro.pointB, (0, 255, 0), lineThickness)
        cv2.imshow("Dro found", image)
        cv2.waitKey(0)