# -*- coding: utf-8 -*-

"""Shadow Renderer Facade"""

import re
import os
import logging

from collections import namedtuple
from io import StringIO
from configparser import ConfigParser

from shadow.search import Explorer
from shadow.renderer import Renderer


logger = logging.getLogger('shadow')


Template = namedtuple('Template', 'source destination')


class MyConfigParser(ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


class Shadow:
    files = None
    configfile = 'shadowconf.json'

    def __init__(self, paths=None, config=None, configfile=None,
                 tmplext='.tpl'):
        self.paths = [] if paths is None else paths
        self.config = config
        if configfile is not None:
            self.configfile = configfile
        self.discovery = Explorer(paths=self.paths, tmplext=tmplext)

    def load_config(self):
        with open(self.configfile, 'r') as fh:

            if ".json" in self.configfile:
                import json
                self.config = json.loads(fh.read())

            elif ".hcl" in self.configfile:
                import hcl
                self.config = hcl.load(fh)

            elif ".env" in self.configfile:
                envre = re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')

                self.config = {}
                for line in fh.readlines():
                    match = envre.match(line)
                    if match is not None:
                        self.config[match.group(1)] = match.group(2)

            elif ".yml" in self.configfile:
                import yaml
                self.config = yaml.load(fh.read())

            elif ".ini" in self.configfile:
                ini = MyConfigParser()
                ini.readfp(StringIO(fh.read()))
                self.config = ini.as_dict()

    def run(self):
        if self.config is None:
            try:
                self.load_config()
            except FileNotFoundError:
                logger.warning(f"No config file present; using shell "
                    "environment.")
                self.config = os.environ.copy()

        if self.files is None:
            self.discovery.discover_paths()
            self.files = [Template(*pair) for pair in
                            self.discovery.pull_records()]

        return self.files

    def render(self):
        renderer = Renderer(self.files, self.config)
        return renderer.render()
