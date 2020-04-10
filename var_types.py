import settings
from value_parsing import parse_value, types_len, parse_string_value, Types


def declare(directory):
    if directory.dirlen() != 3:
        raise ValueError(
            f"Directory {directory.path} of type 'Declare' must have 3 subdirectories but has {directory.dirlen()}")
    var_directory = directory.navigate_to_nth_child(1)
    print(f"VAR TYPES DECLARE {directory.path}")
    name_directory = directory.navigate_to_nth_child(2)
    (var_name, value) = types_dict[Types(directory.get_dir_type())](var_directory, name_directory)

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


def declare_int(bits_dir, name_directory):
    value = parse_value(bits_dir, Types.int, types_len[Types.int])
    if value.__class__ is not int:
        raise ValueError("Type mismatch: expected {0} got {1}".format(int, value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE INT {var_name} = {value}")
    return var_name, value


def declare_float(value_dir, name_directory):
    value = parse_value(value_dir, Types.float, types_len[Types.float])
    if value.__class__ is not float:
        raise ValueError("Type mismatch: expected {0} got {1}".format(float, value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE FLOAT {var_name} = {value}")
    return var_name, value


def declare_char(char_dir, name_directory):
    value = parse_value(char_dir, Types.char, types_len[Types.char])
    if value.__class__ is not str and value.len() > 1:
        raise ValueError("Type mismatch: expected {0} got {1}".format("char", value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE CHAR {var_name} = {value}")
    return var_name, value


def declare_string(chars_dir, name_directory):
    value = parse_value(chars_dir, Types.string, types_len[Types.string])
    if value.__class__ is not str:
        raise ValueError("Type mismatch: expected {0} got {1}".format(str, value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE STRING {var_name} = {value}")
    return var_name, value


def declare_boolean(bit_dir, name_directory):
    value = parse_value(bit_dir, Types.boolean, types_len[Types.boolean])
    if value.__class__ is not bool:
        raise ValueError("Type mismatch: expected {0} got {1}".format(bool, value.__class__))
    var_name = parse_string_value([name_directory])
    print(f"VAR TYPE STRING {var_name} = {value}")
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
    Types.int: declare_int,
    Types.float: declare_float,
    Types.char: declare_char,
    Types.string: declare_string,
    Types.boolean: declare_boolean
}


class char:
    def __init__(self):
        self.data = None
