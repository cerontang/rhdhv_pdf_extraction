import cv2
import numpy as np

im = cv2.imread("img\VBH-1102-001.pdf0.png")
fromCenter = False
numberofROI = round(float(input()))
r = []
for i in range (numberofROI):
    selectedBB = cv2.selectROI(im, fromCenter)
    r.append(selectedBB)
    imCrop = im[int(r[i][1]):int(r[i][1] + r[i][3]), int(r[i][0]):int(r[i][0] + r[i][2])]
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imshow("test", imCrop)
    print(r[i])
    cv2.waitKey(0)
