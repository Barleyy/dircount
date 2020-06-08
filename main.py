import sys
from commands import *

logger = logging.getLogger("main")
logger.setLevel(logging.WARNING)

if len(sys.argv) == 2:
    dirs = sys.argv[1]
elif len(sys.argv) > 2:
    dirs = sys.argv[2]
    if sys.argv[1].lower() == "-d":
        logging.basicConfig(level=logging.NOTSET)
    elif sys.argv[1].lower() == "-df":
        dirs = sys.argv[3]
        logging.basicConfig(filename=sys.argv[2], filemode='w', level=logging.NOTSET)
    else:
        sys.exit("wrong args")
else:
    sys.exit("no command line arguments")

translator.translate(dirs)
