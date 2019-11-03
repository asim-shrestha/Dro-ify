#Info on OpenCV face detection from https://realpython.com/face-recognition-with-python/
#Info on the image to pencil drawing algorithm from https://www.freecodecamp.org/news/sketchify-turn-any-image-into-a-pencil-sketch-with-10-lines-of-code-cf67fa4f68ce/
#Info on the dodge blend algorithm from https://stackoverflow.com/questions/3312606/pil-composite-merge-two-images-as-dodge
import sys
import cv2
from DroDetector import DroDetector, Dro, DroViewer

#Read image
imagePath = sys.argv[1]
droImageName = sys.argv[2]
image = cv2.imread(imagePath)
dro = DroDetector.getDroCoords(image)

#View dro
droViewer = DroViewer(image)
# DroViewer.viewDroInImage(dro, image)
# droImage = DroViewer.getDroImage(dro, image)
# DroViewer.saveDroImage(droImage, droImageName)