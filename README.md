# README.md

# Testar Waveshare Modbus

Testar Waveshare Modbus is a Python project designed to facilitate communication with Modbus devices. It provides a set of utilities and core functionalities for interacting with Modbus protocols, along with a command-line interface for ease of use.

## Features

- Utility functions for logging, boolean conversion, and file path resolution.
- Core functionalities for managing Modbus communication.
- Command-line interface for executing Modbus commands.
- Comprehensive unit tests to ensure code quality and reliability.

## Installation

To install the project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/testar-waveshare-modbus.git
cd testar-waveshare-modbus
pip install -r requirements.txt
```

Alternatively, you can use `poetry` or `pipenv` to manage dependencies.

## Usage

To use the command-line interface, run the following command:

```bash
python -m testar_waveshare_modbus.cli
```

You can also import the utilities and core functionalities in your Python scripts:

```python
from testar_waveshare_modbus.Utils import Utils
from testar_waveshare_modbus.core import CoreFunctionality
```

## Running Tests

To run the tests, use `pytest`:

```bash
pytest
```

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Changelog

For a list of changes, please refer to the [CHANGELOG.md](CHANGELOG.md) file.