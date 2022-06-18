from discord import Guild
from re import match

from ..adapter import discordadapters
from ..interface import verb_required_block
from ..interpreter import Context\


"""
I have to rethink this later"""


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

        {request(user):user|360061101477724170}
        _Leg3ndary#5759
    """

    ACCEPTED_NAMES = ("request", "getdiscord")

    def __init__(self, guild: Guild, limit: int = 3, allow_fetch: bool = True) -> None:
        """
        You need access to a guild object from dpy for this to work.


        ``limit`` is how many blocks are allowed to be used in a single tag
        
        ``allow_fetch`` tells us whether we're allowed to fetch users, or use cache only.

        If set to ``False``, and you're cache is disabled, this block is essentially useless.
        """
        super().__init__()
        self.guild = guild
        self.limit = limit
        self.allow_fetch = allow_fetch

    async def process(self, ctx: Context):
        if "|" not in ctx.verb.payload:
            return f"`YOU DON'T SEEM TO HAVE A PIPE (|)`"
        _type = ctx.verb.payload.split("|")[0].lower()
        query = ctx.verb.payload.split("|")[1]

        if query.isdigit and match("[0-9]{15,19}", query):

            actions = ctx.response.actions.get("request")
            
            if actions:
                if len(actions) > self.limit:
                    return f"`REQUEST LIMIT REACHED ({self.limit})`"
            
            else:
                actions = []
            
            if _type == "channel":
                channel = self.guild.get_channel(int(query)) or (await self.guild.fetch_channel(int(query)))
                if channel:
                    channel = discordadapters.ChannelAdapter(channel)
                else:
                    return f"Channel `{query}` not found"
                    
            elif _type =="user":
                user = self.guild.get_member(int(query)) or (await self.guild.fetch_member(int(query)))
                if user:
                    user = discordadapters.MemberAdapter()
                else:
                    return f"User `{query}` not found"
            else:
                return f"Type {_type} not found"

            ctx.response.actions["request"] = actions.append(f"{_type}:{query}")
