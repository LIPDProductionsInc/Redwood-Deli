import discord
import datetime
import os
import roblox

from discord import Embed, app_commands
from discord.ext import commands
from dotenv import load_dotenv
from roblox import Client
from roblox.bases.basegroup import BaseGroup

load_dotenv()
client = Client(os.getenv("RobloxToken"))

class RobloxConnectionCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name='test', hidden=True)
    @commands.is_owner()
    async def _test(self, ctx):
        user = await client.get_authenticated_user()
        await ctx.send(f'Logged in as {user.name}:{user.id}')
        pass

    @commands.hybrid_command(name='group', description="Display the ROBLOX group")
    @commands.guild_only()
    async def group_command(self, ctx: commands.Context):
        await ctx.send('The Redwood Bagels and Deli group can be found here: https://www.roblox.com/groups/15256757/Redwood-Bagels-and-Deli')
        pass

    @app_commands.command(name='roles', description= "See the group roles for promotion/demotion/dev stuff")
    @commands.has_any_role(993189120400691210, 993190740534509678, 993198036144640070, 993207728849825862)
    async def roles_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="REDWOOD BAGELS AND DELI GROUP ROLES AND IDs",
            colour=discord.Color.orange(),
            description="""
Group ID: 15256757

Owner: 255
The Bot (<@997771133287936111>): 254
General Manager: 253
Shift Manager: 252
Butcher: 4
Employee: 3
Trainee: 2
Citizen: 1"""
        )
        embed.set_footer(text="Developed by LIPD Producctions Inc.#1205")
        embed.timestamp=datetime.datetime.utcnow()
        await interaction.response.send_message(embed=embed, ephemeral=True)
        pass

    @commands.hybrid_command(name='rank', description="Changes someone's rank based on the rank number")
    @commands.has_any_role(993189120400691210,993190740534509678,993198036144640070)
    async def rank_comand(self, ctx: commands.Context, roblox_id: int, rank: int):
        user = await client.get_user(roblox_id)
        group = client.get_base_group(15256757)
        await group.set_rank(int(roblox_id), int(rank))
        if rank == 1:
            role = "Citizen"
        elif rank == 2:
            role = "Trainee"
        elif rank == 3:
            role = "Employee"
        elif rank == 4:
            role = "Butcher"
        elif rank == 252:
            role = "Shift Manager"
        elif rank == 253:
            role = "General Manager"
        channel = ctx.bot.get_channel(os.getenv("LogChannel"))
        embed = discord.Embed(
            title="RANK CHANGE",
            colour=discord.Color.dark_green(),
            description=f"""
**SUBJECT:**
{user.name}

**RANK CHANGED TO:**
{role}

**PERSON RESPONSIBLE:**
{ctx.author.mention}""")
        embed.set_footer(text=f'ID: {ctx.author.id}')
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(name=ctx.guild.name, icon_url=str(ctx.guild.icon))
        await channel.send(embed=embed)
        await ctx.send(f'Rank of {user.name} changed to {role}', ephemeral=True)
        pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RobloxConnectionCog(bot))