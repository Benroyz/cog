import os
import asyncio  # noqa: F401
import datetime
import discord
from redbot.core import commands, checks, Config


class TTTChangelogs(commands.Cog):
    """custom cog for a configurable changelogsion box"""

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

    @commands.group(name="setchangelogs", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def setchangelogs(self, ctx):
        """configuration settings"""

        pass

    
    @setchangelogs.command(name="on", pass_context=True, no_pm=True)
    async def _setchangelogs_on(self, ctx):
        """Turn on changelogsionBox in the current channel"""
        guild_group = self.config.guild(ctx.guild)

        async with guild_group.channels_enabled() as channels_enabled:
            channel = ctx.message.channel
            if channel.id in channels_enabled:
                await ctx.send("changelogsionBox is already on in this channel.")
            else:
                channels_enabled.append(channel.id)

                await ctx.send("changelogsionBox is now on in this channel.")

    @setchangelogs.command(name="off", pass_context=True, no_pm=True)
    async def _setchangelogs_off(self, ctx):
        """Turn off changelogsionBox in the current channel"""
        guild_group = self.config.guild(ctx.guild)

        async with guild_group.channels_enabled() as channels_enabled:
            channel = ctx.message.channel
            if channel.id not in channels_enabled:
                await ctx.send("changelogsionBox is already off in this channel.")
            else:
                channels_enabled.remove(channel.id)

                await ctx.send("changelogsionBox is now off in this channel.")

    @setchangelogs.command(name="block", pass_context=True, no_pm=True)
    async def block(self, ctx, user: discord.Member):
        """Blocks a user from making changelogsions."""
        guild = ctx.guild
        group = self.config.guild(guild)

        async with group.blocked_ids() as blocked_ids:
            if user.id in blocked_ids:
                await ctx.send("This user is already in the block list, did you mean to `--setchangelogs unblock`?")
            else:
                blocked_ids.append(user.id)
                await ctx.send("User blocked.")

    @setchangelogs.command(name="unblock", pass_context=True, no_pm=True)
    async def unblock(self, ctx, user: discord.Member):
        """Unblocks a user from making changelogsions."""
        guild = ctx.guild
        group = self.config.guild(guild)

        async with group.blocked_ids() as blocked_ids:
            if user.id not in blocked_ids:
                await ctx.send("This user isn't in the block list, did you mean to `--setchangelogs block`?")
            else:
                blocked_ids.remove(user.id)
                await ctx.send("User unblocked.")

    @setchangelogs.command(name="anonymous", pass_context=True, no_pm=True)
    async def anonymous(self, ctx):
        """Toggles whether or not the changelogsions are anonymous."""
        guild = ctx.guild

        current_val = await self.config.guild(guild).anonymous()
        current_val = not current_val

        if current_val:
            await ctx.send("changelogsions are now anonymous.")
        else:
            await ctx.send("changelogsions are no longer anonymous.")

        await self.config.guild(guild).anonymous.set(current_val)

    @commands.command(name="applychangelog", pass_context=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def makechangelogsion(self, ctx):
        "make a changelogsion by following the prompts"
        author = ctx.message.author
        guild = ctx.guild
        group = self.config.guild(guild)

        async with group.blocked_ids() as blocked_ids:
            if author.id in self.usercache:
                return await ctx.send("Finish making your prior changelogs "
                                          "before making an additional one")

            if author.id in blocked_ids:
                return await ctx.send("You are blocked from making suggestion.")

            await ctx.send("I will message you to collect your changelogs..")
                    
            self.usercache.append(author.id)
                    
            dm = await author.send("Copy and paste this ```__**x changes**__ \n"
                                    "   *x:*\n"
                                    "     - \n"
                                    "     - \n"
                                    "     - \n``` for the formatting. ")
        
            def check_message(m):
                return m.channel == dm.channel and m.author == author

            message = await self.bot.wait_for("message", check=check_message, timeout=3600)

            if message is None:
                await author.send("I can't wait forever, try again when ready.")
                    
                self.usercache.remove(author.id)
            else:
                await self.send_changelogs(message, guild)
                await author.send("Your changelog was submitted.")

    async def send_changelogs(self, message, guild):
        author = guild.get_member(message.author.id)
        group = self.config.guild(guild)
        changelogsion = message.clean_content
        avatar = author.avatar_url if author.avatar \
            else author.default_avatar_url

        em = discord.Embed(description=changelogsion,
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

            em.set_footer(text="Implemented and changed by " + author.name + "#" + author.discriminator + ".")

            for channel in channels_enabled:
                where = guild.get_channel(channel)
                
                if where is not None:
                    await where.send(embed=em)

            self.usercache.remove(author.id)
