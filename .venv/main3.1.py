import cv2
import pickle
import cvzone
import numpy as np
from sympy.codegen.cnodes import static
from ultralytics import YOLO

# Load YOLO
model = YOLO("yolo11n.pt")

# Load video
vid = cv2.VideoCapture('carPark3.mp4')

# Slot size
width, height = 38, 55

# Load saved positions
with open('carPositions3', 'rb') as file:
    arr = pickle.load(file)

# Example slot grid (you can keep yours)
array = []
(106,33)
x1,y1 = 106, 40
for i in range(18):

    if i != 16:
       array.append((x1,y1))
    x1+=width+1
#lower top left , 20 of these vertically
(30, 103)
x1,y1 = 30, 119
for i in range(20):

    if i != 18 and i!=1:
        array.append((x1,y1))
    x1+=width+1
(30 ,290)
x1,y1 = 30, 290
for i in range(40):
    if i==20:
        x1=30
        y1=375

    array.append((x1,y1))
    x1+=width+1

sendServerDict=dict()

helpcheck=0;
def check(color, x,y):

    if x==106 and y== 40:
        return (0,250,0);
    if x==418 and y==40:
        return (0, 0, 255);
    if x == 459 and y ==290:
        return (0, 250, 0);

    return color
frameCount=10
def work(frame, thresh_img, detections):
    global frameCount
    for x, y in array:
        slot_x1, slot_y1 = x, y - 20
        slot_x2, slot_y2 = x + width - 2, y + height

        # --- Step 1: Image-based check
        imgCroped = thresh_img[max(0, y - 28):y + height, x:x + width - 2]
        count = cv2.countNonZero(imgCroped)

        if count < 1600:
            color = (0, 255, 0)   # empty
            sendServerDict[(x,y)]= True

        elif count > 2200:
            color = (0, 0, 255)   # occupied
            sendServerDict[(x, y)] = False;
        else:
            # --- Step 2: YOLO fallback
            occupied = False
            for box in detections:
                bx1, by1, bx2, by2, conf, cls = box.tolist()
                cls = int(cls)
                if cls in [2, 3, 5, 7]:  # vehicle classes
                    cx = int((bx1 + bx2) / 2)
                    cy = int((by1 + by2) / 2)
                    if slot_x1 <= cx <= slot_x2 and slot_y1 <= cy <= slot_y2:
                        occupied = True
                        break
            if occupied:
                color  = (0,0,255)
                sendServerDict[(x,y)]= False;
            else:
                color=(0, 255, 0)
                sendServerDict[(x,y)]=True;


        color= check(color,x,y)
        cv2.rectangle(frame, (slot_x1, slot_y1), (slot_x2, slot_y2), color, 2)

        cvzone.putTextRect(frame, str(count), (x, y), scale=0.9, thickness=2, offset=0)
        frameCount += 1
    if frameCount % 10 == 0:
        with open("Main3PositionDictionary", "wb") as f:
            pickle.dump(sendServerDict, f)
                


count =1
detections = np.array([])
while True:
        ret, cap = vid.read()
        if not ret:
            vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue


        clahe = cv2.createCLAHE(clipLimit=2.78, tileGridSize=(8, 8))
        gray = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
        cl1 = clahe.apply(gray)

        imgGray = cl1
        imgBlur = cv2.GaussianBlur(cl1, (5,5),3)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255,
                                             cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY_INV, 23, 17)
        imgMedium = cv2.medianBlur(imgThreshold, 7)
        imgMedium2 = imgThreshold
        kernel = np.ones((7,7), np.uint8)
        imgDilate = cv2.dilate(imgMedium2, kernel, iterations=2)



        if count % 60 == 0:
            results = model(cv2.resize(cap, (640, 360)), verbose=False)

            detections = results[0].boxes.data.cpu().numpy()
        else:
            detections = np.array([])

            # --- SLOT CHECK ---
        work(cap, imgDilate, detections)

        cv2.imshow("Parking Detection", cap)
        count+=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

