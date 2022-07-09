from typing import Optional

from ..interface import Block
from ..interpreter import Context


class CommentBlock(Block):
    """
    The comment block is literally just for comments, it will not be
    parsed, however it will be removed from your codes output.

    **Usage:** ``{comment([other]):[text]}``

    **Aliases:** /, Comment, comment, //

    **Payload:** ``text``

    **Parameter:** ``other``

    .. tagscript::

        {//:Comment!}

        {Comment(Something):Comment!}
    """

    ACCEPTED_NAMES = ("/", "Comment", "comment", "//")

    def process(self, ctx: Context) -> Optional[str]:
        """
        Remove the block
        """
        return ""
