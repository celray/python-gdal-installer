You know installing gdal can be annoying especially on windows. That is where "Python GDAL Installer" comes in.

Check the code and contribute: <a href="https://github.com/celray/python-gdal-installer">https://github.com/celray/python-gdal-installer</a>

# Python GDAL Installer

A simple tool to automatically install GDAL Python bindings on Windows and Unix systems. This tool handles the complex process of installing GDAL with proper wheel files for Windows and manages pip installation for Unix systems.

## Features
- Automatic detection of Python version and CPU architecture
- Pre-compiled wheel installation for Windows systems
- Support for multiple Python versions (3.10-3.13)
- Support for different CPU architectures (win32, win_amd64, win_arm64)
- Fallback to pip installation on Unix systems

## Requirements
- Python 3.10 or higher
- pip package manager
- Internet connection
- Required Python packages:
  - requests
  - tqdm

## Installation

1. Install required packages:
```bash
pip install gdal-installer
```

2. Install python-gdal:
```bash
gdal-installer
```

## How It Works

### Windows Systems
- Detects Python version and CPU architecture
- Downloads appropriate GDAL wheel from pre-compiled binaries
- Installs the wheel using pip
- Shows download progress with a progress bar

### Unix Systems
- Uses pip to install GDAL directly from PyPI
- Installs to user site-packages using --user flag

## Supported Configurations

### Python Versions
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

### Windows Architectures
- win32 (32-bit)
- win_amd64 (64-bit)
- win_arm64 (ARM64) - except for python 3.10

## Troubleshooting

1. If you get a "No GDAL wheel found" error:
   - Verify your Python version is supported
   - Check if your CPU architecture is supported
   - Ensure you have internet connectivity

2. For Unix systems:
   - You might need to install GDAL system libraries first
   - Some systems might require `--break-system-packages` flag (not included by default)

## Contributing

Feel free to open issues or submit pull requests if you find bugs or have suggestions for improvements.

## License

MIT License

## Credits

GDAL wheels for Windows are sourced from [cgohlke/geospatial-wheels](https://github.com/cgohlke/geospatial-wheels).
