from typing import Optional

from ..interface import Block
from ..interpreter import Context
from ..verb import Verb


class ShortCutRedirectBlock(Block):
    """
    The shortcut redirect block will redirect the verb to a different verb.
    """

    def __init__(self, var_name: str) -> None:
        """
        Shortcut redirect block
        """
        self.redirect_name = var_name

    def will_accept(self, ctx: Context) -> bool:  # pylint: disable=arguments-differ
        """
        Check if the declaration is a digit
        """
        return ctx.verb.declaration.isdigit()

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the shortcut redirect
        """
        blank = Verb()
        blank.declaration = self.redirect_name
        blank.parameter = ctx.verb.declaration
        ctx.verb = blank
        return None
