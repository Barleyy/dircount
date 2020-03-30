from enum import Enum
import settings
from types import *
from functions import *


class Commands(Enum):
    declare = 1
    _if = 2
    _while = 3
    _for = 4
    _print = 5

def ex_declare():
    declare()

def ex_if():
    return

def ex_while():
    return

def ex_for():
    return

def ex_print():
    return

commands_dict = {
    Commands.declare : ex_declare,
    Commands._if : ex_if,
    Commands._while : ex_while,
    Commands._for : ex_for,
    Commands._print : ex_print
}

def expression():
    commands_dict[Commands(dirlen())]()