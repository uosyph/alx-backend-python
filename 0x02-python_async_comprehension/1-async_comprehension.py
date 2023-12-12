#!/usr/bin/env python3
"""Returns 10 random numbers collected using an async comprehending"""

from typing import List

async_generator = __import__("0-async_generator").async_generator


async def async_comprehension() -> List[float]:
    """collect 10 random numbers using an async comprehending
    over async_generator, then return the 10 random numbers"""
    results = [result async for result in async_generator()]
    return results
