import os
import commands
from directory_functions import Directory


def init(pointer):
    global variables
    variables = {}
    root = Directory(pointer)
    for directory in root.get_directory_children():
        print("SETTINGS",directory.path)
        commands.expression(directory)
    print(variables)
