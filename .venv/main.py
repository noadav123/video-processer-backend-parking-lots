import cv2
import pickle
import cvzone
import numpy as np
from cv2.gapi import kernel

def getRow(x):
    if 43< x<50:
        return 1;
    elif 160 <x < 166:
        return 2;
    elif 390 < x < 404:
        return 3;
    elif 505 < x < 520:
        return 4;
    elif 740 < x < 760:
        return 5;
    elif 900 < x < 920:
        return 6;

vid = cv2.VideoCapture('carPark.mp4')


width, height= 107, 48
with open('carPositions', 'rb') as file:
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

        if count < 800:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            sendServerDict[(x, y)] = {True, 1, getRow(x)};
        else:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)
            sendServerDict[(x, y)] = False;

        cvzone.putTextRect(frame, (str(x)+","+ str(y)), (x, y + 25), scale=1, thickness=1, offset=2)
        frameCount+=1
    if frameCount % 10 == 0:
        with open("MainPositionDictionary", "wb") as f:
            pickle.dump(sendServerDict, f)


while True:
    if vid.get(cv2.CAP_PROP_POS_FRAMES) == vid.get(cv2.CAP_PROP_FRAME_COUNT):
        vid.set(cv2.CAP_PROP_POS_FRAMES ,0)

    dih, cap = vid.read()
    imgGray= cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY )
    imgBlur= cv2.GaussianBlur(imgGray, (3,5),3)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25,17)
    imgMedium = cv2.medianBlur(imgThreshold, 3)
    kernel= np.ones((3,3), np.uint8)

    imgDilate= cv2.dilate(imgMedium, kernel, iterations=1)
    #cv2.imshow("thresh", imgThreshold)
    #cv2.imshow("median", imgMedium)



    cv2.imshow("img" ,cap)
    work(cap, imgDilate)
    #for x, y in arr:
    #    cv2.rectangle(cap, (x, y), (x + width, y + height), 255, 2)
    cv2.imshow("img", cap)

    cv2.waitKey(6)


