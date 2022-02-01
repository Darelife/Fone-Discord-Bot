import discord
from discord.ext import commands
import os
import requests
from datetime import datetime
from urllib.request import urlopen
import urllib.parse
import re
import json
import aiohttp
import random
from bs4 import BeautifulSoup
import asyncio
import personal

colour = personal.colour


class Api(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is running")

    @commands.command(aliases=["m"])
    # @commands.cooldown(rate=1, per=30)
    async def movie(self, ctx, *, movie):
        # jd - imdb
        # js - tmdb regular
        # jv - tmdb videos
        # jr - tmdb recommendations
        # jsi - tmdb similar movies
        url = "https://imdb8.p.rapidapi.com/auto-complete"

        api = os.environ["x-rapidapi-key_movie"]

        headers = {"x-rapidapi-key": api, "x-rapidapi-host": "imdb8.p.rapidapi.com"}
        movie.replace(" ", "_")
        querystring = {"q": movie}
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)
        data = response.text
        data1 = json.loads(data)
        with open("moviedata.json", "w") as f:
            f.write(str(data1))
        color = random.choice(colour)
        listm = discord.Embed(
            title=f"Movie Search Query : {movie.capitalize()}",
            description=f"<@!{ctx.author.id}> Please type the number preceding the movie you want to know about",
            color=color,
            timestamp=ctx.message.created_at,
        )
        number = 1
        title_number = 1
        for x in data1["d"]:
            listm.add_field(
                name=f'{title_number}) {x["l"]}',
                value=f"""id : {x['id'][2:]} • rank : {x['rank']}
""",
                inline=False,
            )
            title_number += 1
            number += 1
            if number == 11:
                break
        # (1)
        mess = await ctx.send(embed=listm)

        def check(m):
            try:
                a = int(m.content)
                return m.channel == ctx.channel
            except:
                pass

        msg = await self.client.wait_for("message", check=check)
        await ctx.channel.trigger_typing()
        a = int(msg.content) - 1
        await msg.delete()
        newcolor = random.choice(colour)
        jd = data1["d"][a]
        movapilink = os.environ["movieapilink"]
        imdblink = f"https://www.imdb.com/title/{jd['id']}/"
        try:
            html = requests.get(imdblink).content
            data1 = BeautifulSoup(html, "html.parser")
            with open("testmov.txt", "w") as f:
                f.write(str(data1))
            parent1 = data1.find("body").find(
                "div", attrs={"class": "credit_summary_item"}
            )
            directorlist = list(str(parent1).split(">"))
            director1 = directorlist[4]
            director = director1[:-3]
        except:
            pass
        link = f"https://api.themoviedb.org/3/find/{jd['id']}{movapilink}"
        print(link)
        try:
            with urlopen(link) as m:
                data10 = json.load(m)
            js = data10["movie_results"][0]
            original_lang = js["original_language"]
            # ("original lang", original_lang)
            tmbd_id = js["id"]
            poster_path = js["poster_path"]
            # ("posterpath", poster_path)
            rating = js["vote_average"]
            # ("vote avg", rating)
            overview = js["overview"]
            # ("overview", overview)
            release_date = js["release_date"]
            # ("release_date", release_date)
            total_votes = js["vote_count"]
            # ("vote count", total_votes)
            backdrop_path = js["backdrop_path"]
            # ("backdrop_path", backdrop_path)
            adult = js["adult"]
            rec_link2 = os.environ["recommendation"]

        except:
            pass

        def genre(n):
            n = int(n)
            if n == 28:
                return "Action"
            if n == 12:
                return "Adventure"
            if n == 16:
                return "Animation"
            if n == 35:
                return "Comedy"
            if n == 80:
                return "Crime"
            if n == 99:
                return "Documentary"
            if n == 18:
                return "Drama"
            if n == 10751:
                return "Family"
            if n == 14:
                return "Fantasy"
            if n == 36:
                return "History"
            if n == 27:
                return "Horror"
            if n == 10402:
                return "Music"
            if n == 9648:
                return "Mystery"
            if n == 10749:
                return "Romance"
            if n == 878:
                return "Science Fiction"
            if n == 10770:
                return "TV Movie"
            if n == 53:
                return "Thriller"
            if n == 10750:
                return "War"
            if n == 37:
                return "Western"

        try:
            genres = []
            for x in js["genre_ids"]:
                genres.append(genre(x))
            genre = " • ".join([str(element) for (element) in genres])
            if "<function Api.movie.<locals>.genre at 0x7faa52d0cdc0>" == str(genre):
                genre = "Couldn't find the genre"
        except:
            pass
        try:
            rank = jd["rank"]
        except:
            pass
        try:
            stars = jd["s"]
        except:
            pass
        try:
            mov = discord.Embed(
                title=f'({a+1}) {jd["l"]}',
                description=overview,
                timestamp=ctx.message.created_at,
                color=newcolor,
            )
        except:
            mov = discord.Embed(
                title=f'({a}) {jd["l"]}',
                description="Couldn't find the movie overview",
                timestamp=ctx.message.created_at,
                color=newcolor,
            )
        mov.set_author(
            icon_url="https://ancpr.org/wp-content/uploads/2019/12/imdb.png",
            name="IMDB",
            url=imdblink,
        )
        try:
            mov.add_field(name="Genre", value=genre, inline=False)
        except:
            pass
        try:
            mov.add_field(name="Rank", value=rank, inline=False)
        except:
            pass
        try:
            mov.add_field(name="Starring", value=stars)
        except:
            pass
        try:
            mov.add_field(name="Director", value=director)
        except:
            pass
        try:
            mov.add_field(name="Rating", value=f"{rating} from {total_votes} votes")
        except:
            pass
        try:
            mov.add_field(name="Original Language", value=original_lang.upper())
        except:
            pass
        try:
            if adult == False:
                adult = "No"
            else:
                adult = "Yes"
        except:
            pass
        try:
            mov.add_field(name="Is It R-Rated?", value=adult)
        except:
            pass
        try:
            mov.set_image(url=f"https://image.tmdb.org/t/p/w500/{backdrop_path}")
        except:
            pass
        try:
            videoapi = os.environ["videosmovie"]
            # https://api.themoviedb.org/3/movie/353081
            vidslink = f"https://api.themoviedb.org/3/movie/{tmbd_id}{videoapi}"
            with urlopen(vidslink) as m:
                datavid = json.load(m)
            jv = datavid["results"][0]
            video_id = jv["key"]
            mov.add_field(
                name="Video",
                value=f"[`Youtube Link`](https://www.youtube.com/watch?v={video_id})",
                inline=False,
            )
        except:
            pass
        try:
            mov.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500/{poster_path}")
        except:
            pass
        try:
            mov.add_field(name="Release Date", value=release_date)
        except:
            pass
        try:
            mov.set_footer(
                text=f"Requested by {ctx.author}, Powered By TMDB and IMDB",
                icon_url=ctx.author.avatar.url,
            )
        except:
            pass
        await mess.edit(embed=mov)
        await mess.add_reaction("<:Movie:843078309352570920>")
        await mess.add_reaction("<:Recommendations:843714124374605894>")
        await mess.add_reaction("<:SimilarMovies:843714124189794325>")
        await mess.add_reaction("<:Credits:843714124600967178>")

        # my recommendation embed
        recommendation_link = f"https://api.themoviedb.org/3/movie/{tmbd_id}{rec_link2}"
        print(recommendation_link)
        try:
            with urlopen(recommendation_link) as m:
                datarec = json.load(m)
            jr = datarec["results"][0]
        except:
            pass
        try:
            adult = jr["adult"]
        except:
            pass
        try:
            back = jr["backdrop_path"]
        except:
            pass
        try:
            genres = []
            for x in jr["genre_ids"]:
                genres.append(genre(x))
            genre_rec = " • ".join([str(element) for (element) in genres])
            if "<function Api.movie.<locals>.genre at 0x7faa52d0cdc0>" == str(genre):
                genre_rec = "Couldn't find the genre"
        except:
            pass
        try:
            title = jr["title"]
        except:
            pass
        try:
            lang = (jr["original_language"]).upper()
        except:
            pass
        try:
            overview = jr["overview"]
        except:
            pass
        try:
            poster = jr["poster_path"]
        except:
            pass
        try:
            budget = jr["budget"]
        except:
            pass
        try:
            adult = jr["adult"]
            if adult == False:
                adult = "No"
            else:
                adult = "Yes"
        except:
            pass
        try:
            poster_path_rec = f'https://image.tmdb.org/t/p/w500/{jr["poster_path"]}'
        except:
            pass
        try:
            backdrop_path = f'https://image.tmdb.org/t/p/w500/{jr["backdrop_path"]}'
        except:
            pass
        try:
            homepage = jr["homepage"]
        except:
            pass
        try:
            status = jr["status"]
        except:
            pass
        try:
            tagline = jr["tagline"]
        except:
            pass
        try:
            release = jr["release_date"]
        except:
            pass
        try:
            vote = f"{jr['vote_average']} from {jr['vote_count']}"
        except:
            pass
        recc = discord.Embed(
            title=f"Recommendation",
            description=f"More Movies Like {jd['l']}",
            color=random.choice(colour),
        )
        try:
            recc.add_field(name=title, value=overview)
        except:
            pass
        try:
            recc.add_field(name="Tagline", value=tagline, inline=False)
        except:
            pass
        try:
            recc.add_field(name="Genre", value=genre_rec, inline=False)
        except:
            pass
        try:
            recc.add_field(name="Status", value=status, inline=True)
        except:
            pass
        try:
            recc.add_field(name="Votes", value=vote, inline=True)
        except:
            pass
        try:
            recc.add_field(name="Budget", value=budget, inline=False)
        except:
            pass
        try:
            recc.add_field(
                name="Homepage Link", value=f"[Homepage Link]({homepage})", inline=True
            )
        except:
            pass
        try:
            recc.add_field(name="Date Of Release", value=release)
        except:
            pass
        try:
            recc.add_field(name="Language", value=lang, inline=True)
        except:
            pass
        try:
            if backdrop_path.startswith("http"):
                recc.set_image(url=backdrop_path)
        except:
            pass
        try:
            if poster_path.startswith("http"):
                print(poster_path_rec)
                recc.set_thumbnail(url=poster_path_rec)
        except:
            pass

        # similar movies embed
        try:
            similarapilink = os.environ["similarmoviesapi"]
            linksim = f"https://api.themoviedb.org/3/movie/{tmbd_id}{similarapilink}"
            with urlopen(linksim) as m:
                datasim = json.load(m)
            jsi = datasim["results"][0]
        except:
            pass
        try:
            s_adult = jsi["adult"]
            if s_adult == False:
                s_adult = "No"
            elif s_adult == True:
                s_adult = "Yes"
        except:
            pass
        try:
            s_backdrop = f"https://image.tmdb.org/t/p/w500/{jsi['backdrop_path']}"
        except:
            pass
        try:
            s_id = jsi["id"]
        except:
            pass
        try:
            s_lang = jsi["original_language"]
        except:
            pass
        try:
            s_title = jsi["original_title"]
        except:
            pass
        try:
            s_overview = jsi["overview"]
        except:
            pass
        try:
            s_poster = f"https://image.tmdb.org/t/p/w500/{jsi['poster_path']}"
        except:
            pass
        try:
            s_release = jsi["release_date"]
        except:
            pass
        try:
            vote = f"{jsi['vote_average']} from {jsi['vote_count']}"
        except:
            pass
        try:
            s = discord.Embed(
                title=s_title, description=s_overview, color=random.choice(colour)
            )
        except:
            pass
        try:
            s.set_author(
                name="Similar Movies",
                icon_url="https://i.pinimg.com/favicons/7951fa82068a0eb2399e656e8ae8770d7dce814f72d5c20c5cb224e5.png?e86714ddd80dcd75c0fce447cd2bc6a1",
                url=f"https://www.themoviedb.org/movie/{s_id}",
            )
        except:
            pass
        try:
            s.set_iamge(url=s_backdrop)
        except:
            pass
        try:
            s.set_thumbnail(url=s_poster)
        except:
            pass
        try:
            s.add_field(name="Original Language", value=s_lang.capitalize())
        except:
            pass
        try:
            s.add_field(name="Release Date", value=s_release)
        except:
            pass
        try:
            s.add_field(name="Movie Id", value=s_id)
        except:
            pass
        try:
            genres = []
            for x in jsi["genre_ids"]:
                genres.append(genre(x))
            s_genre = " • ".join([str(element) for (element) in genres])
            if "<function Api.movie.<locals>.genre at 0x7faa52d0cdc0>" == str(genre):
                s_genre = "Couldn't find the genre"
        except:
            pass
        try:
            s.add_field(name="Genre", value=s_genre)
        except:
            pass

        # credits embed

        creditslink = os.environ["CreditsLink"]

        with urlopen(
            f"https://api.themoviedb.org/3/movie/{tmbd_id}/{creditslink}"
        ) as f:
            creditsjs = json.load(f)
        jc = creditsjs["cast"]
        credits = discord.Embed(title="Credits", description="The Credits of the movie")
        num = 1
        text = ""
        for x in jc:
            credits.add_field(name=x["name"], value=x["character"], inline=False)
            num += 1
            if num == 10:
                text = len(jc) - 10
                break
        credits.set_footer(text=f"And {text} more")

        while True:

            def check(reaction, user):
                # if reaction.emoji.id == 779554066082299954:
                #  print("nice")
                return user == ctx.author

            try:
                reaction, user = await self.client.wait_for(
                    "reaction_add", check=check, timeout=60
                )

                if reaction.emoji.id == 843714124189794325:
                    await mess.remove_reaction(
                        "<:SimilarMovies:843714124189794325>", ctx.author
                    )
                    await mess.edit(embed=s)
                elif reaction.emoji.id == 843714124374605894:
                    await mess.remove_reaction(
                        "<:Recommendations:843714124374605894>", ctx.author
                    )
                    await mess.edit(embed=recc)
                elif reaction.emoji.id == 843078309352570920:
                    await mess.remove_reaction(
                        "<:Movie:843078309352570920>", ctx.author
                    )
                    await mess.edit(embed=mov)
                elif reaction.emoji.id == 843714124600967178:
                    await mess.remove_reaction(
                        "<:Credits:843714124600967178>", ctx.author
                    )
                    await mess.edit(embed=credits)
            except asyncio.TimeoutError:
                await mess.remove_reaction(
                    "<:SimilarMovies:843714124189794325>", self.client.user
                )
                await mess.remove_reaction(
                    "<:Credits:843714124600967178>", self.client.user
                )
                await mess.remove_reaction(
                    "<:Recommendations:843714124374605894>", self.client.user
                )
                await mess.remove_reaction(
                    "<:Movie:843078309352570920>", self.client.user
                )
                break

    @commands.command()
    async def weather(self, ctx, *, city: str):

        api_key = os.environ["weatherapi"]
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        complete_url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={api_key}"
        )
        response = requests.get(complete_url)
        data = response.json()
        hmm = []
        ok = []
        for (key, value) in data.items():
            a = (key, value)
            hmm.append(a)
        sunrise_time = hmm[8]
        sunrise = "".join([str(element) for element in sunrise_time])
        ye = sunrise.split(":")
        yeye = ye[5]
        woah = yeye[:-1]
        b = data["main"]["temp"]
        oke = ok.append(b)
        x = response.json()
        channel = ctx.message.channel
        if x["cod"] != "404":
            try:
                async with channel.typing():
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_temperature_celsiuis = str(
                        round(current_temperature - 273.15)
                    )
                    current_pressure = y["pressure"]
                    current_humidity = y["humidity"]
                    current_visibility = x["visibility"]
                    weather_feelslike = y["feels_like"]
                    current_feelslike_celsiuis = str(round(weather_feelslike - 273.15))
                    # sunrise = x["sunrise"]
                    # print(sunrise)
                    z = x["weather"]
                    # sunrise = x["sunrise"]
                    # hmm1 = (datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S'))
                    dateStr = datetime.fromtimestamp(int(woah)).strftime(
                        "%A, %B %d, %Y %I:%M:%S"
                    )
                    weather_description = str(z[0]["description"])
                    # weather_description = z[0]["description"]
                    if str(weather_description) == "clear sky":
                        yeah = "https://media.discordapp.net/attachments/789671664069247007/800901800801599538/clearsky_1.png"
                    elif str(weather_description) == "mist":
                        yeah = "https://static.thenounproject.com/png/729219-200.png"
                    elif str(weather_description) == "haze":
                        yeah = "https://o.remove.bg/downloads/e0a45f8f-374f-410b-8a29-406461ffa6ef/image-removebg-preview.png"
                    elif str(weather_description) == "broken clouds":
                        yeah = "https://static.thenounproject.com/png/259207-200.png"
                    else:
                        yeah = "https://i.ibb.co/CMrsxdX/weather.png"
                    embed = discord.Embed(
                        title=f"Weather in {city_name}",
                        color=ctx.guild.me.top_role.color,
                        timestamp=ctx.message.created_at,
                    )
                    embed.add_field(
                        name="Descripition",
                        value=f"**{weather_description}**",
                        inline=False,
                    )
                    embed.add_field(
                        name="Temperature(C)",
                        value=f"**{current_temperature_celsiuis}°C**",
                        inline=False,
                    )
                    embed.add_field(
                        name="Feels Like",
                        value=f"**{current_feelslike_celsiuis}°C**",
                        inline=False,
                    )
                    embed.add_field(
                        name="Humidity(%)",
                        value=f"**{current_humidity}%**",
                        inline=False,
                    )
                    embed.add_field(
                        name="Visibility",
                        value=f"**{current_visibility}**",
                        inline=False,
                    )
                    embed.add_field(
                        name="Atmospheric Pressure(hPa)",
                        value=f"**{current_pressure}hPa**",
                        inline=False,
                    )
                    embed.add_field(
                        name="Sunrise", value=f"**{dateStr}**", inline=False
                    )
                    embed.set_thumbnail(url=yeah)
                    embed.set_footer(text=f"Requested by {ctx.author.name}")
                    await ctx.channel.send(embed=embed)
            except:
                await ctx.channel.send("City Not Found")
        else:
            await ctx.channel.send("City not found.")

    @commands.command()
    async def chess(self, ctx, user=None):
        if user == None:
            await ctx.send("please specify a user")
        else:
            link = f"https://api.chess.com/pub/player/{user}"
            with urlopen(link) as m:
                data = json.load(m)
            url = data["url"]
            username = data["username"]
            playerid = data["player_id"]
            followers = data["followers"]
            countryurl = data["country"]
            lastonlineunix = data["last_online"]
            lastonline = datetime.utcfromtimestamp(int(lastonlineunix)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            lastonlinel = list(str(lastonline).split(" "))
            lastonline = f"{lastonlinel[0]}\n{lastonlinel[1]} GMT"
            startedunix = data["joined"]
            started = datetime.utcfromtimestamp(int(startedunix)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            startedl = list(str(started).split(" "))
            started = f"{startedl[0]}\n{startedl[1]} GMT"
            e = discord.Embed(title=f"{username}'s profile", url=url)
            try:
                avatar = data["avatar"]
                e.set_thumbnail(url=avatar)
            except:
                avatar = "https://images-ext-1.discordapp.net/external/7T-Q82uzf0RYcZDU6xMtvEbf6GPYvJQj87Okf8kqSLI/https/play-lh.googleusercontent.com/ngTyk7oHMyHgdaDLWJ7iJ_CtvZvjU5pYn-bugNpGOrzxjNU4dxIavkoeP4F0Zao2HQ?width=480&height=480"
                e.set_thumbnail(url=avatar)
            e.add_field(name="Joined", value=started, inline=False)
            e.add_field(name="Last Online", value=lastonline)
            countr = list(countryurl.split("/"))
            countr = countr[-1]
            e.add_field(
                name="Others",
                value=f"[`{countr}`]({countryurl}) • {followers} followers  • Id:{playerid}",
                inline=False,
            )
            link = f"https://api.chess.com/pub/player/{user}/stats"
            with urlopen(link) as m:
                data = json.load(m)
            cr = ""
            crlast = "**Last** : "
            crlastlist = []
            crlastb = False
            crbest = "**Best** : "
            crbestlist = []
            crbestb = False
            try:
                cr_lastrating = data["chess_rapid"]["last"]["rating"]
                crlastlist.append(f"Rating : {cr_lastrating} ")
                crlastb = True
            except:
                pass
            try:
                cr_bestrating = data["chess_rapid"]["best"]["rating"]
                crbestlist.append(f"Rating : {cr_bestrating} ")
                crbestb = True
            except:
                pass
            try:
                cr_lastgame = data["chess_rapid"]["last"]["game"]
                crlastlist.append(f"Last Game : [`Gamelink`]({cr_lastgame}) ")
                crlastb = True
            except:
                pass
            try:
                cr_bestgame = data["chess_rapid"]["best"]["game"]
                crbestlist.append(f"bestgame : [`Gamelink`]({cr_bestgame}) ")
                crbestb = True
            except:
                pass
            cr_wld = ""
            crwldlist = []
            cr_wldb = False
            try:
                cr_wins = data["chess_rapid"]["record"]["win"]
                crwldlist.append(f"{cr_wins} wins")
                cr_wldb = True
            except:
                pass
            try:
                cr_loss = data["chess_rapid"]["record"]["loss"]
                crwldlist.append(f"{cr_loss} losses")
                cr_wldb = True
            except:
                pass
            try:
                cr_draw = data["chess_rapid"]["record"]["draw"]
                crwldlist.append(f"{cr_draw} draws")
                cr_wldb = True
            except:
                pass
            crb = False
            if crlastb == True:
                crlast = " • ".join([str(elem) for elem in crlastlist])
                crlast = f"Last Game -> {crlast}"
                cr += f"{crlast}\n"
                crb = True
            if crbestb == True:
                crbest = " • ".join([str(elem) for elem in crbestlist])
                crbest = f"Best Game -> {crbest}"
                cr += f"{crbest}\n"
                crb = True
            if cr_wldb == True:
                crwld = " • ".join([str(elem) for elem in crwldlist])
                crwld = f"Data -> {crwld}"
                cr += f"{crwld}\n"
                crb = True

            if crb == True:
                e.add_field(name="Chess Rapid", value=cr)
            await ctx.send(embed=e)

    @commands.command()
    async def youtube(self, ctx, *, search):

        query_string = urllib.parse.urlencode({"search_query": search})
        htm_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string
        )
        search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())

        await ctx.send("http://www.youtube.com/watch?v=" + search_results[0])

    @commands.command()
    async def youtube_r(self, ctx, number: int, *, search):
        if number < 5:
            query_string = urllib.parse.urlencode({"search_query": search})
            htm_content = urllib.request.urlopen(
                "http://www.youtube.com/results?" + query_string
            )
            search_results = re.findall(
                r"watch\?v=(\S{11})", htm_content.read().decode()
            )
            y = 0
            text = ""
            while y < number:
                text += (
                    f"<{y + 1}> http://www.youtube.com/watch?v={search_results[y]}\n"
                )
                y += 1
            await ctx.send(text)
        else:
            await ctx.send("Please enter a number below 5")

    @commands.command()
    async def link(self, ctx, link1):
        a = 0
        if link1.startswith("<"):
            link1 = link1[1:-1]
            print(link1)
            a = 1
        linkRequest = {"destination": link1, "domain": {"fullName": "rebrand.ly"}}

        api = os.environ["rebrandly_link_shortener"]

        requestHeaders = {
            "Content-type": "application/json",
            "apikey": api,
        }

        r = requests.post(
            "https://api.rebrandly.com/v1/links",
            data=json.dumps(linkRequest),
            headers=requestHeaders,
        )

        if r.status_code == requests.codes.ok:
            link = r.json()
            if a == 1:
                await ctx.channel.send(f'<https://{link["shortUrl"]}>')
            else:
                await ctx.channel.send(f'https://{link["shortUrl"]}')

    @commands.command()
    async def news(self, ctx, *, topic=None):
        api = os.environ["newsapi"]
        if topic == None:
            with urlopen(
                f"https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey={api}"
            ) as cu:
                data = json.load(cu)

            with open("news.json", "w") as f:
                json.dump(data, f, indent=2)
            with open("news.json") as f:
                news = json.load(f)
            x = random.randint(0, len(news["articles"]) - 1)
            a = news["articles"][x]
            author = a["author"]
            title = a["title"]
            description = a["description"]
            url = a["url"]
            url_image = a["urlToImage"]
            content = a["content"]
            embed = discord.Embed(
                title=title,
                description=description,
                timestamp=ctx.message.created_at,
                url=url,
                color=random.choice(colour),
            )
            embed.add_field(name="Content", value=content)
            embed.set_image(url=url_image)
            embed.set_footer(
                text=f"Requested by {ctx.author} | story by {author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.channel.send(embed=embed)
        elif topic != None:
            topic = topic.replace(" ", "+")
            print(topic)
            with urlopen(
                f"https://newsapi.org/v2/everything?q={topic}&sortBy=popularity?language=en&apiKey={api}"
            ) as cu:
                data = json.load(cu)

            with open("news.json", "w") as f:
                json.dump(data, f, indent=2)
            with open("news.json") as f:
                news = json.load(f)
            x = random.randint(0, len(news["articles"]) - 1)
            a = news["articles"][x]
            author = a["author"]
            title = a["title"]
            description = a["description"]
            url = a["url"]
            url_image = a["urlToImage"]
            content = a["content"]
            embed = discord.Embed(
                title=title,
                description=description,
                timestamp=ctx.message.created_at,
                url=url,
                color=random.choice(colour),
            )
            embed.add_field(name="Content", value=content)
            embed.set_image(url=url_image)
            embed.set_footer(
                text=f"Requested by {ctx.author} | story by {author}",
                icon_url=ctx.author.avatar.url,
            )
            await ctx.channel.send(embed=embed)

    @commands.command(pass_context=True)
    async def meme(self, ctx):
        embed = discord.Embed(title="", description="")
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.reddit.com/r/memes/hot.json?sort=hot") as r:
                res = await r.json()
                meme = res["data"]["children"][random.randint(0, 25)]["data"]["url"]
                embed.set_image(url=meme)
                await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def memes(self, ctx, subreddit):
        embed = discord.Embed(title="", description="")
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                f"https://www.reddit.com/r/{subreddit}/new.json?sort=hot"
            ) as r:
                res = await r.json()
                embed.set_image(
                    url=res["data"]["children"][random.randint(0, 25)]["data"]["url"]
                )
                await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        with urlopen("https://dog.ceo/api/breeds/image/random") as cu:
            data = json.load(cu)
        image = data["message"]
        embed = discord.Embed(
            title="Here are some dog pics",
            description=f"<@!{ctx.author.id}>",
            timestamp=ctx.message.created_at,
            color=random.choice(colour),
        )
        embed.set_image(url=image)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def ip(self, ctx, ip):
        try:
            with urlopen(f"https://ipinfo.io/{ip}/geo") as cu:
                data = json.load(cu)
            city = data["city"]
            region = data["region"]
            country = data["country"]
            loc = data["loc"]
            postal = data["postal"]
            timezone = data["timezone"]
            embed = discord.Embed(
                title="Info Abt You through your IP address",
                description=f"""<@!{ctx.author.id}> :
        {ip}""",
                timestamp=ctx.message.created_at,
                color=random.choice(colour),
            )
            embed.add_field(name="City", value=city)
            embed.add_field(name="Region", value=region)
            embed.add_field(name="Coordinates", value=loc)
            embed.add_field(name="Postal Code", value=postal)
            embed.add_field(name="Timezone", value=timezone)
            embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
            )
            await ctx.author.send(embed=embed)
            await ctx.channel.send(f"IP details Dm'd to you <@!{ctx.author.id}>")
        except:
            await ctx.channel.send(
                f"Please enter a valid IP address <@!{ctx.author.id}>"
            )

    @commands.command(aliases=["cc"])
    async def currencyconvert(self, ctx, country1, country2, value):
        try:
            value = float(value)
            country1 = country1.upper()
            country2 = country2.upper()
            with open("us.json") as f:
                currency = json.load(f)
                val3 = float(currency["rates"][country1])
                nice = 1 / val3
                val4 = float(currency["rates"][country2])
                hmm = nice * val4 * value
                if hmm >= 1:
                    hmm = int(hmm)
                elif hmm < 1:
                    hmm = float(hmm)
                await ctx.channel.send(hmm)
        except:
            await ctx.channel.send("Please enter a valid currency id")

    @commands.command()
    async def covid19world(self, ctx):
        covid19_link = requests.get("https://www.worldometers.info/coronavirus/")
        soup = BeautifulSoup(covid19_link.content, features="html.parser")
        cases = soup.find("div", attrs={"class": "maincounter-number"}).text
        ct = soup.findAll("div", {"class": "maincounter-number"})
        cte = ct[1]
        recovery = ct[2]
        recoveries = recovery.text
        deaths = cte.text
        embed = discord.Embed(
            title=("Covid 19 cases in the world"), description=(cases)
        )
        embed.add_field(name="Number Of Deaths", value=(deaths))
        embed.add_field(name="Number Of Recoveries", value=(recoveries))
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def covid19(self, ctx, country):
        covid19_link = requests.get(
            f"https://www.worldometers.info/coronavirus/country/{country}/"
        )
        soup = BeautifulSoup(covid19_link.content, features="html.parser")
        cases = soup.find("div", attrs={"class": "maincounter-number"}).text
        ct = soup.findAll("div", {"class": "maincounter-number"})
        cte = ct[1]
        recovery = ct[2]
        recoveries = recovery.text
        deaths = cte.text
        embed = discord.Embed(
            title=(f"Covid 19 cases in {country}"), description=(cases)
        )
        embed.add_field(name="Number Of Deaths", value=(deaths))
        embed.add_field(name="Number Of Recoveries", value=(recoveries))
        embed.add_field(
            name="For more info, visit",
            value=(f"https://www.worldometers.info/coronavirus/country/{country}/"),
            inline=False,
        )
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def bitcoin(self, ctx, cur):
        with urlopen("https://api.coingecko.com/api/v3/exchange_rates") as cu:
            data = json.load(cu)
        cur = data["rates"][cur]
        name = cur["name"]
        unit = cur["unit"]
        value = cur["value"]
        typ = cur["type"]
        embed = discord.Embed(
            title="Value Of Bitcoin",
            description=name,
            timestamp=ctx.message.created_at,
            color=random.choice(colour),
        )
        embed.add_field(name="Unit Of The Currency", value=unit, inline=False)
        embed.add_field(name="Value", value=value, inline=False)
        embed.add_field(name="Type Of Currency", value=typ, inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def bored(self, ctx):
        with urlopen("https://www.boredapi.com/api/activity") as cu:
            data = json.load(cu)
        activity = data["activity"]
        typ = data["type"]
        embed = discord.Embed(
            title="Since you are bored",
            description=f"""<@!{ctx.author.id}> :
        {activity}""",
            timestamp=ctx.message.created_at,
            color=random.choice(colour),
        )
        embed.add_field(name="Type Of Activity", value=typ)
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def age(self, ctx, name: str):
        "attempts to predict your age based on the popularity of your name"
        with urlopen(f"https://api.agify.io?name={name}") as cu:
            data = json.load(cu)
        age = data["age"]
        embed = discord.Embed(
            title="Age Guess",
            description=f"""<@!{ctx.author.id}> :
        your age should probably be around {age}""",
            timestamp=ctx.message.created_at,
            color=random.choice(colour),
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=["movies", "mov"])
    async def movie2(self, ctx, *, movie):
        movie = movie.replace(" ", "%20")
        color = random.choice(colour)
        apilink = os.environ["movieapisearch"]
        with urlopen(f"{apilink}{movie}") as m:
            data = json.load(m)
        # (f"{apilink}{movie}")
        embed = discord.Embed(
            title=f"Movie Search Query : {movie.capitalize()}",
            description=f"<@!{ctx.author.id}> Please type the number preceding the movie you want to know about",
            color=color,
            timestamp=ctx.message.created_at,
        )
        # https://image.tmdb.org/t/p/w500/ -> for the image url
        number = 1
        titlenumber = 1
        for x in data["results"]:
            try:
                embed.add_field(
                    name=f'{titlenumber}) {x["title"]}',
                    value=f"""{x['id']} • {x['vote_average']}
{x['release_date'][:-6]}""",
                    inline=False,
                )
            except:
                embed.add_field(
                    name=f'{titlenumber}) {x["title"]}',
                    value=f"""{x['id']} • {x['vote_average']}
Date Of Release Not Found""",
                    inline=False,
                )
            number += 1
            titlenumber += 1
            if number == 11:
                break
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
        )
        message = await ctx.send(embed=embed)

        def check(m):
            try:
                a = int(m.content)
                return m.channel == ctx.channel
            except:
                pass

        msg = await self.client.wait_for("message", check=check)
        await ctx.channel.trigger_typing()
        a = int(msg.content) - 1
        await msg.delete()
        newcolor = random.choice(colour)
        jd = data["results"][a]
        embed2 = discord.Embed(
            title=jd["title"],
            description=jd["overview"],
            timestamp=ctx.message.created_at,
            color=newcolor,
        )
        try:
            embed2.add_field(name="Adult Content", value=jd["adult"])
        except:
            pass

        def genre(n):
            n = int(n)
            if n == 28:
                return "Action"
            if n == 12:
                return "Adventure"
            if n == 16:
                return "Animation"
            if n == 35:
                return "Comedy"
            if n == 80:
                return "Crime"
            if n == 99:
                return "Documentary"
            if n == 18:
                return "Drama"
            if n == 10751:
                return "Family"
            if n == 14:
                return "Fantasy"
            if n == 36:
                return "History"
            if n == 27:
                return "Horror"
            if n == 10402:
                return "Music"
            if n == 9648:
                return "Mystery"
            if n == 10749:
                return "Romance"
            if n == 878:
                return "Science Fiction"
            if n == 10770:
                return "TV Movie"
            if n == 53:
                return "Thriller"
            if n == 10750:
                return "War"
            if n == 37:
                return "Western"

        try:
            genres = []
            for x in jd["genre_ids"]:
                genres.append(genre(x))
            genree = " • ".join([str(element) for element in genres])
        except:
            pass
        try:
            embed2.add_field(name="Genre", value=genree, inline=False)
        except:
            pass
        try:
            embed2.add_field(
                name="Original Language", value=jd["original_language"], inline=False
            )
        # embed2.add_field(name = "Popularity", value = jd["popularity"])
        except:
            pass
        try:
            embed2.add_field(name="Release Date", value=jd["release_date"])
        except:
            embed2.add_field(name="Release Date", value="Not Found")

        try:
            embed2.add_field(
                name="Rating",
                value=f"{jd['vote_average']} from {jd['vote_count']} votes",
            )
        except:
            pass

        # try:
        #   embed2.add_field(name = "Director", value = director)
        # except:
        #   pass
        try:
            embed2.set_image(
                url=f"https://image.tmdb.org/t/p/w500{jd['backdrop_path']}"
            )
        except:
            pass
        try:
            embed2.set_thumbnail(
                url=f"https://image.tmdb.org/t/p/w500{jd['poster_path']}"
            )
        except:
            pass
        try:
            embed2.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
            )
        except:
            pass
        await message.edit(embed=embed2)


def setup(client):
    client.add_cog(Api(client))
