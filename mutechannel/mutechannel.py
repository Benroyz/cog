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
        await message.guilds.channel.set_permissions(ctx, message.author, read_messages=True,
                                                                   send_messages=False)
        todelete = await self.bot.say("Done :+1:")
        await asyncio.sleep(5)
        await self.bot.delete_message(todelete)

    @checks.admin_or_permissions(manage_channels=True)
    @commands.command(pass_context = True)
    async def unmutechannel(self, ctx):
        perms = discord.PermissionOverwrite()
        perms.send_messages = True
        await message.guilds.channel.set_permissions(ctx, message.author, read_messages=True,
                                                                   send_messages=True)
        todelete = await self.bot.say("Done :+1:")
        await asyncio.sleep(5)
        await self.bot.delete_message(todelete)
