import os
import settings

def dirlen(directory):
    return len(os.listdir(directory))

def dirmove(directory, x):
    return directory + "/" + os.listdir(directory)[x]