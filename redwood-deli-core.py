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

initial_extensions = ['cogs.redwood-deli-apply',
                      'cogs.redwood-deli-errors',
                      'cogs.redwood-deli-owner',
                      'cogs.redwood-deli-roblox'
                    ]

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}, Running Verison 0.0.0.5'.format(bot))
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

@tree.command(name='test-slash', description="testing")
@commands.is_owner()
async def test(interaction: discord.Interaction):
    await interaction.response.send_message('Success!')
    pass

async def main():
    async with bot:
        await bot.start(os.getenv("BotToken"))

asyncio.run(main())