import discord
from discord.ext import commands
import random
import json
import personal
import os

colour = personal.colour


def write_json(data, filename="data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


class Snipes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is running")

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        if ctx.channel.id != 697699660067897374 and ctx.guild.id != 772678294692429865:
            try:
                with open(f"s_{ctx.guild.id}.json", "r") as f:
                    data = json.load(f)
            except:
                with open(f"s_{ctx.guild.id}.json", "w") as f:
                    f.write('{"messages":[]}')
                    data = {"messages": []}
            try:
                print(ctx.attachments[0].url)
                attachments = []
                for x in ctx.attachments:
                    attachments.append(x.proxy_url)
            except:
                pass
            msg = ctx.content
            msg_id = str(ctx.id)
            guild_id = str(ctx.guild.id)
            channel_id = str(ctx.channel.id)
            user_id = str(ctx.author.id)
            time = ctx.created_at.strftime("%H:%M:%S, %A, %d/%B/%Y")
            try:
                data["messages"].append(
                    {
                        "msg_id": msg_id,
                        "guild_id": guild_id,
                        "channel_id": channel_id,
                        "user_id": user_id,
                        "attachments": attachments,
                        "time": time,
                        "msg": msg,
                    }
                )
            except:
                data["messages"].append(
                    {
                        "msg_id": msg_id,
                        "guild_id": guild_id,
                        "channel_id": channel_id,
                        "user_id": user_id,
                        "time": time,
                        "msg": msg,
                    }
                )

            with open(f"s_{ctx.guild.id}.json", "w") as f:
                json.dump(data, f, indent=2)
        else:
            if ctx.channel.id == 697699660067897374:
                try:
                    with open(f"s_homies_general.json", "r") as f:
                        data = json.load(f)
                except:
                    with open(f"s_homies_general.json", "w") as f:
                        f.write('{"messages":[]}')
                        data = {"messages": []}
                try:
                    print(ctx.attachments[0].url)
                    attachments = []
                    for x in ctx.attachments:
                        attachments.append(x.proxy_url)
                except:
                    pass
                msg = ctx.content
                msg_id = str(ctx.id)
                guild_id = str(ctx.guild.id)
                channel_id = str(ctx.channel.id)
                user_id = str(ctx.author.id)
                time = ctx.created_at.strftime("%H:%M:%S, %A, %d-%B-%Y")
                try:
                    data["messages"].append(
                        {
                            "msg_id": msg_id,
                            "guild_id": guild_id,
                            "channel_id": channel_id,
                            "user_id": user_id,
                            "attachments": attachments,
                            "time": time,
                            "msg": msg,
                        }
                    )
                except:
                    data["messages"].append(
                        {
                            "msg_id": msg_id,
                            "guild_id": guild_id,
                            "channel_id": channel_id,
                            "user_id": user_id,
                            "time": time,
                            "msg": msg,
                        }
                    )

                with open(f"s_homies_general.json", "w") as f:
                    json.dump(data, f, indent=2)
            if ctx.guild.id == 772678294692429865:
                try:
                    with open(f"s_10g.json", "r") as f:
                        data = json.load(f)
                except:
                    with open(f"s_10g.json", "w") as f:
                        f.write('{"messages":[]}')
                        data = {"messages": []}
                try:
                    print(ctx.attachments[0].url)
                    attachments = []
                    for x in ctx.attachments:
                        attachments.append(x.proxy_url)
                except:
                    pass
                msg = ctx.content
                msg_id = str(ctx.id)
                guild_id = str(ctx.guild.id)
                channel_id = str(ctx.channel.id)
                user_id = str(ctx.author.id)
                time = ctx.created_at.strftime("%H:%M:%S, %A, %d-%B-%Y")
                try:
                    data["messages"].append(
                        {
                            "msg_id": msg_id,
                            "guild_id": guild_id,
                            "channel_id": channel_id,
                            "user_id": user_id,
                            "attachments": attachments,
                            "time": time,
                            "msg": msg,
                        }
                    )
                except:
                    data["messages"].append(
                        {
                            "msg_id": msg_id,
                            "guild_id": guild_id,
                            "channel_id": channel_id,
                            "user_id": user_id,
                            "time": time,
                            "msg": msg,
                        }
                    )

                with open(f"s_10g.json", "w") as f:
                    json.dump(data, f, indent=2)

    @commands.command(aliases=["s"])
    async def snipe(self, ctx, number: int = 1):
        if number > 9:
            await ctx.send("Please specify a number smaller than or equal to 9")
        else:
            if (
                ctx.guild.id != 772678294692429865
                and ctx.channel.id != 697699660067897374
            ):
                with open(f"s_{ctx.guild.id}.json", "r") as f:
                    data = json.load(f)
                data = data["messages"]
                # print(data)
                # print(type(data))

                data.reverse()
                # print(data)
                embed = discord.Embed(title="Snipe")
                for i in range(number):
                    # print(type(data))
                    msg = data[i]["msg"]
                    msg_id = data[i]["msg_id"]
                    guild_id = data[i]["guild_id"]
                    channel_id = data[i]["channel_id"]
                    user_id, time = data[i]["user_id"], data[i]["time"]
                    user = self.client.get_user(int(user_id))
                    channel = self.client.get_channel(int(channel_id))
                    # print(user.name)
                    try:
                        attachments = data[i]["attachments"]
                        att = True
                    except:
                        att = False
                    # if i == 0: a = "One"
                    # if i == 1: a = "Two"
                    # if i == 2: a = "Three"
                    # if i == 3: a = "Four"
                    # if i == 4: a = "Five"
                    # if i == 5: a = "Six"
                    # if i == 6: a = "Seven"
                    # if i == 7: a = "Eight"
                    # if i == 8: a = "Nine"
                    link = (
                        f"https://discord.com/channels/{guild_id}/{channel_id}/{msg_id}"
                    )
                    if number == 1:
                        if att == False:
                            embed = discord.Embed(
                                title=f"Snipe",
                                description=f"{user.name} said\n```{msg}```in {channel} <a:dot:908591431445266452> {time} <a:dot:908591431445266452> [link]({link})",
                            )
                        if att == True:
                            embed = discord.Embed(
                                title=f"Snipe",
                                description=f"{user.name} said\n```{msg}```in {channel} <a:dot:908591431445266452> {time} <a:dot:908591431445266452> [link]({link})\n The user also sent {attachments}",
                            )
                    else:
                        if att == False:
                            embed.add_field(
                                name=f"Message {i+1}",
                                value=f"{user.name} said ```{msg}``` in {channel} <a:dot:908591431445266452> {time} <a:dot:908591431445266452> [link]({link})",
                                inline=False,
                            )
                        if att == True:
                            embed.add_field(
                                name=f"Message {i+1}",
                                value=f"{user.name} said ```{msg}``` in {channel} <a:dot:908591431445266452> {time} <a:dot:908591431445266452> [link]({link})\n The user also sent {attachments}",
                                inline=False,
                            )
                # todo if number == 1: #need to work on it later
                await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def delsnipe(self, ctx):
        if ctx.author.id == 497352662451224578:
            os.remove(f"s_{ctx.guild.id}.json")
        else:
            await ctx.send("Only my owner can use this command")


def setup(client):
    client.add_cog(Snipes(client))
