#!/usr/bin/python3.10

import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/QR-Code'
if path not in sys.path:
    sys.path.append(path)

from app import app as application

if __name__ == "__main__":
    application.run()
