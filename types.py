from enum import Enum
import settings
from functions import *

class Types(Enum):
    _int = 1
    _float = 2
    _char = 3
    _string = 4

def declare():
    dirmove(1)
    types_dict[Types(dirlen())]()

def declare_int():
    return

def declare_float():
    return

def declare_char():
    return

def declare_string():
    return


types_dict = {
    Types._int : declare_int,
    Types._float : declare_float,
    Types._char : declare_char,
    Types._string : declare_string
}