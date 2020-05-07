import error_factory
import settings
from function_adapter import Function
from value_parsing import parse_value, types_len, parse_string_value, Types
from operation_parsing import parse_operation_argument


def declare(directory):
    if directory.dirlen() != 3:
        error_factory.ErrorFactory.invalid_command_dir_number([3], directory.path, directory.dirlen(), "DECLARE")
    var_directory = directory.navigate_to_nth_child(1)
    print(f"VAR TYPES DECLARE {directory.path}")
    name_directory = directory.navigate_to_nth_child(2)
    (var_name, value) = parse_and_validate(var_directory, name_directory, types_dict[Types(directory.get_dir_type())])

    attach_variable(name_directory.path, var_name, value, Types(directory.get_dir_type()))
    return name_directory.path, var_name, value


def let(directory):
    if directory.dirlen() != 2:
        error_factory.ErrorFactory.invalid_command_dir_number([2], directory.path, directory.dirlen(), "LET")
    var_directory = directory.navigate_to_nth_child(1)
    print(f"VAR TYPES LET {directory.path}")
    var_link = directory.navigate_to_nth_child(0).get_link_path()
    invoked_function = settings.get_currently_invoked_function()
    var_type = invoked_function.variable_stack[var_link][2]
    new_value = parse_value(var_directory, var_type, types_len[var_type])
    update_var_value(var_link, new_value)


def parse_and_validate(data_dir, name_directory, type):
    value = parse_operation_argument(data_dir)
    if value.__class__ is not type:
        error_factory.ErrorFactory.type_mismatch_error(type, value.__class__)
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE {type} {var_name} = {value}")
    return var_name, value


def get_var_names_from_vars_dict(variables):
    return map(lambda var: var[0], list(variables.values()))


def get_var_path_by_varname(variables, name):
    # passing variables dict for function impl
    return


def attach_variable(path, name, value, clazz):
    invoked_function = settings.get_currently_invoked_function()
    if path in invoked_function.variable_stack or name in get_var_names_from_vars_dict(invoked_function.variable_stack):
        error_factory.ErrorFactory.var_already_defined_error(name)
    else:
        invoked_function.variable_stack[path] = (name, value, clazz)


def update_var_value(path, value):
    invoked_function = settings.get_currently_invoked_function()
    if path not in invoked_function.variable_stack:
        error_factory.ErrorFactory.var_not_defined_error(path)
    else:
        var_properties = list(invoked_function.variable_stack[path])
        var_properties[1] = value
        invoked_function.variable_stack[path] = tuple(var_properties)


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
