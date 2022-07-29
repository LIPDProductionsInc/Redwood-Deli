import discord
import datetime
import os

from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

class ApplicationCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="apply", description="Apply to Redwood Deli or to become a manager")
    async def apply_command(self, ctx: commands.Context, type = None) -> None:
        user = ctx.bot.get_user(ctx.author.id)
        channel = ctx.bot.get_channel(os.getenv("GeneralApplyChannel"))
        await ctx.send("Check your DMs")
        if type == None:
            await user.send("What is your ROBLOX name?")

            def check(m):
                return isinstance(m.channel, discord.DMChannel) and m.author == ctx.author
            
            name = await self.bot.wait_for('message', check=check)
            await user.send("Please reply with the link to your profile")
            profile = await self.bot.wait_for('message', check=check)
            await user.send("What position are you applying for?")
            position = await self.bot.wait_for('message', check=check)
            await user.send("Do you have a criminal history? If so, briefly list any charges you have")
            background = await self.bot.wait_for('message', check=check)
            await user.send("How long have you been in Firestone?")
            community = await self.bot.wait_for('message', check=check)
            await user.send("Why do you want to work for Redwood Bagels and Deli?")
            reason = await self.bot.wait_for('message', check=check)
            await user.send("Do you have any experience **IN** or **OUT** of Firestone in the food industry?")
            experience = await self.bot.wait_for('message', check=check)
            await user.send("What is your availability like?")
            availability = await self.bot.wait_for('message', check=check)
            embed = discord.Embed(
                title='**NEW APPLICATION SUBMITTED!**',
                type='rich',
                colour=discord.Color(0xFF9E00),
                description=f'''\n
**NAME**:
{name.content}

**PROFILE**:
{profile.content}

**DISCORD**:
{ctx.author.mention}

**POSITION APPLYING FOR**:
{position.content}

**CRIMINAL HISTORY?**:
{background.content}

**TIME IN FIRESTONE**:
{community.content}

**REASON FOR WORKING**:
{reason.content}

**EXPERIENCE**:
{experience.content}

**AVAILABILITY**:
{availability.content}

*Use the ID below when responding to an application!*
'''
            )
            embed.set_footer(text=f'ID: {ctx.author.id}')
            embed.timestamp=datetime.datetime.utcnow()
            embed.set_author(name=ctx.author)
            embed.set_thumbnail(url=str(ctx.author.avatar))
            await channel.send('@here', embed=embed)
            await user.send("Your application has been sent and will be reviewed by management. Expect a DM from me with the next steps")
            pass
        pass

    @commands.hybrid_command(name='accept', description='Accept an applicant')
    @commands.has_any_role(993189120400691210,993190740534509678,993198036144640070)
    async def accept_command(self, ctx: commands.Context, member: discord.Member) -> None:
        channel = ctx.bot.get_channel(os.getenv("LogChannel"))
        await member.send(f"""
----------------------------------------------------------
FROM: {ctx.author.nick}@discordia.com
TO: {member.nick}@discordia.com
SUBJECT: RE: Application for employment at Redwood Deli
----------------------------------------------------------

Hello {member.nick}!

First off, I would like to personally thank you for applying to Redwood Bagels and Deli. After careful review of your application and qualifications, we have decided to offer you an employment opportunity as a trainee. The next steps would be for you to join the ROBLOX group if you haven't already so you can be ranked.

Once you are ranked, you can use `/update` to get access to the employee area as well as get access to the employee area of our store. The group is attached below.

Thank you once again for your interest in working for Redwood Bagels and Deli!!

Signed,
{ctx.author.nick}
Redwood Bagels and Deli

----------------------------------------------------------
ATTACHMENTS: 
<https://www.roblox.com/groups/15256757/Redwood-Bagels-and-Deli#!/>
----------------------------------------------------------
        """)
        embed=discord.Embed(
            type='rich',
            colour=discord.Color.dark_green(),
            description=f'''
**APPLICATION APPROVED:**
{member.mention}

**APPROVED BY:**
{ctx.author.mention}
'''
                )
        embed.set_footer(text=f'ID: {ctx.author.id}')
        embed.timestamp=datetime.datetime.utcnow()
        embed.set_author(name=ctx.guild.name, icon_url=str(ctx.guild.icon))
        await channel.send(embed=embed)
        await ctx.send('Message sent to user!')
        pass

    pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ApplicationCog(bot))