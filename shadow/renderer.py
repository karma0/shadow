# -*- coding: utf-8 -*-

import os
import logging

from jinja2 import Template


logger = logging.getLogger('shadow')


class Renderer:
    def __init__(self, templates, config=None):
        self.tmpls = templates
        self.config = [] if config is None else config

    def render(self):
        for tmpl in self.tmpls:
            if os.path.isdir(tmpl.source) and not os.path.isdir(tmpl.destination):
                logger.warning(f"Creating path: {tmpl.destination}")
                os.makedirs(tmpl.destination)
            else:
                logger.warning(f"Rendering {tmpl.source} to {tmpl.destination}")
                directory = os.path.dirname(tmpl.destination)
                if directory and not os.path.isdir(directory):
                    os.makedirs(directory)
                self.save_template(tmpl.destination,
                                   self.get_template(tmpl.source),
                                   **self.config)

    def get_template(self, filename):
        with open(filename, 'r') as fh:
            return Template(fh.read())

    def save_template(self, filename, template, **kwargs):
        with open(filename, 'w') as wfh:
            wfh.write(template.render(**kwargs))

