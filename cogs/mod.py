import discord
from discord.ext import commands

# kick, ban, add_role, userinfo, warn, warnings, unmute, mute
guild_ids = [697493731611508737, 772678294692429865, 769789003230216212]


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("mod.py is running")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member):
        """To kick a particular user
```fkick <user.mention>```"""
        await member.kick()
        await ctx.send(f"{member.name} has been kicked by {ctx.author.name}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member):
        await member.ban()
        await ctx.send(f"{member.name} has been banned by {ctx.author.name}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_role(ctx, role: discord.Role, user: discord.User = None):
        if user == None:
            user = ctx.author
        await user.add_roles(role)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def userinfo(self, ctx, member: discord.Member):
        created_at = member.created_at.strftime("%b %d, %Y")
        joined_at = member.joined_at.strftime("%b %d, %Y")
        x = ctx.guild.members
        if member in x:
            roles = [role for role in member.roles]
        if not member:
            member = ctx.message.author
        perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
        hmm = ", ".join([str(element) for element in perm_list])
        roles = member.roles
        embed = discord.Embed(
            title="User Info",
            description=(member.display_name),
            timestamp=ctx.message.created_at,
        )
        embed.add_field(name="User ID", value=member.id)
        embed.add_field(name="Joined discord on", value=created_at)
        embed.add_field(name="Joined this server on", value=joined_at)
        embed.add_field(name="Roles", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Bot?", value=member.bot)
        embed.add_field(name="Permissions", value=hmm)
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url="https://cdn.discordapp.com/avatars/720602862622736425/3ef604388ab08477fd8c57bdb797f122.png",
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason=None):
        message = await ctx.send(member)
        if ctx.channel.permissions_for(ctx.author).administrator is True:
            if member == None:
                await message.edit(
                    content="The value of the member is not defined. Please try again"
                )
                return
            if reason == None:
                member = member.nick
                await message.edit(
                    content="""Please mention the reason too
    ```f.warn <user> <reason>```"""
                )
                reason = "No reason given"
            else:
                await message.channel.send(f"The member has been warned for {reason}")
            warnsfile = open("warnsfile.txt", "a+")
            warnsfile.write(
                f"WarningID:{str(ctx.message.id)}{str(ctx.guild.id)} | User: {(member.display_name)} . {str(ctx.author.discriminator)} . {str(member.id)} | Reason: {reason}\n"
            )
        else:
            await ctx.send("You do not have the permission to use this command")

    @commands.command(aliases=["infractions"])
    @commands.has_permissions(administrator=True)
    async def warnings(self, message, member1: discord.Member = None):
        # embed = discord.Embed(title='Warnings')
        if member1 == None:
            await message.edit(
                content="The value of the member is not defined. Please try again"
            )
        else:
            warnings = []
            f = open("warnsfile.txt", "r")
            mylines = f.readlines()
            for line1 in mylines:
                if str(member1.id) in line1:
                    warnings.append(line1)
            w = discord.Embed(
                title=f"{member1.name}'s Infractons",
                timestamp=message.created_at,
                color=discord.Color.Random(),
            )
            y = 1
            for x in warnings:
                while y - 1 < len(x) - 1:
                    w.add_field(name=y, value=warnings[y - 1])
                    y += 1
            await message.send(embed=w)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(member.guild.roles, name="Muted")
        await member.remove_roles(role)
        embed = discord.Embed(
            title="User Unuted!",
            description="**{0}** was unmuted by **{1}**!".format(
                member, ctx.message.author
            ),
        )
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def modmailresponse(self, ctx, userid: int, *, msg):
        user = self.client.get_user(userid)
        await user.send(msg)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member):
        role = discord.utils.get(member.guild.roles, name="Muted")
        await member.add_roles(role)
        embed = discord.Embed(
            title="User Muted!",
            description="**{0}** was muted by **{1}**!".format(
                member, ctx.message.author
            ),
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Mod(client))
