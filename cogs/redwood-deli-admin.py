import discord
import asyncio
import datetime
import os

from discord import commands
from dotenv import load_dotenv
load_dotenv()

class AdminCog(commands.Cog, name="Admin Cog"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name="ban", description="Ban a user from the server")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban_command(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        channel = ctx.bot.get_channel(os.getenv("LogChannel"))
        await member.ban(reason=reason)
        embed=discord.Embed(
            colour=discord.Color.green(),
            description=f''':white_check_mark: ***{member} was banned*** | {reason}'''
            )
        embed2=discord.Embed(
            colour=discord.Color.red()
            )
        embed2.set_author(name=f"Ban | {member}", icon_url=member.avatar_url)
        embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True).add_field(name="Reason", value=f"{reason}", inline=True)
        embed2.set_footer(text=f"ID: {member.id}")
        embed2.timestamp=datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        await channel.send(embed=embed2)
        pass

    @commands.command(name="kick", description="Kick a user from the server")
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick_command(self, ctx: commands.Context, member: discord.Member, *, reason: str = None):
        channel = ctx.bot.get_channel(os.getenv("LogChannel"))
        await member.kick(reason=reason)
        embed=discord.Embed(
            colour=discord.Color.green(),
            description=f''':white_check_mark: ***{member} was kicked*** | {reason}'''
            )
        embed2=discord.Embed(
            colour=discord.Color.red()
            )
        embed2.set_author(name=f"Kick | {member}", icon_url=member.avatar_url)
        embed2.add_field(name="User", value=f"{member.mention}", inline=True).add_field(name="Moderator", value=f"{ctx.author.mention}", inline=True).add_field(name="Reason", value=f"{reason}", inline=True)
        embed2.set_footer(text=f"ID: {member.id}")
        embed2.timestamp=datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        await channel.send(embed=embed2)
        pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))