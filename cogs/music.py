import discord
from discord.ext import commands
import pychord

# need to add transpose to it (for capo) (pychord.transpose)

colour = [0xDC143C, 0xD35400, 0x48C9B0, 0x7FB3D5, 0xFFA0A2]

guild_ids = [697493731611508737, 772678294692429865, 769789003230216212]


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("music.py is running")

    @commands.command(aliases=["ch"])
    async def chord(self, ctx, chord: str = "C"):
        chord = pychord.Chord(chord)
        embed = discord.Embed(
            title=f"<a:badge:908591430879027201> {chord} Chord",
            description="<a:lines:908590724688248833><a:lines:908590724688248833><a:lines:908590724688248833><a:lines:908590724688248833><a:lines:908590724688248833><a:lines:908590724688248833><a:lines:908590724688248833>",
        )
        try:
            filePath = f"chordimages/{chord}.png"
            file = discord.File(filePath)
            embed.set_image(url=f"attachment://chordimages/{chord}.png")
        except:
            pass
        components = " ".join([str(element) for element in chord.components()])
        embed.add_field(
            name="<a:dot:908591431445266452> Components", value=f"**`{components}`**"
        )
        info = chord.info()

        if "maj" in info[1]:
            qualities = list(info[1].split("maj"))
            quality = f"Major {qualities[-1]}"
        else:
            quality = "Major"
        print(type(info[1]))

        embed.add_field(
            name="<a:dot:908591431445266452> Quality",
            value=f"**`{quality}`**",
            inline=False,
        )
        # quality = quality_tags[info[1]]
        # if info[2] ==
        # await ctx.send(info[1])

        await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
