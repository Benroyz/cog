import os
import asyncio  # noqa: F401
import datetime
import discord
from redbot.core import commands, checks, Config


class TTTSuggest(commands.Cog):
    """custom cog for a configurable suggestrotion box"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=(3322665 + 1))
        self.usercache = []

        default_guild = {
            "inactive": True,
            "channels_enabled": [],
            "cleanup": False,
            "anonymous": True,
            "blocked_ids": []
        }

        self.config.register_guild(**default_guild)

    @commands.group(name="setsuggestrot", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def setsuggestrot(self, ctx):
        """configuration settings"""

        pass

    
    @setsuggestrot.command(name="on", pass_context=True, no_pm=True)
    async def _setsuggestrot_on(self, ctx):
        """Turn on suggestrotionBox in the current channel"""
        guild_group = self.config.guild(ctx.guild)

        async with guild_group.channels_enabled() as channels_enabled:
            channel = ctx.message.channel
            if channel.id in channels_enabled:
                await ctx.send("suggestrotionBox is already on in this channel.")
            else:
                channels_enabled.append(channel.id)

                await ctx.send("suggestrotionBox is now on in this channel.")

    @setsuggestrot.command(name="off", pass_context=True, no_pm=True)
    async def _setsuggestrot_off(self, ctx):
        """Turn off suggestrotionBox in the current channel"""
        guild_group = self.config.guild(ctx.guild)

        async with guild_group.channels_enabled() as channels_enabled:
            channel = ctx.message.channel
            if channel.id not in channels_enabled:
                await ctx.send("suggestrotionBox is already off in this channel.")
            else:
                channels_enabled.remove(channel.id)

                await ctx.send("suggestrotionBox is now off in this channel.")

    @setsuggestrot.command(name="block", pass_context=True, no_pm=True)
    async def block(self, ctx, user: discord.Member):
        """Blocks a user from making suggestrotions."""
        guild = ctx.guild
        group = self.config.guild(guild)

        async with group.blocked_ids() as blocked_ids:
            if user.id in blocked_ids:
                await ctx.send("This user is already in the block list, did you mean to `--setsuggestrot unblock`?")
            else:
                blocked_ids.append(user.id)
                await ctx.send("User blocked.")

    @setsuggestrot.command(name="unblock", pass_context=True, no_pm=True)
    async def unblock(self, ctx, user: discord.Member):
        """Unblocks a user from making suggestrotions."""
        guild = ctx.guild
        group = self.config.guild(guild)

        async with group.blocked_ids() as blocked_ids:
            if user.id not in blocked_ids:
                await ctx.send("This user isn't in the block list, did you mean to `--setsuggestrot block`?")
            else:
                blocked_ids.remove(user.id)
                await ctx.send("User unblocked.")

    @setsuggestrot.command(name="anonymous", pass_context=True, no_pm=True)
    async def anonymous(self, ctx):
        """Toggles whether or not the suggestrotions are anonymous."""
        guild = ctx.guild

        current_val = await self.config.guild(guild).anonymous()
        current_val = not current_val

        if current_val:
            await ctx.send("suggestrotions are now anonymous.")
        else:
            await ctx.send("suggestrotions are no longer anonymous.")

        await self.config.guild(guild).anonymous.set(current_val)

    @commands.command(name="suggestrot", pass_context=True)
    async def makesuggestrotion(self, ctx):
        "make a suggestrotion by following the prompts"
        author = ctx.message.author
        guild = ctx.guild
        group = self.config.guild(guild)

        async with group.blocked_ids() as blocked_ids:
            if author.id in self.usercache:
                return await ctx.send("Finish making your prior suggestion "
                                          "before making an additional one")

            if author.id in blocked_ids:
                return await ctx.send("You are blocked from making suggestion.")

            await ctx.send("I will message you to collect your suggestion.")
                    
            self.usercache.append(author.id)
                    
            dm = await author.send("Please respond to this message with your server suggestion. Bug Reports encouraged!")
        
            def check_message(m):
                return m.channel == dm.channel and m.author == author

            message = await self.bot.wait_for("message", check=check_message, timeout=300)

            if message is None:
                await author.send("I can't wait forever, try again when ready.")
                    
                self.usercache.remove(author.id)
            else:
                await self.send_suggestrot(message, guild)
                await author.send("Your suggestion was submitted.")

    async def send_suggestrot(self, message, guild):
        author = guild.get_member(message.author.id)
        group = self.config.guild(guild)
        suggestrotion = message.clean_content
        avatar = author.avatar_url if author.avatar \
            else author.default_avatar_url

        em = discord.Embed(description=suggestrotion,
                           color=discord.Color.purple())


        if len(message.attachments) > 0:
            item = message.attachments[0]

            if item.url.endswith((".jpg", ".png", ".gif", ".jpeg")):
                em.set_image(url=item.url)

        anonymous = await group.anonymous()

        async with group.channels_enabled() as channels_enabled:
            if anonymous:
                em.set_author(name='Anonymous / ' + datetime.date.today().strftime("%B %d, %Y"))
            else:
                em.set_author(name=author.name + "#" + author.discriminator + " / " + datetime.date.today().strftime("%B %d, %Y"), icon_url=avatar)

            em.set_footer(text="Vote on whether or not you'd like to see this implemented!")

            for channel in channels_enabled:
                where = guild.get_channel(channel)
                
                if where is not None:
                    await where.send(embed=em)

            self.usercache.remove(author.id)
 
