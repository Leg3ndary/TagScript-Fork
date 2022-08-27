from typing import Optional

from ...interface import verb_required_block
from ...interpreter import Context


class CommandBlock(verb_required_block(True, payload=True)):
    """
    Run a command as if the tag invoker had ran it. Only 3 command
    blocks can be used in a tag.

    **Usage:** ``{command:<command>}``

    **Aliases:** ``c, com, command``

    **Payload:** command

    **Parameter:** None

    **Examples:**

    .. tagscript::

        {c:ping}
        # Invokes ping command

        {c:ban {target(id)} Chatflood/spam}
        # Invokes ban command on the pinged user with the reason as "Chatflood/spam"
    """

    ACCEPTED_NAMES = ("c", "com", "command")

    def __init__(self, limit: int = 3) -> None:
        """
        Construct the command block.
        """
        self.limit = limit
        super().__init__()

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the block and update response.actions
        """
        command = ctx.verb.payload.strip()
        actions = ctx.response.actions.get("commands")
        if actions:
            if len(actions) >= self.limit:
                return f"<{ctx.verb.declaration} error: limit reached ({self.limit})>"
        else:
            ctx.response.actions["commands"] = []
        ctx.response.actions["commands"].append(command)
        return ""
