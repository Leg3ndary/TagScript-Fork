from typing import Optional

from ..interface import verb_required_block
from ..interpreter import Context


class CountBlock(verb_required_block(True, payload=True)):
    """
    The count block will count how much of text is in message.
    This is case sensitive and will include substrings, if you
    don't provide a parameter, it will count the spaces in the
    message.


    **Usage:** ``{count([text]):<message>}``

    **Aliases:** ``None``

    **Payload:** ``message``

    **Parameter:** text

    .. tagscript::

        {count(Tag):TagScript}
        1

        {count(Tag):Tag Script TagScript}
        2

        {count(t):Hello World, Tag, Script}
        1 as there's only one lowercase t in the entire string
    """

    ACCEPTED_NAMES = ("count",)

    def process(self, ctx: Context) -> Optional[str]:
        """
        Check the count of a string
        """
        if ctx.verb.parameter:
            return ctx.verb.payload.count(ctx.verb.parameter)
        return len(ctx.verb.payload) + 1
