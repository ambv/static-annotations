- [ ] Relax the wording on things that won't work as class decorators
    ```
    global_ns = sys.modules[cls.__module__].__dict__
    local_ns = collections.ChainMap({cls.__name__: cls}, cls.__dict__)
    ```

- [ ] Include "why not drop annotations with -O" in rejected ideas

    Yes, this is a possibility that I should address in the PEP explicitly.
    There are two reasons this is not satisfying:

    1. This only addresses runtime cost, not forward references, those still
    cannot be safely used in source code. Even if a single one was used in a
    single module, the entire program now has to be executed with this new
    hypothetical -O switch. Nobody would agree to dependencies like that.

    2. This throws the baby out with the bath water. Now *no* runtime annotation
    use can be performed. There's work on new tools that use PEP 484-compliant
    type annotations at runtime (Larry is reviving his dryparse library, Eric
    Smith is working on data classes). Those would not work with this
    hypothetical -O switch but are fine with the string form since they already
    need to use `typing.get_type_hints()`.

- [ ] Mention that if `__annotations__` filled at runtime by functions with
  their local state is a requirement, the code can access the dictionary directly.

  If somebody badly needs to store arbitrary data as annotations in generated
  functions, they still can directly write to `__annotations__`

- [ ] Explain "this is like absolute imports" better.

  Annotations inside nested classes which are using local scope currently have
  to use the local names directly instead of using the qualified name. This has
  similar issues to relative imports:

  ```
  class Menu(UIComponent): ...

  class Restaurant:
      class Menu(Enum):
          SPAM = 1
          EGGS = 2

      def generate_menu_component(self) -> Menu: ...
  ```

  It is impossible today to use the global "Menu" type in the annotation of the
  example method. This PEP is proposing to use qualified names in this case
  which disambiguates between the global "Menu" and "Restaurant.Menu". In this
  sense it felt similar to absolute imports to me.

- [ ] Talk about validating the expressions after the module gets compiled
  since both GvR and Steven stressed this is important.

  The idea would be to validate the expressions after the entire module is
  compiled, something like what the flake8-pyi plugin is doing today for .pyi
  files. Guido pointed out that it's not trivial since the compiler doesn't keep
  a symbol table around. But I'd invest time in this since I agree with your
  point that we should raise errors as early as possible.
