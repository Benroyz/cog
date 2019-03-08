from redbot.core import commands, checks
import discord

class RoleID(commands.Cog):
    """Role ID."""

    def __init__(self, bot):
        self.bot = bot
        self.messager = {}
        self.messagem = {}

    @commands.command(pass_context=True, no_pm=True)
    async def roleid(ctx, self, role: str=None):
        if role:
            role_obj = [x for x in ctx.message.guild if x.name == role]

            if len(role_obj) > 0:
                await self.ctx.send("**ID of {0}**: {1}".format(role, role_obj[0].id))
            else:
                await self.ctx.send("{0} is not a valid role.".format(role))
