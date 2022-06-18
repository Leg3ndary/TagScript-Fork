from urllib.parse import unquote, unquote_plus

from ..interface import verb_required_block
from ..interpreter import Context


class URLDecodeBlock(verb_required_block(True, payload=True)):
    """
    This block will decode a given url into a string
    with non-url compliant characters replaced. Using ``+`` as the parameter
    will replace spaces with ``+`` rather than ``%20``.

    **Usage:** ``{urldecode(["+"]):<string>}``

    **Payload:** string

    **Parameter:** "+", None

    **Examples:**

    .. tagscript::

        {urldecode:covid-19%20sucks}
        # covid-19 sucks

        {urldecode(+):im+stuck+at+home+writing+docs}
        # im stuck at home writing docs

    This block is just the reverse of the urlencode block
    """

    ACCEPTED_NAMES = ("urldecode",)

    def process(self, ctx: Context):
        method = unquote_plus if ctx.verb.parameter == "+" else unquote
        return method(ctx.verb.payload)
