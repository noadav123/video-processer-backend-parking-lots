import cv2
import pickle
import cvzone
import numpy as np
from cv2.gapi import kernel

vid = cv2.VideoCapture('carPark2.mp4')


width, height= 52, 100
with open('carPositions2', 'rb') as file:
    arr = pickle.load(file)

empty = []

frameCount=10
sendServerDict=dict()
def work(frame, thresh_img):
    global frameCount
    global sendServerDict
    for x, y in arr:
        imgCroped = thresh_img[y:y + height, x:x + width]

        count = cv2.countNonZero(imgCroped)


        if count < 600:
            cv2.rectangle(frame, (x+2, y), (x + width-2, y +height), (0, 255, 0), 2)
            sendServerDict[(x, y)] = True;

        else:
            cv2.rectangle(frame, (x+2, y), (x + width-2, y + height), (0, 0, 255), 2)
            sendServerDict[(x, y)] = False;
        frameCount += 1


    if frameCount % 10 == 0:
        with open("Main2PositionDictionary", "wb") as f:
            pickle.dump(sendServerDict, f)


while True:


    dih, cap = vid.read()
    if not dih:
        vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    imgGray= cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY )
    imgBlur= cv2.GaussianBlur(imgGray, (3,3),3)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25,17)
    imgMedium = cv2.medianBlur(imgThreshold, 3)
    kernel= np.ones((3,3), np.uint8)

    imgDilate= cv2.dilate(imgMedium, kernel, iterations=1)
    #cv2.imshow("thresh", imgThreshold)
    #cv2.imshow("median", imgMedium)

    #cv2.imshow("img" ,cap)
    work(cap, imgDilate)

    cv2.imshow("img", cap)

    cv2.waitKey(3)




