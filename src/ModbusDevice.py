#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Denis Schoener"
__copyright__ = "Copyright (C) 2025 Denis Schoener (denis@schoener-one.de)"
__license__ = "MIT"

from pymodbus import ModbusException
from pymodbus.client import ModbusSerialClient
from Utils import *
import logging

_log = logging.getLogger(__name__)


class ModbusDevice:
    """Represents a general modbus device which can be
    controlled by the Modbus RTU interface"""

    REGISTER_BAUDRATE = 0x2000
    REGISTER_ADDRESS = 0x4000
    REGISTER_SW_VERSION = 0x8000

    BAUDRATE_CODES = {
        4800: 0x00,
        9600: 0x01,
        19200: 0x02,
        38400: 0x03,
        57600: 0x04,
        115200: 0x05,
        128000: 0x06,
        256000: 0x07,
    }

    MAX_REQUEST_TIMEOUT = 2  # seconds

    class InvalidConfigurationException(Exception):
        """Thrown if a invalid device configuration was passed"""

        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    class FunctionNotSupported(Exception):
        """Thrown if a function is not supported by a derived class"""

        def __init__(self, func_name) -> None:
            super().__init__(f"function {func_name} not supported")

    def __init__(self, serial_device, baudrate, address, channels):
        """Initializes the communication to a Modbus device.

        Args:
            serial_device (str): Serial communication interface device (i.e. /dev/ttyUSB0).
            baudrate (int):  Baudrate to be used for communication.
            address (int): Device bus address 0x01 - 0x0ff. Device address 0x00 is a broadcast address.
            channels (int): Number of channels the device provides.
        """
        self.address = address
        self.baudrate = baudrate
        self.serial_device = serial_device
        self.channels = channels
        self.modbus_client = None
        self._reconnect()

    def _reconnect(self) -> None:
        self.close_connection()
        self.modbus_client = ModbusSerialClient(
            self.serial_device,
            baudrate=self.baudrate,
            timeout=ModbusDevice.MAX_REQUEST_TIMEOUT,
        )
        self.modbus_client.connect()

    def close_connection(self) -> None:
        """Close an existing Modbus connection"""
        if self.modbus_client:
            self.modbus_client.close()

    @staticmethod
    def _convert_bits_to_int32(bits, endian="big") -> int:
        """The bits are converted into an 32bit integer with appropriate endianess"""
        assert len(bits) == 32
        i = int("".join([str(int(x)) for x in bits]), 2)
        return int.from_bytes(i.to_bytes(4, "little"), endian)

    def get_channels(self) -> int:
        """Get the number of channels"""
        return self.channels

    def _convert_register_bits_to_value_list(self, bits) -> list:
        """Converts the received value register bits to a list of values in the correct order
        regarding to endianness and byte bit order"""
        if len(bits) == 32:
            # The value register is stored as 32bit with big endianness so we need the
            # the channel values in the expected order from 0 - 31.
            value_register = ModbusDevice._convert_bits_to_int32(bits, endian="big")
        else:
            value_register = int("".join([str(int(x)) for x in bits]), 2)
        # The bits are received with MSB first!
        return [value_register >> i & 1 for i in reversed(range(0, self.channels))]

    def read_output_channel_values(self) -> list:
        """Read all output channel values at once.

        Returns:
            list: List of channel values starting from 0.
        """
        _log.debug("Read output channel values of device %d", self.address)
        response = self.modbus_client.read_coils(
            slave=self.address, address=0, count=self.channels
        )
        if isinstance(response, ModbusException):
            raise response
        return self._convert_register_bits_to_value_list(response.bits)

    def read_single_output_channel_value(self, channel) -> bool:
        """Read a single output channel value."""
        return self.read_output_channel_values()[channel]

    def read_input_channel_values(self) -> list:
        """Read all single input channel values at once.

        Returns:
            list: List of channel values starting from 0.
        """
        _log.debug("Read input channel values of device %d", self.address)
        response = self.modbus_client.read_discrete_inputs(
            slave=self.address, address=0, count=self.channels
        )
        if isinstance(response, ModbusException):
            raise response
        return self._convert_register_bits_to_value_list(response.bits)

    def read_single_input_channel_value(self, channel) -> bool:
        """Read a single input channel value."""
        return self.read_input_channel_values()[channel]

    def write_all_output_channel_values(self, value):
        """Write all channels to one value at once"""
        self.write_output_channel_values([value for i in range(self.channels)])

    def write_output_channel_values(self, value_list):
        """Write multiple channel values at once.

        Args:
            value_list (list): List of channel values (boolean).
                The list must have the same length like the number of channels!
        """
        _log.debug(
            "Write multiple output channel values at once to device %d: %s",
            self.address,
            str(value_list),
        )
        response = self.modbus_client.write_coils(
            slave=self.address, address=0, values=value_list
        )
        if isinstance(response, ModbusException):
            raise response

    def write_single_output_channel_value(self, channel, value: bool):
        """Write a single channel value"""
        if isinstance(value, str):
            value = Utils.to_bool(value)
        _log.debug(
            "Write output channel %d value of device %d: %s",
            channel,
            self.address,
            value,
        )
        response = self.modbus_client.write_coil(
            slave=self.address, address=channel, value=value
        )
        # FIXME Sometimes the modbus devices does not respond!
        if isinstance(response, ModbusException):
            raise response

    def write_output_channel_values_by_indices(self, channels, value: bool):
        """Write multiple channel values according to the index list.
        The index is expected to start by 1!
        """
        if isinstance(value, str):
            value = Utils.to_bool(value)
        for channel in channels:
            if channel < 1 or channel > self.channels:
                raise ModbusDevice.InvalidConfigurationException(
                    f"invalid channel index: {channel}"
                )
            self.write_single_output_channel_value(channel - 1, value)

    @staticmethod
    def _get_baudrate_code(baudrate: int) -> int:
        if baudrate not in ModbusDevice.BAUDRATE_CODES.keys():
            raise ModbusDevice.InvalidConfigurationException(
                f"baudrate {baudrate} is not supported"
            )
        return ModbusDevice.BAUDRATE_CODES[baudrate]

    def set_baudrate(self, baudrate) -> None:
        """Set a new device baudrate"""
        response = self.modbus_client.write_register(
            slave=self.address,
            address=ModbusDevice.REGISTER_BAUDRATE,
            value=ModbusDevice._get_baudrate_code(baudrate),
        )
        if isinstance(response, ModbusException):
            raise response
        # Success: we have to change our own baudrate as well!
        self._reconnect()

    def set_address(self, new_address) -> None:
        """Set a new device address"""
        if new_address < 1 or new_address > 0xFF:
            raise ModbusDevice.InvalidConfigurationException(
                f"address {hex(new_address)} is out of valid range 0x01-0xff"
            )
        response = self.modbus_client.write_register(
            slave=self.address,
            address=ModbusDevice.REGISTER_ADDRESS,
            value=new_address,
        )
        if isinstance(response, ModbusException):
            raise response
        # Success: we have to change our own address to new one!
        self.address = new_address

    def _get_register_values(self, reg_addr, count=1) -> bytes:
        response = self.modbus_client.read_holding_registers(
            slave=self.address, address=reg_addr, count=count
        )
        if isinstance(response, ModbusException):
            raise response
        return response.registers

    def get_address(self) -> int:
        """Get the device address"""
        return self.address

    def get_software_version(self) -> int:
        """Get the device software version"""
        return self._get_register_values(ModbusDevice.REGISTER_SW_VERSION)[0]

    def reset(self) -> None:
        """Resets the state of the device to default."""
        _log.debug("Reset device")
        self.write_output_channel_values([False] * self.channels)
