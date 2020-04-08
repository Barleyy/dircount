import commands
from directory_functions import Directory
from var_types import parse_declare_value, Types


def _if(directory):
    if not 3 >= directory.dirlen() >= 2:
        raise ValueError(f"Expected 2-3 dirs at {directory.path} for if command, given {directory.dirlen()}")
    if parse_declare_value(directory.navigate_to_nth_child(0), Types.boolean, 1):
        print("IF true execution")
        root = Directory(directory.navigate_to_nth_child(1).path)
        for directory in root.get_directory_children():
            print("SETTINGS", directory.path)
            commands.expression(directory)

    else:
        print("IF false execution")
        root = Directory(directory.navigate_to_nth_child(1).path)
        for directory in root.get_directory_children():
            print("SETTINGS", directory.path)
            commands.expression(directory)
