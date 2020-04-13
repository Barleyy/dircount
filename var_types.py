import settings
from value_parsing import parse_value, types_len, parse_string_value, Types
from operation_parsing import parse_operation_argument


def declare(directory):
    if directory.dirlen() != 3:
        raise ValueError(
            f"Directory {directory.path} of type 'Declare' must have 3 subdirectories but has {directory.dirlen()}")
    var_directory = directory.navigate_to_nth_child(1)
    print(f"VAR TYPES DECLARE {directory.path}")
    name_directory = directory.navigate_to_nth_child(2)
    (var_name, value) = parse_and_validate(var_directory, name_directory, types_dict[Types(directory.get_dir_type())])

    attach_variable(name_directory.path, var_name, value, Types(directory.get_dir_type()))


def let(directory):
    if directory.dirlen() != 2:
        raise ValueError(
            f"Directory {directory.path} of type 'Let' must have 2 subdirectories varlink, value but has {directory.dirlen()}")
    var_directory = directory.navigate_to_nth_child(1)
    print(f"VAR TYPES LET {directory.path}")
    var_link = directory.navigate_to_nth_child(0).get_link_path()
    var_type = settings.variables[var_link][2]
    new_value = parse_value(var_directory, var_type, types_len[var_type])
    update_var_value(var_link, new_value)


def parse_and_validate(data_dir, name_directory, type):
    value = parse_operation_argument(data_dir)
    if value.__class__ is not type:
        raise ValueError("Type mismatch: expected {0} got {1}".format(type, value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE {type} {var_name} = {value}")
    return var_name, value


def get_var_names_from_vars_dict(variables):
    return map(lambda var: var[0], list(variables.values()))


def get_var_path_by_varname(variables, name):
    # passing variables dict for function impl
    return


def attach_variable(path, name, value, clazz):
    if path in settings.variables or name in get_var_names_from_vars_dict(settings.variables):
        raise ValueError(f"Variable {name} already defined")
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
    Types.int: int,
    Types.float: float,
    Types.char: str,
    Types.string: str,
    Types.boolean: bool,
    Types.list: list
}


class char:
    def __init__(self):
        self.data = None
