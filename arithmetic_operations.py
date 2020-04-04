from enum import Enum


class ArithmeticOperation(Enum):
    add = 1
    subtract = 2
    multiply = 3
    divide = 4
    power = 5
    mod = 6
    less = 7
    greater = 8
    leq = 9
    geq = 10
    eq = 11


global operations_dict

operations_dict = {
    ArithmeticOperation.add: lambda x, y: x + y,
    ArithmeticOperation.subtract: lambda x, y: x - y,
    ArithmeticOperation.multiply: lambda x, y: x * y,
    ArithmeticOperation.divide: lambda x, y: x / y,
    ArithmeticOperation.power: lambda x, y: x ** y,
    ArithmeticOperation.mod: lambda x, y: x % y,
    ArithmeticOperation.less: lambda x, y: x < y,
    ArithmeticOperation.greater: lambda x, y: x > y,
    ArithmeticOperation.leq: lambda x, y: x <= y,
    ArithmeticOperation.geq: lambda x, y: x >= y,
    ArithmeticOperation.eq: lambda x, y: x == y,

}
