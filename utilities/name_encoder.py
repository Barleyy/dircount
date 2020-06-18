from directory_functions import *
import os
import sys

logger = logging.getLogger("name_encoder")
logging.basicConfig(level=logging.DEBUG)


class Encoder:
    def __init__(self):
        self.encodings = {}
        self.symlinks_to_change = []

    def encode(self, root_dir, out_dir):
        root = Directory(root_dir)
        if not os.path.exists(os.path.abspath(out_dir)):
            os.mkdir(os.path.abspath(out_dir))
        self.encode_dir(root, os.path.abspath(out_dir), 0)
        for symlink in self.symlinks_to_change:
            self.setup_symlink(symlink[0], symlink[1], symlink[2])
        self.__init__()

    def encode_dir(self, directory, current_path, order):
        if os.path.islink(directory.path):
            return
        new_path = f"{current_path}{Directory.path_separator}UntitledFolder{order}"
        os.mkdir(new_path)
        for num, file in enumerate(self.links_only(directory.path)):
            self.setup_symlink(f"{directory.path}{Directory.path_separator}{file}", new_path, num)
        self.encodings[f"{directory.path}"] = new_path
        logger.debug(f"Encoded {directory.path}  to  {new_path}")
        for num, child in enumerate(directory.get_directory_children()):
            self.encode_dir(child, new_path, num)

    def setup_symlink(self, file_path, new_parent_path, order):
        src = os.readlink(file_path)
        link = src[:-1] if src.endswith("/") else src
        new_destination = f"{new_parent_path}{Directory.path_separator}Untitled{order}"
        if link.startswith("."):
            logger.debug(f"creating symlink {new_destination}  --->  {link}")
            os.symlink(link, new_destination)
        elif link in self.encodings:
            logger.debug(f"creating symlink {new_destination}  --->  {self.encodings[link]}")
            os.symlink(self.encodings[link], new_destination)
        else:
            self.symlinks_to_change.append((file_path, new_parent_path, order))

    def links_only(self, path):
        for file in os.listdir(path):
            if os.path.islink(os.path.join(path, file)):
                yield file


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    encoder = Encoder()
    encoder.encode(input_dir, output_dir)