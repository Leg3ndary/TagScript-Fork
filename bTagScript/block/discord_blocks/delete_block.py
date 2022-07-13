from typing import Optional

from ...interface import Block
from ...interpreter import Context
from .. import helper_parse_if


class DeleteBlock(Block):
    """
    The delete block will delete the message if the condition provided in
    the parameter is met, or if just the block is added, the message will
    be deleted. Only one delete block will be processed, the rest,
    removed, but ignored.

    .. note::

        This block will only set the actions "delete" key to True/False.
        You must set the behaviour manually.

    **Usage:** ``{delete(<expression>)}``

    **Aliases:** ``del``

    **Payload:** ``None``

    **Parameter:** ``expression``

    .. tagscript::

        {delete}
        {del(true==true)}
    """

    ACCEPTED_NAMES = ("delete", "del")

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the delete
        """
        if "delete" in ctx.response.actions.keys():
            return ""
        if ctx.verb.parameter is None:
            value = True
        else:
            value = helper_parse_if(ctx.verb.parameter)
        ctx.response.actions["delete"] = value
        return ""
