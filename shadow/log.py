# -*- coding: utf-8 -*-

"""Logging module"""

import logging


logger = logging.getLogger('shadow')


def setup_logger(quiet, verbose):
    """Use quiet and verbosity count to configure the log level"""
    if quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=[
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
        ][min(verbose, 2)])
