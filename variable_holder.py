import translator


class VariableId:
    def __init__(self, pointer, name):
        self.name = name
        self.pointer = pointer

    def __eq__(self, another):
        return hasattr(another, 'name') and hasattr(another, 'pointer') \
               and self.name == another.name and self.pointer == another.pointer

    def __hash__(self):
        return hash((self.pointer, self.name))

    def __str__(self):
        return str(self.name) + ", " + str(self.pointer)


class VariableHolder:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __str__(self):
        return ', '.join([str(s) for s in [self.value, self.type]])


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
            print("WARNING", f"NOT FOUND {name} in function local stack")
            return translator.get_global_var_by_name(name)

    def get_var_by_path(self, var_pointer):
        for key in self.var_stack.keys():
            if key.pointer == var_pointer:
                return self.var_stack.get(key)
        else:
            print("WARNING", f"NOT FOUND {var_pointer} in function local stack")
            return translator.get_global_var_by_path(var_pointer)

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

    def clear(self):
        self.var_stack.clear()

    def __str__(self):
        return ", ".join(" = ".join((str(k), str(v))) for k, v in self.var_stack.items())
