import copy
import logging

import atexit
import time
import shutil
import os
import commands
import error_factory
from directory_functions import Directory
from function_adapter import Function
from value_parsing import parse_list_value, match_type
from var_types import parse_value, Types, declare, let
from variable_holder import VariableStack, VariableId, VariableHolder

logger = logging.getLogger("complex_operations")


def _if(directory):
    if not 3 >= directory.dirlen() >= 2:
        error_factory.ErrorFactory.invalid_command_dir_number([2, 3], directory.path, directory.dirlen(), "IF")
    if parse_value(directory.navigate_to_nth_child(0), Types.boolean, 1):
        logger.debug(_if.__name__ + ": true execution")
        root = Directory(directory.navigate_to_nth_child(1).path)
        for directory in root.get_directory_children():
            logger.debug(_if.__name__ + ": COMPLEX TRUE " + directory.path)
            commands.expression(directory)

    elif directory.dirlen() == 3:
        logger.debug(_if.__name__ + ": false execution")
        root = Directory(directory.navigate_to_nth_child(1).path)
        for directory in root.get_directory_children():
            logger.debug(_if.__name__ + ": COMPLEX FALSE " + directory.path)
            commands.expression(directory)


def _while(directory):
    if directory.dirlen() != 2:  # logical condition, list of commands
        error_factory.ErrorFactory.invalid_command_dir_number([2], directory.path, directory.dirlen(), "WHILE")

    condition_dir = directory.navigate_to_nth_child(0)
    counter = 1
    while parse_value(condition_dir, Types.boolean, 1):
        logger.debug(_while.__name__ + f" executing {counter} times")
        root = Directory(directory.navigate_to_nth_child(1).path)
        execute_all_loop_commands(root)
        counter += 1


def _for(directory):
    # list of commands
    # var_declare, boolean_expression,  list of commands
    # var_declare, boolean_expression, let_expression, list of commands
    if directory.dirlen() not in for_arguments_dict.keys():
        error_factory.ErrorFactory.invalid_command_dir_number([1, 3, 4], directory.path, directory.dirlen(), "FOR")
    for_arguments_dict[directory.dirlen()](directory)


def _infinite_for(directory):
    logger.debug(_infinite_for.__name__ + " Starting infinite for loop")
    while True:
        execute_all_loop_commands(directory.navigate_to_nth_child(0))


def _var_and_condition_for(directory):
    path, _, _ = declare(directory.navigate_to_nth_child(0))
    boolean_dir = directory.navigate_to_nth_child(1)
    commands_root = directory.navigate_to_nth_child(2)
    counter = 1
    while parse_value(boolean_dir, Types.boolean, 1):
        logger.debug(_var_and_condition_for.__name__ + f" FOR executing {counter} times")
        execute_all_loop_commands(commands_root)
        counter += 1
    remove_var_from_scope(path)


def _full_for(directory):
    path, _, _ = declare(directory.navigate_to_nth_child(0))
    boolean_dir = directory.navigate_to_nth_child(1)
    let_dir = directory.navigate_to_nth_child(2)
    commands_root = directory.navigate_to_nth_child(3)
    counter = 1
    while parse_value(boolean_dir, Types.boolean, 1):
        logger.debug(_full_for.__name__ + f" FOR executing {counter} times")
        execute_all_loop_commands(commands_root)
        let(let_dir)
        counter += 1
    remove_var_from_scope(path)


def execute_all_loop_commands(root):
    for commands_dir in root.get_directory_children():
        logger.debug(execute_all_loop_commands.__name__ + " COMPLEX WHEN command at " + commands_dir.path)
        commands.expression(commands_dir)


def remove_var_from_scope(path):
    import function_utils
    invoked_function = function_utils.get_currently_invoked_function()
    del invoked_function.variable_stack[path]


def _function(directory):
    logger.debug(_function.__name__ + f" EXECUTING FUNC AT PATH {directory.path}")
    if directory.dirlen() != 2:  # logical condition, list of commands
        error_factory.ErrorFactory.invalid_command_dir_number([2], directory.path, directory.dirlen(), "EXEC FUNC")

    else:
        logger.debug(directory.children_paths)
        var_link = directory.navigate_to_nth_child(0).get_link_path()
        logger.debug(var_link)
        import function_utils
        invoked_function = function_utils.get_currently_invoked_function()
        fun_instance_template = invoked_function.variable_stack.get_var_by_path(var_link).value
        fun_instance = copy.deepcopy(fun_instance_template)

        logger.debug(directory.navigate_to_nth_child(1).path)
        args_list = parse_list_value([directory.navigate_to_nth_child(1)])
        logger.info(_function.__name__ + " FUNCTION ARGS_LIST " + str(args_list))
        if len(args_list) != fun_instance.get_arguments_len():
            error_factory.ErrorFactory.invalid_arg_no_passed(len(args_list), fun_instance.get_arguments_len(),
                                                             fun_instance.name)
        else:
            var_stack = VariableStack()
            for item in list(zip(fun_instance.args_no, args_list)):
                var_stack.create_var(VariableId(item[0], str(item[0])), VariableHolder(match_type(item[1]), item[1]))
            fun_instance.variable_stack = var_stack
        Function.function_stack.append(fun_instance)
        logger.debug(_function.__name__ + " FUNC BEFORE EXEC STACK" + str(fun_instance.variable_stack))
        fun_instance.perform_function_code()
        fun_instance.clear_var_stack()
        logger.debug(_function.__name__ + " FUNC AFTER EXEC STACK " + str(fun_instance.variable_stack))
        Function.function_stack.pop()


for_arguments_dict = {
    1: _infinite_for,
    3: _var_and_condition_for,
    4: _full_for,
}

def input(directory):
    logger.debug(input.__name__ + f" ECECUTING INPUT")
    # 2 command expression dir holds var name, can be used as link
    # input dir is created at root path
    input_dir = directory.get_root_path() + "/input"
    delete_input_dir(input_dir)
    os.mkdir(input_dir)
    # delete input dir if program gets terminated
    atexit.register(delete_input_dir, input_dir=input_dir)
    wait_for_input(input_dir, directory)

def wait_for_input(input_dir, link_path):
    while(len(os.listdir(input_dir)) == 0):
        time.sleep(0.2)
    declare( Directory(input_dir).navigate_to_nth_child(0), link = link_path )
    shutil.rmtree(input_dir)

def delete_input_dir(input_dir):
    if(os.path.isdir(input_dir)):
        shutil.rmtree(input_dir)