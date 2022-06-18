import asyncio
from typing import Union

from discord import Guild
from re import match

from ..adapter import discordadapters
from ..interface import verb_required_block
from ..interpreter import Context


class GetDiscord(verb_required_block(True, payload=True, parameter=True)):
    """
    This block allows users to get or fetch discord objects such as users, channels, etc.

    This will set the target block with new attributes


    **Usage:** ``{request(["Any Target attribute"]):<string>}``

    **Payload:** request_type|query

    Request type can be any of the following: "channel", "user", query is just what you're searching for

    **Parameter:** "channel", "user"

    **Example:**
    
    .. tagscript::

        {request(user):_Leg3ndary#5759}
        covid-19%20sucks

        {urlencode(+):im stuck at home writing docs}
        im+stuck+at+home+writing+docs

        You can use this to search up blocks
        Eg if {args} is command block

        <https://btagscript.readthedocs.io/en/latest/search.html?q={urlencode(+):{args}}&check_keywords=yes&area=default>
        <https://btagscript.readthedocs.io/en/latest/search.html?q=command+block&check_keywords=yes&area=default>
    """

    ACCEPTED_NAMES = ("request", "getdiscord")

    def __init__(self, guild: Guild, loop: asyncio.AbstractEventLoop, limit: int = 3, allow_fetch: bool = True) -> None:
        """
        You need access to a guild object from dpy.


        ``limit`` is how many blocks are allowed to be used in a single tag
        
        ``allow_fetch`` tells us whether we're allowed to fetch users, or use cache only.

        If set to ``False``, and you're cache is disabled, this block is essentially useless.
        """
        super().__init__()
        self.loop = loop  
        self.guild = guild
        self.limit = limit
        self.allow_fetch = allow_fetch

    def process(self, ctx: Context):
        _type = ctx.verb.payload.split("|")[0].lower()
        query = ctx.verb.payload.split("|")[1]

        if query.isdigit and match("[0-9]{15,19}", query):

            actions = ctx.response.actions.get("request")
            
            if actions:
                if len(actions) > self.limit:
                    return f"`REQUEST LIMIT REACHED ({self.limit})`"
            
            if _type == "channel":
                channel = self.guild.get_channel(int(query)) or self.client.loop.run_in_executor(None, self.client.fetch_channel, int(query))
                if channel:
                    channel = discordadapters.ChannelAdapter(channel)
                else:
                    pass
            elif _type =="user":
                user = self.client.get_user(int(query)) or self.client.loop.run_in_executor(None, self.client.get_mem, int(query))
                if user:
                    user = discordadapters.MemberAdapter

            else:
                ""

            return ""
