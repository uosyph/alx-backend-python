#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

element_length =  __import__('9-element_length').element_length

print(element_length.__annotations__)
