import sys

from commands import *

if len(sys.argv) > 1:
    dirs = sys.argv[1]
else:
    sys.exit("no command line arguments")

translator.translate(dirs)