from urllib.parse import quote, quote_plus

from ..interface import verb_required_block
from ..interpreter import Context


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
