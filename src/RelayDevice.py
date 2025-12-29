#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Denis Schoener"
__copyright__ = "Copyright (C) 2025 Denis Schoener (denis@schoener-one.de)"
__license__ = "MIT"

import logging
from ModbusDevice import ModbusDevice

_log = logging.getLogger(__name__)


class RelayDevice(ModbusDevice):
    """Represents a 16 channel relay device which is
    controlled by the Modbus RTU interface"""

    SHORT_NAME = "rel16"
    CHANNELS = 16

    def __init__(self, serial_device, baudrate, address):
        _log.debug("Creating 16ch relay device")
        super().__init__(serial_device, baudrate, address, RelayDevice.CHANNELS)

    def read_input_channel_values(self) -> list:
        raise ModbusDevice.FunctionNotSupported(
            "read_input_channel_values for this device"
        )  # the relay does not have input channels!
