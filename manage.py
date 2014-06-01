#!/usr/bin/env python
import logging
import os
import sys

from qed import settings


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qed.settings")
    logging.basicConfig(level=settings.LOGGING_LEVEL)
    from pyon.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

