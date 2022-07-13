from typing import Optional

from ...interface import Block
from ...interpreter import Context


class OverrideBlock(Block):
    """
    Override a command's permission requirements. This can override
    mod, admin, or general user permission requirements when running commands
    with the :ref:`Command Block`. Passing no parameter will default to overriding
    all permissions.

    In order to add a tag with the override block, the tag author must have ``Manage
    Server`` permissions.

    This will not override bot owner commands or command checks.

    **Usage:** ``{override(["admin"|"mod"|"permissions"]):[command]}``

    **Aliases:** ``bypass``

    **Payload:** ``command``

    **Parameter:** ``"admin", "mod", "permissions"``

    **Examples:**

    .. tagscript::

        {override}
        overrides all commands and permissions

        {override(admin)}
        overrides commands that require the admin role

        {bypass(permissions)}
        {bypass(mod)}
        overrides commands that require the mod role or have user permission requirements
    """

    ACCEPTED_NAMES = ("override", "bypass")

    def process(self, ctx: Context) -> Optional[str]:
        """
        Process the block and update response.actions with correct overrides
        """
        param = ctx.verb.parameter
        if not param:
            ctx.response.actions["overrides"] = {"admin": True, "mod": True, "permissions": True}
            return ""

        param = param.strip().lower()
        if param not in ("admin", "mod", "permissions"):
            return None
        overrides = ctx.response.actions.get(
            "overrides", {"admin": False, "mod": False, "permissions": False}
        )
        overrides[param] = True
        ctx.response.actions["overrides"] = overrides
        return ""
