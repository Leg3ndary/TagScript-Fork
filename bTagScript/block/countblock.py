from typing import Optional
from ..interface import verb_required_block
from ..interpreter import Context


class CountBlock(verb_required_block(True, payload=True)):
    """
    The count block will count how much of x is in string.
    This is case sensitive and will include substrings

    **Usage:** ``{count(<Optional Character(s)>):<String>}``

    **Aliases:** ``None``

    **Payload:** String to check length of

    **Parameter:** Optional, if present, will count it, if not, will check "empty characters" (len + 1)

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
            return len(ctx.verb.payload.count(ctx.verb.parameter))
        else:
            return len(ctx.verb.parameter) + 1