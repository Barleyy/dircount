import math
import os
import logging
from enum import Enum

import error_factory
from directory_functions import Directory
from function_adapter import Function
from operation_parsing import parse_operation_argument, operation_parsing
from operations import ArithmeticOperation, ComparisonOperation, StringOperation

logger = logging.getLogger("value_parsing")


class Types(Enum):
    function = 0
    int = 1
    float = 2
    char = 3
    string = 4
    boolean = 5
    list = 6
    dict = 7


def parse_generic_value(data_dir, type_class, basic_type_length):
    parsing_function = parsing_dict[type_class]

    if data_dir.dirlen() == basic_type_length:
        return parsing_function([data_dir, True])
    else:
        error_factory.ErrorFactory.unparsable_expression(data_dir.path)


def parse_value(data_dir, type_class, basic_type_length):
    logger.info(parse_value.__name__ + f" VAR TYPES Parsing declare value of type {type_class}")

    parsing_function = parsing_dict[type_class]

    if data_dir.dirlen() == basic_type_length:
        return parsing_function([data_dir, True])

    elif data_dir.dirlen() == 3:  # operation result
        return operation_parsing(data_dir)

    else:
        error_factory.ErrorFactory.unparsable_value(data_dir.parent_path.path, basic_type_length, data_dir.path,
                                                    type_class)


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
            error_factory.ErrorFactory.unparsable_value(char_dir.parent_path.path, 8, char_dir.path, Types.char)
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


def parse_dict_value(parsing_dict_data):
    vals_dir = parsing_dict_data[0]

    _dict = {}
    for pair in vals_dir.navigate_to_nth_child(0).get_directory_children():
        if pair.dirlen() != 2:
            error_factory.ErrorFactory.directory_parsing_error(pair.path, pair.dirlen())
        _dict[parse_operation_argument(pair.navigate_to_nth_child(0))] = parse_operation_argument(
            pair.navigate_to_nth_child(1))
    return _dict


def define_function(parsing_func_data):
    commands_root = parsing_func_data[0].navigate_to_nth_child(0).path

    fun_name = parse_and_validate_only_value(parsing_func_data[0].parent_path.navigate_to_nth_child(2), str)
    args_list = parse_list_value([parsing_func_data[0].navigate_to_nth_child(1)])

    if any(arg.__class__ is not str for arg in args_list):
        error_factory.ErrorFactory.invalid_argument_name()
    elif len(set(args_list)) != len(args_list):
        error_factory.ErrorFactory.duplicate_arg_name(fun_name)
    if parsing_func_data[0].navigate_to_nth_child(2).dirlen() != 0:
        return_val_id = parse_and_validate_only_value(parsing_func_data[0].navigate_to_nth_child(2), str)
    else:
        return_val_id = None
    if len(args_list) < 0:
        error_factory.ErrorFactory.invalid_function_args_no(len(args_list))

    logger.info(define_function.__name__ + " FUNCTION DEFINED TO " + commands_root + " " + fun_name + " " + str(args_list))
    return Function(commands_root, fun_name, args_list, return_val_id)


def parse_and_validate_only_value(data_dir, type):
    value = parse_operation_argument(data_dir)
    if value.__class__ is not type:
        error_factory.ErrorFactory.type_mismatch_error(type, value.__class__)
    logger.debug(parse_and_validate_only_value.__name__ + f" VAR TYPE {type} = {value}")
    return value


def parse_link(self):
    if self.dirlen() == 1:
        logger.debug(parse_link.__name__ + " LINK")
        return (os.readlink(self.navigate_to_nth_child(0).path), os.readlink(self.navigate_to_nth_child(0).path)[:-1])[
            os.readlink(self.navigate_to_nth_child(0).path).endswith('/')]
    elif self.dirlen() == 3:
        logger.debug(parse_link.__name__ + " NAME")
        str_dirs = list(filter(lambda it_dir: not os.path.islink(it_dir.path), self.get_directory_children()))
        return parse_string_value([Directory(children=str_dirs)])
    else:
        error_factory.ErrorFactory.command_not_found(self.path, self.dirlen())


def match_type(value):
    return python_types_dict[value.__class__]


parsing_dict = {
    Types.int: parse_integer_value,
    Types.float: parse_float_value,
    Types.char: parse_char_value,
    Types.string: parse_string_value,
    Types.boolean: parse_boolean_value,
    Types.list: parse_list_value,
    Types.dict: parse_dict_value,
    Types.function: define_function
}

types_operations_dict = {ArithmeticOperation: [Types.int, Types.float],
                         ComparisonOperation: [Types.int, Types.float, Types.string, Types.char, Types.boolean],
                         StringOperation: [Types.string, Types.char]}
# NONE TYPE CAN HAS LENGTH 3 or 6 (operation / function)!!!

types_len = {
    Types.int: 16,
    Types.float: 32,
    Types.char: 8,
    Types.string: 2,
    Types.list: 4,
    Types.dict: 5,
    Types.boolean: 1,
    Types.function: 6
}

len_types = {
    16: Types.int,
    32: Types.float,
    8: Types.char,
    1: Types.boolean,
    4: Types.list,
    5: Types.dict,
    2: Types.string,
    6: Types.function
}

python_types_dict = {
    int: Types.int,
    float: Types.float,
    str: Types.string,
    bool: Types.boolean,
    list: Types.list,
    dict: Types.dict,
    Function: Types.function
}
