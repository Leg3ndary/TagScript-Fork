from typing import Optional
from ..interface import verb_required_block
from ..interpreter import Context


class CommentBlock(verb_required_block(True, payload=True)):
    """
    The count block will count how much of x is in string.
    This is case sensitive and will include substrings

    **Usage:** ``{comment(<Optional String>):<String>}``

    **Aliases:** ``/, Comment``

    **Payload:** Whatever you want to comment, won't do anything with it

    **Parameter:** Optional, put whatever here

    .. tagscript::

        {/:Comment!}

        {Comment(Something):Comment!}
    """

    ACCEPTED_NAMES = ("/", "Comment", "comment")

    def process(self, ctx: Context) -> Optional[str]:
        """
        Check the count of a string
        """
        return ""
