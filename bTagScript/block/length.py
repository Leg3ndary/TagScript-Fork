from typing import Optional
from ..interface import verb_required_block
from ..interpreter import Context


class LengthBlock(verb_required_block(True, payload=True)):
    """
    The length block will check the length of the given String.
    If a parameter is passed in, the block will check the length
    split by the given "delimiter".

    **Usage:** ``{length(<Optional Character(s)>):<String>}``

    **Aliases:** ``len``

    **Payload:** String to check length of

    **Parameter:** 

    .. tagscript::

        {length:TagScript}
        9

        {len( ):Tag Script}
        2

        {len(,):Hello World, Tag, Script}
        3
    """

    ACCEPTED_NAMES = ("length", "len")

    def process(self, ctx: Context) -> Optional[str]:
        """
        Check the length of a string
        """
        if ctx.verb.parameter:
            return len(ctx.verb.payload.split(ctx.verb.parameter))
        else:
            return len(ctx.verb.payload)