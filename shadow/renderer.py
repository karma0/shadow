# -*- coding: utf-8 -*-

import os
import logging

from jinja2 import Template


logger = logging.getLogger('shadow')


class Renderer:
    def __init__(self, *templates, config=None):
        self.tmpls = templates

    def render(self, *args, **kwargs):
        for tmpl in self.tmpls:
            if os.path.isdir(tmpl.source):
                logger.debug(f"Creating path: {tmpl.destination}")
                os.makedirs(tmpl.destination)
            else:
                logger.debug(f"Rendering {tmpl.source} to {tmpl.destination}")
                os.makedirs(os.dirname(tmpl.destination))
                self.save_template(tmpl.destination,
                                   self.get_template(tmpl.source),
                                   **self.config)

    def get_template(self, filename):
        with open(filename, 'r') as fh:
            return Template(fh.read())

    def save_template(self, filename, template, **kwargs):
        with open(filename, 'w') as wfh:
            wfh.write(template.render(**kwargs))

