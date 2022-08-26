from typing import Optional

from ..interface import Block
from ..interpreter import Context
from ..verb import Verb


class DigitShorthandBlock(Block):
    """
    DigitShorthand Blocks are used to provide a shorthand for variables.
    This is usually used for arguments, so you can set {1} == {args(1)}
    {2} == {args(2)} etc.

    .. tagscript::

        Check the description.
    """

    def __init__(self, var_name: str) -> None:
        """
        Initialize the DigitShorthandBlock with the block you want to be digitted. If thats a word.
        """
        self.redirect_name = var_name

    def will_accept(self, ctx: Context) -> bool:  # pylint: disable=arguments-differ
        """
        Check if the declaration is a digit
        """
        return ctx.verb.declaration.isdigit()

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the digital shorthand
        """
        blank = Verb()
        blank.declaration = self.redirect_name
        blank.parameter = ctx.verb.declaration
        ctx.verb = blank
        return None
