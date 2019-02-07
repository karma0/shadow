# -*- coding: utf-8 -*-

"""Renderer Module - for rendering sources to their destinations."""

import os

from jinja2 import Template, Environment, BaseLoader, meta

from shadow.log import logger


def get_template(filename):
    """Read in a template"""
    with open(filename, 'r') as handle:
        return Template(handle.read())


def save_template(filename, template, **kwargs):
    """Write out a template"""
    with open(filename, 'w') as wfh:
        wfh.write(template.render(**kwargs))


class Renderer:
    """Renderer Base Class
    Takes in a list of template namedtuples (source, destination) and sets up
    file and filename rendering on them.
    """
    def __init__(self, templates, config=None):
        self.tmpls = templates
        self.config = [] if config is None else config
        logger.debug(f"Launching renderer on templates: {templates}")

    def render(self):
        """Primary render action for generating the output."""
        for tmpl in self.tmpls:

            logger.info(f"Running on template: {tmpl.source} to {tmpl.destination}")

            # Loop on rendered template destinations
            for destination, context in self.render_path(tmpl.destination):

                # Bypass bogus destinations
                if destination is None:
                    continue

                # Create directory tree to a template directory
                elif os.path.isdir(tmpl.source) and \
                        not os.path.isdir(destination):
                    logger.warning(f"Creating path: {tmpl.destination}")
                    os.makedirs(destination)

                # Working with a file template - create the path and render it
                else:
                    logger.warning(f"Rendering {tmpl.source} to {destination}")
                    directory = os.path.dirname(destination)
                    if directory and not os.path.isdir(directory):
                        os.makedirs(directory)
                    save_template(destination,
                                  get_template(tmpl.source),
                                  **self.config)

    def render_path(self, destination):
        """Render path names"""
        env = Environment(loader=BaseLoader())
        content = env.from_string(destination)
        parsed_content = env.parse(destination)

        logger.debug(f"Rendering destination filename: {destination}")

        undefvars = meta.find_undeclared_variables(parsed_content)
        if not undefvars:
            logger.debug(f"Destination filename good as is: {destination}")
            yield destination, None

        else:
            for variable in undefvars:
                for confname, value in list(self._get_vars(variable)):
                    if confname is not None:
                        yield content.render({variable: confname}), value

    def _get_vars(self, variable):
        """Yields variable names in a template."""
        config = self._get_conf_by_path(variable)
        if isinstance(config, list):
            for item in config:
                yield item, None
        elif isinstance(config, dict):
            for item, conf in config.keys():
                yield item, conf
        elif isinstance(config, str):
            yield config, None
        else:
            yield None, None

    def _get_conf_by_path(self, path):
        """Translates a template variable by name to its object in the
        shadowconf.
        """
        conf = None
        for item in path.split('.'):
            if conf is None:
                conf = self.config.get(item, None)
                if conf is None:
                    return None
            else:
                conf = conf.get(item, None)
        return conf
