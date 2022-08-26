import re
from inspect import isawaitable
from typing import Any, Awaitable, Callable, Union

__all__ = ("escape_content", "maybe_await")

pattern = re.compile(r"(?<!\\)([{():|}])")


def _sub_match(match: re.Match) -> str:
    """
    Check if the character has a \ in front of it

    Parameters
    ----------
    match: re.Match
        The match object.

    Returns
    -------
    str
        The escaped character.
    """
    return "\\" + match.group(1)


def escape_content(string: str) -> str:
    """
    Escapes given input to avoid tampering with engine/block behavior.

    Parameters
    ----------
    string: str
        The string to escape.

    Returns
    -------
    str
        The escaped content.
    """
    if string is None:
        return
    return pattern.sub(_sub_match, string)


async def maybe_await(func: Union[Callable[..., Any], Awaitable[Any]], *args, **kwargs) -> Any:
    """
    Await the given function if it is awaitable or call it synchronously.

    Parameters
    ----------
    func: Union[Callable[..., Any], Awaitable[Any]]
        The function callable to call.
    *args: Any
        The arguments to pass to the function.
    **kwargs: Any
        The keyword arguments to pass to the function.

    Returns
    -------
    Any
        The result of the awaitable function.
    """
    value = func(*args, **kwargs)
    return await value if isawaitable(value) else value
