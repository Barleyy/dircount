from enum import Enum
import settings
from directory_functions import *

class Types(Enum):
    _int = 1
    _float = 2
    _char = 3
    _string = 4

def declare(directory):
    directory = dirmove(directory, 0)
    types_dict[Types(dirlen(directory))](directory)

def declare_int(directory):
    print("declaring int")

def declare_float(directory):
    print("declaring float")

def declare_char(directory):
    print("declaring char")

def declare_string(directory):
    print("declaring string")


types_dict = {
    Types._int : declare_int,
    Types._float : declare_float,
    Types._char : declare_char,
    Types._string : declare_string
}