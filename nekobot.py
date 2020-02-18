import discord
from Commands.Commands import *
from mechanics.getToken import *
from mechanics.CommandCreator import CommandCreator
from mechanics.prefix import Prefix


class Bot(discord.Client):
    token = GetToken.get_token()

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('Bot Ready')

    async def on_message(self, message):
        if message.author == self.user:
            return
        prefix_class = Prefix()
        prefix = await prefix_class.getPrefix()
        if message.content.startswith(prefix):
            command = CommandCreator()
            cmd = await command.get_cmd_and_args(message.content)
            print('received command ' + cmd[0])
            try:
                commands = Commands()
                cmdcall = getattr(commands, cmd[0])
            except Exception as e:
                print('Command ' + cmd[0] + ' doesn\'t exists')
                return
            response = await cmdcall(self, message, cmd)
            await message.channel.send(embed=response)


bot = Bot()
bot.run(Bot.token)
