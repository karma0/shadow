# -*- coding: utf-8 -*-

"""Template Discovery Module"""

import os
import logging


logger = logging.getLogger('shadow')


class Cabinet:
    def __init__(self, path, tmplext='.tpl'):
        self.source = path
        self.tmplext = tmplext

    def pull(self):
        return (self.source, self.dest)

    @property.setter
    def source(self, path):
        return self.source[:-(len(self.tmplext))]

    @property
    def dest(self):
        return self.source[:-(len(self.tmplext))]


class File(Cabinet):
    pass


class Folder(Cabinet):
    pass


class Drawer(Cabinet):
    records: list = []

    def create_file_list(self):
        for dirpath, dirnames, filenames in \
                os.walk(self.source, followlinks=False):

            for dirname in dirnames:
                self.records.append(
                    Folder(os.path.join(dirpath, dirname), self.tmplext))

            for fname in filenames:
                self.records.append(
                    File(os.path.join(dirpath, fname), self.tmplext))

    def pull(self):
        return (rec.pull() for rec in self.records)


class Explorer:
    records: list = []
    excludes: list = []

    def __init__(self, paths=None, tmplext=None):
        self.paths = '.' if paths is None else paths
        self.tmplext = '.tpl' if tmplext is None else tmplext

    def discover_paths(self):
        for path in self.paths:
            if os.path.isdir(path):
                if path.endswith(self.tmplext):
                    self.records.append(Drawer(path, self.tmplext))
                else:
                    self.walk(path)

            elif os.path.isfile(path):
                self.records.append(File(path, self.tmplext))
            else:
                logger.warning(f"Unknown path: {path}")

    def walk(self, source):
        for dirpath, dirnames, filenames in \
                os.walk(source, followlinks=False):

            for dirname in dirnames:
                if dirname.endswith(self.tmplext):
                    self.records.append(
                        Drawer(os.path.join(dirpath, dirname), self.tmplext))
                    self.excludes.append(dirname)

            dirnames[:] = [dr for dr in dirnames if dr not in self.excludes]

            for fname in filenames:
                if fname.endswith(self.tmplext):
                    self.records.append(
                        File(os.path.join(dirpath, fname), self.tmplext))
