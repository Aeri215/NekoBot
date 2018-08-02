from Commands import *
from prefix import Prefix
from CommandCreator import CommandCreator
from getToken import *

TOKEN = GetToken.get_token()

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    prefix = Prefix()
    current_prefix = await prefix.getPrefix()
    if message.content.startswith(current_prefix):
        command = CommandCreator()
        commands = Commands()
        cmd = await command.get_cmd_and_args(message.content)
        print('received command ' + cmd[0])
        try:
            cmdcall = getattr(commands, cmd[0])
        except Exception as e:
            print('Command ' + cmd[0] + ' doesn\'t exists')
            return
        del cmd[0]
        response = await cmdcall(message, cmd)
        await send_message(message, response)


async def send_message(message, response):
    await client.send_message(message.channel, embed=response)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('Bot Ready')

client.run(TOKEN)
