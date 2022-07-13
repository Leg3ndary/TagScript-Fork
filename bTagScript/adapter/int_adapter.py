from ..interface import Adapter
from ..verb import Verb


class IntAdapter(Adapter):
    """
    IntAdapter, so far no use for this?
    """

    __slots__ = ("integer",)

    def __init__(self, integer: int) -> None:
        """
        Construct the int adapter
        """
        self.integer: int = int(integer)

    def __repr__(self) -> str:
        """
        String repr
        """
        return f"<{type(self).__qualname__} integer={repr(self.integer)}>"

    def get_value(self, ctx: Verb) -> str:
        """
        Get the value of the int into string, not sure why this even exists
        """
        return str(self.integer)
