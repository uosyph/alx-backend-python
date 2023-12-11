#!/usr/bin/env python3
"""Asynchronous coroutine that returns and integer after a random delay"""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Takes an integer, waits for a random delay, then returns it"""
    delay: float = random.uniform(0, max_delay)
    await asyncio.sleep(delay)
    return delay
