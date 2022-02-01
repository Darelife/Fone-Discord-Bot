import discord
import os
from discord.ext import commands
import pytz
import keep_alive
import random
import asyncio
import datetime
import requests
import personal as pm

# from PIL import Image
# import json
# import time
# import urllib
# import inspect
# import nltk
# from nltk.stem.lancaster import lancasterStemmer
# import numpy
# import tflearn
# import tensorflow
# import time
# from discord_components import Button, Select, SelectOption, ComponentsBot
# from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
# from discord.ext import tasks
# from discord import Webhook, RequestsWebhookAdapter
# from discord.ext.commands import BotMissingPermissions
# import math
# from datetime import datetime
# from pygicord import Paginator
# import re
# from bs4 import BeautifulSoup
# import operator
# from urllib.request import urlopen
# import urllib.request

ist = pytz.timezone("Asia/Calcutta")
today = datetime.datetime.now(ist)
print("Month:", today.month)
print("Day :", today.day)

intents = discord.Intents().all()
client = commands.Bot(
    command_prefix=["f", "F"],
    debug_guilds=[697493731611508737, 890890610339373106, 772678294692429865],
    intents=intents,
    allowed_mentions=discord.AllowedMentions(replied_user=False),
)
client.remove_command("help")


@client.event
async def on_ready():
    channel = client.get_channel(890989628188934196)
    await channel.send(
        "running through <https://replit.com/@darelife/clean-fone#main.py>"
    )
    print("ight..........lets start")


# To update the status
async def ch_pr():
    await client.wait_until_ready()
    while not client.is_closed():
        hmm = ["a song", f"{len(client.guilds)} servers", "fhelp", "You"]
        # nice = [await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name='a fucking song')), await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=f'{len(client.guilds)} servers')), await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="f.help")), await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="You", status=discord.Status.dnd))]
        # todo = random.choice(nice)

        # status = discord.Status.dnd
        # game = discord.ActivityType.listening(name = "with the API")
        # await client.change_presence(status=discord.Status.idle, activity=game, afk = False, shard_id = 2)

        status1 = random.choice(hmm)
        await client.change_presence(
            status=discord.Status.idle, activity=discord.Activity(type=2, name=status1)
        )
        await asyncio.sleep(300)


client.loop.create_task(ch_pr())

# to load the cogs in ./cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

# TO load a cog, it will load by default though because of the for loop above
@client.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id == 497352662451224578 or ctx.author.id == 629243339379834880:
        client.load_extension(f"cogs.{extension}")


# TO unload a cog
@client.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id == 497352662451224578 or ctx.author.id == 629243339379834880:
        client.unload_extension(f"cogs.{extension}")


pm.jsonsave(
    "https://api.exchangerate-api.com/v4/latest/USD", "us.json"
)  # it's for the currency command


# Ratelimit Check
r = requests.head(url="https://discord.com/api/v1")
try:
    print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
    print("No rate limit")

keep_alive.keep_alive()
token = os.environ.get("TOKEN")
client.run(token)
