import cv2
import pickle


img = cv2.imread('car_image3.jpeg')

width, height= 38, 70
pos = []

def load_positions(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

def save_positions(filename, pos):
    with open(filename, "wb") as f:
        pickle.dump(pos, f)


pos = load_positions("carPositions3")

def click(event, x, y, flags, param):
    if event == cv2.EVENT_RBUTTONDOWN:
        pos.append((x, y))
        print(x,y)
    elif event == cv2.EVENT_LBUTTONDOWN:
        for x1, y1 in pos[:]:
            print(x1, y1)
            if x1 < x < x1 + width and y1< y < y1 + height:
                pos.remove((x1, y1))
    save_positions("carPositions3", pos)




while True:

    img = cv2.imread('car_image3.jpeg')

    for x, y in pos:
        cv2.rectangle(img, (x, y), (x + width, y + height), 255, 2)
    cv2.imshow("image", img)
    cv2.setMouseCallback("image", click)
    cv2.waitKey(1)

    #cv2.imshow("img2", img2)

print(pos)
cv2.destroyAllWindows()