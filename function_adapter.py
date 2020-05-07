import commands
import error_factory
from directory_functions import Directory


class Function:
    function_stack = []

    def __init__(self, pointer, name, args_no, return_val_id):
        self.variable_stack = {}
        self.root = Directory(pointer)
        self.name = name
        self.args_no = args_no
        self.return_val_id = return_val_id

    def perform_function_code(self):
        print("PERFORMING FUNCTION", self.name)
        for directory in self.root.get_directory_children():
            print(self.name, directory.path)
            commands.expression(directory)
        if self.return_val_id is not None:
            return self.find_var_by_name(self.return_val_id)[1]

    def find_var_by_name(self, var_name):
        for key in self.variable_stack.keys():
            if self.variable_stack.get(key)[0] == var_name:
                return self.variable_stack.get(key)
        else:
            error_factory.ErrorFactory.var_not_defined_error(var_name)

    def __str__(self):
        return ",".join([str(s) for s in [self.root.path, self.name, self.return_val_id]])
