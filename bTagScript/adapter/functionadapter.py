from typing import Callable

from ..interface import Adapter
from ..verb import Verb


class FunctionAdapter(Adapter):
    """
    Function adapter...
    
    Would be cool to have functions in tagscript
    """

    __slots__ = ("fn",)

    def __init__(self, function_pointer: Callable[[], str]) -> None:
        """
        Construct the adapter
        """
        self.fn = function_pointer
        super().__init__()

    def __repr__(self) -> str:
        """
        String repr"""
        return f"<{type(self).__qualname__} fn={self.fn!r}>"

    def get_value(self, ctx: Verb) -> str:
        """
        Run the function and get the value
        """
        return str(self.fn())
