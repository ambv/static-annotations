from enum import Enum
from typing import List, get_type_hints


def class_decorator(cls):
    annotations = get_type_hints(cls)
    print(f'Annotations for {cls}: {annotations}')
    return cls


@class_decorator
class Restaurant:
    class MenuOption(Enum):
        SPAM = 1
        EGGS = 2

    default_menu: List[MenuOption] = []
