import json
import pygame
import math
from multipledispatch import dispatch

def JsonReader(folder):
    with open(folder, 'r') as f:
        filecontent = json.load(f)
        f.close
        return filecontent

def JsonWriter(folder, Content):
    with open(folder, "w") as f:
        Jsoninfo = json.dumps(Content, indent=4)
        f.write(Jsoninfo)
        f.close

def mouseCollision(A, B:pygame.Rect):
    return (A[0] >= B.x and A[0] <= B.x + B.width) and (A[1] >= B.y and A[1] <= B.y + B.height)

def pointCircleCollision(A, Bc, Bd):
    Diffrence = [Bc[0]-A.x, Bc[1]-A.y]
    D2 = math.sqrt(Diffrence[0]**2 + Diffrence[1]**2)
    return D2 <= Bd/2

@dispatch(float, int)
def Snap(i:float, s:int) -> int: return (i+s/2) // s * s

@dispatch(int, int)
def Snap(i:float, s:int) -> int: return (i+s/2) // s * s

@dispatch(tuple, int)
def Snap(i:tuple, s:int) -> tuple: return (Snap(i[0], s), Snap(i[1], s))