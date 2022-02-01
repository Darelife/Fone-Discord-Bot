import discord
from discord.ext import commands
import time
import os
import asyncio
import random
import personal

colour = personal.colour
update_latest_time = 0  # required for the global variable in the update event. It can probably be improved, but yeah it's just there, and i don't want to look into it rn

# the 2 lists below are for are for the bot to react to sad messages :(, i really need to do the same thing for message which express happiness
sad = [
    "sad",
    "depressed",
    "sadge ",
    "bad",
    "boring",
    "lost",
    "depressing",
    "depress",
    "cry",
    "cries",
    "crying",
    ":(",
    "hard",
    "bored",
]
sadreactions = [
    "<:pepecries:837507320270815252>",
    "<:pepecrying:837507321570918400>",
    "<:pepesad:837508592155754526>",
    "<:pepesadge:837508114646564914>",
    "<:depressed:837507320731664414>",
    "<:owosadness:837507322783727659>",
]


class dontghostpingus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is running")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # print(message.mentions)
        for x in message.mentions:
            if message.author.id != x.id:
                pingeduser = x.id
                user = self.client.get_user(pingeduser)
                embed = discord.Embed(
                    title="Ping",
                    description=(
                        f"""||<@!{message.author.id}>|| aka {message.author.display_name} pinged you in {message.channel} in the {message.guild} server"""
                    ),
                )
                embed.add_field(
                    name="LINK",
                    value=(
                        f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
                    ),
                )
                embed.add_field(name="message", value=f"{message.content}")
                await user.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        global update_latest_time
        # print(dir(before))

        update_latest_time1 = int(time.strftime("%H%M%S"))
        if update_latest_time - update_latest_time1 == 0:
            pass
        else:
            update_latest_time = update_latest_time1

            if (before.bot) != True:
                if before.nick != after.nick:
                    data = f"{before} just changed his/her status from {before.nick} to {after.nick}\n"
                    with open("nick_member_update.txt", "a") as f:
                        f.write(data)
                    channel = self.client.get_channel(920683139674800209)
                    await channel.send(data)
                if before.activity != after.activity:
                    data = f"{before} just changed his/her status from {before.activity} to {after.activity}\n"
                    if after.activity != None and after.activity.name == "Spotify":
                        pass
                    else:
                        with open("activity_member_update.txt", "a") as f:
                            f.write(data)
                        channel = self.client.get_channel(920683334231793774)
                        await channel.send(data)
                if before.status != after.status and before.id != 629243339379834880:
                    data = f"{before} just changed his/her status from {before.status} to {after.status}\n"
                    with open("status_member_update.txt", "a") as f:
                        f.write(data)
                    channel = self.client.get_channel(920683012746776606)
                    await channel.send(data)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            channel = self.client.get_channel(890901800394301452)
            command = ctx.invoked_with
            await channel.send(
                f"{command}```{error}```<@!{ctx.author.id}> - {ctx.author} in <#{ctx.channel.id}>"
            )
            print(
                f"{command}```{error}```<@!{ctx.author.id}> - {ctx.author} in <#{ctx.channel.id}>"
            )

    @commands.Cog.listener()
    async def on_message(self, ctx):
        # Dank memer React to memes to save them
        if ctx.channel.id == 765811477998469120 and ctx.author.id == 270904126974590976:
            embed_footer = ctx.embeds[0].footer
            if (str(embed_footer)[17:]).startswith("👍"):
                channel = self.self.client.get_channel(797456725770371105)  # change
                await ctx.add_reaction("<:Upvote:724918642092933140>")
                global reaction_user
                webhooks = await channel.webhooks()
                print(1)

                def check(reaction, user):
                    global reaction_user
                    reaction_user = user
                    return reaction.message.id == ctx.id and user != self.client.user

                def confirm(reaction, user):
                    return reaction.message.id == ctx.id and user != self.client.user

                while True:
                    try:

                        webhookToken = os.environ["webhook_url_saved_memes"]
                        print(2)
                        reaction, user = await self.client.wait_for(
                            "reaction_add", timeout=360.0, check=check
                        )
                        if reaction.emoji.id == 724918642092933140:
                            try:
                                await ctx.add_reaction("<:AYes:765142287902441492>")
                                reaction2, user2 = await self.client.wait_for(
                                    "reaction_add", timeout=10.0, check=confirm
                                )

                                if reaction2.emoji.id == 765142287902441492:
                                    await ctx.remove_reaction(
                                        "<:AYes:765142287902441492>", reaction_user
                                    )
                                    await ctx.remove_reaction(
                                        "<:AYes:765142287902441492>", self.client.user
                                    )
                                    # await ctx.channel.send("test")
                                    webhook = discord.Webhook.partial(
                                        id=927439881200861216,
                                        token=webhookToken,
                                        adapter=discord.RequestsWebhookAdapter(),
                                    )
                                    # webhook = Webhook.from_url(f"https://discord.com/api/webhooks/927439881200861216/{webhookToken}", adapter=RequestsWebhookAdapter())  #change
                                    webhook.send(
                                        username=reaction_user.name,
                                        avatar_url=reaction_user.avatar.url,
                                        embed=ctx.embeds[0],
                                    )

                                    # await channel.send(embed = ctx.embeds[0])
                                    await ctx.remove_reaction(
                                        "<:Upvote:724918642092933140>", reaction_user
                                    )
                            except asyncio.TimeoutError:
                                await ctx.remove_reaction(
                                    "<:AYes:765142287902441492> ", self.client.user
                                )
                    except asyncio.TimeoutError:
                        await ctx.remove_reaction(
                            "<:Upvote:724918642092933140>", self.client.user
                        )
                        break

        # To Respond To DM's
        try:
            a = ctx.channel.name
        except:
            channel = self.client.get_channel(769789003230216215)
            try:
                embed = ctx.embeds[0]
                await channel.send(
                    f"""{ctx.content} 
                    ~ {ctx.author.name}#{ctx.author.discriminator} aka <@!{ctx.author.id}>""",
                    embed=embed,
                )
            except:
                await channel.send(
                    f"""{ctx.content} 
                    ~ {ctx.author.name}#{ctx.author.discriminator} aka <@!{ctx.author.id}>"""
                )

        # To respond to Sad Messages
        if random.randint(0, 10) <= 1:
            if " " in ctx.content:
                for x in sad:
                    x = f" {x} "
                    if x in ctx.content:
                        print(x)
                        em = random.choice(sadreactions)
                        await ctx.add_reaction(em)
                        await asyncio.sleep(20)
                        await ctx.remove_reaction(em, self.client.user)
                        break
            else:
                for x in sad:
                    if x in ctx.content:
                        if x == ctx.content:
                            print(x)
                            em = random.choice(sadreactions)
                            await ctx.add_reaction(em)
                            await asyncio.sleep(20)
                            await ctx.remove_reaction(em, self.client.user)
                            break

        # Responding with an upvote and downvote to youtube links in a particular channel for people to rate it
        if ctx.channel.id == 833206532719247361:
            if "https://youtu" in ctx.content or "https://www.youtu" in ctx.content:
                await ctx.add_reaction("⬆️")
                await ctx.add_reaction("⬇️")

        # Krunker
        if ctx.content.startswith("https://krunker.io/?game"):
            await ctx.delete()
            linkchar = []
            x = 0
            while x < 34:
                linkchar.append(ctx.content[x])
                x += 1
            link = "".join([str(element) for element in linkchar])
            embed = discord.Embed(
                title="My Krunker Game's Link",
                description=f"""[`Click Here To Join The Game`]({link})
    ```Game Id : {link[29:]}```""",
                timestamp=ctx.created_at,
                color=random.choice(colour),
            )
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(
                url="https://mir-s3-cdn-cf.behance.net/projects/404/a09146108307929.Y3JvcCwxMzgwLDEwODAsMjcwLDA.png"
            )
            embed.set_footer(text="Enjoy Your Game")
            text = f"```{ctx.content}```"
            if ctx.content != link:
                await ctx.channel.send(text, embed=embed)
            else:
                await ctx.channel.send(embed=embed)

        # For the afk command
        if ("<@") in ctx.content:
            try:
                message1 = f" {ctx.content}"
                woah = list(message1.split("<"))
                woah.pop(0)
                noice = "".join([str(element) for element in woah])
                yes = list(noice.split(">"))
                fnu4jfn = yes[0]
                noice1 = "".join([str(element) for element in fnu4jfn])
                a = list(noice1.split("!"))
                a.pop(0)
                hmm = a[0]
                okay = hmm[:-1]
                ye = "".join([str(element) for element in okay])
                fh = open("afk_users_list.txt")
                filter_object = filter(lambda a: (ye) in a, fh)

                for line in filter_object:
                    c = list(line)
                    p = "".join([str(element) for element in c])
                    a = []
                    x = 0
                    for c in p:
                        while x < 18:
                            a.append(p[x])
                            x += 1
                    de = "".join([str(element) for element in a])
                    use = self.client.get_user(int(de))
                    await ctx.reply(f"{use.name} is {p[22:]}")
            except:
                pass
            # damn = open('afk_users_list.txt')
            # afk_list = damn.readlines()
            # for i in afk_list:
            # i1 = list(i)
            # woah1 = i1[:-1]
            # woah1 = ''.join([str(element) for element in woah1])
            # if (ye) in woah1:
            # if (ye) in woah1:
            # await ctx.channel.send('He is AFK rn...Please try later.')
        member = ctx.author.id
        with open("afk_users_list.txt", "r") as h:
            afk_list = h.readlines()
            for i in afk_list:
                if str(member) in i:
                    afk_list.remove(i)
                    with open("afk_users_list.txt", "w") as s:
                        for y in afk_list:
                            if "/n" not in y:
                                y = y + "/n"
                        for x in afk_list:
                            s.write(f"{x}\n")
                        # s.write(str(afk_list))
                        await ctx.reply("Removed you from afk.")

        # need to the add the message link thing
        # the code below is to let commands run cuz discord.py doesn't let users run commands without it if "on_message" is in the code
        await self.client.process_commands(ctx)


def setup(client):
    client.add_cog(dontghostpingus(client))
