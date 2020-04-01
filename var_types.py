from enum import Enum
import settings
from directory_functions import *

class Types(Enum):
    _int = 1
    _float = 2
    _char = 3
    _string = 4

def declare(directory):
    if directory.dirlen() != 3:
        raise ValueError("Directory of type 'Declare' must have 3 subdirectories but has".format(directory.dirlen()))
    var_directory = directory.navigate_to_nth_child(1)
    name_directory = directory.navigate_to_nth_child(2)
    types_dict[Types(directory.get_dir_type())](var_directory, name_directory)

def declare_int(bits_dir, name_directory):
    if bits_dir.dirlen() != 16:
        raise ValueError("First subdirectory of directory of type 'declare int' must have 15 subdirectories but has {}".format(bits_dir.dirlen()))
    bit_values = [2**i for i in range(15)]

    def directory_to_bit(directory_path):
        n_subdirs = Directory(directory_path).dirlen()
        if n_subdirs > 1:
            raise ValueError("Directories inside bits declaration can only have either 0 or 1 subdirectories but {} has {}".format(directory_path, n_subdirs))
        else:
            return n_subdirs

    bits = list(map(directory_to_bit, bits_dir.get_children_paths()))
    res = [b*e for b, e in zip(bit_values, bits[1:])]
    sign = -1 if bits[0] else 1
    print(sign*sum(res)) # TODO to se trzeba zapisać


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