from typing import Sequence


def fetch_one(value: Sequence):
    return next(iter(value))
