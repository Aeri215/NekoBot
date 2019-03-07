import discord
import yaml
import os
import requests
import re

from shutil import copy
from mechanics.prefix import Prefix
from mechanics.utils import Utils
from random import randint


client = discord.Client()


class Commands(object):
    async def hello(self, message , cmd):
        response = discord.Embed(title=f'Hello {message.author}')
        return response

    async def help(self, message, cmd):
        p = Prefix()
        prefix = await p.getPrefix()
        response = discord.Embed(title=f'NekoBot, the bot')
        cmd_list = f'Current prefix is :  **{prefix}** \r'
        cmd_list += 'help : display this list\r'
        cmd_list += 'hello : the bot greets you\r'
        cmd_list += 'setprefix: change the prefix\r'
        cmd_list += 'info : show info about you or someone else\r'
        cmd_list += 'convert: Convert a number to it\'s short scale\r'
        cmd_list += 'mine: work hard and get money\r'
        cmd_list += 'shop: upgrade your stuff yo get more money\r'
        cmd_list += 'calc: Determine your number\r'
        cmd_list += 'stream: check if given streamer is currently streaming'
        response.add_field(name='List of all commands', value=cmd_list)
        return response

    async def info(self, message, cmd):
        if message.mentions:
            target = message.mentions[0]
        else:
            target = message.author
        response = discord.Embed(color=target.color)
        response.set_author(name=f"{target.display_name}'s profile", icon_url=target.avatar_url)
        info = f"Your id : {target.id}\r"
        info += f"Is a bot : {'Yes' if target.bot else 'No'}"
        response.add_field(name="Infrmations", value=info)

        return response

    async def setprefix(self, message, cmd):
        if int(message.author.id) == 146009771743379457:
            prefix = Prefix()
            prefix = await prefix.setPrefix(cmd[0])
            response = discord.Embed(title='New prefix', description=f'Prefix has been changed to {prefix}')
            return response
        else:
            print(message.author.id)
            response = discord.Embed(title='Owner only', description=f'I can\'t let you do that')
            return response

    async def convert(self, message, cmd):
        data = [
            "Million",
            "Billion",
            "Trillion",
            "Quadrillion",
            "Quintillion",
            "Sextillion",
            "Septillion",
            "Octillion",
            "Nonillion",
        ]
        data2 = [
            "",
            "Un",
            "Duo",
            "Tre",
            "Quattuor",
            "Quin",
            "Sex",
            "Septen",
            "Octo",
            "Nonin"
        ]
        data3 = [
            "Decillion",
            "Vigintillion",
            "Trigintillion",
            "quadragintillion",
            "quinquagintillion",
            "sexagintillion",
            "septuagintillion",
            "octogintillion",
            "nonagintillion",
            "centillion"
        ]

        number = await Utils.clean_number(cmd[0])
        nbrofnbr = len(number)
        if nbrofnbr%3 == 0:
            step = nbrofnbr//3
        else:
            step = nbrofnbr//3 + 1
        firstnumber = number
        while len(number) > 3:
            number = number[:-3]
        response = discord.Embed(title='Convert tool')
        if len(firstnumber) > 10:
            firstnumber = f"{firstnumber[:15]}..."
        if step < 3:
            result = f"{firstnumber}"
        elif step > 11:
            step += 1
            decade = (step//10) - 1
            unit = (step % 10) - 3
            result = f"{number} {data2[unit]}{data3[decade]}"
        else:
            stepnbr = data[step-3]
            result = f"{number} {stepnbr}"
        response.add_field(name="input", value=firstnumber)
        response.add_field(name="result", value=result)
        return response

    async def stats(self, message, cmd):

        with open(f"users/{str(message.author.id)}.yaml", 'r') as stream:
            stats = yaml.load(stream)
        response = discord.Embed(title="Your stats")
        response.add_field(name="Money", value=f"{stats['money']} $")
        response.add_field(name="Strength", value=stats["stats"]["strength"])
        response.add_field(name="Pickaxe", value=stats["stats"]["pickaxe"])
        response.add_field(name="Refinery", value=stats["stats"]["refinery"])
        response.add_field(name="Market expertise", value=stats["stats"]["market_expertise"])
        response.add_field(name="Luck", value=f"{stats['stats']['luck']}%")
        return response

    async def mine(self, message, cmd):
        if os.path.isfile(f'./users/{str(message.author.id)}.yaml'):
            with open(f"users/{str(message.author.id)}.yaml", 'r') as stream:
                stats = yaml.load(stream)
            response = discord.Embed(title="You worked hard")
            count = stats["stats"]["strength"]
            text = f"You slammed {count} time (strength level {stats['stats']['strength']})\r"
            count *= stats["stats"]["pickaxe"]
            text += f"You got {count} rocks (pickaxe level {stats['stats']['pickaxe']})\r"
            count *= stats["stats"]["refinery"]
            text += f"You got {count} gold ore (refinery level {stats['stats']['refinery']})\r"
            count *= stats["stats"]["market_expertise"]
            if randint(0, 100 ) < stats["stats"]["luck"]:
                count *= 2
                text += f"You got lucky, you sold it for {count} dollars (market expertise level{stats['stats']['market_expertise']}))\r"
            else:
                text += f"You sold it for {count} dollars (market expertise level {stats['stats']['market_expertise']})\r"
            stats["money"] += count
            text += f"You have now {stats['money']} dollars"
            with open("users/" + str(message.author.id) + ".yaml", "w") as outfile:
                yaml.dump(stats, outfile, default_flow_style=False)
            response.add_field(name="Here's what you got", value=text)
            return response
        else:
            copy("tatic/Idle/baseStats.yaml", "users")
            os.rename("users/stats.yaml", f"users/{str(message.author.id)}.yaml")
            response = discord.Embed(title="Congratulations", description="You started your adventure")
            return response

    async def shop(self, message, cmd):
        with open(f"users/{str(message.author.id)}.yaml", 'r') as stream:
            stats = yaml.load(stream)
        try:
            choice = cmd[0].lower()
            if choice == "luck":
                if stats["money"] - pow(2, stats["stats"]["luck"]) >= 0:
                    stats["money"] -= pow(2, stats["stats"]["luck"])
                    stats["stats"][choice] += 1
                else:
                    response = discord.Embed(title="Upgrade failed", description="You can't afford it")
                    return response

            else:
                if stats["money"] - pow(10, stats["stats"][choice]) >= 0:
                    stats["money"] -= pow(10, stats["stats"][choice])
                    stats["stats"][choice] += 1
                else:
                    response = discord.Embed(title="Upgrade failed", description="You can't afford it")
                    return response
            with open("users/" + str(message.author.id) + ".yaml", "w") as outfile:
                yaml.dump(stats, outfile, default_flow_style=False)
            response = discord.Embed(title="Upgrade done", description=f"{choice} upgraded")
            return response
        except:
            response = discord.Embed(title="Shop")
            response.add_field(name="Money", value=f"{stats['money']}$")
            response.add_field(name="Strength", value=pow(10, stats["stats"]["strength"]))
            response.add_field(name="Pickaxe", value=pow(10, stats["stats"]["pickaxe"]))
            response.add_field(name="Refinery", value=pow(10, stats["stats"]["refinery"]))
            response.add_field(name="Market expertise", value=pow(10, stats["stats"]["market_expertise"]))
            response.add_field(name="Luck", value=pow(2, stats["stats"]["luck"]))
            response.add_field(name="How To buy", value="Use \'shop\' with the name of the upgrade you want to buy it")
        return response

    async def calc(self, message, cmd):
        if message.mentions:
            target = message.mentions[0]
        else:
            target = message.author
        init = str(target.id)
        nbr1 = init[1]
        nbr2 = init[3]
        nbr3 = init[5]
        result = (int(nbr1) + int(nbr2) + int(nbr3)) * 100 // 27
        if target.id == str(146009771743379457):  # it's me
            result = 100
        response = discord.Embed(title=f"You are {result}%", color=target.color)
        response.set_author(name=target.display_name, icon_url=target.avatar_url)
        return response

    async def stream(self, message, cmd):
        try:
            streamer = cmd[0].lower()
            stream = requests.get(f"https://api.twitch.tv/kraken/streams/{streamer}?client_id=89e2ba6q47mxe2m5bvw1k8nyjn9t1x")
            stream = stream.json()
            if stream["stream"] == None:
                response = discord.Embed(title=f"{cmd[0]} is not streaming, or doesn't exist")
            else:
                channel = stream["stream"]["channel"]
                response = discord.Embed(title=f'{channel["status"]}', url=channel["url"])
                response.set_author(name=channel["name"], icon_url=channel["logo"])
                response.set_thumbnail(url=channel["logo"])
                response.set_image(url=stream["stream"]["preview"]["large"])
        except Exception as e:
            print(e)
            response = discord.Embed(title="No argument given")
        return response

    async def ping(self, message, cmd):
        response = discord.Embed(title="Pong")
        return response

    async def keepnbr(self, message, cmd):
        try:
            result = await Utils.clean_number(cmd[0])
            response = discord.Embed(title=result)
            print(result)
        except Exception as e:
            print(e)
            response = discord.Embed(title="error")
        return response

    async def addstr(self, message, cmd):
        try:
            newcmd = ""
            for i in cmd:
                newcmd += i
            newcmd = await Utils.clean_number(newcmd)
            print(newcmd)
            result = re.search(r"(\d*)+(\d*)", newcmd)
            print(result)
            print(result.group(0))
            print(result.group(1))
            print(result.group(2))
            print(result.groups())
            response = discord.Embed(title="ok")
        except Exception as e:
            print(e)
            response = discord.Embed(title="error")
        return response