import pickle
from audioop import error

try:
    with open( "Main3PositionDictionary", "rb") as f:
        dict = pickle.load(f)
        x=0
        print("---- Parking Status ----")
        for key, value in dict.items():
            x+=1
            print(key, "=>", value)
        print(x)
except (EOFError, pickle.UnpicklingError):
     print(error)


try:
    with open( 'carPositions3', "rb") as f:
        arr = pickle.load(f)
        x=0
        print("---- Parking Status ----")
        for   value in dict.items():
            x+=1
            print( value)
        print(x)
except (EOFError, pickle.UnpicklingError):
     print(error)


