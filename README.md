```
        _____                                 _____        ___________ 
______ ____(_)________________ ______ __________  /___________  /___(_)
_  __ `/__  / __  ___/___  __ \_  __ \__  ___/_  __/_  ___/__  / __  / 
/ /_/ / _  /  _  /    __  /_/ // /_/ /_  /    / /_  / /__  _  /  _  /  
\__,_/  /_/   /_/     _  .___/ \____/ /_/     \__/  \___/  /_/   /_/   
                      /_/
```

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![GitHub issues](https://img.shields.io/github/issues/Dynosol/airport-cli)](https://github.com/Dynosol/airport-cli/issues)
[![GitHub stars](https://img.shields.io/github/stars/Dynosol/airport-cli)](https://github.com/Dynosol/airport-cli/stargazers)


A Python-based command line interface for AirPort wireless on macOS, designed to replace the `airport` utility, depricated in macOS Sonoma 14.4.

## Usage

```
Usage:
  airportcli info [-l|--long]
  airportcli -I | -getinfo [-l|--long]
  airportcli join <SSID>
  airportcli quality
  airportcli off
  airportcli on
  airportcli scan [<query>]
  airportcli -s [<query>]
  airportcli ssid
  airportcli -h | --help | help
  airportcli --version
  
  Add -v or --verbose to any command for detailed logging output.
```

### Subcommands

| Command | Description |
|---------|-------------|
| `info`, `-I`, `-getinfo` | Print the current network SSID and quality percentage. Use the `-l` or `--long` options to print detailed information about the connection. |
| `join` | Join the specified network. (deprecated) |
| `quality` | Show the wireless quality as a percentage. |
| `off` | Turn wireless off. (deprecated) |
| `on` | Turn wireless on. (deprecated) |
| `scan`, `-s` | Perform a scan for wireless networks. |
| `ssid` | Print the current network's SSID. |
| `help` | Display help information. |

### Options

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Display help information. |
| `--version` | Display version information. |
| `-v`, `--verbose` | Enable verbose logging output. |

## Installation

### pip

To install with pip:

```bash
pip install git+https://github.com/Dynosol/airportcli.git
```

### PyPI (coming soon, or probably never)

```bash
pip install airportcli
```

### Homebrew (coming soon, or also probably never)

```bash
brew install airportcli
```

### Manual

To install manually, clone the repository and install:

```bash
git clone https://github.com/Dynosol/airportcli.git
cd airportcli
pip install -e .
```

## Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
4. Install development dependencies: `pip install -e .`

## Compatibility

- macOS Sonoma 14.4 and later
- Python 3.6+

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the original `airport` utility in macOS
- Special thanks to [@xwmx](https://github.com/xwmx) for the original airport utility
