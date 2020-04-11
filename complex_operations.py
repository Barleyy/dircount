import commands
import settings
from directory_functions import Directory
from var_types import parse_value, Types


def _if(directory):
    if not 3 >= directory.dirlen() >= 2:
        raise ValueError(f"Expected 2-3 dirs at {directory.path} for if command, given {directory.dirlen()}")
    if parse_value(directory.navigate_to_nth_child(0), Types.boolean, 1):
        print("IF true execution")
        root = Directory(directory.navigate_to_nth_child(1).path)
        for directory in root.get_directory_children():
            print("COMPLEX IF TRUE", directory.path)
            commands.expression(directory)

    else:
        print("IF false execution")
        root = Directory(directory.navigate_to_nth_child(1).path)
        for directory in root.get_directory_children():
            print("COMPLEX IF FALSE", directory.path)
            commands.expression(directory)


def _while(directory):
    if directory.dirlen() != 2:  # logical condition, list of commands
        raise ValueError(f"Expected 2 dirs at {directory.path} for while command, given {directory.dirlen()}")

    condition_dir = directory.navigate_to_nth_child(0)
    counter = 1
    while parse_value(condition_dir, Types.boolean, 1):
        print(f"WHILE executing {counter} times")
        root = Directory(directory.navigate_to_nth_child(1).path)
        for commands_dir in root.get_directory_children():
            print("COMPLEX WHEN command at", commands_dir.path)
            commands.expression(commands_dir)
        counter += 1
