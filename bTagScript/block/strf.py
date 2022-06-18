from datetime import datetime, timezone
from typing import Optional

from ..interface import Block
from ..interpreter import Context


class StrfBlock(Block):
    """
    The strf block converts and formats timestamps based on `strftime formatting spec <https://strftime.org/>`_.
    Two types of timestamps are supported: ISO and epoch.
    If a timestamp isn't passed, the current UTC time is used.

    Invoking this block with `unix` will return the current Unix timestamp.

    **Usage:** ``{strf([timestamp]):<format>}``

    **Aliases:** ``unix``

    **Payload:** format, None

    **Parameter:** timestamp

    **Example:** ::

        {strf:%Y-%m-%d}
        # 2021-07-11

        {strf({user(timestamp)}):%c}
        # Fri Jun 29 21:10:28 2018

        {strf(1420070400):%A %d, %B %Y}
        # Thursday 01, January 2015

        {strf(2019-10-09T01:45:00.805000):%H:%M %d-%B-%Y}
        # 01:45 09-October-2019

        {unix}
        # 1629182008
    """

    ACCEPTED_NAMES = ("strf", "unix")

    def process(self, ctx: Context) -> Optional[str]:
        if ctx.verb.declaration.lower() == "unix":
            return str(int(datetime.now(timezone.utc).timestamp()))
        if not ctx.verb.payload:
            return None
        if ctx.verb.parameter:
            if ctx.verb.parameter.isdigit():
                try:
                    t = datetime.fromtimestamp(int(ctx.verb.parameter))
                except:
                    return
            else:
                try:
                    t = datetime.fromisoformat(ctx.verb.parameter)
                    # converts datetime.__str__ to datetime
                except ValueError:
                    return
        else:
            t = datetime.now()
        if not t.tzinfo:
            t = t.replace(tzinfo=timezone.utc)
        return t.strftime(ctx.verb.payload)
