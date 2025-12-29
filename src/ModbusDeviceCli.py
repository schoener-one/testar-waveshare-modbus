#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Denis Schoener"
__copyright__ = "Copyright (C) 2025 Denis Schoener (denis@schoener-one.de)"
__license__ = "MIT"
__doc__ = "Contains the CLI interface for the Modbus device controls"

import argparse
import logging
import sys
from pymodbus import ModbusException
from pymodbus.logging import Log as PymodbusLog
from RelayDevice import RelayDevice
from DigitalIoDevice import DigitalIoDevice
from ModbusDevice import ModbusDevice
from Utils import Utils, LOG_LEVELS


_log = logging.getLogger(__name__)


def create_device(args):
    if args.device_type == RelayDevice.SHORT_NAME:
        return RelayDevice(args.serial_device, args.baudrate, args.device_number)
    elif args.device_type == DigitalIoDevice.SHORT_NAME:
        return DigitalIoDevice(args.serial_device, args.baudrate, args.device_number)
    else:
        raise argparse.ArgumentError(
            None, message=f"unknown device type: {args.device_type}"
        )


def read_channels(args):
    device = create_device(args)
    if args.input_channels:
        values = device.read_input_channel_values()
    else:
        values = device.read_output_channel_values()
    if device:
        _log.info("Channel values: %s", " ".join("%0.2x" % int(x) for x in values))


def write_channels(args):
    device = create_device(args)
    value = Utils.to_bool(args.set_value) if args.set_value else False
    if args.channels:
        int_channels = [int(x) for x in args.channels.split(",")]
        device.write_output_channel_values_by_indices(
            channels=int_channels,
            value=value,
        )
    elif args.all:
        device.write_all_output_channel_values(value=value)


def config_device(args):
    device = create_device(args)
    if args.set_baudrate:
        device.set_baudrate(int(args.set_baudrate))
    if args.set_address:
        device.set_address(int(args.set_address))
    if not args.set_baudrate and not args.set_address:
        # Just print current configuration
        _log.info("Device Software version: %s", device.get_software_version())
        _log.info("Device address: %0.2x", device.get_address())


def main_cli() -> int:
    """Main CLI entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser("Modbus RTU channel controlling tool")
    parser.add_argument(
        "-d",
        "--serial-device",
        help="Serial communication device for Modbus RTU (i.e. /dev/ttyUSB0)",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--device-type",
        choices=[
            RelayDevice.SHORT_NAME,
            DigitalIoDevice.SHORT_NAME,
        ],
        default=RelayDevice.SHORT_NAME,
        help="Device type [rel32: 32ch relay, dio: digital-io, ain: analog-input, aout: analog-output, rel16: 16ch relay]",
    )
    parser.add_argument(
        "-n",
        "--device-number",
        type=int,
        default=1,
        help="Number of the device to be used for Modbus RTU communication",
    )
    parser.add_argument(
        "-b",
        "--baudrate",
        type=int,
        help="baudrate for communication (default: 115200)",
        default=115200,
    )
    parser.add_argument(
        "-L",
        "--log-submodules",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Indicates if submodules should be logged",
    )
    parser.add_argument(
        "-l", "--log-level", choices=LOG_LEVELS.keys(), default="info"
    )
    sub_parsers = parser.add_subparsers(help="sub-command help")

    # Add sub-command for channel read:
    parser_read = sub_parsers.add_parser("read", help="read channel values")
    parser_read.set_defaults(func=read_channels)
    parser_read.add_argument(
        "-i",
        "--input-channels",
        action=argparse.BooleanOptionalAction,
        help="Indicates if the input channels or the output channels should be read, depending on if the argument is set or not",
    )

    # Add sub-command for channel write:
    parser_write = sub_parsers.add_parser("write", help="write channel values")
    parser_write.add_argument(
        "-c",
        "--channels",
        help="List of comma separated channel indices which should be written. The channel numbers start with 1.",
    )
    parser_write.add_argument(
        "-a",
        "--all",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Indicates if all channels should be set",
    )
    parser_write.add_argument(
        "-s",
        "--set-value",
        default="0",
        help="channel value to be set (default: 0)",
    )
    parser_write.set_defaults(func=write_channels)

    # Add sub-command for device configuration:
    parser_config = sub_parsers.add_parser("config", help="set channel configuration")
    parser_config.add_argument(
        "-B",
        "--set-baudrate",
        type=int,
        default=None,
        help="new baudrate to set",
    )
    parser_config.add_argument(
        "-A",
        "--set-address",
        type=lambda x: int(x, 0),
        default=None,
        help="new device address to set",
    )
    parser_config.set_defaults(func=config_device)

    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s]: %(name)s - %(message)s",
        level=LOG_LEVELS[args.log_level],
    )

    for name in [
        __name__,
        RelayDevice.__name__,
        DigitalIoDevice.__name__,
        ModbusDevice.__name__,
    ]:
        logging.getLogger(name).setLevel(LOG_LEVELS[args.log_level])

    if args.log_submodules:
        PymodbusLog.setLevel(_log.level)

    try:
        args.func(args)
    except ModbusException as ex:
        _log.error(str(ex))
        sys.exit(1)


if __name__ == "__main__":
    main_cli()
