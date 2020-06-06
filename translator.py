import logging
from function_adapter import Function

logger=logging.getLogger("main.translator")
def translate(pointer):
    function_main = Function(pointer, "MAIN", 0, None)
    Function.function_stack.append(function_main)
    function_main.perform_function_code()
    logger.debug(function_main.variable_stack)
    Function.function_stack.pop()
