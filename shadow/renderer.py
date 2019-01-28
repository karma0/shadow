# -*- coding: utf-8 -*-

import os
import logging

from jinja2 import Template, Environment, BaseLoader, meta


logger = logging.getLogger('shadow')


class Renderer:
    def __init__(self, templates, config=None):
        self.tmpls = templates
        self.config = [] if config is None else config

    def render(self):
        for tmpl in self.tmpls:
            for destination in self.render_path(tmpl.destination):
                if destination is None:
                    continue
                elif os.path.isdir(tmpl.source) and not os.path.isdir(destination):
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

    def render_path(self, destination):
        env = Environment(loader=BaseLoader())
        content = env.from_string(destination)
        parsed_content = env.parse(destination)

        undefvars = meta.find_undeclared_variables(parsed_content)
        if not undefvars:
            return [destination]

        for variable in undefvars:
            values = self._get_vars(variable)
            for value in values:
                if value is not None:
                    yield content.render({variable: value})

    def _get_vars(self, variable):
        config = self._get_conf_by_path(variable)
        if isinstance(config, list):
            for item in config:
                yield config
        elif isinstance(config, dict):
            for item in config.keys():
                yield item
        elif isinstance(config, str):
            yield config
        else:
            yield None

    def _get_conf_by_path(self, path):
        conf = None
        for item in path.split('.'):
            if conf is None:
                conf = self.config.get(item, None)
                if conf is None:
                    return None
            else:
                conf = conf.get(item, None)
        return conf

    def get_template(self, filename):
        with open(filename, 'r') as fh:
            return Template(fh.read())

    def save_template(self, filename, template, **kwargs):
        with open(filename, 'w') as wfh:
            wfh.write(template.render(**kwargs))

