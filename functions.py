import os
import settings

def dirlen():
    return len(os.listdir(settings.pointer))

def dirmove(x):
    settings.pointer = os.listdir(settings.pointer)[x]
    