# -*- coding: utf-8 -*-

"""Shadow Renderer Facade"""

import re
from io import StringIO
from configparser import ConfigParser

from shadow.search import Explorer


class MyConfigParser(ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


class Shadow:
    files = None

    def __init__(self, config=None, configfile='shadowconf.json',
                 tmplext='.tpl'):
        self.config = config
        self.configfile = configfile
        self.discovery = Explorer(tmplext)

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

    def find_templates(self, *paths):
        if paths:
            for path in paths:
                if os.path.isdir(path):
                    if path.endswith(self.template_ext):
                        

    def run(self):
        if self.config is None:
            self.load_config()

        if self.files is None:
            self.find_templates()
