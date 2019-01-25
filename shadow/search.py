# -*- coding: utf-8 -*-

"""Template Discovery Module"""

import os
import logging


logger = logging.getLogger('shadow')


class Cabinet:
    _dest = None

    def __init__(self, path, tmplext='.tpl'):
        logger.debug(f"New Cabinet at {path}")
        self.source = path
        self.tmplext = tmplext

    def pull(self):
        return (self.source, self.dest)

    @property
    def dest(self):
        if self._dest is None:
            self._dest = self.source[:-len(self.tmplext)]
        return self._dest

    @dest.setter
    def dest(self, value):
        self._dest = value


class File(Cabinet):
    pass


class Folder(Cabinet):
    pass


class Drawer(Cabinet):
    records: list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug(f"Creating Drawer for source: {self.source}")
        for dirpath, dirnames, filenames in \
                os.walk(self.source, followlinks=False):
            destpath = f"{self.dest}{dirpath[len(self.source):]}"

            for dirname in dirnames:
                self.records.append(
                    Folder(os.path.join(dirpath, dirname), self.tmplext))
                self.records[-1].dest = os.path.join(destpath, dirname)

            for fname in filenames:
                self.records.append(
                    File(os.path.join(dirpath, fname), self.tmplext))
                self.records[-1].dest = os.path.join(destpath, fname)

    def pull(self):
        return (rec.pull() for rec in self.records)

    def __repr__(self):
        return f"<Drawer with {len(self.records)} in it>"


class Explorer:
    records: list = []
    excludes: list = []

    def __init__(self, paths=None, tmplext=None):
        logger.debug(f"New Explorer at paths: {paths}")

        if not paths or paths is None:
            logger.warning(f"Using current working directory")
            self.paths = ['.']
        else:
            self.paths = paths

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

    def pull_records(self):
        for record in self.records:
            if isinstance(record, Drawer):
                for rec in record.pull():
                    yield rec
            else:
                yield record.pull()

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
