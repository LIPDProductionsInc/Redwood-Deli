import discord
import aiohttp
import asyncio
import datetime
import json
import psutil
import sys
import traceback

from discord.ext import commands

class OwnerCog(commands.Cog, name="Owner Commands"):

    def __init__(self, bot):
        self.bot = bot
    
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, cog: str):
        await ctx.send(f'**`Loading Cog: {cog}...`**')
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            print('Loading cog...')
            await asyncio.sleep(0.1)
            print('Cog name:')
            await asyncio.sleep(0.1)
            print(cog)
            await asyncio.sleep(2)
            await self.bot.load_extension(f'cogs.redwood-deli-{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Cog: {cog} has loaded successfully`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, *, cog: str):
        await ctx.send(f'**`Unloading Cog: {cog}...`**')
        await asyncio.sleep(2)
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            print('Unloading cog...')
            await asyncio.sleep(0.1)
            print('Cog name:')
            await asyncio.sleep(0.1)
            print(cog)
            await self.bot.unload_extension(f'cogs.redwood-deli-{cog}')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            print(f'{cog} has unloaded successfully!')
            await ctx.send(f'**`Successfuly unloaded Cog: {cog}`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        print('Reloading cog...')
        await asyncio.sleep(0.1)
        print('Cog Name:')
        await asyncio.sleep(0.1)
        print(cog)
        try:
            await ctx.send(f'**`Unloading Cog: {cog}...`**')
            await self.bot.unload_extension(f'cogs.redwood-deli-{cog}')
            await asyncio.sleep(2)
            await ctx.send(f'**`Loading Cog: {cog}...`**')
            await self.bot.load_extension(f'cogs.redwood-deli-{cog}')
            await asyncio.sleep(1)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f'**`Successfully loaded {cog}`**')
            print(f'Cog: {cog} has loaded sucessfuly!')
            pass
        pass

    @commands.command(name='sync', hidden=True)
    @commands.is_owner()
    async def _sync(self, ctx) -> None:
        await ctx.send('`Syncing Slash commands...`')
        print('Syncing slash commands')
        synced = await ctx.bot.tree.sync()
        await ctx.send(f"`Synced {len(synced)} commands`")
        print(f"Synced {len(synced)} commands")
        return

    
    @commands.command(name='eval', hidden=True)
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')
                pass
            pass
        pass
    
    @commands.command(name='rules')
    @commands.is_owner()
    async def _rules(self, ctx):
        channel = self.bot.get_channel(993206728252477450)
        embed = discord.Embed(
            colour=discord.Colour(0xFF9E00)
            )
        embed.set_author(name='Redwood Bagels and Deli Rules', icon_url='https://cdn.discordapp.com/attachments/841000000000000000/841000000000000000/Redwood_Deli_Logo.png')
        embed.add_field(name='Rule 1', value='[Discord Terms of Service](https://discord.com/terms) and the [Discord Community Guidelines](https://discord.com/guidelines) **MUST** be followed at all times.', inline=False)
        embed.add_field(name='Rule 2', value='Be respectful to all members of the community. **No hateful messages to members**', inline=False)
        embed.add_field(name='Rule 3', value='Leaking personal information of anyone is **not** allowed', inline=False)
        embed.add_field(name='Rule 4', value='Spamming and/or mic-spamming is **not** allowed', inline=False)
        embed.add_field(name='Rule 5', value='NSFW or inappropriate content is **not** allowed. This can be pornographic, gore, highly sensitive material, etc.', inline=False)
        embed.add_field(name='Rule 6', value='Advertising your material is **not** allowed. Government related activities can be granted a case-by-case exemption, open a <#999293384504119326>.', inline=False)
        embed.add_field(name='Rule 7', value='Do **not** post malicious links, files, or anything of that sort. This include referral links.', inline=False)
        embed.add_field(name='Rule 8', value='Sharing discord direct messages (DMS) in order to provoke them and make them look bad is **not** tolerated.', inline=False)
        embed.add_field(name='Rule 9', value='Racism/Homophobia/Discrimination is **not** tolerated in this discord', inline=False)
        embed.add_field(name='Rule 10', value='This is an English speaking discord', inline=False)
        embed.add_field(name='Rule 11', value='Targeting someone in order to provoke by any means is forbidden', inline=False)
        embed.add_field(name='Rule 12', value='Do **not** impersonate any staff member, bots, or any other member of the community', inline=False)
        embed.add_field(name='Rule 13', value='Your display name **MUST** be set to your **ROBLOX** username. **NO EXCEPTIONS!!!** Callsigns are allowed if your department provides one.', inline=False)
        embed.add_field(name='Rule 14', value='Trolling and/or providing false information on purpose is forbidden', inline=False)
        embed.set_footer(text='Rules lase updated on:')
        embed.timestamp = datetime.datetime.now()
        await channel.send(embed=embed)
        pass
    
    @commands.command(name='edit')
    @commands.is_owner()
    async def _edit(self, ctx, id, content):
        message = await channel.fetch_message(id)
        await message.edit(content=content)
        pass
    
    @commands.command(name='stats')
    @commands.is_owner()
    async def _stats(self, ctx):
        embed = discord.Embed(
            title='Redwood Deli',
            type='rich',
            colour=discord.Color(0xFF9E00),
            description=f'''
Python Version: **{sys.version}**

Discord.py Version: **{discord.__version__}**

Current CPU Usage: **{psutil.cpu_percent()}**

Current RAM Usage: **{psutil.virtual_memory().percent}**

Average System Load: **{[x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]}%**

Latency: **{round(self.bot.latency * 1000)}**ms
'''
            )
        embed.set_footer(text="Developed by LIPD Producctions Inc.#1205")
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    @commands.command(name='role-request', hidden=True)
    @commands.is_owner()
    async def _rolerequest(self, ctx):
        request_role = """
The following roles can be requested from <@155149108183695360> using `?rank` followed by the name of the role:
- <@&1000334009651429467>
- <@&1001014065822453800>
- <@&1001013976840294450>
        """
        notice = """
- Your up-to-date callsign or rank **MUST** be a part of your nickname
- Applicants, Candidates, Probationary Officers, etc., do **NOT** get department roles
        """
        embed = discord.Embed(
            title="**ROLE REQUEST**",
            colour=discord.Color.blue(),
            description="""
To be able to view all the necessary channels in this server, you must have the appropriate role(s).

If you have verified with <@426537812993638400> before, check your DM's, because most likely your roles have already been given to you.
If you have not verified with <@426537812993638400> before, run `/verify` and make sure to select the command from <@426537812993638400> to get yourself verified.
If you still have not gotten all the roles you need, open a <#999293384504119326> to request the roles you need. **ANY REQUESTS MADE IN THIS CHANNEL WILL NOT BE SEEN!!!**

If you need new roles, first run `/update` from <@426537812993638400> to get your roles updated, if that fails, open a <#999293384504119326>."""
        )
        embed.add_field(name='**Requestable Roles**', value=request_role, inline=True)
        embed.add_field(name='**Notice to Department Employees:**', value=notice, inline=True)
        embed.set_footer(text="Developed by LIPD Producctions Inc.#1205", icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=str(self.bot.user.avatar))
        await ctx.send(embed=embed)
        pass

    pass

async def setup(bot):
    await bot.add_cog(OwnerCog(bot))