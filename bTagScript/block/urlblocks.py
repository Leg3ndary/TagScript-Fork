from urllib.parse import unquote, unquote_plus, quote, quote_plus

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


class URLEncodeBlock(verb_required_block(True, payload=True)):
    """
    This block will encode a given string into a properly formatted url
    with non-url compliant characters replaced. Using ``+`` as the parameter
    will replace spaces with ``+`` rather than ``%20``.

    **Usage:** ``{urlencode(["+"]):<string>}``

    **Payload:** string

    **Parameter:** "+", None

    **Example:**

    .. tagscript::

        {urlencode:covid-19 sucks}
        covid-19%20sucks

        {urlencode(+):im stuck at home writing docs}
        im+stuck+at+home+writing+docs

        You can use this to search up blocks
        Eg if {args} is command block

        <https://btagscript.readthedocs.io/en/latest/search.html?q={urlencode(+):{args}}&check_keywords=yes&area=default>
        <https://btagscript.readthedocs.io/en/latest/search.html?q=command+block&check_keywords=yes&area=default>
    """

    ACCEPTED_NAMES = ("urlencode",)

    def process(self, ctx: Context):
        method = quote_plus if ctx.verb.parameter == "+" else quote
        return method(ctx.verb.payload)
