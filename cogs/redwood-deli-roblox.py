import discord
import datetime
import os
import roblox

from discord.ext import commands
from dotenv import load_dotenv
from roblox import Client

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

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RobloxConnectionCog(bot))