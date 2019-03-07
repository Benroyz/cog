import asyncio
import discord
from redbot.core import commands, checks

class mutechannel(commands.Cog):
    """Channel mute"""
    
    def __init__(self, bot):
        self.bot = bot
        self.messager = {}
        self.messagem = {}

    @checks.admin_or_permissions(manage_channels=True)
    @commands.command(pass_context = True)
    async def mutechannel(self, ctx):
        perms = discord.PermissionOverwrite()
        perms.send_messages = False
        await ctx.message.channel.set_permissions(ctx.message.channel, ctx.message.server.default_role ,perms)
        todelete = await ctx.send("Done :+1:")
        await asyncio.sleep(5)
        await ctx.message.delete()

    @checks.admin_or_permissions(manage_channels=True)
    @commands.command(pass_context = True)
    async def unmutechannel(self, ctx):
        perms = discord.PermissionOverwrite()
        perms.send_messages = True
        await ctx.message.channel.set_permissions(ctx.message.channel, ctx.message.server.default_role ,perms)
        todelete = await ctx.send("Done :+1:")
        await asyncio.sleep(5)
        await ctx.message.delete()
