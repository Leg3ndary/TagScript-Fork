from typing import Optional

from ..interface import Block
from ..interpreter import Context


class DebugBlock(Block):
    """
    The debug block allows you to debug your tagscript quickly and easily,
    it will save the output to the debug_var key in the response dict.
    Separate the variables you want to include or exclude with a comma or
    a tilde.

    If no parameters are provided in addition to no payload, all variables
    will be included. If no parameters are provided and a payload is
    provided, it will assume you want to include those variables.

    **Usage:** ``{debug(["i", "include", "e", "exclude"]):<variables>}``

    **Aliases:** ``None``

    **Payload:** ``variables``

    **Parameter:** ``"i", "include", "e", "exclude"``

    .. note::

        {debug} is the same as {debug(exclude):}

        {debug:somevar~anothervar} is the same as {debug(include):somevar~anothervar}

    **Examples:**

    .. note::

            THIS SHOULD ALWAYS BE PLACED AT THE VERY BOTTOM, IT WILL NOT RETURN ANYTHING UNDER IT.

    .. tagscript::

        Assuming we have the following tagscript, we first set the var something, then set
        parsed (using the dollar sign method), to Hello|World, (assume we actually wanted just the Hello
        but we forgot)

        {=(something):Hello/World}
        {$parsed:{something(1)}}
        {if({parsed}==Hello):Hello|Bye}

        Running this would provided the output Bye, using the debug block below:
        {debug}
        We'll get all the variables at their, "final state"
        This will be provided in a dict, which you can further parse and output to your liking.

        EG, in YAML format:
        something: Hello/World
        parsed: Hello/World

        This allow's you to see that you forgot to parse with a delimiter which will lead to easy fixing.
    """

    ACCEPTED_NAMES = ("debug",)

    def process(self, ctx: Context) -> Optional[str]:  # pylint: disable=too-many-branches
        """
        Debug the tagscript!
        """
        debug = {}

        if ctx.verb.parameter:
            if ctx.verb.parameter in ("e", "exc", "exclude"):
                if ctx.verb.payload:
                    if "~" in ctx.verb.payload:
                        exclude = ctx.verb.payload.split("~")
                    else:
                        exclude = ctx.verb.payload.split(",")
                    for k, v in ctx.response.variables.items():
                        if k not in exclude:
                            debug[k] = v.get_value(ctx.verb)
                else:
                    return None

            elif ctx.verb.parameter in ("i", "inc", "include"):
                if ctx.verb.payload:
                    if "~" in ctx.verb.payload:
                        include = ctx.verb.payload.split("~")
                    else:
                        include = ctx.verb.payload.split(",")

                    for k, v in ctx.response.variables.items():
                        if k in include:
                            debug[k] = v.get_value(ctx.verb)
                else:
                    return None

        elif ctx.verb.payload:
            if "~" in ctx.verb.payload:
                include = ctx.verb.payload.split("~")
            else:
                include = ctx.verb.payload.split(",")

            for k, v in ctx.response.variables.items():
                if k in include:
                    debug[k] = v.get_value(ctx.verb)
        else:
            for k, v in ctx.response.variables.items():
                debug[k] = v.get_value(ctx.verb)
        ctx.response.extras["debug"] = debug
        return ""
