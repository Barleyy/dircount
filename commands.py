from enum import Enum
import settings
from var_types import *
from directory_functions import *


class Commands(Enum):
    declare = 1
    _if = 2
    _while = 3
    _for = 4
    _print = 5

def ex_declare(directory):
    declare(directory)

def ex_if(directory):
    return

def ex_while(directory):
    return

def ex_for(directory):
    return

def ex_print(directory):
    return

commands_dict = {
    Commands.declare : ex_declare,
    Commands._if : ex_if,
    Commands._while : ex_while,
    Commands._for : ex_for,
    Commands._print : ex_print
}

def expression(directory):
    commands_dict[Commands(dirlen(directory))](directory)