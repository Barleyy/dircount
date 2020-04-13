from enum import Enum

from complex_operations import _if, _while, _for
from var_types import *


class Commands(Enum):
    declare = 1
    let = 2
    _if = 3
    _while = 4
    _for = 5
    print = 6


def ex_declare(directory):
    if directory.dirlen() != 2:
        raise ValueError(
            f"Directory {directory.path} of type Command.declare must have 2 subdirectories, given {directory.dirlen()}")
    declare(directory.navigate_to_nth_child(1))


def ex_let(directory):
    if directory.dirlen() != 2:
        raise ValueError(
            f"Directory {directory.path} of type Command.let must have 2 subdirectories , given{directory.dirlen()}")
    let(directory.navigate_to_nth_child(1))


def ex_if(directory):
    if directory.dirlen() != 2:
        raise ValueError(
            f"Directory {directory.path} of type Command.if must have 2 subdirectories , given {directory.dirlen()}")
    _if(directory.navigate_to_nth_child(1))


def ex_while(directory):
    if directory.dirlen() != 2:
        raise ValueError(
            f"Directory {directory.path} of type Command.while must have 2 subdirectories , given {directory.dirlen()}")
    _while(directory.navigate_to_nth_child(1))


def ex_for(directory):
    if directory.dirlen() != 2:
        raise ValueError(
            f"Directory {directory.path} of type Command.for must have 2 subdirectories , given {directory.dirlen()}")
    _for(directory.navigate_to_nth_child(1))


def ex_print(directory):
    return


commands_dict = {
    Commands.declare: ex_declare,
    Commands.let: ex_let,
    Commands._if: ex_if,
    Commands._while: ex_while,
    Commands._for: ex_for,
    Commands.print: ex_print
}


def expression(directory):
    commands_dict[Commands(directory.get_dir_type())](directory)
