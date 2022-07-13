from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..interpreter import Context


class Adapter:
    """
    The base class for TagScript adapters.

    Implementations must subclass this to create adapters.
    """

    def __repr__(self) -> str:
        """
        String repr
        """
        return f"<{type(self).__qualname__} at {hex(id(self))}>"

    def get_value(self, ctx: Context) -> Optional[str]:
        """
        Processes the adapter's actions for a given :class:`~bTagScript.interpreter.Context`.

        Subclasses must implement this.

        Parameters
        ----------
        ctx: Context
            The context object containing the TagScript :class:`~bTagScript.verb.Verb`.

        Returns
        -------
        Optional[str]
            The adapters's processed value.

        Raises
        ------
        NotImplementedError
            The subclass did not implement this required method.
        """
        raise NotImplementedError
