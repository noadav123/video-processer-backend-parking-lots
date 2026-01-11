"""Configuration for each parking lot camera/video"""

PARKING_CONFIGS = {
    "lot1": {
        "video_path": "carPark.mp4",
        "positions_file": "carPositions",
        "output_dict": "MainPositionDictionary",
        "slot_width": 107,
        "slot_height": 48,
        "threshold": 800,
        "window_name": "Parking Lot 1",
        "use_yolo": False,
        "wait_key": 6,
    },
    "lot2": {
        "video_path": "carPark2.mp4",
        "positions_file": "carPositions2",
        "output_dict": "Main2PositionDictionary",
        "slot_width": 52,
        "slot_height": 100,
        "threshold": 550,
        "window_name": "Parking Lot 2",
        "use_yolo": False,
        "wait_key": 3,
    },
    "lot3": {
        "video_path": "carPark3.mp4",
        "positions_file": "carPositions3",
        "output_dict": "Main3PositionDictionary",
        "slot_width": 38,
        "slot_height": 55,
        "threshold_low": 1600,
        "threshold_high": 2200,
        "window_name": "Parking Lot 3 (YOLO)",
        "use_yolo": True,
        "wait_key": 1,
        "yolo_model": "yolo11n.pt",
        "yolo_interval": 60,
    }
}

