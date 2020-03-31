from enum import Enum
import settings
from directory_functions import *

class Types(Enum):
    _int = 1
    _float = 2
    _char = 3
    _string = 4

def declare(directory):
    var_directory = dirmove(directory, 0)
    types_dict[Types(dirlen(directory))](var_directory)     # TODO mosze jakiś ładny error

def declare_int(directory):
    print("declaring int")
    bit_values = [2**i for i in range(16)]
    def directory_to_bit(directory_):
        n_subdirs = len(os.listdir(directory + "/bits/" + directory_))
        if n_subdirs > 1:
            raise ValueError("Directories inside int declaration can only have either 0 or 1 subdirectories")
        else:
            return n_subdirs
    bits_dir = dirmove(directory, 0)
    bits = map(directory_to_bit, os.listdir(bits_dir))
    res = [b*e for b, e in zip(bit_values, list(bits))] # TODO to se trzeba zapisać
    print(sum(res))


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