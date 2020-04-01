from enum import Enum
from directory_functions import *
import settings
import math


class Types(Enum):
    _int = 1
    _float = 2
    _char = 3
    _string = 4


def declare(directory):
    if directory.dirlen() != 3:
        raise ValueError(
            f"Directory {directory.path} of type 'Declare' must have 3 subdirectories but has {directory.dirlen()}")
    var_directory = directory.navigate_to_nth_child(1)
    print(f"VAR TYPES {directory.path}")
    name_directory = directory.navigate_to_nth_child(2)
    types_dict[Types(directory.get_dir_type())](var_directory, name_directory)


def declare_int(bits_dir, name_directory):
    if bits_dir.dirlen() != 16:
        raise ValueError(
            f"First subdirectory of directory {bits_dir.parent_path.path} of type 'declare int' must have 16 subdirectories but has {bits_dir.dirlen()}")
    value = parse_integer_value(bits_dir, True)
    var_name = parse_string_value(name_directory)
    attach_variable(var_name, value)
    print(f"VAR TYPE INT {var_name} = {value}")


def declare_float(value_dir, name_directory):
    if value_dir.dirlen() != 32:
        raise ValueError(
            f"First subdirectory of directory {value_dir.parent_path.path} of type 'declare float' must have 32 subdirectories but has {value_dir.dirlen()}")
    mantissa_values = [2 ** -i for i in range(1,24)]
    exponent_values = [2 ** i for i in range(7,-1,-1)]
    bits = list(map(Directory.directory_to_bit, value_dir.get_children_paths()))
    exponent = sum([b * e for b, e in zip(exponent_values, bits[1:8])]) - 127
    mantissa = 1 + sum([b * e for b, e in zip(mantissa_values, bits[9:])])
    sign = (1, -1)[bits[0]]
    var_name = parse_string_value(name_directory)
    value = sign*mantissa*math.pow(2,exponent)
    attach_variable(var_name,value)
    print(f"VAR TYPE FLOAT {var_name} = {value}")


def declare_char(char_dir, name_directory):
    if char_dir.dirlen() != 8:
        raise ValueError(
            f"First subdirectory of directory {char_dir.parent_path.path} of type 'declare char' must have 8 subdirectories "
            f"ASCII (0-127) but has {char_dir.dirlen()}")
    char = chr(parse_integer_value(char_dir, False))
    var_name = parse_string_value(name_directory)
    attach_variable(var_name, char)
    print(f"VAR TYPE CHAR {var_name} = {char}")


def declare_string(chars_dir, name_directory):
    string = parse_string_value(chars_dir)
    var_name = parse_string_value(name_directory)
    attach_variable(var_name, string)
    print(f"VAR TYPE STRING {var_name} = {string}")


def parse_string_value(chars_dir):
    string_array = []
    for char_dir in chars_dir.get_directory_children():
        if char_dir.dirlen() != 8:
            raise ValueError(
                f"First subdirectory of directory {char_dir.path} of type 'declare char' must have 8 subdirectories "
                f"ASCII (0-127) but has {char_dir.dirlen()}")
        string_array.append(chr(parse_integer_value(char_dir, False)))
    return "".join(string_array)


def parse_integer_value(data_dir, is_number):
    range_value = data_dir.dirlen() - 1
    start_index = (0, 1)[is_number]
    bit_values = [2 ** i for i in range(range_value)]
    bits = list(map(Directory.directory_to_bit, data_dir.get_children_paths()))
    res = [b * e for b, e in zip(bit_values, bits[start_index:])]
    sign = (1, -1)[is_number and bits[0]]
    return sign * sum(res)


def attach_variable(name, value):
    if name in settings.variables:
        raise ValueError(f"Variable {name} already defined to {settings.variables[name]}")
    else:
        settings.variables[name] = value


types_dict = {
    Types._int: declare_int,
    Types._float: declare_float,
    Types._char: declare_char,
    Types._string: declare_string
}
