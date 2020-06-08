import logging

logger=logging.getLogger("error_factory")


class ErrorFactory:
    @staticmethod
    def declare_parsing_error(message):
        template_message = f"DECLARE PARSING ERROR: {message}"
        raise ParsingError(template_message) from None

    @staticmethod
    def let_parsing_error(message):
        template_message = f"LET PARSING ERROR: {message}"
        raise ParsingError(template_message) from None

    @staticmethod
    def dir_length_error(command_type, path_to_dir, dir_length):
        template_message = f"Directory {path_to_dir} of type Command.{command_type} must have 2 subdirectories, " \
                           f"given {dir_length}"
        raise ParsingError(template_message) from None

    @staticmethod
    def command_not_found(command_dir, command_type):
        template_message = f"Unknown command type at {command_dir} of length {command_type}"
        raise ParsingError(template_message) from None

    @staticmethod
    def bit_directory_error(directory_path, n_subdirs):
        template_message = "Directories inside bits declaration can only have either 0 or 1 subdirectories but {0} " \
                           "has {1}".format(directory_path, n_subdirs)
        raise ParsingError(template_message) from None

    @staticmethod
    def invalid_command_dir_number(count_list, dir_path, dir_len, command_name):
        dir_list_string = ",".join([str(elem) for elem in count_list])
        template_message = f"Expected {dir_list_string} dirs at {dir_path} for {command_name} command, given {dir_len}"
        raise ParsingError(template_message) from None

    @staticmethod
    def type_mismatch_error(type, __class__):
        template_message = "Type mismatch: expected {0} got {1}".format(type, __class__)
        raise ParsingError(template_message) from None

    @staticmethod
    def unparsable_expression(path):
        template_message = f"Could not parse value at {path}"
        raise ParsingError(template_message) from None

    @staticmethod
    def unparsable_value(path, basic_type_length, path1, type_class):
        template_message = "Either first subdirectory of directory {0} of type value type {1} must have {2} " \
                           "subdirectories or operation returning type {3} value at level {4} expected" \
            .format(path, type_class, basic_type_length, type_class, path1)
        raise ParsingError(template_message) from None

    @staticmethod
    def directory_parsing_error(path, dirlen):
        template_message = f"Invalid number of dirs {path} Each entry in dictionary must have 2 dirs, {dirlen} given"
        raise ParsingError(template_message) from None

    @staticmethod
    def var_not_defined_error(path):
        template_message = f"Variable {path} not defined"
        raise ParsingError(template_message) from None

    @staticmethod
    def var_already_defined_error(name):
        template_message = f"Variable {name} already defined"
        raise ParsingError(template_message) from None

    @staticmethod
    def invalid_function_args_no(args_no):
        template_message = f"Function must have at least 0 args, given {args_no}"
        raise ParsingError(template_message) from None

    @staticmethod
    def restricted_variable_name_prefix(path, name):
        template_message = f"Variable at path {path} cannot has '/' at first place, given {name}"
        raise ParsingError(template_message) from None

    @staticmethod
    def invalid_argument_name():
        template_message = f"Function argument token must be str class"
        raise ParsingError(template_message) from None

    @staticmethod
    def invalid_arg_no_passed(given, expected, name):
        template_message = f"Function {name} expects {expected} number of args, given {given}"
        raise ParsingError(template_message) from None

    @staticmethod
    def duplicate_arg_name(name):
        template_message = f"Function args names must be distinct, {name} invalidates"
        raise ParsingError(template_message) from None


class ParsingError(ValueError):
    def __init__(self, message):
        logger.error(message)
        super(ParsingError, self).__init__(message)
