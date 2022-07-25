import discord

from discord.ext import commands

class ExtraCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name='ping', description='Get the ping of the bot')
    @commands.guild_only()
    async def ping_command(self, ctx: commands.Context):
        await ctx.send("Pong!")
        pass

    @commands.hybrid_command(name="source", description="Get the source code for Redwood Deli")
    @commands.guild_only()
    async def sourcecode(self, ctx: commands.Context):
        await ctx.send("Check out the source code for Redwood Deli and help add to the bot here: https://github.com/LIPDProductionsInc/Redwood-Deli")
        pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExtraCommandsCog(bot))