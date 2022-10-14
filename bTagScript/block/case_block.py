from typing import Optional

from ..interface import verb_required_block
from ..interpreter import Context


class UpperBlock(verb_required_block(True, payload=True)):
    """
    The Upper block will do exactly as it and will make the payload uppercase. The
    block alone will not do anything.

    **Usage:** ``{upper:<string>}``

    **Aliases:** ``upper``

    **Payload:** ``string``

    **Parameter:** ``None``

    **Examples:**

    .. tagscript::

        {upper:I love strawberries!} -> I LOVE STRAWBERRIES!
    """

    ACCEPTED_NAMES = "upper"

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the block and break the tag.
        """
        return ctx.verb.payload.upper()


class LowerBlock(verb_required_block(True, payload=True)):
    """
    The Lower block will make the payload lowercase. The block alone will
    not do anything.

    **Usage:** ``{lower:<string>}``

    **Aliases:** ``lower``

    **Payload:** ``string``

    **Parameter:** ``None``

    **Examples:**

    .. tagscript::

        {lower:I LOVE STRAWBERRIES!} -> i love strawberries!
    """

    ACCEPTED_NAMES = "lower"

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the block and break the tag.
        """
        return ctx.verb.payload.lower()
