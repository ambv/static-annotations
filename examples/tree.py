import sys
from typing import get_type_hints


def resolve_types(cls):
    globalns = sys.modules[cls.__module__].__dict__
    return get_type_hints(cls, globalns=globalns)


def class_decorator(cls):
    annotations = resolve_types(cls)
    print(annotations)
    return cls


# a class decorator won't work because the name "Tree" isn't assigned yet
#@class_decorator
class Tree:
    left: 'Tree'
    right: 'Tree'

    def __init__(self, left: 'Tree', right: 'Tree'):
        self.left = left
        self.right = right


print(resolve_types(Tree))
