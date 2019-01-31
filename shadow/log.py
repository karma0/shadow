# -*- coding: utf-8 -*-

"""Logging module"""

import logging


logger = logging.getLogger('shadow')


def setup_logger(quiet, verbose):
    """Use quiet and verbosity count to configure the log level"""
    if quiet:
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel([
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
        ][verbose])
