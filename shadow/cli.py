# -*- coding: utf-8 -*-

"""Console script for shadow."""
import os
import sys
import click
import logging

from shadow import __version__
from shadow.shadow import Shadow


def setup_logger(quiet, verbose):
    logger = logging.getLogger('shadow')
    if quiet:
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel([
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
        ][verbose])


@click.group()
@click.option('-V', '--version', is_flag=True, help='Display the version and '
              'exit')
def main(version):
    """Console script for shadow.
    Name your template files with the ``.tpl`` extension or put them in a
    directory with this extension, or you may specify ``-t`` to use a different
    extension. All variables will be drawn from the specified configuration
    file (default: shadowconf.json).


    Examples:

        ``shadow sim`` - Displays all of the template files and directories
        found with the ``.tpl`` extension.

        ``shadow fax`` - Find all templates in the current working directory
        and generate them using the config file ``shadowconf.json`` as the
        variables to build them.

        ``shadow reset`` - Find all generated templates and remove them.

        ``shadow fax -e -t .j2 tests`` - Generate templates in the ``tests``
        directory on files ending in *.j2, using environment variables to
        fill and render the templates.

        ``shadow fax -c test.txt.hcl test.txt.tpl`` - Generate the single template file
        named ``test.txt`` using the HCL config file ``test.txt.hcl``.
    """
    if version:
        click.echo(__version__)
        return 0

    return 0


@main.command(context_settings={"ignore_unknown_options": True})
@click.option('-t', '--tmplextension', help='The extension that templates '
              'can be identified with')
@click.option('-v', '--verbose', count=True, help='Increase verbosity; use '
              'multiple times to increase verbosity')
@click.option('-q', '--quiet', is_flag=True, help='Suppress all but critical '
              'output')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def sim(environment, configfile, verbose, quiet, files):
    """Show the files that would get rendered."""
    shadow = Shadow()
    for tmpl in shadow.find_templates(*files):
        click.echo(tmpl)
    return 0


@main.command()
@click.option('-e', '--environment', is_flag=True, help='Import the '
              'environment for template variable resolution')
@click.option('-c', '--configfile', help='Configuration (ini, json, hcl, or '
              'env file)')
@click.option('-t', '--tmplextension', help='The extension that templates '
              'can be identified with')
@click.option('-v', '--verbose', count=True, help='Increase verbosity; use '
              'multiple times to increase verbosity')
@click.option('-q', '--quiet', is_flag=True, help='Suppress all but critical '
              'output')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def fax(environment, configfile, verbose, quiet, files):
    """Render the current tree."""
    config = None
    if environment:
        config = os.environ.copy()

    shadow = Shadow(config=config, configfile=configfile)
    shadow.find_templates(*files)
    shadow.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
