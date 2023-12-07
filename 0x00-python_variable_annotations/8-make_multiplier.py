#!/usr/bin/env python3
"""Takes multiplier, returns a function that multiplies by multiplier"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Takes a float multiplier and returns function multiplier"""
    return lambda x: multiplier * x
