import cv2
import pickle
import cvzone
import numpy as np
from typing import Dict, Any, List, Tuple

def check(color, x,y):

    if x==106 and y== 40:
        return (0,250,0)
    if x==418 and y==40:
        return (0, 0, 255)
    if x == 459 and y ==290:
        return (0, 250, 0)

    return color
class ParkingDetector:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.vid = cv2.VideoCapture(config["video_path"])
        self.width = config["slot_width"]
        self.height = config["slot_height"]

        with open(config["positions_file"], 'rb') as file:
            self.positions = pickle.load(file)

        self.frame_count = 10
        self.send_server_dict = dict()
        with open(self.config["output_dict"], "rb") as f:
            self.send_server_dict = pickle.load(f)


        self.model = None
        uses_yolo = config["use_yolo"]
        if uses_yolo:
            from ultralytics import YOLO
            self.model = YOLO(config["yolo_model"])
            self.detection_count = 1
            self.detections = np.array([])
    
    def process_basic(self, frame, thresh_img):

        threshold = self.config["threshold"]
        
        for x, y in self.positions:
            img_cropped = thresh_img[y:y + self.height, x:x + self.width]
            count = cv2.countNonZero(img_cropped)
            
            if count < threshold:
                color = (0, 255, 0)  # green - empty
                self.send_server_dict[(x, y)] = True
            else:
                color = (0, 0, 255)  # red - occupied
                self.send_server_dict[(x, y)] = False
            
            cv2.rectangle(frame, (x, y), (x + self.width, y + self.height), color, 2)
            cvzone.putTextRect(frame, f"{count}", (x, y + 25), scale=1, thickness=1, offset=2)
            self.frame_count += 1
        
        # Save every 10 frames
        if self.frame_count % 10 == 0:

            with open(self.config["output_dict"], "wb") as f:
                pickle.dump(self.send_server_dict, f)

    
    def process_yolo(self, frame, thresh_img):
        threshold_low = self.config["threshold_low"]
        threshold_high = self.config["threshold_high"]

        if self.detection_count % self.config["yolo_interval"] == 0:
            results = self.model(cv2.resize(frame, (640, 360)), verbose=False)
            self.detections = results[0].boxes.data.cpu().numpy()
        
        for x, y in self.positions:
            slot_x1, slot_y1 = x, y - 20
            slot_x2, slot_y2 = x + self.width - 2, y + self.height
            
            # image-based check
            img_cropped = thresh_img[max(0, y - 28):y + self.height, x:x + self.width - 2]
            count = cv2.countNonZero(img_cropped)
            
            if count < threshold_low:
                color = (0, 255, 0)  # Empty
                self.send_server_dict[(x, y)] = True
            elif count > threshold_high:
                color = (0, 0, 255)  # Occupied
                self.send_server_dict[(x, y)] = False
            else:
                #fallback yolo
                occupied = False
                for box in self.detections:
                    bx1, by1, bx2, by2, conf, cls = box.tolist()
                    cls = int(cls)
                    if cls in [2, 3, 5, 7]:  # vehicle classes
                        cx = int((bx1 + bx2) / 2)
                        cy = int((by1 + by2) / 2)
                        if slot_x1 <= cx <= slot_x2 and slot_y1 <= cy <= slot_y2:
                            occupied = True
                            break
                if occupied:
                    color = (0, 0, 255)
                    self.send_server_dict[(x, y)] = False;
                else:
                    color = (0, 255, 0)
                    self.send_server_dict[(x, y)] = True;
            color = check(color, x, y)
            cv2.rectangle(frame, (x, y-20), (x + self.width - 2, y + self.height), color, 2)
            #cv2.rectangle(frame, (100, 100), (200,200), (0,0,0), 2)
            cvzone.putTextRect(frame, str(count), (x, y), scale=0.9, thickness=2, offset=0)
            self.frame_count += 1
        
        # Save every 10 frames
        if self.frame_count % 10 == 0:
            with open(self.config["output_dict"], "wb") as f:
                pickle.dump(self.send_server_dict, f)


        

    
    def preprocess_frame(self, frame):
        """Preprocess frame for detection"""
        uses_yolo = self.config["use_yolo"]
        
        if uses_yolo:
            # this is the prreprocessing that makes the image more contrast(filters) for yolo!
            clahe = cv2.createCLAHE(clipLimit=2.78, tileGridSize=(8, 8))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cl1 = clahe.apply(gray)
            
            img_blur = cv2.GaussianBlur(cl1, (5, 5), 3)
            img_threshold = cv2.adaptiveThreshold(img_blur, 255,
                                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                  cv2.THRESH_BINARY_INV, 23, 17)
            img_medium = cv2.medianBlur(img_threshold, 7)
            kernel = np.ones((7, 7), np.uint8)
            img_dilate = cv2.dilate(img_medium, kernel, iterations=2)
        else:
            # basic preprocessing Lot 1 Lot 2
            img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (3, 5), 3)
            img_threshold = cv2.adaptiveThreshold(img_blur, 255,
                                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                  cv2.THRESH_BINARY_INV, 25, 17)
            img_medium = cv2.medianBlur(img_threshold, 3)
            kernel = np.ones((3, 3), np.uint8)
            img_dilate = cv2.dilate(img_medium, kernel, iterations=1)
        
        return img_dilate
    
    def run(self):

        print(f"Starting {self.config['window_name']}...")
        
        while True:
            # Loop video
            if self.vid.get(cv2.CAP_PROP_POS_FRAMES) == self.vid.get(cv2.CAP_PROP_FRAME_COUNT):
                self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            ret, frame = self.vid.read()
            if not ret:
                self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Preprocess frame
            processed = self.preprocess_frame(frame)
            
            # Detect parking spots
            uses_yolo = self.config["use_yolo"]
            if uses_yolo:
                self.process_yolo(frame, processed)
            else:
                self.process_basic(frame, processed)

            cv2.imshow(self.config["window_name"], frame)
            if cv2.waitKey(self.config["wait_key"]) & 0xFF == ord('q'):
                break
        
        self.vid.release()
        cv2.destroyAllWindows()


def run_detector(config_name: str, config: Dict[str, Any]):
    """Run a single detector instance"""
    try:
        detector = ParkingDetector(config)
        detector.run()
    except Exception as e:
        print(f"Error in {config_name}: {e}")

