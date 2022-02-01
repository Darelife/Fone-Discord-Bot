import operator
from urllib.request import urlopen
import urllib.request
import discord
from discord.ext import commands
import requests
import os
import json
import random
import time
import asyncio
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup

colour = [0xDC143C, 0xD35400, 0x48C9B0, 0x7FB3D5, 0xFFA0A2]
# fd is the final data
fd = {}

API_KEY = os.environ["lastfmapikey"]


def commas(word):
    e = list(word.split(".")[0])
    for i in range(len(e))[::-3][1:]:
        e.insert(i + 1, ",")
    result = "".join(e)
    return result


def replacelement(word):
    # return urllib.parse.quote(word.encode("utf-8"))
    word = word.replace('"', "%22")
    word = word.replace("&", "%26")
    word = word.replace("#", "%23")
    word = word.replace("'", "%27")
    word = word.replace("!", "%21")
    word = word.replace("?", "%3F")
    word = word.replace(":", "%3A")
    word = word.replace(";", "%3B")
    word = word.replace("÷", "%F7")
    return word


class lastfmbot:
    # fd is the final data
    # to future me, this global command is basically the thing which kinda lets me do stuff without editing the test.json file....to everyone else, yeah, i spent abt 2 days trying to figure out why the code i had written was working...like...i forgot that i added the global function and that all the data was being stored in the fd dictionary
    # to the past me, sup
    global fd

    def __init__(self, lu, did, artist, name, album, server):
        self.user = lu
        self.discordid = did
        self.api = API_KEY
        self.artist = artist
        self.name = name
        self.album = album
        self.server = server
        replacelement(self.name)
        replacelement(self.album)
        replacelement(self.artist)

    def trackdata(self):

        link = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&user={self.user}&api_key={self.api}&artist={self.artist}&track={self.name}&format=json"
        print(link)

        print(link)
        link = link.replace(" ", "+")
        print(link)
        # with urllib.request.urlopen(link) as f:
        #     data = json.load(f)
        data = lastfm_get(
            {
                "user": self.user,
                "method": "track.getInfo",
                "artist": self.artist,
                "track": self.name,
            }
        )
        data = data.json()
        fd["track"] = {}
        fd["user"] = {}
        try:
            fd["track"]["songname"] = data["track"]["name"]
        except:
            pass
        try:
            fd["track"]["lastfmsongurl"] = data["track"]["url"]
        except:
            pass
        try:
            fd["track"]["listeners"] = data["track"]["listeners"]
        except:
            pass
        try:
            fd["track"]["lastfmsonglisteners"] = data["track"]["listeners"]
        except:
            pass
        try:
            fd["track"]["lastfmsongplaycount"] = data["track"]["playcount"]
        except:
            pass
        try:
            fd["track"]["lastfmsongplaycount"] = data["track"]["playcount"]
        except:
            pass
        try:
            fd["track"]["duration"] = data["track"]["duration"]
        except:
            pass
        try:
            fd["track"]["artistname"] = data["track"]["artist"]["name"]
        except:
            pass
        try:
            fd["track"]["lastfmartisturl"] = data["track"]["artist"]["url"]
        except:
            pass
        try:
            fd["track"]["lastfmalbumurl"] = data["track"]["album"]["url"]
        except:
            pass
        try:
            fd["track"]["album"] = data["track"]["album"]["title"]
        except:
            pass
        try:
            fd["user"]["trackplays"] = data["track"]["userplaycount"]
        except:
            pass
        try:
            genres = []
            for x in data["track"]["toptags"]["tag"]:
                genres.append(x["name"])
            genre = " - ".join([str(elem) for elem in genres])
            fd["track"]["genre"] = genre
        except:
            pass
        try:
            fd["track"]["image"] = data["track"]["album"]["image"][-1]
        except:
            pass
        # with open("test.json", "w") as f:
        #   json.dump(fd,f,indent = 2)

    def artistdata(self):

        link = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&user={self.user}&artist={self.artist}&api_key={self.api}&format=json"
        # print(2)

        link = link.replace(" ", "+")
        print(link)
        # print(2)
        # with urllib.request.urlopen(link) as f:
        #     data = json.load(f)
        data = lastfm_get(
            {"user": self.user, "method": "artist.getInfo", "artist": self.artist}
        )
        data = data.json()
        # with open("test.json", "r") as f:
        #     fd = json.load(f)
        fd["artist"] = {}
        try:
            fd["artist"]["name"] = data["artist"]["name"]
        except:
            pass
        try:
            fd["artist"]["mbid"] = data["artist"]["mbid"]
        except:
            pass
        try:
            fd["artist"]["lastfmurl"] = data["artist"]["url"]
        except:
            pass
        try:
            fd["artist"]["listeners"] = data["artist"]["stats"]["listeners"]
        except:
            pass
        try:
            fd["artist"]["playcount"] = data["artist"]["stats"]["playcount"]
        except:
            pass
        try:
            fd["user"]["artistplays"] = data["artist"]["stats"]["userplaycount"]
        except:
            pass
        # need to add similar artists
        try:
            fd["artist"]["published"] = data["artist"]["bio"]["published"]
        except:
            pass
        try:
            fd["artist"]["summary"] = data["artist"]["bio"]["summary"]
        except:
            pass
        try:
            fd["artist"]["content"] = data["artist"]["bio"]["content"]
        except:
            pass
        # with open('test.json', "w") as f:
        #   json.dump(fd,f,indent = 2)

    def albumdata(self):
        link = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={self.api}&user={self.user}&artist={self.artist}&album={self.album}&format=json"

        link = link.replace(" ", "+")
        # with urllib.request.urlopen(link) as f:
        #     data = json.load(f)
        data = lastfm_get(
            {
                "user": self.user,
                "method": "album.getInfo",
                "artist": self.artist,
                "album": self.album,
            }
        )
        data = data.json()
        # with open("test.json", "r") as f:
        #   fd = json.load(f)
        fd["album"] = {}
        try:
            fd["album"]["listeners"] = data["album"]["listeners"]
        except:
            pass
        try:
            fd["album"]["playcount"] = data["album"]["playcount"]
        except:
            pass
        try:
            fd["album"]["artist"] = data["album"]["artist"]
        except:
            pass
        try:
            fd["album"]["mbid"] = data["album"]["mbid"]
        except:
            pass
        try:
            fd["album"]["lastfmurl"] = data["album"]["url"]
        except:
            pass
        try:
            fd["album"]["name"] = data["album"]["name"]
        except:
            pass
        try:
            fd["user"]["albumplays"] = data["album"]["userplaycount"]
        except:
            pass
        # with open("test.json", "w") as f:
        #   json.dump(fd,f,indent = 2)

    def who_knows_artist(self):
        if self.server == "697493731611508737":
            users = ["itzp", "Noir4200", "DNFphobia", "m14127", "DudeChill_"]
        else:
            users = [
                "itzp",
                "Noir4200",
                "ItzSD06",
                "DNFphobia",
                "m14127",
                "DudeChill_",
                "Rischit356",
            ]
        returnlist = []
        for x in users:
            u = int(get_user_artist_plays(self.artist, x))
            returnlist.append(int(u))
            returnlist.append(x)
        # returnlist.append(fd["user"]["artistplays"])
        # returnlist.append(self.user)
        wkvalues = []
        wkusers = []

        y = 0
        for x in returnlist:
            if y % 2 == 0:
                wkvalues.append(int(x))
            elif y % 2 != 0:
                wkusers.append(x)
            y += 1
        x = max(wkvalues)
        wkstuff = {}
        y = 0
        for x in wkusers:
            if wkvalues[y] != 0:
                wkstuff[x] = wkvalues[y]
            y += 1
        # wkstuff = {wkusers[0] : wkvalues[0], wkusers[1] : wkvalues[1], wkusers[2] : wkvalues[2], wkusers[3] : wkvalues[3], wkusers[4] : wkvalues[4], wkusers[5] : wkvalues[5], wkusers[6] : wkvalues[6]}
        cd = sorted(wkstuff.items(), key=operator.itemgetter(1), reverse=True)
        wktext = ""
        for x in cd:
            wktext += f"{x[0]} ({x[1]})\n"
        fd["who_knows_artist"] = wktext
        # result = {}
        # y = 0
        # for x in cd:
        #   result[cd[y][0]] = cd[y][1]
        #   y += 1
        # print(result)

    def who_knows_track(self):
        if self.server == "697493731611508737":
            users = ["itzp", "Noir4200", "DNFphobia", "m14127", "DudeChill_"]
        else:
            users = [
                "itzp",
                "Noir4200",
                "ItzSD06",
                "DNFphobia",
                "m14127",
                "DudeChill_",
                "Rischit356",
            ]
        returnlist = []
        for x in users:
            if x != self.user:
                u = int(get_user_track_plays(self.artist, self.name, x))
                returnlist.append(int(u))
                returnlist.append(x)
        returnlist.append(fd["user"]["trackplays"])
        returnlist.append(self.user)
        wkvalues = []
        wkusers = []

        y = 0
        for x in returnlist:
            if y % 2 == 0:
                wkvalues.append(int(x))
            elif y % 2 != 0:
                wkusers.append(x)
            y += 1
        x = max(wkvalues)
        wkstuff = {}
        y = 0
        for x in wkusers:
            if wkvalues[y] != 0:
                wkstuff[x] = wkvalues[y]
            y += 1

        # wkstuff = {wkusers[0] : wkvalues[0], wkusers[1] : wkvalues[1], wkusers[2] : wkvalues[2], wkusers[3] : wkvalues[3], wkusers[4] : wkvalues[4], wkusers[5] : wkvalues[5], wkusers[6] : wkvalues[6]}
        cd = sorted(wkstuff.items(), key=operator.itemgetter(1), reverse=True)
        wktext = ""
        for x in cd:
            wktext += f"{x[0]} ({x[1]})\n"
        fd["who_knows_track"] = wktext
        # with open("test.json", "w") as f:
        #     json.dump(fd, f, indent = 2)

    def favs(self):
        link = f"http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={self.user}&limit=1000&api_key={self.api}&format=json"

        link = link.replace(" ", "+")
        # with open("test.json", "r") as f:
        #     fd = json.load(f)
        # with urllib.request.urlopen(link) as f:
        #     data = json.load(f)
        data = lastfm_get(
            {"user": self.user, "method": "user.gettoptracks", "limit": "1000"}
        )
        data = data.json()
        page = 0
        total = int(data["toptracks"]["@attr"]["totalPages"])
        fav = {}
        print(total)
        while page < total:
            page += 1
            startTime = time.time()
            link = f"http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&page={page}&user={self.user}&limit=1000&api_key={self.api}&format=json"

            link = link.replace(" ", "+")
            with urllib.request.urlopen(link) as f:
                data = json.load(f)
            tracks = data["toptracks"]["track"]
            endTime = time.time()
            print("favs", endTime - startTime)

            for x in tracks:
                artist = x["artist"]["name"]
                if artist == self.artist:
                    fav[x["name"]] = f"{x['playcount']}|{x['url']}"
        fd["favs"] = {}
        favv = {}
        a = 0
        if len(fav) >= 24:
            for x in fav:
                a += 1
                if a < 24:
                    favv[x] = fav[x]
                elif a == 24:
                    favv[x] = fav[x]
                    favv["** **"] = f"and {len(fav)-24} more | "
                else:
                    break
        else:
            favv = fav

        fd["favs"]["fav"] = favv

        # with open("test.json", "w") as f:
        #     json.dump(fd, f, indent = 2)

    def topartists(self):
        link = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={self.user}&api_key={self.api}&format=json"

        link = link.replace(" ", "+")
        data = lastfm_get({"user": self.user, "method": "user.gettopartists"})
        data = data.json()
        fd["topartists"] = {}
        for x in data["topartists"]["artist"]:
            fd["topartists"][x["name"]] = x["playcount"]
            if int(x["@attr"]["rank"]) == 25:
                break


