import settings
import value_parsing
from operations import operation_type, OperationType, operations_dict


def parse_operation_argument(operation_arg_dir):
    # assuming none var type has size 3 (int 16, float 32, bool 1, char 8, string 2)
    is_link_val = operation_arg_dir.is_var_linked()

    if is_link_val:  # is link
        invoked_function = settings.get_currently_invoked_function()
        arg_val = invoked_function.variable_stack.get_var_by_path(operation_arg_dir.navigate_to_nth_child(0).get_link_path()).value

    elif operation_arg_dir.dirlen() != 3:  # not link and not operation -> simple type
        _type = value_parsing.len_types[operation_arg_dir.dirlen()]
        arg_val = value_parsing.parse_generic_value(operation_arg_dir, _type, value_parsing.types_len[_type])

    else:  # arg is operation
        arg_val = operation_parsing(operation_arg_dir)

    return arg_val


def operation_parsing(data_dir):
    # operation tree ends when 2 operation values have equal dirlens
    operation_type_dir = data_dir.navigate_to_nth_child(0)
    operation_type_enum = operation_type[OperationType(operation_type_dir.get_dir_type())]
    operation_arg1_dir = data_dir.navigate_to_nth_child(1)
    operation_arg2_dir = data_dir.navigate_to_nth_child(2)

    val1 = parse_operation_argument(operation_arg1_dir)
    val2 = parse_operation_argument(operation_arg2_dir)

    return operations_dict[operation_type_enum(operation_type_dir.navigate_to_nth_child(1).dirlen())](val1, val2)
