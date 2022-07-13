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


class LengthBlock(verb_required_block(True, payload=True)):
    """
    The length block will check the length of the given String.
    If a parameter is passed in, the block will check the length
    based on what you passed in, w for word, s for spaces.
    If you provide an invalid parameter, the block will return -1.

    **Usage:** ``{length(["w", "s"]):<text>}``

    **Aliases:** ``len``

    **Payload:** ``text``

    **Parameter:** ``"w", "s"``

    .. tagscript::

        {length:TagScript}
        9

        {len(w):Tag Script}
        2

        {len(s):Hello World, Tag, Script}
        3

        {len(space):Hello World, Tag, Script}
        -1
    """

    ACCEPTED_NAMES = ("length", "len")

    def process(self, ctx: Context) -> Optional[str]:
        """
        Check the length of a string
        """
        if ctx.verb.parameter:
            if ctx.verb.parameter in ("w", "words", "word"):
                return str(len(ctx.verb.payload.split(" ")))
            if ctx.verb.parameter in ("s", "spaces", "space"):
                return str(len(ctx.verb.payload.split(" ") - 1))
            return "-1"
        return len(ctx.verb.payload)