def lastfm_get(payload):
    start = time.time()
    # define headers and URL
    headers = {"user-agent": USER_AGENT}
    url = "https://ws.audioscrobbler.com/2.0/"

    # Add API key and format to the payload
    payload["api_key"] = API_KEY
    payload["format"] = "json"

    response = requests.get(url, headers=headers, params=payload)
    print(response.url)
    end = time.time()
    delta = end - start
    print(f"lastfm_get - {delta}")

    return response


def get_user_artist_plays(sartist, lu):
    start = time.time()
    link = f"http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&user={lu}&artist={sartist}&api_key={API_KEY}&format=json"
    # print(2)

    link = link.replace(" ", "+")
    # print(2)
    # with urllib.request.urlopen(link) as f:
    #     data = json.load(f)
    data = lastfm_get(
        {"user": lu, "method": "artist.getinfo", "artist": sartist, "api_key": API_KEY}
    )
    data = data.json()
    end = time.time()
    delta = end - start
    print(f"get_user_artist_plays - {delta}")
    return data["artist"]["stats"]["userplaycount"]


def get_user_album_plays(sartist, salbum, lu):
    start = time.time()
    sartist = sartist.replace("&", "%26")
    link = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={API_KEY}&user={lu}&artist={sartist}&album={salbum}&format=json"

    link = link.replace(" ", "+")
    # print(3)
    # with urllib.request.urlopen(link) as f:
    #     data = json.load(f)
    data = lastfm_get(
        {
            "user": lu,
            "method": "album.getinfo",
            "artist": sartist,
            "album": salbum,
            "api_key": API_KEY,
        }
    )
    data = data.json()
    end = time.time()
    delta = end - start
    print(f"get_user_album_plays - {delta}")
    return data["album"]["userplaycount"]


