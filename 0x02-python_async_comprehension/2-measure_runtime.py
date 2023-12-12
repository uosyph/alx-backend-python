#!/usr/bin/env python3
"""Returns the execute time for 4 comprehension running in parallel"""

import asyncio
import time

async_comprehension = __import__("1-async_comprehension").async_comprehension


async def measure_runtime() -> float:
    """Executes 4 comprehensions in parallel, then return runtime"""
    start_timer = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    stop_timer = time.perf_counter()
    return stop_timer - start_timer
