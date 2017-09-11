from collections import ChainMap
import sys


def get_class_globals(cls):
    """Computes the full globals for a given class."""

    result = {}
    result.update(sys.modules[cls.__module__].__dict__)
    for child in cls.__qualname__.split('.'):
        result.update(result[child].__dict__)

    return result