def get_user_track_plays(sartist, sname, lu):
    start = time.time()
    sartist = sartist.replace("&", "%26")
    link = f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&user={lu}&api_key={API_KEY}&artist={sartist}&track={sname}&format=json"

    link = link.replace(" ", "+")
    # print(link)
    # print(4)
    # with urllib.request.urlopen(link) as f:
    #   data = json.load(f)
    data = lastfm_get(
        {
            "user": lu,
            "method": "track.getinfo",
            "artist": sartist,
            "track": sname,
            "api_key": API_KEY,
        }
    )
    data = data.json()
    end = time.time()
    delta = end - start
    print(f"get_user_track_plays - {delta}")
    return data["track"]["userplaycount"]


def who_knows_track(sartist, sname, lu):
    start = time.time()
    returnlist = []
    # i did this to reduce the number of api calls i make, but yeah, i could have made it wayy more efficient
    if "lastfmusername" != lu:
        name = int(get_user_track_plays(sartist, sname, "lastfmusername"))
        returnlist.append(int(name))
        returnlist.append("lastfmusername")

    end = time.time()
    delta = end - start
    print(f"who_knows_track - {delta}")
    return returnlist


def who_knows(sartist, lu):
    start = time.time()
    returnlist = []
    if "lastfmusername" != lu:
        name = int(get_user_artist_plays(sartist, "lastfmusername"))
        returnlist.append(int(name))
        returnlist.append("name")
    end = time.time()
    delta = end - start
    print(f"who_knows - {delta}")
    return returnlist


