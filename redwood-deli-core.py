import discord
import asyncio
import datetime
import os
import random
import time

from discord import Guild, app_commands
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

class MyBot(commands.Bot):
    async def setup_hook(self):
        for extension in initial_extensions:
            await self.load_extension(extension)

bot = MyBot(command_prefix="!", help_command=None, case_insensitive=True, intents=discord.Intents.all(), fetch_offline_users=True)
tree = bot.tree

initial_extensions = ['cogs.redwood-deli-admin',
                      'cogs.redwood-deli-apply',
                      'cogs.redwood-deli-commands',
                      'cogs.redwood-deli-errors',
                      'cogs.redwood-deli-owner',
                      'cogs.redwood-deli-roblox'
                    ]
@bot.event
async def on_member_update(before, after):
    """Checks is a member has gotten a timeout and sends embed to the logs channel with their name, length of timeout, and who did it.
    The embed is also local timestamped and has the member's id in the footer"""
    if before.timeout != after.timeout:
        if after.timeout is not None:
            timeout = after.timeout
            timeout = timeout.replace(tzinfo=None)
            timeout = timeout - datetime.datetime.now()
            timeout = int(timeout.total_seconds())
            timeout = str(datetime.timedelta(seconds=timeout))
            embed = discord.Embed(
                title="Timeout",
                description=f"{after.mention} has been timed out for {timeout}",
                color=0x00ff00)
            embed.set_footer(text=f"ID: {after.id}")
            embed.timestamp = datetime.datetime.now()
            channel = bot.get_channel(os.getenv('LogChannel'))
            await channel.send(embed=embed)
            pass
        pass
    pass

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}, Running Verison 0.0.0.9'.format(bot))
    activity = discord.Activity(name='with food | !help', type=discord.ActivityType.playing)
    await bot.change_presence(activity=activity)
    await asyncio.sleep(1)
    bot.owner = (await bot.application_info()).owner
    await tree.sync()
    print('Slash commands synced!')
    await asyncio.sleep(2)
    print('Running discord.py version ' + discord.__version__)
    await asyncio.sleep(2)
    print('Cogs loaded:')
    await asyncio.sleep(1)
    print(bot.cogs)

@bot.event
async def on_user_update(before, after):
    try:
        if after.id == bot.owner.id and before.name != after.name:
            bot.owner = bot.get_user(after.id)
    except AttributeError:
        pass

@tree.command(name='test-slash', description="testing")
@commands.is_owner()
async def test(interaction: discord.Interaction):
    await interaction.response.send_message('Success!')
    pass

async def main():
    async with bot:
        await bot.start(os.getenv("BotToken"))

asyncio.run(main())