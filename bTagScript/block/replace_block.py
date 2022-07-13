from typing import Optional

from ..interface import verb_required_block
from ..interpreter import Context


class ReplaceBlock(verb_required_block(True, payload=True, parameter=True)):
    """
    The replace block will replace specific characters in a string.
    The parameter should split by a ``,``, containing the characters to find
    before the command and the replacements after.

    **Usage:** ``{replace(<original,new>):<message>}``

    **Aliases:** ``sub``

    **Payload:** message

    **Parameter:** original, new

    .. tagscript::

        {replace(o,i):welcome to the server}
        welcime ti the server

        {replace(1,6):{args}}
        if {args} is 1637812
        6637862

        {replace(, ):Test}
        T e s t
    """

    ACCEPTED_NAMES = ("replace", "sub")

    def process(self, ctx: Context) -> Optional[str]:
        """
        Replace the characters in the payload
        """
        try:
            before, after = ctx.verb.parameter.split(",", 1)
        except ValueError:
            return None

        return ctx.verb.payload.replace(before, after)


class PythonBlock(verb_required_block(True, payload=True, parameter=True)):
    """
    The in block serves three different purposes depending on the alias that is used.

    The ``in`` alias checks if the parameter is anywhere in the payload.

    ``contain`` strictly checks if the parameter is the payload, split by whitespace.

    ``index`` finds the location of the parameter in the payload, split by whitespace.
    If the parameter string is not found in the payload, it returns 1.

    index is used to return the value of the string form the given list of

    **Usage:** ``{in(<string>):<payload>}``

    **Aliases:** ``index, contains``

    **Payload:** ``payload``

    **Parameter:** ``string``

    **Examples:**

    .. tagscript::

        {in(apple pie):banana pie apple pie and other pie}
        true
        {in(mute):How does it feel to be muted?}
        true
        {in(a):How does it feel to be muted?}
        false

        {contains(mute):How does it feel to be muted?}
        false
        {contains(muted?):How does it feel to be muted?}
        false

        {index(food):I love to eat food. everyone does.}
        4
        {index(pie):I love to eat food. everyone does.}
        -1
    """

    def will_accept(self, ctx: Context) -> bool:
        """
        Check if we can accept
        """
        dec = ctx.verb.declaration.lower()
        return dec in ("contains", "in", "index")

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the block
        """
        dec = ctx.verb.declaration.lower()
        if dec == "contains":
            return str(bool(ctx.verb.parameter in ctx.verb.payload.split())).lower()
        if dec == "in":
            return str(bool(ctx.verb.parameter in ctx.verb.payload)).lower()
        try:
            return str(ctx.verb.payload.strip().split().index(ctx.verb.parameter))
        except ValueError:
            return "-1"