# this is actually the main one, but it uses webscraping..so yeah
def artistpic2(sartist):
    start = time.time()
    link = f"https://www.last.fm/music/{sartist}/+images"

    link = link.replace(" ", "+")
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")
    images = soup.find_all("img")
    a = (list(images))[1]
    b = list(str(a).split('src="'))
    c = b[1]
    d = c[:-3]
    end = time.time()
    delta = end - start
    print(f"artistpic2 - {delta}")
    return d


# this is more like an album pic but yeah it's backup
def artistpic(sartist, salbum, sname):
    start = time.time()
    # print(6)
    link = f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={API_KEY}&artist={sartist}&album={salbum}&format=json"

    link = link.replace(" ", "+")
    with urllib.request.urlopen(link) as f:
        # ainfo is the artist info
        ainfo = json.load(f)
    pic = ainfo["album"]["image"][2]["#text"]
    if pic == "":
        link = f"http://ws.audioscrobbler.com/2.0/?method=track.getinfo&api_key={API_KEY}&artist={sartist}&album={salbum}&track={sname}&format=json"

        link = link.replace(" ", "+")
        with urllib.request.urlopen(link) as f:
            # ainfo is the artist info
            ainfo = json.load(f)
        pic = ainfo["track"]["image"][2]["#text"]
    end = time.time()
    delta = end - start
    print(f"artistpic - {delta}")
    return pic


