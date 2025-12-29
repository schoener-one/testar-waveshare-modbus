#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Denis Schoener"
__copyright__ = "Copyright (C) 2025 Denis Schoener (denis@schoener-one.de)"
__license__ = "MIT"

from ModbusDevice import ModbusDevice
import logging

_log = logging.getLogger(__name__)


class DigitalIoDevice(ModbusDevice):
    """Represents a 8 channel digital io device which is
    controlled by the Modbus RTU interface"""

    SHORT_NAME = "dio"
    CHANNELS = 8

    def __init__(self, serial_device, baudrate, address):
        _log.debug("Creating 8ch digital io device")
        super().__init__(serial_device, baudrate, address, DigitalIoDevice.CHANNELS)
