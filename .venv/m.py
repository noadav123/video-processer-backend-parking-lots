import cv2
import pickle


img = cv2.imread('car_image.png')
(45,93)
width, height= 107, 48
pos = []
def click(event, x ,y , params, blah):
    if event == cv2.EVENT_RBUTTONDOWN:
        pos.append((x,y))
        print(x,y)
    if event == cv2.EVENT_LBUTTONDOWN:
        for x1,y1 in pos:
            if x1 < x < x1+width and y1< y < y1+height:
                pos.remove((x1,y1))
                #cv2.rectangle(img , (x ,y), (x+10, y+10), (0,255,0) , 2)

    with open("carPositions", "wb") as f:
       pickle.dump(pos,f)




while True:

    img = cv2.imread('car_image.png')
    with open("carPositions", "rb") as f:
        pos = pickle.load(f)
    for x, y in pos:
        cv2.rectangle(img, (x, y), (x + width, y + height), 255, 2)
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", click)
    cv2.waitKey(1)
    #cv2.imshow("img2", img2)


cv2.destroyAllWindows()