def spotifylink(sartist, sname):
    start = time.time()
    url = f"https://www.last.fm/music/{sartist}/_/{sname}"
    url = url.replace(" ", "+")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    a = list(str(soup).split('"'))
    b = []
    for x in a:
        if "https://open.spotify.com/track/" in x:
            b.append(x)
    end = time.time()
    delta = end - start
    print(f"who_knows - {delta}")
    return b[0]


users = {
    "497352662451224578": "itzp",
    "806777960618524672": "itzp",
    "687348489109372971": "m14127",
    "782496071959838730": "m14127",
    "629243339379834880": "Noir4200",
    "730100904652570664": "Noir4200",
    "688023206380044306": "DudeChill_",
    "820162158226046988": "DudeChill_",
    "614867178281369723": "DNFphobia",
    "801081243386249237": "DNFphobia",
    "772680586480582667": "ItzSD06",
    "772680286898487297": "Rischit356",
}

# dictionry with everyones discord ids and usernames
users = {"discord_id(str)": "lastfmusername(str)"}

# for some reason, i just did this too, don't judge me
ids = {"lastfmusername(str)": "discord_id(str)"}

USER_AGENT = "Dataquest"

headers = {"user-agent": USER_AGENT}

payload = {"api_key": API_KEY, "method": "chart.gettopartists", "format": "json"}

r = requests.get("https://ws.audioscrobbler.com/2.0/", headers=headers, params=payload)


