import discord
from discord.ext import commands


class classname(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is running")


def setup(client):
    client.add_cog(classname(client))
