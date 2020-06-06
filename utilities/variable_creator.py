from pathlib import Path
import sys
import struct
from enum import Enum

path=sys.argv[1]
var_type=sys.argv[2]
var_name=sys.argv[3]
var_val=sys.argv[4]

class Types(Enum):
    function = 0
    int = 1
    float = 2
    char = 3
    string = 4
    boolean = 5
    list = 6
    dict = 7

def createTypeDir(var_type,path):
    for i in range(0, Types[var_type].value):
        Path(path+var_type+str(i)+"/").mkdir(parents=True, exist_ok=True)


def createIntDirs(var_val,path):
    if int(var_val)<0:
        Path(path + "/bit0/negative/").mkdir(parents=True, exist_ok=True)
    else:
        Path(path + "/bit0/").mkdir(parents=True, exist_ok=True)
    stringBinaryVal='{0:015b}'.format(int(var_val))
    for i in range(0,len(stringBinaryVal)):
        if stringBinaryVal[len(stringBinaryVal)-1-i]=="1":
            Path(path + "/bit"+str(i+1)+"/1/").mkdir(parents=True, exist_ok=True)
        else:
            Path(path + "/bit" +str(i + 1) + "/").mkdir(parents=True, exist_ok=True)


def createCharDirs(var_val,path):
    binaryChar=format(ord(var_val), '08b')
    for i in range(0,len(binaryChar)):
        if binaryChar[len(binaryChar)-1-i]=="1":
            Path(path + "/bit"+str(i+1)+"/1/").mkdir(parents=True, exist_ok=True)
        else:
            Path(path + "/bit" + str(i + 1) + "/").mkdir(parents=True, exist_ok=True)

def createStringDir(var_val,path):
    for i in range(0,len(var_val)):
        createCharDirs(var_val[i],path+"/str1/char"+str(i)+"/")
    Path(path+"str2").mkdir(parents=True, exist_ok=True)


def createBoolDir(var_val, path):
    if(var_val.lower()=="false"):
        Path(path + "/0/").mkdir(parents=True, exist_ok=True)
    elif(var_val.lower()=="true"):
        Path(path+ "/1/1/").mkdir(parents=True, exist_ok=True)

def float_to_bin(num):
    return format(struct.unpack('!I', struct.pack('!f', num))[0], '032b')

def createFloatDir(var_val, path):
    binaryFloat=float_to_bin(float(var_val))[::-1]
    for i in range(0,len(binaryFloat)):
        if binaryFloat[i]=="1":
            Path(path + "/bit"+str(i+1)+"/1/").mkdir(parents=True, exist_ok=True)
        else:
            Path(path + "/bit" + str(i + 1) + "/").mkdir(parents=True, exist_ok=True)


def createVarDirs(path,var_type,var_name,var_val):
    createTypeDir(var_type,path+"/dir0/")
    if var_type.lower()=="int":
        createIntDirs(var_val,path+"/dir1/")
    elif var_type.lower()=="float":
        createFloatDir(var_val,path+"/dir1/")
    elif var_type.lower()=="char":
        createCharDirs(var_val,path+"/dir1/")
    elif var_type.lower()=="string":
        createStringDir(var_val,path+"/dir1/")
    elif var_type.lower()=="boolean":
        createBoolDir(var_val,path+"/dir1/")
    createStringDir(var_name,path+"/dir2/")


createVarDirs(path,var_type,var_name,var_val)

