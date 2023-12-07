#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

zoom_array =  __import__('102-type_checking').zoom_array

print(zoom_array.__annotations__)
