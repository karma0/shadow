# -*- coding: utf-8 -*-

import os
import logging

from jinja2 import Template, Environment, BaseLoader


logger = logging.getLogger('shadow')


class Renderer:
    def __init__(self, templates, config=None):
        self.tmpls = templates
        self.config = [] if config is None else config

    def render(self):
        for tmpl in self.tmpls:
            for destination in self.render_path(tmpl):
                if os.path.isdir(tmpl.source) and not os.path.isdir(destination):
                    logger.warning(f"Creating path: {tmpl.destination}")
                    os.makedirs(destination)
                else:
                    logger.warning(f"Rendering {tmpl.source} to {destination}")
                    directory = os.path.dirname(destination)
                    if directory and not os.path.isdir(directory):
                        os.makedirs(directory)
                    self.save_template(destination,
                                       self.get_template(tmpl.source),
                                       **self.config)

    def render_path(self, tmpl):
        rtemplate = Environment(loader=BaseLoader()).from_string(tmpl.destination)

    def get_template(self, filename):
        with open(filename, 'r') as fh:
            return Template(fh.read())

    def save_template(self, filename, template, **kwargs):
        with open(filename, 'w') as wfh:
            wfh.write(template.render(**kwargs))

