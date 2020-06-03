from function_adapter import Function


def get_currently_invoked_function():
    return Function.function_stack[len(Function.function_stack) - 1]


def get_global_var_by_path(var_pointer):
    return Function.function_stack[0].find_var_by_path(var_pointer)


def get_global_var_by_name(var_name):
    return Function.function_stack[0].find_var_by_name(var_name)
