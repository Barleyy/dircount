from pathlib import Path
import sys
import struct
from enum import Enum

path = sys.argv[1]
var_type = sys.argv[2]
var_name = sys.argv[3]
var_val = sys.argv[4]


class Types(Enum):
    function = 0
    int = 1
    float = 2
    char = 3
    string = 4
    boolean = 5
    list = 6
    dict = 7


def create_type_dir(var_type_arg, path_arg):
    for i in range(0, Types[var_type_arg].value):
        Path(path_arg + var_type_arg + str(i) + "/").mkdir(parents=True, exist_ok=True)


def create_int_dirs(var_val_arg, path_arg):
    if int(var_val_arg) < 0:
        Path(path_arg + "/bit0/negative/").mkdir(parents=True, exist_ok=True)
    else:
        Path(path_arg + "/bit0/").mkdir(parents=True, exist_ok=True)
    string_binary_val = '{0:015b}'.format(int(var_val_arg))
    create_int_based_dir(path_arg, string_binary_val)


def create_int_based_dir(path_arg, string_binary_val):
    for i in range(0, len(string_binary_val)):
        if string_binary_val[len(string_binary_val) - 1 - i] == "1":
            Path(path_arg + "/bit" + str(i + 1) + "/1/").mkdir(parents=True, exist_ok=True)
        else:
            Path(path_arg + "/bit" + str(i + 1) + "/").mkdir(parents=True, exist_ok=True)


def create_char_dirs(var_val_arg, path_arg):
    binary_char = format(ord(var_val_arg), '08b')
    create_int_based_dir(path_arg, binary_char)


def create_string_dir(var_val_arg, path_arg):
    for i in range(0, len(var_val_arg)):
        create_char_dirs(var_val_arg[i], path_arg + "/str1/char" + str(i) + "/")
    Path(path_arg + "str2").mkdir(parents=True, exist_ok=True)


def create_bool_dir(var_val_arg, path_arg):
    if var_val_arg.lower() == "false":
        Path(path_arg + "/0/").mkdir(parents=True, exist_ok=True)
    elif var_val_arg.lower() == "true":
        Path(path_arg + "/1/1/").mkdir(parents=True, exist_ok=True)


def create_float_dir(var_val_arg, path_arg):
    binary_float = float_to_bin(float(var_val_arg))[::-1]
    for i in range(0, len(binary_float)):
        if binary_float[i] == "1":
            Path(path_arg + "/bit" + str(i + 1) + "/1/").mkdir(parents=True, exist_ok=True)
        else:
            Path(path_arg + "/bit" + str(i + 1) + "/").mkdir(parents=True, exist_ok=True)


def float_to_bin(num):
    return format(struct.unpack('!I', struct.pack('!f', num))[0], '032b')


def create_var_dirs(path_arg, var_type_arg, var_name_arg, var_val_arg):
    create_type_dir(var_type_arg, path_arg + "/dir0/")
    if var_type_arg.lower() == "int":
        create_int_dirs(var_val_arg, path_arg + "/dir1/")
    elif var_type_arg.lower() == "float":
        create_float_dir(var_val_arg, path_arg + "/dir1/")
    elif var_type_arg.lower() == "char":
        create_char_dirs(var_val_arg, path_arg + "/dir1/")
    elif var_type_arg.lower() == "string":
        create_string_dir(var_val_arg, path_arg + "/dir1/")
    elif var_type_arg.lower() == "boolean":
        create_bool_dir(var_val_arg, path_arg + "/dir1/")
    create_string_dir(var_name_arg, path_arg + "/dir2/")


create_var_dirs(path, var_type, var_name, var_val)
