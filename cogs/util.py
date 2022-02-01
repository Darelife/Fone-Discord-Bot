import discord
from discord.ext import commands
import datetime
import asyncio
import os
import requests
import shutil
import json
import random
from urllib.request import urlopen
import personal
from bs4 import BeautifulSoup

colour = personal.colour


def final_name(subject):
    chem = ["c", "chem", "chemistry"]
    phy = ["p", "phy", "physics"]
    math = ["m", "math", "maths", "mathematics"]
    if subject in chem:
        return "Chemistry"
    if subject in math:
        return "Mathematics"
    if subject in phy:
        return "Physics"


def d2(text):
    if len(str(text)) == 1:
        text1 = f"0{text}"
        return text1
    else:
        return text


def decimalToBinary(n):
    return bin(n).replace("0b", "")


def binaryToDecimal(n):
    return int(n, 2)


def download_image(url, name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36"
    }
    extension = url[-3:]
    response = requests.get(url, stream=True, headers=headers)
    with open(f"images\\{name}.{extension}", "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)


class util(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is running")

    @commands.command(
        case_insensitive=True, aliases=["remind", "remindme", "remind_me"]
    )
    @commands.bot_has_permissions(attach_files=True, embed_links=True)
    async def reminder(self, ctx, time, *, reminder):
        print(time)
        print(reminder)
        user = ctx.message.author
        embed = discord.Embed(color=0x55A7F7, timestamp=datetime.datetime.utcnow())
        embed.set_footer(
            text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden",
            icon_url=f"{self.client.user.avatar.url}",
        )
        seconds = 0
        if reminder is None:
            embed.add_field(
                name="Warning",
                value="Please specify what do you want me to remind you about.",
            )  # Error message
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"
        if seconds == 0:
            embed.add_field(
                name="Warning",
                value="Please specify a proper duration, send `reminder_help` for more information.",
            )
        elif seconds > 7776000:
            embed.add_field(
                name="Warning",
                value="You have specified a too long duration!\nMaximum duration is 90 days.",
            )
        else:
            await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
            await asyncio.sleep(seconds)
            await ctx.send(
                f"Hi <@!{ctx.author.id}>, you asked me to remind you about {reminder} {counter} ago."
            )
            return
        await ctx.send(embed=embed)

    @commands.command()
    async def cal(self, ctx, *, stuff):
        await ctx.send(eval(stuff))

    @commands.slash_command()
    async def createevent(
        self, ctx, name: str, channel_id: str, study_related: bool = True
    ):
        await ctx.defer()
        now = datetime.datetime.now()
        timestamp = datetime.datetime.timestamp(now)
        timestamp += 30
        guild = ctx.guild
        channel_id = int(channel_id)
        channel = self.client.get_channel(channel_id)
        a = await guild.create_scheduled_event(
            name=name,
            start_time=(datetime.datetime.fromtimestamp(timestamp)),
            location=channel,
        )
        event_id = a.id
        event = await guild.fetch_scheduled_event(event_id)
        if study_related == True:
            with open("1Morningstudy.jpg", "rb") as image_file:
                img = image_file.read()
            await event.edit(cover=img)
        await ctx.respond(
            f"[Join the {name} event](https://discord.com/events/{guild.id}/{event_id})"
        )

    @commands.command()
    async def create_event(
        self, ctx, name: str, channel_id: str, study_related: str = "True"
    ):
        if study_related == "True":
            (study_related) = True
        else:
            study_related = False
        now = datetime.datetime.now()
        timestamp = datetime.datetime.timestamp(now)
        timestamp += 30
        guild = ctx.guild
        channel_id = int(channel_id)
        channel = self.client.get_channel(channel_id)
        a = await guild.create_scheduled_event(
            name=name,
            start_time=(datetime.datetime.fromtimestamp(timestamp)),
            location=channel,
        )
        event_id = a.id
        event = await guild.fetch_scheduled_event(event_id)
        if study_related == True:
            with open("1Morningstudy.jpg", "rb") as image_file:
                img = image_file.read()
            await event.edit(cover=img)
        await ctx.send(
            f"Event Successfully created at {datetime.datetime.now()}, named {name}\nhttps://discord.com/events/{guild.id}/{event_id}"
        )

    @commands.command()
    async def c(ctx, *, text):
        text.replace(" ", "+")

        api = os.environ["chatbot_api"]

        resp = requests.request(
            method="GET",
            url=f"https://api.pgamerx.com/ai/response?api_key={api}&message={text}",
        )
        message = resp.text
        await ctx.reply(message[2:-2])

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(
            f"Pong! {int(self.client.latency*1000)} ms (the number might remain stable for a while cuz i have got money to buy a stable server!!!) 3"
        )

    @commands.command()
    async def dict(self, ctx, word):
        response = requests.get(
            "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/master/dictionary.json"
        )
        data = response.json()
        await ctx.send(data[word])

    @commands.command()
    async def ce(
        self,
        ctx,
        title,
        description,
        fields: int = 1,
        text: str = "a, b, c, d, e, f, g",
    ):
        a = list(text.split(","))
        embed = discord.Embed(title=title, description=description)
        x = 0
        d = 0
        while x < fields:
            embed.add_field(name=a[d], value=a[d + 1])
            x += 1
            d += 2
        await ctx.send(embed=embed)

    @commands.command()
    async def goalsstart(self, ctx):
        with open("todo.json", "r") as f:
            data = json.load(f)
        x = {
            str(ctx.author.id): [
                {"sunday": []},
                {"monday": []},
                {"tuesday": []},
                {"wednesday": []},
                {"thursday": []},
                {"friday": []},
                {"saturday": []},
            ]
        }
        print(x)
        data["user"].append(x)
        print(data)
        with open("todo.json", "w") as f:
            json.dump(data, f, indent=2)

    @commands.command()
    async def add(self, ctx, *, task):
        with open("todo.json", "r") as f:
            todo = json.load(f)
        print(1)

        try:
            todo[str(ctx.author.id)].append(task)
        except:
            todo[str(ctx.author.id)] = []
            todo[str(ctx.author.id)].append(task)
        with open("todo.json", "w") as f:
            json.dump(todo, f, indent=2)
        await ctx.send(f"{task} successfully added to the todo list")

    @commands.command()
    async def addm(self, ctx, *, tasks):
        with open("todo.json", "r") as f:
            todo = json.load(f)
        tasks = list(tasks.split("|"))
        try:
            for x in tasks:
                todo[str(ctx.author.id)].append(x)
        except:
            todo[str(ctx.author.id)] = []
            for x in tasks:
                todo[str(ctx.author.id)].append(x)
        with open("todo.json", "w") as f:
            json.dump(todo, f, indent=2)
        await ctx.send(f"{tasks} successfully added to the todo list")

    @commands.command()
    async def show(self, ctx):
        with open("todo.json", "r") as f:
            todo = json.load(f)
        t = discord.Embed(
            title="**THINGS YOU HAVE TO DO TODAY!**", color=random.choice(colour)
        )
        t.set_thumbnail(
            url="https://media.discordapp.net/attachments/835543156362575892/843451592854601788/cooltext384200855851258.png"
        )
        y = 1
        for x in todo[str(ctx.author.id)]:
            t.add_field(
                name=f"{y}) <:point:880437248896684063> {x}",
                value="━━━━━━━━━━━━━━━━━━━━━━",
                inline=False,
            )
            y += 1
        t.set_footer(text="noiceee....u can do it!!")

        await ctx.send(embed=t)

    @commands.command()
    async def pop(self, ctx, index: int):
        with open("todo.json", "r") as f:
            todo = json.load(f)
        l = todo[str(ctx.author.id)]
        p = l[index - 1]
        l.pop(index - 1)
        todo[str(ctx.author.id)] = l
        with open("todo.json", "w") as f:
            json.dump(todo, f, indent=2)
        await ctx.send(f"{p} has been removed from the todo list")

    @commands.command()
    async def doing(self, ctx, index: int):
        with open("todo.json", "r") as f:
            todo = json.load(f)
        l = todo[str(ctx.author.id)]
        p = l[(index - 1)]
        l[
            (index - 1)
        ] = f"{l[(index-1)]} <:yellowtick:854227936608649216>  `In Progress`"
        todo[str(ctx.author.id)] = l
        with open("todo.json", "w") as f:
            json.dump(todo, f, indent=2)
        await ctx.send(f"{p} has been marked as -> `In Progress`")

    @commands.command()
    async def done(self, ctx, index: int):
        with open("todo.json", "r") as f:
            todo = json.load(f)
        l = todo[str(ctx.author.id)]
        p = l[(index - 1)]
        if "<:yellowtick:854227936608649216>" in l[(index - 1)]:
            l[(index - 1)] = str(l[(index - 1)])[:-47]
        l[(index - 1)] = f"~~{l[(index-1)]}~~ <:greentick:854227936919552040> `done`"
        todo[str(ctx.author.id)] = l
        with open("todo.json", "w") as f:
            json.dump(todo, f, indent=2)
        await ctx.send(f"{p} has been marked as done")

    @commands.command()
    async def edit(self, ctx, index: int, *, text):
        with open("todo.json", "r") as f:
            todo = json.load(f)
        l = todo[str(ctx.author.id)]
        p = l[index - 1]
        l[(index - 1)] = text
        todo[str(ctx.author.id)] = l
        with open("todo.json", "w") as f:
            json.dump(todo, f, indent=2)
        await ctx.send(f"{p} has been edited to {text}")

    @commands.command()
    async def sunday(self, ctx, *, todo):
        with open("todo.json", "r") as f:
            data = json.load(f)
        # try:
        print(1)
        x = {"x": todo}
        ids = str(ctx.author.id)
        for da in data["user"]:
            if ids in da:
                print("ues")
                da[0].append(x)
        with open("todo.json", "w") as f:
            json.dump(data, f, indent=2)

        # except:
        #   await ctx.send("please run the `fgoalsstart` command first")
        await ctx.send("done")

    @commands.command()
    async def say(self, ctx, message):
        await ctx.send(f"{str(message)}\n~{ctx.author} ||{ctx.author.id}||")

    # @commands.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
    # @commands.bot_has_permissions(attach_files = True, embed_links = True)
    # async def reminder(ctx, time1, *, reminder):
    #     print(time1)
    #     print(reminder)
    #     user = ctx.message.author
    #     embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    #     embed.set_footer(text="If you have any questions, suggestions or bug reports, please join our support Discord Server: link hidden", icon_url = "https://cdn.discordapp.com/avatars/829870450657198121/88ec0a9277781d79ff40cbbe5fc6ba25.png")
    #     seconds = 0
    #     if reminder is None:
    #         embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    #     if time1.lower().endswith("d"):
    #         seconds += int(time1[:-1]) * 60 * 60 * 24
    #         counter = f"{seconds // 60 // 60 // 24} days"
    #     if time1.lower().endswith("h"):
    #         seconds += int(time1[:-1]) * 60 * 60
    #         counter = f"{seconds // 60 // 60} hours"
    #     elif time1.lower().endswith("m"):
    #         seconds += int(time1[:-1]) * 60
    #         counter = f"{seconds // 60} minutes"
    #     elif time1.lower().endswith("s"):
    #         seconds += int(time1[:-1])
    #         counter = f"{seconds} seconds"
    #     if seconds == 0:
    #         embed.add_field(name='Warning',
    #                         value='Please specify a proper duration, send `reminder_help` for more information.')
    #     elif seconds < 300:
    #         embed.add_field(name='Warning',
    #                         value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    #     elif seconds > 7776000:
    #         embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    #     else:
    #         await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
    #         await asyncio.sleep(seconds)
    #         await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
    #         return
    #     await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, suggestion):
        warnsfile = open("suggestion.txt", "a+")
        warnsfile.write(f"{suggestion}\n")
        await ctx.send("Thank you for the suggestion")

    @commands.command(aliases=["char"])
    async def charactercount(self, ctx, message):
        x = 0
        for y in message:
            x += 1
        await ctx.send(x)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        p = member.avatar.url
        await ctx.send(str(p))

    @commands.command(pass_context=True)
    async def coinflip(self, ctx):
        variable = [
            "heads",
            "tails",
        ]
        await ctx.send(random.choice(variable))

    @commands.command()
    async def afk(self, ctx, *, text=None):
        """an afk command - type in present continuous. 
        
Credits : Android aka xNoir#5158"""
        member = ctx.author
        if text == None:
            text = "AFK"
        # if ctx.channel.permissions_for(ctx.author).administrator is True:
        await ctx.channel.send(f"{member} is afk!")
        warnsfile = open("afk_users_list.txt", "a+")
        warnsfile.write(f"{(member.id)} is {text}\n")

    @commands.command()
    async def no_afk(self, ctx):
        "Basically the opposite of the afk command and u can actually type anything to do what this does if u are afk"
        await ctx.channel.send("Removed you from afk.")
        member = ctx.author.id
        with open("afk_users_list.txt", "r") as h:
            afk_list = h.readlines()
            for i in afk_list:
                if str(member) in i:
                    afk_list.remove(i)
                    with open("afk_users_list.txt", "w") as s:
                        for y in afk_list:
                            if "/n" not in y:
                                y = y
                        s.write(afk_list)

    @commands.command(pass_context=True)
    async def kill(self, ctx, *, text):
        variable = [
            (
                f" {text} learnt about how sad life is after which the inferior {text} decided to jump out of the building"
            ),
            (
                f" {text} got into a gunfight with the pope after which a god came and kicked his ass instantly killing him"
            ),
            (f" {text} boarded a plane. Unfortunately, there was a snake in it"),
            (
                f" {text} and {ctx.author} were hanging out. {text} said a lame joke and then {ctx.author} decided to slit his/her throat. F's in the chat"
            ),
            (f"{text} accidently clicked on a browser ad saying ‘DIE FOR FREE!’"),
            (f"{text} was bitten by a vampire in Transylvania"),
            (
                f"{text} decided to hold his breath for about 23 hrs and 59 min. F's in the chat."
            ),
            (
                f"{text} decided to succumb to suicidal temptations. It’s a way of telling God “You can’t fire me, I QUIT!”"
            ),
        ]
        await ctx.channel.send(random.choice(variable))

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Invite Link",
            description="https://discord.com/api/oauth2/authorize?client_id=829870450657198121&permissions=7091973712&scope=applications.commands%20bot",
        )
        await ctx.channel.send(embed=embed)

    @commands.command(name="info")
    async def all_or_channels(self, ctx):
        embed = discord.Embed(
            title="ALL OUR CHANNELS", description="What is this server about?"
        )
        embed.set_author(
            name="HOMIES",
            url="https://scene7.zumiez.com/is/image/zumiez/image/Know-Bad-Daze-For-The-Homies-Sticker-_314491.jpg",
            icon_url="https://media.discordapp.net/attachments/789671664069247007/826656657618370560/image.jpeg?width=400&height=400",
        )
        embed.add_field(
            name="What is this server meant to be for?",
            value="This server is meant to be mainly for a group of people from the class 10G. They have personalized the layout and everything else of this server according to their needs.",
        )
        embed.add_field(
            name="General",
            value="Where we have general talk and it is also the most active channel in this server.",
        )
        embed.add_field(
            name="Bots",
            value="A channel dedicated just for having fun with our bots. We have a lot of bots in this server.",
        )
        embed.add_field(
            name="Random Stuff Spam",
            value="A channel where we share random shit stuff occasionally and just spam",
        )
        embed.add_field(
            name="Dank Memer", value="A channel just for the dank memer bot"
        )
        embed.add_field(
            name="Anime", value="A channel for the anime weebs. Are you one of them?"
        )
        embed.add_field(
            name="THE CLASSES CATEGORY",
            value="Where we talk abt our school realted stuff <#762900260669882419> <#730105916191408189> <#746967717311021107> <#754915827987251291>",
        )
        embed.add_field(
            name="Game Stuff",
            value="Where we talk abt gaming realted stuff <#722380450214969365>",
        )
        embed.add_field(
            name="Music",
            value="We listen to music in this channel and we have a lot of bots for music.",
        )
        embed.add_field(
            name="EXTRA CHANNELS",
            value="We have some dead or extra channels too. <#789671664069247007> <#785144552305459230> <#781404894821089310> <#747763296072892486> <#740430703573073980> <#735331852793020511> and <#729747241966764204>",
        )
        embed.set_footer(text="We need your help in growing!! Please support us!!")
        await ctx.send(embed=embed)

    @commands.command()
    async def saye(self, ctx, *, message):
        await ctx.message.delete()
        embed = discord.Embed(
            title=(f"{ctx.author.display_name} said"),
            url=str(ctx.author.avatar.url),
            description=(message),
            color=discord.Color.blue(),
        )
        embed.set_author(
            name=ctx.author.display_name,
            url=(ctx.author.avatar.url),
            icon_url=ctx.author.avatar.url,
        )
        await ctx.channel.send(embed=embed)

    # @commands.command()
    # async def say(self, ctx, *, message):
    #     await ctx.message.delete()
    #     await ctx.send(f"""{message}
    #           ~ {ctx.author.name}#{ctx.author.discriminator}""")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(
            title="MESSAGES PURGED",
            description=(f"<@!{ctx.author.id}> successfully purged {amount} messages"),
        )
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def purge_(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def poll_yn(self, ctx, *, p_message):
        embed = discord.Embed(title="Poll", description=p_message)
        my_msg = await ctx.send(embed=embed)
        await my_msg.add_reaction("👍")
        await my_msg.add_reaction("👎")

    @commands.command()
    async def addreaction(self, ctx, msgid, emoji):
        msg = await ctx.fetch_message(msgid)
        await msg.add_reaction(emoji)
        await ctx.send(f"```{emoji}```")
        print(emoji)

    @commands.command()
    async def poll_no(self, ctx, number: int, *, p_message):
        my_msg = await ctx.send(p_message)
        hmm = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        x = -1
        for emoji in hmm:
            if x + 1 < number:
                x += 1
                await my_msg.add_reaction(hmm[x])

    @commands.command()
    async def did(self, ctx, num: int):
        binary = decimalToBinary(num)
        decimalbinary = binary[:-22]
        decimal = binaryToDecimal(decimalbinary)
        unix = int(decimal) + 1420070400000
        s = int(float(unix) / 1000)
        with urlopen(
            f"https://showcase.api.linx.twenty57.net/UnixTime/fromunixtimestamp?unixtimestamp={s}"
        ) as cu:
            # print(cu)
            data = json.load(cu)
        finaltime = data["Datetime"]
        await ctx.channel.send(finaltime)

    @commands.command(aliases=["b_add", "birthday_a", "b_a"])
    async def birthday_add(self, ctx, dd, mm):
        dd = d2(dd)
        print(1)
        mm = d2(mm)
        print(2)
        date1 = f"{dd}-{mm}"
        print(3)
        with open("birthday.json", "r") as json_file:
            data = json.load(json_file)
        data["birthdays"].append({"userid": ctx.author.id, "date": date1})
        with open("birthday.json", "r") as f:
            x = f.readlines()
        if str(ctx.author.id) in str(x):
            await ctx.send("You have already registered your birthday")
        else:
            with open("birthday.json", "w") as outfile:
                json.dump(data, outfile)

    @commands.command()
    async def b_update(self, ctx, dd, mm):
        dd = d2(dd)
        mm = d2(mm)
        date1 = f"{dd}-{mm}"
        with open("birthday.json", "r") as f:
            read_data = json.load(f)
        for x in read_data["birthdays"]:
            if str(ctx.author.id) in str(x):
                x.update({"date": date1})
        await ctx.send(read_data)
        with open("birthday.json", "w") as outfile:
            json.dump(read_data, outfile)

    @commands.command()
    # an ncert command, only for class 11 tho...too lazy to make it for other classes
    # if your school isn't affiliated by the Central Board of Secondary Education (CBSE), ncert books are the books published by the it in india and you don't need to worry about it
    async def ncert(self, ctx, subject, chapter):
        if subject == "rr":
            embed = discord.Embed(
                title="NCERT",
                description=f"""[PDF](https://bit.ly/3g0Mn27)
[Ncert's Website](https://bit.ly/3g0Mn27)
[Download The Book](https://bit.ly/3g0Mn27)""",
                url="https://ncert.nic.in/textbook.php",
                color=discord.Colour.random(),
            )
            embed.set_footer(text=f"Chapter : {chapter} | Subject : physics")
            await ctx.send(embed=embed)
        else:
            subname = final_name(subject)
            if len(chapter) == 1:
                chapter1 = f"0{chapter}"
            if subject == "math" or subject == "mathematics" or subject == "m":
                ye = "m"
                booknumber = "1"
                total = "16"
            elif subject == "chem" or subject == "chemistry" or subject == "c":
                ye = "c"
                booknumber = "1"
                total = "7"
            elif subject == "phy" or subject == "physics" or subject == "p":
                ye = "p"
                booknumber = "1"
                total = "8"
            elif subject == "chem2" or subject == "chemistry2" or subject == "c2":
                ye = "c"
                booknumber = "2"
                total = "7"
            elif subject == "phy2" or subject == "physics2" or subject == "p2":
                ye = "p"
                booknumber = "2"
                total = "7"
            else:
                embed = discord.Embed(
                    title="Invalid Subject",
                    description="""```m or math or mathematics -> math
    c or chem or chemistry -> chem
    p or phy or physics -> phy
    c2 or chem2 or chemistry -> chem book 2
    p2 or physics2 or chemistry2 -> physics book 2 ```""",
                )
                await ctx.channel.send(embed=embed)
            if subject in [
                "m",
                "math",
                "mathematics",
                "chem",
                "c",
                "chemistry",
                "p",
                "phy",
                "physics",
                "c2",
                "chem2",
                "chemistry2",
                "p2",
                "phy2",
                "physics2",
            ]:
                download_link = (
                    f"https://ncert.nic.in/textbook/pdf/ke{ye}h{booknumber}dd.zip"
                )
                # creates the embed
                embed = discord.Embed(
                    title="NCERT",
                    description=f"""[PDF](https://ncert.nic.in/textbook/pdf/ke{ye}h{booknumber}{(chapter1)}.pdf)
[Ncert's Website](https://ncert.nic.in/textbook.php?ke{ye}h{booknumber}={(chapter)}-{total})
[Download The Book]({download_link})""",
                    url="https://ncert.nic.in/textbook.php",
                    color=discord.Colour.random(),
                )
                embed.set_footer(text=f"Chapter : {chapter} | Subject : {subname}")
                await ctx.send(embed=embed)

    # gonna be a much more cleaner and better code
    @commands.command()
    async def ncert2(self, ctx, subject, ch_no):
        pass

    @commands.command()
    async def mc(self, ctx, craft):
        url = "https://www.minecraftcrafting.info/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        sup = craft.capitalize()
        sup = f"Craft {sup}"
        images = soup.find_all("img", attrs={"alt": sup})
        text = "Try making it plural or maybe you entered a non craftable item"
        if len(images) == 0:
            await ctx.send(text)
        for image in images:
            image_src = image["src"]
            print(image)
            url_final = url + image_src
            text = url_final
            await ctx.reply(text)
            if image == None:
                await ctx.reply(
                    "Try making it plural or maybe you entered a non craftable item"
                )


def setup(client):
    client.add_cog(util(client))
