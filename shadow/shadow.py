# -*- coding: utf-8 -*-

"""Shadow Renderer Facade"""

import re
import os
import json

from collections import namedtuple
from io import StringIO
from configparser import ConfigParser

from shadow.log import logger
from shadow.search import Explorer
from shadow.renderer import Renderer


Template = namedtuple('Template', 'source destination')
"""Template object for housing source/destination pairs of template files."""


class MyConfigParser(ConfigParser):
    """ConfigParser for parsing ``*.ini`` files"""
    def as_dict(self):
        """Generate and return the configuration as a dictionary object"""
        sections = dict(self._sections)
        for key in sections:
            sections[key] = dict(self._defaults, **sections[key])
            sections[key].pop('__name__', None)
        return sections


class Shadow:
    """Application class for orchestrating the various pieces and providing a
    functional facade.
    """
    files = None
    config: dict = {}

    # possible config files
    configfiles = [
        'shadowconf.json',
        'shadowconf.hcl',
        'shadowconf.env',
        'shadowconf.ini'
    ]
    configfile = None

    def __init__(self, paths=None, config=None, configfile=None,
                 tmplext='.tpl'):
        self.paths = [] if paths is None else paths

        if isinstance(config, str):
            config = json.loads(config)

        self.config = config

        if config is None:
            self.find_config(configfile)

        self.discovery = Explorer(paths=self.paths, tmplext=tmplext)

    def find_config(self, configfile):
        # Search for valid configuration files
        if configfile is None:
            for file in reversed(self.configfiles):
                if os.path.exists(file):
                    logger.info(f"Using config file: {file}")
                    self.configfile = file

            if self.configfile is None:  # Still not found to be present
                logger.info("No config file present; using environment")
                self.load_env()

        else:
            logger.warning(f"Using config file: {file}")
            self.configfile = configfile

    def load_env(self):
        self.config = os.environ.copy()

    def load_config(self):
        """Open and load the config file using it's file format as determined by
        filename extension.
        """
        with open(self.configfile, 'r') as handle:

            if ".json" in self.configfile:
                self.config = json.loads(handle.read())

            elif ".hcl" in self.configfile:
                import hcl
                self.config = hcl.load(handle)

            elif ".env" in self.configfile:
                envre = \
                    re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')

                for line in handle.readlines():
                    match = envre.match(line)
                    if match is not None:
                        self.config[match.group(1)] = match.group(2)

            elif ".yml" in self.configfile:
                import yaml
                self.config = yaml.load(handle.read())

            elif ".ini" in self.configfile:
                ini = MyConfigParser()
                ini.readfp(StringIO(handle.read()))
                self.config = ini.as_dict()

            else:
                raise FileNotFoundError

            logger.info(f"Using config: {self.config}")

    def search(self):
        """Execute the application as configured, without generating output"""
        if not self.config or self.config is None:
            try:
                self.load_config()
            except FileNotFoundError:
                logger.warning(
                    "No config file present; using shell environment.")
                self.load_env()

        if self.files is None:
            self.discovery.discover_paths()
            self.files = [Template(*pair) for pair in
                          self.discovery.pull_records()]

        return self.files

    def render(self):
        """Render the discovered templates"""
        renderer = Renderer(self.files, self.config)
        return renderer.render()

    def run(self):
        """Wrap full functionality"""
        self.search()
        self.render()
