from inspect import ismethod

from ..interface import Adapter
from ..verb import Verb


class SafeObjectAdapter(Adapter):
    """
    For objects
    """
    __slots__ = ("object",)

    def __init__(self, base) -> None:
        """
        Construct the safe object adapter.
        """
        self.object = base

    def __repr__(self) -> str:
        """
        String repr"""
        return f"<{type(self).__qualname__} object={repr(self.object)}>"

    def get_value(self, ctx: Verb) -> str:
        """
        Get the value safely
        """
        if ctx.parameter is None:
            return str(self.object)
        if ctx.parameter.startswith("_") or "." in ctx.parameter:
            return
        try:
            attribute = getattr(self.object, ctx.parameter)
        except AttributeError:
            return
        if ismethod(attribute):
            return
        if isinstance(attribute, float):
            attribute = int(attribute)
        return str(attribute)
