"""This is an example of postponed evaluation from a different module. It also
includes a tricky example with nested classes."""

import sys

from util import get_class_globals
import stringify
from some_package.some_module import D


def evaluate_other_module():
    """Demonstrates how to evaluate annotations for a different module."""
    stringify_globals = stringify.__dict__
    mod_annotations = {}
    for k, v in stringify.__annotations__.items():
        mod_annotations[k] = eval(v, stringify_globals, stringify_globals)
    print('Other module:', mod_annotations)


def evaluate_method(C):
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
    c_locals = get_class_globals(c_meth.__self__.__class__)
    c_meth_annotations = {}
    for k, v in C.method_with_arbitrary_annotations.__annotations__.items():
        c_meth_annotations[k] = eval(v, c_meth_globals, c_locals)
    print(f'Method on an instance of {C}: {c_meth_annotations}')


def evaluate_classvar(C):
    """Demonstrates how to evaluate classvar annotations."""

    c_globals = get_class_globals(C)
    c_locals = C.__dict__
    c_annotations = {}
    for k, v in C.__annotations__.items():
        c_annotations[k] = eval(v, c_globals, c_locals)
    print(f'Class vars for {C}: {c_annotations}')


if __name__ == '__main__':
    evaluate_other_module()
    evaluate_method(C=stringify.C)
    evaluate_method(C=D.E)
    evaluate_classvar(C=stringify.C)
    evaluate_classvar(C=D.E)
