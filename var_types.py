import error_factory
import logging
from function_adapter import Function
from operation_parsing import parse_operation_argument
from value_parsing import parse_value, types_len, parse_string_value, Types, parse_link
from variable_holder import VariableId, VariableHolder

logger = logging.getLogger("var_types")


def declare(directory):
    if directory.dirlen() != 3:
        error_factory.ErrorFactory.invalid_command_dir_number([3], directory.path, directory.dirlen(), "DECLARE")
    var_directory = directory.navigate_to_nth_child(1)
    logger.debug(declare.__name__ + f" VAR TYPES DECLARE {directory.path}")
    name_directory = directory.navigate_to_nth_child(2)
    (var_name, value) = parse_and_validate(var_directory, name_directory, types_dict[Types(directory.get_dir_type())])

    attach_variable(name_directory.path, var_name, value, Types(directory.get_dir_type()))
    return name_directory.path, var_name, value


def let(directory):
    if directory.dirlen() != 2:
        error_factory.ErrorFactory.invalid_command_dir_number([2], directory.path, directory.dirlen(), "LET")
    var_directory = directory.navigate_to_nth_child(1)
    logger.debug(let.__name__ + f" VAR TYPES LET {directory.path}")
    var_link = parse_link(directory.navigate_to_nth_child(0))
    import function_utils
    invoked_function = function_utils.get_currently_invoked_function()
    var_type = invoked_function.get_var(var_link).type
    new_value = parse_value(var_directory, var_type, types_len[var_type])
    update_var_value(var_link, new_value)


def parse_and_validate(data_dir, name_directory, type):
    value = parse_operation_argument(data_dir)
    if value.__class__ is not type:
        error_factory.ErrorFactory.type_mismatch_error(type, value.__class__)
    var_name = parse_string_value([name_directory])
    if var_name.startswith('/'):
        error_factory.ErrorFactory.restricted_variable_name_prefix(data_dir, var_name)
    logger.debug(parse_and_validate.__name__ + f" VAR TYPE {type} {var_name} = {value}")
    return var_name, value


def attach_variable(path, name, value, clazz):
    import function_utils
    invoked_function = function_utils.get_currently_invoked_function()
    variable_id = VariableId(path, name)
    variable_value = VariableHolder(clazz, value)
    if invoked_function.variable_stack.check_if_var_exists_by_path(
            path) or invoked_function.variable_stack.check_if_var_exists_by_name(name):
        error_factory.ErrorFactory.var_already_defined_error(name)
    else:
        invoked_function.variable_stack.create_var(variable_id, variable_value)


def update_var_value(path, value):
    import function_utils
    invoked_function = function_utils.get_currently_invoked_function()
    if not invoked_function.variable_stack.check_if_var_exists_by_path(
            path):
        error_factory.ErrorFactory.var_not_defined_error(path)
    else:
        var_value = invoked_function.variable_stack.get_var_by_path(path)
        var_value.value = value


types_dict = {
    Types.int: int,
    Types.float: float,
    Types.char: str,
    Types.string: str,
    Types.boolean: bool,
    Types.list: list,
    Types.dict: dict,
    Types.function: Function
}


class char:
    def __init__(self):
        self.data = None
