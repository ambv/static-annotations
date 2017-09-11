from typing import TYPE_CHECKING, List, get_type_hints

if TYPE_CHECKING:
    from stringify import C


def function(arg: 'List[C]') -> None:
    ...


def main():
    annotations = get_type_hints(function)  # this raises NameError on 'C'
    print(f'Annotations for {function}: {annotations}')


if __name__ == '__main__':
    main()
