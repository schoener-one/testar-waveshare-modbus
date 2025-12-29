# Main Documentation for Testar Waveshare Modbus

Welcome to the **Testar Waveshare Modbus** project! This documentation provides an overview of the project, its structure, and how to get started.

## Overview

The Testar Waveshare Modbus project is designed to facilitate communication with Modbus devices. It includes utilities for logging, core functionalities, and a command-line interface for ease of use.

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

To get started with the Testar Waveshare Modbus project, clone the repository and install the required dependencies. Refer to the [README.md](../README.md) for detailed installation instructions.

## Project Structure

The project is organized as follows:

```
testar-waveshare-modbus/
├── src/
│   └── testar_waveshare_modbus/
│       ├── __init__.py
│       ├── Utils.py
│       ├── core.py
│       ├── modbus.py
│       └── cli.py
├── tests/
│   ├── __init__.py
│   ├── test_utils.py
│   ├── test_core.py
│   └── test_modbus.py
├── docs/
│   ├── index.md
│   └── architecture.md
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── .pre-commit-config.yaml
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── pyproject.toml
├── README.md
└── tox.ini
```

## Usage

Refer to the [README.md](../README.md) for usage examples and command-line interface instructions.

## Testing

To run the tests, use the following command:

```bash
pytest
```

Make sure to have all dependencies installed as specified in the `pyproject.toml`.

## Contributing

We welcome contributions! Please refer to the [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on how to contribute to the project.

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for more details.