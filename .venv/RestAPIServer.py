#from fastapi import FastAPI
import time
from contextlib import asynccontextmanager
import random
import json
from pathlib import Path
from typing import List
#from pydantic import BaseModel
#from fastapi.middleware.cors import CORSMiddleware
import pickle
while True:
    try:
        with open("MainPositionDictionary", "rb") as f:
            dict1 = pickle.load(f)
        
        with open("Main2PositionDictionary", "rb") as f2:
            dict2 = pickle.load(f2)
        
        with open("Main3PositionDictionary", "rb") as f3:
            dict3 = pickle.load(f3)
        
        available1 = sum(1 for v in dict1.values() if v)
        available2 = sum(1 for v in dict2.values() if v)
        available3 = sum(1 for v in dict3.values() if v)
        
        print(f"Lot 1: {available1}/{len(dict1)} available | "
              f"Lot 2: {available2}/{len(dict2)} available | "
              f"Lot 3: {available3}/{len(dict3)} available", end='\r')
        
    except FileNotFoundError as e:
        print(f"Waiting for dictionary files... ({e.filename})", end='\r')
    except Exception as e:
        print(f"Error: {e}", end='\r')
    
    time.sleep(1)

 