class Lastfm(commands.Cog):
    def __init__(self, client):
        self.client = client

    # def __init__(self, client, slash):
    #     self.client = client
    #     self.slash = slash?? i tried this but then i needed to define slash....and idk how to do that

    @commands.Cog.listener()
    async def on_ready(self):
        print("lastfm.py is running")

    @commands.command()
    async def np(self, ctx):
        global fd
        did = ctx.author.id
        # did = 629243339379834880
        nick = ctx.author.nick
        lu = users[str(did)]
        recent = lastfm_get({"user": lu, "method": "user.getRecentTracks"})
        recent = recent.json()
        nowplaying = False
        try:
            thumbnail_image = recent["recenttracks"]["track"][0]["image"][-1]["#text"]
        except:
            thumbnail_image = None
        # with open("recenttest.json", "w") as f:
        #     f.write(str(recent))
        try:
            if recent["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
                nowplaying = True
        except:
            pass

        if nowplaying == True:
            author_text = f"{lu}'s Current Song"
        elif nowplaying == False:
            author_text = f"{lu}'s last Song"
        artist = recent["recenttracks"]["track"][0]["artist"]["#text"]
        print(artist)
        album = recent["recenttracks"]["track"][0]["album"]["#text"]
        print(album)
        track = recent["recenttracks"]["track"][0]["name"]
        print(track)
        lastfmclass = lastfmbot(lu, did, artist, track, album, str(ctx.guild.id))
        lastfmclass.trackdata()
        lastfmclass.artistdata()
        lastfmclass.albumdata()
        # with open("test.json", "r") as f:
        # fd = json.load(f)
        try:
            splink = spotifylink(artist, track)
        except:
            pass
        try:
            np = discord.Embed(
                title=f"<:spotifylogo:874184029153411083> {fd['track']['songname']}",
                description=f'**{fd["artist"]["name"]}** | {fd["album"]["name"]}',
                color=random.choice(colour),
                url=splink,
            )
        except:
            np = discord.Embed(
                title=f"{fd['track']['songname']}",
                description=f'**{fd["artist"]["name"]}** | {fd["album"]["name"]}',
                color=random.choice(colour),
                url=fd["track"]["lastfmsongurl"],
            )

        np.set_author(
            name=author_text,
            url=f"https://www.last.fm/user/{lu}",
            icon_url=ctx.author.avatar.url,
        )

        try:
            np.set_thumbnail(url=thumbnail_image)
        except:
            pass

        footer_text = ""

        try:
            if fd["track"]["genre"] == "":
                pass
            else:
                footer_text += f"• {fd['track']['genre']}\n"
        except:
            pass

        try:
            footer_text += f"• {fd['user']['artistplays']} artist plays • {fd['user']['albumplays']} album plays • {fd['user']['trackplays']} song plays\n"
        except:
            pass

        try:
            footer_text += f"• {fd['track']['lastfmsonglisteners']} lastfm song listeners ({fd['track']['lastfmsongplaycount']})"
        except:
            pass

        try:
            np.set_footer(text=footer_text)
        except:
            pass

        # with open("test.json", "w") as f:
        #     json.dump(fd, f, indent = 2)
        mess = await ctx.send(embed=np)
        await mess.add_reaction("<:spotifylogo:874184029153411083>")
        await mess.add_reaction("<:stats:879373496617156618>")
        await mess.add_reaction("<:artistinfo:880034051765977149>")
        await mess.add_reaction("<:fav:885913052980068372>")
        if thumbnail_image != None:
            await mess.add_reaction("<:cover:886104532159975464>")
        await mess.add_reaction("<:topartist:886551866027167784>")
        page2 = True
        favspage = True
        topartist = True

        while True:

            def check(reaction, user):
                # if reaction.emoji.id == 779554066082299954:
                #  print("nice")
                return user == ctx.author and reaction.message.id == mess.id

            try:
                reaction, user = await self.client.wait_for(
                    "reaction_add", check=check, timeout=60
                )
                # print(reaction)

                if reaction.emoji.id == 879373496617156618:
                    await mess.remove_reaction(
                        "<:stats:879373496617156618>", ctx.author
                    )
                    await mess.add_reaction("<a:loading:894978191331041371>")
                    try:
                        # await mess.edit(content = "Please wait", embed = np)
                        if page2 == True:
                            lastfmclass.who_knows_artist()
                            lastfmclass.who_knows_track()
                            page2 = False

                        wkar = discord.Embed(
                            title=f"{artist} - {track}", color=random.choice(colour)
                        )
                        if (
                            fd["who_knows_artist"] != None
                            and fd["who_knows_artist"] != ""
                            and fd["who_knows_artist"] != " "
                        ):
                            wkar.add_field(
                                name="WK Artist", value=fd["who_knows_artist"]
                            )
                        if (
                            fd["who_knows_track"] != None
                            and fd["who_knows_track"] != ""
                            and fd["who_knows_track"] != " "
                        ):
                            wkar.add_field(name="WK Track", value=fd["who_knows_track"])
                        await mess.remove_reaction(
                            "<a:loading:894978191331041371>", self.client.user
                        )
                        await mess.edit(content=None, embed=wkar)
                    except:
                        await mess.add_reaction("<:Timesup:879423783063150642>")
                        await mess.remove_reaction(
                            "<a:loading:894978191331041371>", self.client.user
                        )
                    # np.add_field(name = "WK Track", value = fd["who_knows_track"])
                    # np.add_field(name = "WK Artist", value = fd["who_knows_artist"])

                if reaction.emoji.id == 886104532159975464:
                    await mess.remove_reaction(
                        "<:cover:886104532159975464>", ctx.author
                    )
                    await mess.edit(content=str(thumbnail_image), embed=None)
                if reaction.emoji.id == 874184029153411083:
                    await mess.remove_reaction(
                        "<:spotifylogo:874184029153411083>", ctx.author
                    )
                    await mess.edit(content=None, embed=np)
                if reaction.emoji.id == 885913052980068372:
                    await mess.remove_reaction("<:fav:885913052980068372>", ctx.author)
                    await mess.add_reaction("<a:loading:894978191331041371>")
                    try:
                        if favspage == True:
                            lastfmclass.favs()
                            favspage = False

                        des = ""
                        # with open("test.json", "r") as f:
                        # fd = json.load(f)
                        favvv = fd["favs"]["fav"]
                        srno = 1

                        for x in favvv:
                            values = list(favvv[x].split("|"))
                            number = values[0]
                            link = values[1]
                            des += f"{srno}. [**{x}**]({link}) - {number} plays\n"
                            srno += 1

                        favv = discord.Embed(
                            description=des, color=random.choice(colour)
                        )
                        favv.set_thumbnail(url=thumbnail_image)
                        favv.set_author(
                            name=f"{ctx.author}'s top {artist} songs",
                            url=f"https://www.last.fm/user/{lu}",
                            icon_url=ctx.author.avatar.url,
                        )
                        # np.add_field(name = f"[{ctx.author}'s top {artist} songs](https://www.last.fm/user/{lu})", value = des)
                        await mess.remove_reaction(
                            "<a:loading:894978191331041371>", self.client.user
                        )
                        await mess.edit(content=None, embed=favv)
                    except:
                        await mess.add_reaction("<:Timesup:879423783063150642>")
                        await mess.remove_reaction(
                            "<a:loading:894978191331041371>", self.client.user
                        )
                if reaction.emoji.id == 880034051765977149:
                    await mess.remove_reaction(
                        "<:artistinfo:880034051765977149>", ctx.author
                    )
                    await mess.add_reaction("<a:loading:894978191331041371>")
                    try:
                        summary = fd["artist"]["summary"]
                        summary = list(
                            summary.split('<a href="https://www.last.fm/music/')
                        )
                        summary1 = str(summary[-1])[:-26]
                        summary2 = f"{summary[0]} \n Read More On [last.fm](https://www.last.fm/music/{summary1})"
                        artistinfo = discord.Embed(
                            title=f"{str(artist).capitalize()}'s info",
                            description=summary2,
                            color=random.choice(colour),
                        )
                        await mess.remove_reaction(
                            "<a:loading:894978191331041371>", self.client.user
                        )
                        await mess.edit(content=None, embed=artistinfo)
                    except:
                        await mess.add_reaction("<:Timesup:879423783063150642>")
                        await mess.remove_reaction(
                            "<a:loading:894978191331041371>", self.client.user
                        )
                if reaction.emoji.id == 886551866027167784:
                    await mess.remove_reaction(
                        "<:topartist:886551866027167784>", ctx.author
                    )
                    await mess.add_reaction("<a:loading:894978191331041371>")
                    try:
                        if topartist == True:
                            lastfmclass.topartists()
                            topartist = False
                        ar = ""
                        va = ""
                        y = 1
                        for x in fd["topartists"]:
                            ar += f"{y}. {x}\n"
                            va += f"{fd['topartists'][x]}\n"
                            y += 1
                        top = discord.Embed(
                            title=f"{ctx.author}'s top artists",
                            color=random.choice(colour),
                        )
                        top.add_field(name="Artists", value=ar)
                        top.add_field(name="Playcount", value=va)
                        await mess.remove_reaction(
                            "<a:loading:894978191331041371>", self.client.user
                        )
                    except:
                        await mess.add_reaction("<:Timesup:879423783063150642>")
                        await mess.remove_reaction(
                            "<a:loading:894978191331041371>", self.client.user
                        )
                    await mess.edit(content=None, embed=top)
            # asyncio.TimeoutError
            except asyncio.TimeoutError:
                await mess.add_reaction("<:Timesup:879423783063150642>")
                # await mess.remove_reaction("<:stats:879373496617156618>", self.client.user)
                break

        # to prevent the data of the previous artist to get mixed with the new data in case the new artist's data isn't enough
        fd = {}


def setup(client):
    client.add_cog(Lastfm(client))
