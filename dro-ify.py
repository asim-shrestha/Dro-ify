import sys
import cv2
from droDetector import DroDetector, Dro, DroViewer

#Read image
imagePath = sys.argv[1]
image = cv2.imread(imagePath)
dro = DroDetector.getDroCoords(image)

# Draw a rectangle around the faces
print('Point A: ', dro.pointA)
print('Point B: ', dro.pointB)
DroViewer.viewDroInImage(dro, image)