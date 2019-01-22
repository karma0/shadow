# -*- coding: utf-8 -*-

"""Console script for shadow."""
import os
import re
import sys
import click

from io import StringIO

from shadow import __version__


class MyConfigParser(ConfigParser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


def load_config(configfile: str):
    with open(configfile, 'r') as fh:

        if ".json" in configfile:
            import json
            return json.loads(fh.read())

        elif ".hcl" in configfile:
            import hcl
            return hcl.load(fh)

        elif ".env" in configfile:
            envre = re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')

            result = {}
            for line in fh.readlines():
                match = envre.match(line)
                if match is not None:
                    result[match.group(1)] = match.group(2)
            return result

        elif ".yml" in configfile:
            import yaml
            return yaml.load(fh.read())

        elif ".ini" in configfile:
            ini = MyConfigParser()
            ini.readfp(StringIO(fh.read()))
            return ini.as_dict()


@click.command()
@click.option('-v', '--version', is_flag=True, help='Display the version and '
              'exit')
@click.option('-e', '--environment', is_flag=True, help='Import the '
              'environment for template variable resolution.')
@click.option('-c', '--config', help='Configuration (ini, json, hcl, or env '
              'file)')
@click.option('-o', '--output', help="The path/file to render to.")
@click.option('-v', '--verbose', count=True, help='Increase verbosity; use '
              'multiple times to increase verbosity.')
@click.option('-q', '--quiet', is_flag=True, help="Suppress all but critical '
              'output')
def main(version, environment, config, output, verbose, quiet):
    """Console script for shadow."""
    if version:
        click.echo(__version__)
        return 0

    if environment:
        conf = os.environ.copy()
    elif os.path.isfile(config):
        conf = load_config(config)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
