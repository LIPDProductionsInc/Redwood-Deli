import discord
import datetime

from discord.ext import commands

class ExtraCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name='ping', description='Get the ping of the bot')
    @commands.guild_only()
    async def ping_command(self, ctx: commands.Context):
        embed=discord.Embed(
            title='ROOM SEALER PINGS :ping_pong:',
            type='rich',
            colour=discord.Color(0xFF9E00),
            description=f'''Pong!
Bot Ping: **{round(self.bot.latency * 1000)}**ms'''
            )
        embed.set_footer(text=f"Developed by {self.bot.owner}")
        embed.timestamp=datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        pass

    @commands.hybrid_command(name="source", description="Get the source code for Redwood Deli")
    @commands.guild_only()
    async def sourcecode(self, ctx: commands.Context):
        await ctx.send("Check out the source code for Redwood Deli and help add to the bot here: https://github.com/LIPDProductionsInc/Redwood-Deli")
        pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExtraCommandsCog(bot))