PEP: 5XX
Title:
Version: $Revision$
Last-Modified: $Date$
Author: Łukasz Langa <lukasz@langa.pl>
Discussions-To: Python-Dev <python-dev@python.org>
Status: Draft
Type: Standards Track
Content-Type: text/x-rst
Created: 8-Sep-2017
Python-Version: 3.7
Post-History:
Resolution:


Abstract
========

PEP 3107 introduced syntax for function annotations, but the semantics
were deliberately left undefined.  PEP 484 introduced a standard meaning
to annotations: type hints.  PEP 526 defined variable annotations,
explicitly tying them with the type hinting use case.

This PEP proposes changing function annotations and variable annotations
so that they are no longer evaluated at function definition time.
Instead, they are preserved in ``__annotations__`` in string form.


Rationale and Goals
===================

PEP 3107 added support for arbitrary annotations on parts of a function
definition.  Just like default values, annotations are evaluated at
function definition time.  This creates a number of issues for the type
hinting use case:

* forward references: when a type hint contains names that have not been
  defined yet, that definition needs to be expressed as a string
  literal;

* type hints are executed at module import time, which is not
  computationally free.

Postponing the evaluation of annotations solves both problems.

Non-goals
---------

Just like in PEP 484 and PEP 526, it should be emphasized that **Python
will remain a dynamically typed language, and the authors have no desire
to ever make type hints mandatory, even by convention.**

Annotations are still available for arbitrary use besides type checking.
Using ``@typing.no_type_hints`` in this case is recommended to
disambiguate the use case.


Implementation
==============

In a future version of Python, function and variable annotations will no
longer be evaluated at definition time.  Instead, a string form will be
preserved in the respective ``__annotations__`` dictionary.  Static type
checkers will see no difference in behavior, whereas tools using
annotations at runtime will have to perform postponed evaluation.

If an annotation was already a string, this string is preserved
verbatim.  In other cases, the string form is obtained from the AST
during the compilation step, which means that the string form preserved
might not preserve the exact formatting of the source.

Annotations need to be syntactically valid Python expressions, also when
passed as literal strings (i.e. ``compile(literal, '', 'eval')``).

Note that as per PEP 526, local variable annotations are not evaluated
at all since they are not accessible outside of the function's closure.

Enabling the future behavior in Python 3.7
------------------------------------------

The functionality described above can be enabled starting from Python
3.7 using the following special import::

    from __future__ import annotations


Resolving Type Hints at Runtime
===============================

To resolve an annotation at runtime from its string form to the result
of the enclosed expression, user code needs to evaluate the string.

For code that uses type hints, the ``typing.get_type_hints()`` function
correctly evaluates expressions back from its string form.  Note that
all valid code currently using ``__annotations__`` should already be
doing that since a type annotation can be expressed as a string literal.

For code which uses annotations for different purposes, ``FunctionX`` is
provided which resolves the annotation correctly, providing the right
globals to the compiler.  Using ``eval()`` directly is not recommended
due to this reason.

Runtime annotation resolution and class decorators
--------------------------------------------------

Metaclasses and class decorators that need to resolve annotations for
the current class will fail for annotations that use the name of the
current class.  Example::

    def class_decorator(cls):
        annotations = get_type_hints(cls)  # raises NameError on 'C'
        print(f'Annotations for {cls}: {annotations}')
        return cls

    @class_decorator
    class C:
        singleton: 'C' = None

This was already true before this PEP.  The class decorator acts on
the class before it's assigned a name in the current definition scope.

The situation is made somewhat stricter when class-level variables are
considered.  Previously, when the string form wasn't used in annotations,
a class decorator would be able to cover situations like::

    @class_decorator
    class Restaurant:
        class MenuOption(Enum):
            SPAM = 1
            EGGS = 2

        default_menu: List[MenuOption] = []

This is no longer possible.

Runtime annotation resolution and ``TYPE_CHECKING``
---------------------------------------------------

Sometimes there's code that must be seen by a type checker but should
not be executed.  For such situations the ``typing`` module defines a
constant, ``TYPE_CHECKING``, that is considered ``True`` during type
checking but ``False`` at runtime.  Example::

  import typing

  if typing.TYPE_CHECKING:
      import expensive_mod

  def a_func(arg: expensive_mod.SomeClass) -> None:
      a_var: expensive_mod.SomeClass = arg
      ...

This approach is also useful when handling import cycles.

Trying to resolve annotations of ``a_func`` at runtime using
``typing.get_type_hints()`` will fail since the name ``expensive_mod``
is not defined (``TYPE_CHECKING`` variable being ``False`` at runtime).
This was already true before this PEP.


Backwards Compatibility
=======================

This is a backwards incompatible change.  Applications depending on
arbitrary objects to be directly present in annotations will break
if they are not using ``typing.get_type_hints()`` or ``FunctionX``.

Resolving function or class variable annotations that depend on
function-local closures at the time of the function/class definition is
no longer possible.  Example::

    def generate_class():
        some_local = datetime.datetime.now()
        class C:
            field: some_local = 1  # NOTE: INVALID ANNOTATION
            def method(self, arg: some_local.day) -> None:  # NOTE: INVALID ANNOTATION
                ...

Annotations using nested classes and their respective state are still
valid.  Example::

    class C:
        field = 'c_field'
        def method(self, arg: field) -> None:  # this is OK
            ...

        class D:
            field2 = 'd_field'
            def method(self, arg: field -> field2:  # this is OK
                ...

Note that if ``field`` and ``field2`` shared a name, addressing both
would no longer be possible due to variable shadowing.  It would also
be misleading to the reader.  Thus, using a fully qualified name is
now recommended.  Modifying the previous example::

    class C:
        field = 'c_field'
        def method(self, arg: C.field) -> None:  # this is OK
            ...

        class D:
            field2 = 'd_field'
            def method(self, arg: C.field -> D.field2:  # this is OK
                ...

Deprecation policy
------------------

In Python 3.7, a ``__future__`` import is required to use the described
functionality and a ``PendingDeprecationWarning`` is raised by the
compiler in the presence of type annotations in modules without the
``__future__`` import.  In Python 3.8 the warning becomes a
``DeprecationWarning``.  In the next version this will become the
default behavior.


PEP Development Process
=======================

A live draft for this PEP lives on GitHub [github]_.  There is also an
issue tracker [issues]_, where much of the technical discussion takes
place.

The draft on GitHub is updated regularly in small increments.  The
official PEPS repo [peps]_ is (usually) only updated when a new draft
is posted to python-dev.


Acknowledgements
================

This document could not be completed without valuable input,
encouragement and advice from Guido van Rossum, Jukka Lehtosalo, and
Ivan Levkivskyi.


References
==========

.. [github]
   https://github.com/ambv/static-annotations

.. [issues]
   https://github.com/python/static-annotations/issues

.. [peps]
   https://github.com/python/peps/blob/master/pep-05XX.txt


Copyright
=========

This document has been placed in the public domain.



..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   coding: utf-8
   End:


### Remaining things from PEP 484


A compromise is possible where a ``__future__`` import could enable
turning *all* annotations in a given module into string literals, as
follows::

  from __future__ import annotations

  class ImSet:
      def add(self, a: ImSet) -> List[ImSet]: ...

  assert ImSet.add.__annotations__ == {'a': 'ImSet', 'return': 'List[ImSet]'}

Such a ``__future__`` import statement may be proposed in a separate
PEP.
