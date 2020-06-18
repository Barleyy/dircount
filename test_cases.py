from enum import Enum
from commands import *
import os

current_dir = os.getcwd()
test_dir = f"{current_dir}/ex_prog"


class VariableExpectation:
    def __init__(self, _name, _value, _type):
        self.name = _name
        self.value = _value
        self.type = _type


def expectation(name, value, type):
    return VariableExpectation(name, value, type)


class Case:
    def __init__(self, test_command_path, variable_expectations):
        self.test_command_path = test_command_path
        self.variable_expectations = variable_expectations


class CaseDefinition(Enum):
    command1 = Case(f"{test_dir}/command1", [expectation("var0", -1, Types.int)])
    command2 = Case(f"{test_dir}/command2", [expectation("var1", "A", Types.char)])
    command3 = Case(f"{test_dir}/command3", [expectation("var2", "KUR", Types.string)])
    command4 = Case(f"{test_dir}/command4", [expectation("var3", -12.5, Types.float)])
    command5 = Case(f"{test_dir}/command5", [expectation('var4', 0, Types.int)])
    command6 = Case(f"{test_dir}/command6", [expectation('var5', "KURKUR", Types.string)])
    command7 = Case(f"{test_dir}/command7", [expectation('var6', False, Types.boolean)])
    command10 = Case(f"{test_dir}/command10", [])
    command11 = Case(f"{test_dir}/command11", [expectation('var<', -1, Types.int)])
    command13 = Case(f"{test_dir}/command13", [expectation('var8', 0, Types.int)])
    command14 = Case(f"{test_dir}/command14", [])
    command15 = Case(f"{test_dir}/command15", [expectation('var111', [-1, 'var1', 1, False], Types.list)])

    @staticmethod
    def get_all_paths():
        return list(map(lambda x: x.value.test_command_path, CaseDefinition))

    @staticmethod
    def get_all_expectations():
        return list(map(lambda x: x.value.variable_expectations, CaseDefinition))
