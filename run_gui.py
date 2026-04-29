#!/usr/bin/env python3
"""
Script to run the orbital mechanics simulator GUI
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from gui.main_window import main

if __name__ == "__main__":
    main()
