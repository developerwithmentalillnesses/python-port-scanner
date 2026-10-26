# Python Port Scanner

A Python-based TCP port scanner developed as a personal cybersecurity project. It features both a command-line interface (CLI) and a graphical user interface (GUI) with a cyberpunk-inspired design.

The project explores network scanning, socket programming, error handling, result analysis, and modular software development in Python.

## Features

- **TCP Port Scanning:** scans a configurable range of ports on a target IPv4 address.
- **Command-Line Interface:** interactively configure and run scans from the terminal.
- **Graphical User Interface:** launch scans through a custom dark-themed interface built with CustomTkinter.
- **Port Status Detection:** displays open and closed ports, as well as connection errors.
- **Service Identification:** attempts to identify the services associated with scanned ports.
- **Result Filtering:** filter scan results through the CLI.
- **Scan Statistics:** summarizes scanned ports, open ports, closed ports, and errors.
- **Execution Timing:** measures the duration of CLI scans.
- **Input Validation:** validates IPv4 addresses and port ranges in the GUI.
- **Modular Architecture:** separates scanning logic, configuration, data models, interfaces, and result processing.

## Technologies

- Python 3
- TCP/IP networking
- `socket`
- `ipaddress`
- `threading`
- CustomTkinter
- Git and GitHub

## Project Structure

```text
Port-Scanner/
├── cli.py       # Command-line interaction
├── config.py    # Scanner configuration
├── gui.py       # Graphical user interface
├── main.py      # CLI application entry point
├── models.py    # Scan result data models
├── results.py   # Result filtering and statistics
├── scanner.py   # Core scanning logic
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or later recommended.
- CustomTkinter for the graphical interface.
- Network access to the target being scanned.

The CLI uses Python's standard library and the project's internal modules. The GUI requires CustomTkinter.

## Installation

Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
cd Port-Scanner
```

Install the GUI dependency:

```bash
python -m pip install customtkinter
```

## Usage

### Command-Line Interface

Run the CLI application:

```bash
python main.py
```

Follow the interactive prompts to enter the target IP address, select a port range, and choose how to filter the results.

### Graphical User Interface

Launch the GUI:

```bash
python gui.py
```

Enter the target IPv4 address, the starting port, and the ending port. Click **SCAN** to start the scan.

The interface displays scan results, port statuses, detected services, errors, and summary statistics.

## Learning Objectives

This project was built to practise and develop skills in:

- Python socket programming and TCP connections.
- Network port scanning fundamentals.
- Input validation and exception handling.
- Multithreading and responsive GUI design.
- Data modelling and result processing.
- Modular code organization.
- Version control using Git.

## Responsible Use

Use this tool only on systems you own or have explicit permission to test. Ensure that your scanning activities comply with applicable laws, organizational policies, and network terms of service.

## Disclaimer

This project is intended for educational purposes and authorized security testing only. The author is not responsible for unauthorized or unlawful use.

## Author

Developed as a personal Python and cybersecurity portfolio project.
