from typing import Optional

from ..interface import Block
from ..interpreter import Context


class LooseVariableGetterBlock(Block):
    """
    The loose variable block represents the adapters for any seeded or defined variables.
    This variable implementation is considered "loose" since it checks whether the variable is
    valid during :meth:`process`, rather than :meth:`will_accept`.

    **Usage:** ``{<variable_name>([parameter]):[payload]}``

    **Aliases:** This block is valid for any inputted declaration.

    **Payload:** Depends on the variable's underlying adapter.

    **Parameter:** Depends on the variable's underlying adapter.

    **Examples:**

    .. tagscript::

        {=(example):This is my variable.}
        {example}
        This is my variable.
    """

    def will_accept(self, ctx: Context) -> bool:
        return True

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.declaration in ctx.response.variables:
            if ctx.verb.parameter:
                if ctx.verb.parameter.isdigit() or ctx.verb.parameter.startswith("-") and ctx.verb.parameter.split("-", 1)[1].isdigit():
                    return (
                        ctx.response.variables[ctx.verb.declaration]
                        .get_value(ctx.verb)
                        .split(ctx.verb.payload if ctx.verb.payload else " ")[
                            int(ctx.verb.parameter) - 1
                        ]
                    )
                elif ctx.verb.parameter.starswith("+") and ctx.verb.parameter.split("+", 1)[1].isdigit():
                    return (
                        ctx.response.variables[ctx.verb.declaration]
                        .get_value(ctx.verb)
                        .split(ctx.verb.payload if ctx.verb.payload else " ")[
                            0:int(ctx.verb.parameter)
                        ]
                    )
            else:
                return ctx.response.variables[ctx.verb.declaration].get_value(ctx.verb)
        else:
            return None
