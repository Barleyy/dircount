import math
from enum import Enum

import settings
from arithmetic_operations import operations_dict, ArithmeticOperation
from directory_functions import *


class Types(Enum):
    int = 1
    float = 2
    char = 3
    string = 4
    boolean = 5


def declare(directory):
    if directory.dirlen() != 3:
        raise ValueError(
            f"Directory {directory.path} of type 'Declare' must have 3 subdirectories but has {directory.dirlen()}")
    var_directory = directory.navigate_to_nth_child(1)
    print(f"VAR TYPES {directory.path}")
    name_directory = directory.navigate_to_nth_child(2)
    types_dict[Types(directory.get_dir_type())](var_directory, name_directory)


def declare_int(bits_dir, name_directory):
    value = parse_declare_value(bits_dir, Types.int, 16)
    var_name = parse_string_value([name_directory])
    attach_variable(var_name, value)
    print(f"VAR TYPE INT {var_name} = {value}")


def declare_float(value_dir, name_directory):
    value = parse_declare_value(value_dir, Types.float, 32)
    var_name = parse_string_value([name_directory])
    attach_variable(var_name, value)
    print(f"VAR TYPE FLOAT {var_name} = {value}")


def declare_char(char_dir, name_directory):
    value = parse_declare_value(char_dir, Types.char, 8)
    var_name = parse_string_value([name_directory])
    attach_variable(var_name, value)
    print(f"VAR TYPE CHAR {var_name} = {value}")


def declare_string(chars_dir, name_directory):
    string = parse_declare_value(chars_dir, Types.string, 8)
    var_name = parse_string_value([name_directory])
    attach_variable(var_name, string)
    print(f"VAR TYPE STRING {var_name} = {string}")


def parse_declare_value(data_dir, type_class, basic_type_length):
    print(f"VAR TYPES Parsing declare value of type {type_class}")

    parsing_function = parsing_dict[type_class]

    if data_dir.dirlen() == basic_type_length or data_dir.get_dir_type() == basic_type_length:
        return parsing_function([data_dir, True])

    elif data_dir.dirlen() == 3 and ((data_dir.get_dir_type() < 2 or data_dir.get_dir_type() > 6)
                                     or type_class in supported_complex_operations_classes):

        return operations_dict[ArithmeticOperation(data_dir.get_dir_type())](
            parse_declare_value(data_dir.navigate_to_nth_child(1), type_class, basic_type_length),
            parse_declare_value(data_dir.navigate_to_nth_child(2), type_class, basic_type_length))
    else:
        raise ValueError(
            types_errors_dict[type_class].format(data_dir.parent_path.path, basic_type_length, data_dir.path))


def parse_integer_value(parsing_int_data):
    data_dir = parsing_int_data[0]
    is_number = parsing_int_data[1]
    range_value = data_dir.dirlen() - 1
    start_index = (0, 1)[is_number]
    bit_values = [2 ** i for i in range(range_value)]
    bits = list(map(Directory.directory_to_bit, data_dir.get_children_paths()))
    res = [b * e for b, e in zip(bit_values, bits[start_index:])]
    sign = (1, -1)[is_number and bits[0]]
    return sign * sum(res)


def parse_float_value(parsing_float_data):
    value_dir = parsing_float_data[0]
    mantissa_values = [2 ** -i for i in range(1, 24)]
    exponent_values = [2 ** i for i in range(7, -1, -1)]
    bits = list(map(Directory.directory_to_bit, value_dir.get_children_paths()))
    exponent = sum([b * e for b, e in zip(exponent_values, bits[1:8])]) - 127
    mantissa = 1 + sum([b * e for b, e in zip(mantissa_values, bits[9:])])
    sign = (1, -1)[bits[0]]
    value = sign * mantissa * math.pow(2, exponent)
    return value


def parse_char_value(parsing_char_data):
    char_dir = parsing_char_data[0]
    char = chr(parse_integer_value([char_dir, False]))
    return char


def parse_string_value(parsing_string_data):
    chars_dir = parsing_string_data[0]

    string_array = []
    for char_dir in chars_dir.get_directory_children():
        if char_dir.dirlen() != 8:
            raise ValueError(
                f"First subdirectory of directory {char_dir.path} of type 'declare char' must have 8 subdirectories "
                f"ASCII (0-127) but has {char_dir.dirlen()}")
        string_array.append(chr(parse_integer_value([char_dir, False])))
    return "".join(string_array)


def attach_variable(name, value):
    if name in settings.variables:
        raise ValueError(f"Variable {name} already defined to {settings.variables[name]}")
    else:
        settings.variables[name] = value


types_dict = {
    Types.int: declare_int,
    Types.float: declare_float,
    Types.char: declare_char,
    Types.string: declare_string,
    # Types.boolean: declare_boolean todo add boolean handling
}

parsing_dict = {
    Types.int: parse_integer_value,
    Types.float: parse_float_value,
    Types.char: parse_char_value,
    Types.string: parse_string_value
}

types_errors_dict = {
    Types.int: "Either first subdirectory of directory {0} of type 'declare int' must have {1} subdirectories or "
               "operation returning int value at level {2} expected",
    Types.float: "Either first subdirectory of directory {0} of type 'declare float' must have {1} subdirectories or "
                 "operation returning float value at level {2} expected",
    Types.char: "Either first subdirectory of directory {0} of type 'declare char' must have 8 subdirectories or "
                "operation returning char value at level {2} expected",
    Types.string: "Either data subdir of directory {0} of type 'declare string' must have 8 subdirectories or "
                  "operation returning string value at level {2} expected"

}

supported_complex_operations_classes = [Types.int, Types.float]
