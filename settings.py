import os
import commands

def init(pointer):
    global variables
    variables = {}
    for directory in os.listdir(pointer):
        subdir = pointer + "/" + directory
        if not os.path.isdir(subdir):
            continue
        commands.expression(subdir)
