import stringify


class D:
    D_CLASS_VAR = 'D_CLASS_VAR_VALUE'

    class E:
        E_CLASS_VAR: 'stringify.SOME_GLOBAL + D.D_CLASS_VAR' = 'E_CLASS_VAR_VALUE'

        def method_with_arbitrary_annotations(a: 'stringify.SOME_GLOBAL + "3"') -> '{"s": D.E.E_CLASS_VAR, "t": D.D_CLASS_VAR}':
            """Note: class variables need fully-qualified prefixes now.

            Also, the no_type_check decorator here is missing to demonstrate that
            postponed evaluation doesn't require it. It's still recommended though.
            """
