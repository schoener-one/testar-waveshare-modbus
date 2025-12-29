__author__ = "Denis Schoener"
__copyright__ = "Copyright (C) 2025 Denis Schoener (denis@schoener-one.de)"
__license__ = "MIT"

import importlib.metadata


try:
    __version__ = importlib.metadata.version("testar-waveshare-modbus")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"
