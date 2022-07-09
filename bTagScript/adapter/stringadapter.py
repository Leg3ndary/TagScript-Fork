from ..interface import Adapter
from ..utils import escape_content
from ..verb import Verb


class StringAdapter(Adapter):
    """
    String adapter, allows blocks to be parsed, used basically only for variables
    """

    __slots__ = ("string", "escape_content")

    def __init__(self, string: str, *, escape: bool = False) -> None:
        """
        Construction for string adapter
        """
        self.string: str = str(string)
        self.escape_content = escape

    def __repr__(self) -> str:
        """
        String repr
        """
        return f"<{type(self).__qualname__} string={repr(self.string)}>"

    def get_value(self, ctx: Verb) -> str:
        """
        Get the value given the verb
        """
        self.return_value(self.handle_ctx(ctx))

    def handle_ctx(self, ctx: Verb) -> str:
        """
        Transform any parsing data the block may have
        """
        if ctx.parameter is None:
            return self.string

        try:
            splitter = " " if ctx.payload is None else ctx.payload
            if ctx.parameter.isdigit():
                index = int(ctx.parameter) - 1
                return self.string.split(splitter)[index]

            elif ctx.parameter.startswith("-") and ctx.parameter.split("-", 1)[-1].isdigit():
                index = int(ctx.parameter)
                return self.string.split(splitter)[index]

            else:
                index = (
                    int(ctx.parameter.replace("+", "")) - 1
                    if int(ctx.parameter.replace("+", "")) > 0
                    else int(ctx.parameter.replace("+", ""))
                )
                splitter = " " if ctx.payload is None else ctx.payload
                if ctx.parameter.startswith("+"):
                    return splitter.join(self.string.split(splitter)[: index + 1])
                elif ctx.parameter.endswith("+"):
                    return splitter.join(self.string.split(splitter)[index:])
                else:
                    return self.string.split(splitter)[index]
        except: #pylint: disable=bare-except
            return self.string

    def return_value(self, string: str) -> str:
        """
        Return the value, escaped
        """
        return escape_content(string) if self.escape_content else string
