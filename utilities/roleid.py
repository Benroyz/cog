from redbot.core import commands, checks
import discord

class RoleID(commands.Cog)
    """Role ID."""

    def __init__(self, bot):
        self.bot = bot
        self.messager = {}
        self.messagem = {}

    @commands.command(pass_context=True, no_pm=True)
async def roleid(self, ctx, role: str=None):
    if role:
        role_obj = [x for x in ctx.message.server.roles if x.name == role]

        if len(role_obj) > 0:
            await self.ctx.say("**ID of {0}**: {1}".format(role, role_obj[0].id))
        else:
            await self.ctx.say("{0} is not a valid role.".format(role))

def setup(bot):
    bot.add_cog(RoleID(bot))
