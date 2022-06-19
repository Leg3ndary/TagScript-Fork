from typing import Optional
from ..interface import verb_required_block
from ..interpreter import Context


class LengthBlock(verb_required_block(True, payload=True)):
    """
    The length block will check the length of the given String.
    If a parameter is passed in, the block will check the length
    based on what you passed in, w for word, s for spaces.
    If you provide an invalid paramet

    **Usage:** ``{length(<w, s>):<String>}``

    **Aliases:** ``len``

    **Payload:** String to check length of

    **Parameter:** w or s, words or spaces, if not one of these will return -1

    .. tagscript::

        {length:TagScript}
        9

        {len(w):Tag Script}
        2

        {len(s):Hello World, Tag, Script}
        3

        {len(S):Hello World, Tag, Script}
        -1
    """

    ACCEPTED_NAMES = ("length", "len")

    def process(self, ctx: Context) -> Optional[str]:
        """
        Check the length of a string
        """
        if ctx.verb.parameter:
            if ctx.verb.parameter == "w":
                return str(len(ctx.verb.payload.split(" ")))
            elif ctx.verb.parameter == "s":
                return str(len(ctx.verb.payload.split(" ") - 1))
            else:
                return "-1"
            
        else:
            return len(ctx.verb.payload)