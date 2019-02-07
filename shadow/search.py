# -*- coding: utf-8 -*-

"""Template Discovery Module"""

import os

from shadow.log import logger


class Cabinet:
    """A base class for encapsulating functionality within a File, Folder, or
    Drawer object.
    """
    _dest = None

    def __init__(self, path, tmplext='.tpl'):
        logger.debug(f"New Cabinet at {path}")
        self.source = path
        self.tmplext = tmplext

    def pull(self):
        """Return the source/destination"""
        return (self.source, self.dest)

    @property
    def dest(self):
        """Return the destination, computing and removing the template
        extension.
        """
        if self._dest is None:
            self._dest = self.source[:-len(self.tmplext)]
        return self._dest

    @dest.setter
    def dest(self, value):
        """Set the destination"""
        self._dest = value


class File(Cabinet):
    """A File class"""
    pass


class Folder(Cabinet):
    """A Folder class"""
    pass


class Drawer(Cabinet):
    """A collection of Files and Folders"""
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
        return f"<Drawer with {len(self.records)} records in it>"


class Explorer:
    """Cabinet and Drawer facade for discovering records on disk"""
    records: list = []
    excludes: list = []

    def __init__(self, paths=None, tmplext=None):
        logger.debug(f"New Explorer at paths: {paths}")

        if not paths or paths is None:
            logger.warning(f"No path specified. Using current working directory.")
            self.paths = ['.']
        else:
            self.paths = paths

        self.tmplext = '.tpl' if tmplext is None else tmplext

    def discover_paths(self):
        """Search the paths for templates, walking the tree as necessary"""
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
        """Yield (source, destination) tuples"""
        for record in self.records:
            if isinstance(record, Drawer):
                for rec in record.pull():
                    yield rec
            else:
                yield record.pull()

    def walk(self, source):
        """Walking the tree to search the paths for templates. If a directory
        ends with the template extension, add all files under it.
        """
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
