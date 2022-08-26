from typing import Optional

from ..adapter import StringAdapter
from ..interface import Block
from ..interpreter import Context


class LooseVariableGetterBlock(Block):
    """
    The loose variable block represents the adapters for any seeded or defined variables.
    This variable implementation is considered "loose" since it checks whether the variable is
    valid during :meth:`process`, rather than :meth:`will_accept`.
    You may also define variables here with {$<variable name>:<value>}, note that this is not
    available using the StrictVariableGetterBlock class.

    **Usage:** ``{<variable_name>([parameter]):[payload]}``

    **Aliases:** This block is valid for any inputted declaration.

    **Payload:** Depends on the variable's underlying adapter.

    **Parameter:** Depends on the variable's underlying adapter.

    **Examples:**

    .. tagscript::

        {=(example):This is my variable.}
        {example}
        This is my variable.

        {$variablename:This is another variable.}
        {variablename}
        This is another variable.
    """

    def will_accept(self, ctx: Context) -> bool:  # pylint: disable=arguments-differ
        """
        This block will accept any declaration.
        """
        return True

    def process(self, ctx: Context) -> Optional[str]:
        """
        This block will check whether the variable is valid.
        """
        if ctx.verb.declaration.startswith("$"):
            varname = ctx.verb.declaration.split("$", 1)[1]
            ctx.response.variables[varname] = StringAdapter(str(ctx.verb.payload))
            return ""
        if ctx.verb.declaration in ctx.response.variables:
            return ctx.response.variables[ctx.verb.declaration].get_value(ctx.verb)
        return None


class StrictVariableGetterBlock(Block):
    """
    The strict variable block represents the adapters for any seeded or defined variables.
    This variable implementation is considered "strict" since it checks whether the variable is
    valid during :meth:`will_accept` and is only processed if the declaration refers to a valid
    variable. The main difference between this and the LooseVariableGetterBlock is that this
    block will only attempt to process if the variable's already been defined.

    **Usage:** ``{<variable_name>([parameter]):[payload]}``

    **Aliases:** This block is valid for any variable name in `Response.variables`.

    **Payload:** Depends on the variable's underlying adapter.

    **Parameter:** Depends on the variable's underlying adapter.

    **Examples:**

    .. tagscript::

        {=(example):This is my variable.}
        {example}
        This is my variable.
    """

    def will_accept(self, ctx: Context) -> bool:  # pylint: disable=arguments-differ
        """
        Check if the declaration is in the response variables
        """
        return ctx.verb.declaration in ctx.response.variables

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the strict variable block
        """
        return ctx.response.variables[ctx.verb.declaration].get_value(ctx.verb)
