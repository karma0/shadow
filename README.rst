======
Shadow
======


.. image:: https://img.shields.io/pypi/v/shadow-cli.svg
        :target: https://pypi.python.org/pypi/shadow-cli

.. image:: https://img.shields.io/travis/karma0/shadow.svg
        :target: https://travis-ci.org/karma0/shadow

.. image:: https://readthedocs.org/projects/shadow/badge/?version=latest
        :target: https://shadow.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/karma0/shadow/shield.svg
     :target: https://pyup.io/repos/github/karma0/shadow/
     :alt: Updates

A comprehensive command line utility to render templates and ease code generation.


* Free software: GNU General Public License v3
* Documentation: https://shadow.readthedocs.io.


.. image:: https://github.com/karma0/shadow/raw/master/shadow-devil.gif

Features
--------

* Incorporates a *convention over configuration* mentality.
* Use the default ``*.tpl`` extension to find and render templates, or specify
  your own.
* Use the template extension on a directory to render all files under it.
* Specify the path(s) or let it default to searching for templates in the
  current working directory.
* Use template variables in filenames to render scalar filename outputs.
* Use hash/dict or list/array types in filenames to render multiple files.
* Default configuration expects a file named ``shadowconf`` with any of the
  following extensions: ``.json``, ``.hcl``, ``.env``, ``.yml``, ``.ini``.
* If no configuration file is specified, it will load and use the shell
  environment to render variables.
* All defaults can be overriden.

Quick Install
-------------

Install from PyPi::

    pip install shadow-cli

Install from GitHub::

    git clone https://github.com/karma0/shadow
    cd shadow
    pip install -U .

Examples
--------

Display the help and exit::

    shadow --help

Discover templates to be generated::

    shadow sim

Find all templates in the current working directory
and generate them using the config file ``shadowconf.json`` as the
variables to build them::

    shadow fax

Find all generated templates and remove them::

    shadow clean

Generate templates in the ``tests`` directory on files ending in ``*.j2``, using
environment variables to fill and render the templates::

    shadow fax -e -t .j2 tests

Generate the single template file named ``test.txt`` using the HCL config file
``test.txt.hcl``::

    shadow fax -c test.txt.hcl test.txt.tpl



Credits
-------

Created and maintained by karma0_.

This package was created with Cookiecutter_ and the `karma0/cookiecutter-pypackage`_ project template.

.. _karma0: https://github.com/karma0
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`karma0/cookiecutter-pypackage`: https://github.com/karma0/cookiecutter-pypackage
