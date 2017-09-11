"""A bunch of examples of how to resolve annotations whose evaluation was
postponed.

Note: globals and functions are purposefully out of order to demonstrate the
forward reference problem.
"""

from util import get_class_globals

from typing import no_type_check


@no_type_check
def function_with_arbitrary_annotations(a: 'SOME_GLOBAL + "1"') -> '{"s": SOME_GLOBAL}':
    """Note: the no_type_check decorator is not mandatory but is recommended."""


class C:
    CLASS_VAR: 'SOME_GLOBAL + "2"' = 'CLASS_VAR_VALUE'

    def method_with_arbitrary_annotations(a: 'SOME_GLOBAL + "3"') -> '{"s": CLASS_VAR}':
        """Note: The no_type_check decorator here is missing to demonstrate that
        postponed evaluation doesn't require it. It's still recommended though.
        """


def evaluate_current_module():
    """Demonstrates how to evaluate annotations for the current module."""
    mod_annotations = {}
    for k, v in __annotations__.items():
        mod_annotations[k] = eval(v, globals(), globals())
    print('Current module:', mod_annotations)


def evaluate_method():
    """Demonstrates how to evaluate method annotations."""

    # unbound, just a function object
    c_meth = C.method_with_arbitrary_annotations
    c_meth_globals = c_meth.__globals__
    c_locals = get_class_globals(C)  # we need to know the class, if any
    c_meth_annotations = {}
    for k, v in C.method_with_arbitrary_annotations.__annotations__.items():
        c_meth_annotations[k] = eval(v, c_meth_globals, c_locals)
    print(f'Method on {C}: {c_meth_annotations}')

    # bound, can use __self__
    c_meth = C().method_with_arbitrary_annotations
    c_meth_globals = c_meth.__globals__
    c_locals = get_class_globals(c_meth.__self__.__class__)  # note: NOT the instance's dict
    c_meth_annotations = {}
    for k, v in C.method_with_arbitrary_annotations.__annotations__.items():
        c_meth_annotations[k] = eval(v, c_meth_globals, c_locals)
    print(f'Method on an instance of {C}: {c_meth_annotations}')


def evaluate_classvar():
    """Demonstrates how to evaluate classvar annotations."""
    c_globals = get_class_globals(C)
    c_locals = C.__dict__
    c_annotations = {}
    for k, v in C.__annotations__.items():
        c_annotations[k] = eval(v, c_globals, c_locals)
    print(f'Class vars for {C}: {c_annotations}')


SOME_GLOBAL: 'OTHER_GLOBAL' = 'SOME_GLOBAL_VALUE'
OTHER_GLOBAL: 'OTHER_GLOBAL' = 'OTHER_GLOBAL_VALUE'


if __name__ == '__main__':
    evaluate_current_module()
    evaluate_method()
    evaluate_classvar()
