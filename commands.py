from enum import Enum

from complex_operations import _if, _while, _for, _function
from value_parsing import parse_list_value
from var_types import *


class Commands(Enum):
    function = 0
    declare = 1
    let = 2
    _if = 3
    _while = 4
    _for = 5
    print = 6


def ex_declare(directory):
    if directory.dirlen() != 2:
        error_factory.ErrorFactory.dir_length_error("DECLARE", directory.path, directory.dirlen())
    declare(directory.navigate_to_nth_child(1))


def ex_let(directory):
    if directory.dirlen() != 2:
        error_factory.ErrorFactory.dir_length_error("LET", directory.path, directory.dirlen())
    let(directory.navigate_to_nth_child(1))


def ex_if(directory):
    if directory.dirlen() != 2:
        error_factory.ErrorFactory.dir_length_error("IF", directory.path, directory.dirlen())
    _if(directory.navigate_to_nth_child(1))


def ex_while(directory):
    if directory.dirlen() != 2:
        error_factory.ErrorFactory.dir_length_error("WHILE", directory.path, directory.dirlen())
    _while(directory.navigate_to_nth_child(1))


def ex_for(directory):
    if directory.dirlen() != 2:
        error_factory.ErrorFactory.dir_length_error("FOR", directory.path, directory.dirlen())
    _for(directory.navigate_to_nth_child(1))


def ex_print(directory):
    args = parse_list_value([directory.navigate_to_nth_child(1)])
    print(*args)


def ex_function(directory):
    print("TO DO EXEC")
    if directory.dirlen() != 2:
        error_factory.ErrorFactory.dir_length_error("EXEC FUN", directory.path, directory.dirlen())
    _function(directory.navigate_to_nth_child(1))


commands_dict = {
    Commands.declare: ex_declare,
    Commands.let: ex_let,
    Commands._if: ex_if,
    Commands._while: ex_while,
    Commands._for: ex_for,
    Commands.print: ex_print,
    Commands.function: ex_function
}


def expression(directory):
    commands_dict[Commands(directory.get_dir_type())](directory)
