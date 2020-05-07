from function_adapter import Function


def get_currently_invoked_function():
    print(Function.function_stack)
    return Function.function_stack[len(Function.function_stack) - 1]


def init(pointer):
    function_main = Function(pointer, "MAIN", 0, None)
    Function.function_stack.append(function_main)
    function_main.perform_function_code()
    print(function_main.variable_stack)
    Function.function_stack.pop()
