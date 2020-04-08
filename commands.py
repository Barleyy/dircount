from enum import Enum
import settings
from var_types import *
from directory_functions import *


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
            f"Directory {directory.path} of type Command let must have 2 subdirectories : type, expression, given{directory.dirlen()}")
    let(directory.navigate_to_nth_child(1))


def ex_if(directory):
    return


def ex_while(directory):
    return


def ex_for(directory):
    return


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
