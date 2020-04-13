import math
from enum import Enum

from directory_functions import Directory
from operation_parsing import operation_parsing, parse_operation_argument
from operations import ArithmeticOperation, ComparisonOperation, StringOperation


class Types(Enum):
    int = 1
    float = 2
    char = 3
    string = 4
    boolean = 5
    list = 6


def parse_generic_value(data_dir, type_class, basic_type_length):
    parsing_function = parsing_dict[type_class]

    if data_dir.dirlen() == basic_type_length:
        return parsing_function([data_dir, True])
    else:
        raise ValueError(f"Could not parse value at {data_dir.path}")


def parse_value(data_dir, type_class, basic_type_length):
    print(f"VAR TYPES Parsing declare value of type {type_class}")

    parsing_function = parsing_dict[type_class]

    if data_dir.dirlen() == basic_type_length:
        return parsing_function([data_dir, True])

    elif data_dir.dirlen() == 3:  # operation result
        return operation_parsing(data_dir)

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
    mantissa_values = [2 ** -i for i in range(23, 0, -1)]
    exponent_values = [2 ** i for i in range(8)]
    bits = list(map(Directory.directory_to_bit, value_dir.get_children_paths()))
    exponent = sum([b * e for b, e in zip(exponent_values, bits[23:32])]) - 127
    mantissa = 1 + sum([b * e for b, e in zip(mantissa_values, bits[:23])])
    sign = (1, -1)[bits[31]]
    value = sign * mantissa * math.pow(2, exponent)
    return value


def parse_char_value(parsing_char_data):
    char_dir = parsing_char_data[0]
    char = chr(parse_integer_value([char_dir, False]))
    return char


def parse_string_value(parsing_string_data):
    chars_dir = parsing_string_data[0]

    string_array = []
    for char_dir in chars_dir.navigate_to_nth_child(0).get_directory_children():
        if char_dir.dirlen() != 8:
            raise ValueError(
                f"First subdirectory of directory {char_dir.path} of type 'declare char' must have 8 subdirectories "
                f"ASCII (0-127) but has {char_dir.dirlen()}")
        string_array.append(chr(parse_integer_value([char_dir, False])))
    return "".join(string_array)


def parse_boolean_value(parsing_boolean_data):
    boolean_dir = parsing_boolean_data[0]
    return bool(boolean_dir.get_dir_type())


def parse_list_value(parsing_list_data):
    vals_dir = parsing_list_data[0]

    list_array = []
    for val in vals_dir.navigate_to_nth_child(0).get_directory_children():
        list_array.append(parse_operation_argument(val))
    return list_array


parsing_dict = {
    Types.int: parse_integer_value,
    Types.float: parse_float_value,
    Types.char: parse_char_value,
    Types.string: parse_string_value,
    Types.boolean: parse_boolean_value,
    Types.list: parse_list_value
}

types_errors_dict = {
    Types.int: "Either first subdirectory of directory {0} of type 'declare int' must have {1} subdirectories or "
               "operation returning int value at level {2} expected",
    Types.float: "Either first subdirectory of directory {0} of type 'declare float' must have {1} subdirectories or "
                 "operation returning float value at level {2} expected",
    Types.char: "Either first subdirectory of directory {0} of type 'declare char' must have 8 subdirectories or "
                "operation returning char value at level {2} expected",
    Types.string: "Either data subdir of directory {0} of type 'declare string' must have 8 subdirectories or "
                  "operation returning string value at level {2} expected",
    Types.boolean: "Either first subdirectory of directory {0} of type 'declare boolean' must have 0-1 subdirectories "
                   "or operation returning boolean value at level {2} expected"
}

types_operations_dict = {ArithmeticOperation: [Types.int, Types.float],
                         ComparisonOperation: [Types.int, Types.float, Types.string, Types.char, Types.boolean],
                         StringOperation: [Types.string, Types.char]}

# NONE TYPE CAN HAS LENGTH 3!!!
types_len = {
    Types.int: 16,
    Types.float: 32,
    Types.char: 8,
    Types.string: 2,
    Types.list: 4,
    Types.boolean: 1
}

len_types = {
    16: Types.int,
    32: Types.float,
    8: Types.char,
    1: Types.boolean,
    4: Types.list,
    2: Types.string
}
