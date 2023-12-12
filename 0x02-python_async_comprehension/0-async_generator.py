#!/usr/bin/env python3
"""Yields a random number (0-10) every 1 asynchronous second for 10 seconds"""

import asyncio
import random
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """Loop 10 times, each time asynchronously wait 1 second,
    then yield a random number between 0 and 10"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
