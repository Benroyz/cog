import asyncio
import discord
from redbot.core import commands, checks

class channelmute(commands.cog):
    """Channel mute"""

    @checks.admin_or_permissions(manage_channels=True)
    @commands.command(pass_context = True)
    async def mutechannel(self, ctx):
        perms = discord.PermissionOverwrite()
        perms.send_messages = False
        await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.default_role ,perms)
        todelete = await self.bot.say("Done :+1:")
        await asyncio.sleep(5)
        await self.bot.delete_message(todelete)

    @checks.admin_or_permissions(manage_channels=True)
    @commands.command(pass_context = True)
    async def unmutechannel(self, ctx):
        perms = discord.PermissionOverwrite()
        perms.send_messages = True
        await self.bot.edit_channel_permissions(ctx.message.channel, ctx.message.server.default_role ,perms)
        todelete = await self.bot.say("Done :+1:")
        await asyncio.sleep(5)
        await self.bot.delete_message(todelete)
