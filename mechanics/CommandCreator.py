import discord
from mechanics.prefix import Prefix


class CommandCreator(object):

    async def get_cmd_and_args(message: discord.Message, content):
        prefix = Prefix()
        pfx = await prefix.getPrefix()
        content = content[len(pfx):]
        cmd = content.split(" ")
        return cmd

