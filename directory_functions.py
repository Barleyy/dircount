import os


class Directory:
    path_separator = '/'

    def __init__(self, path, parent_path=None):
        self.parent_path = parent_path
        self.path = path
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
        return self.navigate_to_nth_child(0).dirlen()
