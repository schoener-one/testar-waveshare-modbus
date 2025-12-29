#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Denis Schoener"
__copyright__ = "Copyright (C) 2025 Denis Schoener (denis@schoener-one.de)"
__license__ = "MIT"
__doc__ = "Contains commonly utilized functions"

import logging
from pathlib import Path

LOG_LEVELS = {
    "fatal": logging.FATAL,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}


class Utils:
    """Class which contains different utils for testing"""

    @staticmethod
    def setup_logging(level=logging.INFO, logger_list: list = None) -> None:
        """Sets up the logging configuration"""
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s]: %(name)s - %(message)s",
            level=level,
        )
        if logger_list is not None:
            for logger_name in logger_list:
                logging.getLogger(logger_name).setLevel(level)

    @staticmethod
    def to_bool(value: str) -> bool:
        """Converts a string to boolean"""
        return False if value.lower() in ("false", "0", "no", "off") else True

    @staticmethod
    def resolve_file(target_name: str, base_path: Path = None) -> Path:
        """Resolves a file path."""
        path = Path(target_name) if base_path is None else base_path / target_name
        if path.is_file():
            return path.resolve()

        raise FileNotFoundError(f"File '{target_name}' not found")
