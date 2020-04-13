from enum import Enum


class OperationType(Enum):
    arithmetic = 1
    comparison = 2
    string = 3
    list = 4


class ArithmeticOperation(Enum):
    add = 1
    subtract = 2
    multiply = 3
    divide = 4
    power = 5
    mod = 6


class ComparisonOperation(Enum):
    less = 1
    greater = 2
    leq = 3
    geq = 4
    eq = 5


class StringOperation(Enum):
    concat = 1
    eq = 2
    neq = 3


class ListOperation(Enum):
    get = 1
    concat = 2


global operations_dict
global operation_type

operations_dict = {
    ArithmeticOperation.add: lambda x, y: x + y,
    ArithmeticOperation.subtract: lambda x, y: x - y,
    ArithmeticOperation.multiply: lambda x, y: x * y,
    ArithmeticOperation.divide: lambda x, y: x / y,
    ArithmeticOperation.power: lambda x, y: x ** y,
    ArithmeticOperation.mod: lambda x, y: x % y,
    ComparisonOperation.less: lambda x, y: x < y,
    ComparisonOperation.greater: lambda x, y: x > y,
    ComparisonOperation.leq: lambda x, y: x <= y,
    ComparisonOperation.geq: lambda x, y: x >= y,
    ComparisonOperation.eq: lambda x, y: x == y,
    StringOperation.concat: lambda x, y: x + y,
    StringOperation.eq: lambda x, y: x == y,
    StringOperation.neq: lambda x, y: x != y,
    ListOperation.get: lambda x, y: x[y],
    ListOperation.concat: lambda x, y: x + y
}

operation_type = {
    OperationType.arithmetic: ArithmeticOperation,
    OperationType.comparison: ComparisonOperation,
    OperationType.string: StringOperation,
    OperationType.list: ListOperation,
}
