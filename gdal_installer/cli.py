import os
import sys
import platform

def main():
    """Entry point for the install-gdal command."""
    # Use python3 on Unix-like systems, python on Windows
    python_cmd = 'python3' if platform.system() != 'Windows' else 'python'
    
    # go to the path of the cli script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Path to the installation script
    script_path = "./install-gdal.py"
    
    # Execute the installation script
    return os.system(f'{python_cmd} "{script_path}"')

if __name__ == '__main__':
    sys.exit(main())
