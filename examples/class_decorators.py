from typing import List, get_type_hints


def class_decorator(cls):
    annotations = get_type_hints(cls)
    print(f'Annotations for {cls}: {annotations}')
    return cls


@class_decorator
class C:
    singleton: 'C' = None
