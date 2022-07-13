from typing import Optional

from ...interface import verb_required_block
from ...interpreter import Context


class ReactBlock(verb_required_block(True, payload=True)):
    """
    The react block will set the actions "react" key to a list of reactions.

    .. note::

        You must set the behaviour manually.

    **Usage:** ``{react:<emojis>}``

    **Aliases:** ``None``

    **Payload:** ``emojis``

    **Parameter:** ``None``

    .. tagscript::

        {react:💩}
        {react:💩,:)}
        {react:💩~:)~:D}
    """

    ACCEPTED_NAMES = ("react",)

    def __init__(self, limit: int = 5) -> None:
        """
        Initialize the block

        Limit is the maximum number of reactions the block will add
        """
        self.limit = limit
        super().__init__()

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the reactions
        """
        return ""
