import sys,os,re
from pathlib import Path,PurePath

if len(sys.argv) > 1:
    root_path = os.path.abspath(sys.argv[1])
else:
    sys.exit("no command line arguments")

def fix_link(path,link):
    y = re.search("/", root_path[::-1],1)
    root_dir = root_path[len(root_path)-y.start():]
    pattern = re.search(root_dir,str(link))
    link_without_root = str(link)[pattern.end():]
    new_path = root_path + link_without_root
    tmpLink = "tmplink"
    print("New Target: " + new_path)
    os.symlink(new_path, tmpLink)
    os.rename(tmpLink, path)

for root, dirs, files in os.walk(root_path, topdown=False):
    for name in files:
        path=os.path.join(root, name)
        if not os.path.exists(path):
            target = Path(path).resolve()
            fix_link(path,target)
    for name in dirs:
        path = os.path.join(root, name)
        if not os.path.exists(path):
            pass