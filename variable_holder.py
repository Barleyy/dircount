import error_factory


class VariableId:
    def __init__(self, pointer, name):
        self.name = name
        self.pointer = pointer

    def __eq__(self, another):
        return hasattr(another, 'name') and hasattr(another, 'pointer') \
               and self.name == another.name and self.pointer == another.pointer

    def __hash__(self):
        return hash((self.pointer, self.name))


class VariableHolder:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __str__(self):
        return ','.join([str(s) for s in [self.value, self.type]])


class VariableStack:
    def __init__(self):
        self.var_stack = {}

    # TODO: generify variable retrieve onto one method kind of switch case, if varname starts with '/' we assume
    #  it is link otherwise retrieve by name and use only generified one among project privating 2 other ones
    def get_var_by_name(self, name):
        for var in self.var_stack.keys():
            if var.name == name:
                return self.var_stack.get(var)
        else:
            error_factory.ErrorFactory.var_not_defined_error(name)

    def get_var_by_path(self, var_pointer):
        for key in self.var_stack.keys():
            if key.pointer == var_pointer:
                return self.var_stack.get(key)
        else:
            error_factory.ErrorFactory.var_not_defined_error(var_pointer)

    def check_if_var_exists_by_name(self, var_name):
        for key in self.var_stack.keys():
            if key.pointer == var_name:
                return True
        else:
            return False

    def check_if_var_exists_by_path(self, var_path):
        for key in self.var_stack.keys():
            if key.pointer == var_path:
                return True
        else:
            return False

    def create_var(self, var_id, var_value):
        self.var_stack[var_id] = var_value
