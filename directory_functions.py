import os, pwd
import re
import settings 


class Directory:
    path_separator = '/'
    user = pwd.getpwuid(os.getuid()).pw_name
    def __init__(self, path, parent_path=None):
        self.parent_path = parent_path
        self.path = os.path.abspath(path)
        children = os.listdir(path)
        children = list(filter(lambda x: os.path.isdir(self.get_child_path(x)), children))
        children.sort(key=lambda x: (len(x), x))
        self.children_paths = [self.get_child_path(child) for child in children]

    def get_path(self):
        return self.path

    def get_nth_child_path(self, n):
        return self.children_paths[n]

    def get_child_path(self, child_name):
        return self.path + self.path_separator + child_name

    def navigate_to_nth_child(self, n):
        return Directory(self.get_nth_child_path(n), parent_path=self)

    def get_children_paths(self):
        return self.children_paths

    def get_directory_children(self):
        return [Directory(child, parent_path=self.path) for child in self.children_paths]

    def dirlen(self):
        return len(self.children_paths)

    def get_dir_type(self):
        print("DIR FUNC ",self.navigate_to_nth_child(0).path)
        return self.navigate_to_nth_child(0).dirlen()

    def get_link_path(self):
        link = self.change_user_link(os.readlink(self.path))
        return link[:-1] if link[-1] == "/" else link

    def is_link(self):
        return os.path.islink(self.path)

    @staticmethod
    def directory_to_bit(directory_path):
        n_subdirs = Directory(directory_path).dirlen()
        if n_subdirs > 1:
            raise ValueError(
                "Directories inside bits declaration can only have either 0 or 1 subdirectories but {0} has {1}".format(
                    directory_path, n_subdirs))
        else:
            return n_subdirs
