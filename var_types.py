import math
from enum import Enum

import settings
from directory_functions import *
from operations import operations_dict, operation_type, OperationType, ArithmeticOperation, ComparisonOperation, \
    StringOperation


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
    (var_name, value) = types_dict[Types(directory.get_dir_type())](var_directory, name_directory)
    attach_variable(name_directory.path, var_name, value, Types(directory.get_dir_type()))


def let(directory):
    if directory.dirlen() != 2:
        raise ValueError(
            f"Directory {directory.path} of type 'Let' must have 2 subdirectories varlink, value but has {directory.dirlen()}")
    var_directory = directory.navigate_to_nth_child(1)
    print(f"VAR TYPES {directory.path}")
    var_link = directory.navigate_to_nth_child(0).get_link_path()
    var_type = settings.variables[var_link][2]
    new_value = parse_declare_value(var_directory, var_type, types_len[var_type])
    update_var_value(var_link, new_value)


def declare_int(bits_dir, name_directory):
    value = parse_declare_value(bits_dir, Types.int, types_len[Types.int])
    if value.__class__ is not int:
        raise ValueError("Type mismatch: expected {0} got {1}".format(int, value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE INT {var_name} = {value}")
    return var_name, value


def declare_float(value_dir, name_directory):
    value = parse_declare_value(value_dir, Types.float, types_len[Types.float])
    if value.__class__ is not float:
        raise ValueError("Type mismatch: expected {0} got {1}".format(float, value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE FLOAT {var_name} = {value}")
    return var_name, value


def declare_char(char_dir, name_directory):
    value = parse_declare_value(char_dir, Types.char, types_len[Types.char])
    if value.__class__ is not str and value.len() > 1:
        raise ValueError("Type mismatch: expected {0} got {1}".format("char", value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE CHAR {var_name} = {value}")
    return var_name, value


def declare_string(chars_dir, name_directory):
    value = parse_declare_value(chars_dir, Types.string, types_len[Types.string])
    if value.__class__ is not str:
        raise ValueError("Type mismatch: expected {0} got {1}".format(str, value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE STRING {var_name} = {value}")
    return var_name, value


def declare_boolean(bit_dir, name_directory):
    value = parse_declare_value(bit_dir, Types.boolean, types_len[Types.boolean])
    if value.__class__ is not bool:
        raise ValueError("Type mismatch: expected {0} got {1}".format(bool, value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE STRING {var_name} = {value}")
    return var_name, value


def operation_parsing(data_dir):
    # operation tree ends when 2 operation values have equal dirlens
    operation_type_dir = data_dir.navigate_to_nth_child(0)
    operation_type_enum = operation_type[OperationType(operation_type_dir.get_dir_type())]
    is_link_val1 = data_dir.navigate_to_nth_child(1).is_link()
    is_link_val2 = data_dir.navigate_to_nth_child(2).is_link()

    val1 = None
    val2 = None
    if is_link_val1:
        print("A",settings.variables[data_dir.navigate_to_nth_child(1).get_link_path()])
        val1 = settings.variables[data_dir.navigate_to_nth_child(1).get_link_path()][1]
        print("B",val1)

    if is_link_val2:
        print("C",settings.variables[data_dir.navigate_to_nth_child(1).get_link_path()])
        val2 = settings.variables[data_dir.navigate_to_nth_child(2).get_link_path()][1]
        print("D",val2)

    if (data_dir.navigate_to_nth_child(1).dirlen() == data_dir.navigate_to_nth_child(
            2).dirlen() and data_dir.navigate_to_nth_child(1).dirlen() != 3) or is_link_val1 or is_link_val2:  # leaves of operation ast
        type = len_types[data_dir.navigate_to_nth_child(2).dirlen()]
        print("E",data_dir.navigate_to_nth_child(2).path)
        print("F",is_link_val1)
        val1 = val1 if is_link_val1 else parse_declare_value(data_dir.navigate_to_nth_child(1), type, types_len[type])
        print("G",val1)
        val2 = val2 if is_link_val2 else parse_declare_value(data_dir.navigate_to_nth_child(2), type, types_len[type])
        print("H",val2)
    else:  # one of args is operation
        is_operation_at_first = data_dir.navigate_to_nth_child(1).dirlen() == 3
        if is_operation_at_first:
            val1 = operation_parsing(data_dir.navigate_to_nth_child(1))
        else:
            type = len_types[data_dir.navigate_to_nth_child(1).dirlen()]
            val1 = parse_declare_value(data_dir.navigate_to_nth_child(1), type, types_len[type])
        is_operation_at_second = data_dir.navigate_to_nth_child(2).dirlen() == 3
        if is_operation_at_second:
            val2 = operation_parsing(data_dir.navigate_to_nth_child(2))
        else:
            type = len_types[data_dir.navigate_to_nth_child(2).dirlen()]
            val2 = parse_declare_value(data_dir.navigate_to_nth_child(2), type, types_len[type])
    return operations_dict[operation_type_enum(operation_type_dir.navigate_to_nth_child(1).dirlen())](val1, val2)

def parse_declare_value(data_dir, type_class, basic_type_length):
    print(f"VAR TYPES Parsing declare value of type {type_class}")
    print(data_dir.path)
    parsing_function = parsing_dict[type_class]
    print(parsing_function.__name__)
    print(data_dir.dirlen())
    print(basic_type_length)
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


def attach_variable(path, name, value, clazz):
    if path in settings.variables:
        raise ValueError(f"Variable {name} already defined to {settings.variables[name]}")
    else:
        settings.variables[path] = (name, value, clazz)


def update_var_value(path, value):
    if path not in settings.variables:
        raise ValueError(f"Variable at {path} not defined")
    else:
        var_properties = list(settings.variables[path])
        var_properties[1] = value
        settings.variables[path] = tuple(var_properties)


types_dict = {
    Types.int: declare_int,
    Types.float: declare_float,
    Types.char: declare_char,
    Types.string: declare_string,
    Types.boolean: declare_boolean
}

parsing_dict = {
    Types.int: parse_integer_value,
    Types.float: parse_float_value,
    Types.char: parse_char_value,
    Types.string: parse_string_value,
    Types.boolean: parse_boolean_value
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
    Types.boolean: 1
}

len_types = {
    16: Types.int,
    32: Types.float,
    8: Types.char,
    1: Types.boolean,
    2: Types.string
}


class char:
    def __init__(self):
        self.data = None
