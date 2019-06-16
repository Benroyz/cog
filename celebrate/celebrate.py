import discord
import asyncio  # noqa: F401
from redbot.core import commands, checks, Config

class Celebrate(commands.Cog):
    """You can now celebrate about anything"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=(3322665 + 1))
        self.usercache = []
        self.messager = {}
        self.messagem = {}
        
        default_guild = {
            "blocked_ids": []
        }

        self.config.register_guild(**default_guild)

    @commands.group(name="setcelebrate", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(kick_members=True)
    async def setcelebrate(self, ctx):
        """configuration settings"""

        pass

    
    @setcelebrate.command(name="add", pass_context=True, no_pm=True)
    async def _setcelebrate_add(self, ctx, user: discord.Member):
        """Blocks a user from using celebrate."""
        guild = ctx.guild
        group = self.config.guild(guild)

        async with group.blocked_ids() as blocked_ids:
            if user.id in blocked_ids:
                await ctx.send("This user is already in the block list, did you mean to `--setcelebrate remove`?")
            else:
                blocked_ids.append(user.id)
                await ctx.send("User blocked.")

    @setcelebrate.command(name="remove", pass_context=True, no_pm=True)
    async def _setcelebrate_remove(self, ctx, user: discord.Member):
        """Unblocks a user from using celebrate."""
        guild = ctx.guild
        group = self.config.guild(guild)

        async with group.blocked_ids() as blocked_ids:
            if user.id not in blocked_ids:
                await ctx.send("This user isn't in the block list, did you mean to `--setcelebrate add`?")
            else:
                blocked_ids.remove(user.id)
                await ctx.send("User unblocked.")

    @commands.command(pass_context=True, no_pm=True)
    async def celebrate(self, ctx, user: discord.User=None):
        """Pay Respects by pressing f"""

        author = ctx.author
        channel = ctx.channel

        if channel.id in self.messager or channel.id in self.messagem:
            return await ctx.send("Oops! I'm still paying celebrated in this channel, you'll have to wait until I'm done.")
        
        def check_message(m):
            return (m.author == author and m.channel == channel)

        if user:
            answer = user.display_name
        else:
            await ctx.send("What do you want to pay celebrated to?")
            message = await self.bot.wait_for("message", check=check_message, timeout=120.0)

            if message is None:
                return await ctx.send("You took too long to reply.")
        
            answer = message.content
        
        msg = f"Everyone, let's pay celebrated to **{answer}**! Press the F reaction on this message to pay celebrated."

        message = await ctx.send(msg)

        try:
            await message.add_reaction("celebrate")
            self.messager[channel.id] = []
            react = True
        except:
            self.messagem[channel.id] = []
            react = False
            await message.edit(content=f"Everyone, let's pay celebrated to **{answer}**! Press the F reaction on the this message to pay celebrated.")

            def check(m):
                return m.channel == ctx.channel

            await self.bot.wait_for("message", check=check)

        await asyncio.sleep(120)
        await message.delete()

        if react:
            amount = len(self.messager[channel.id])
        else:
            amount = len(self.messagem[channel.id])

        amount_of_people = "person has" if str(amount) == "1" else "people have"
        await channel.send(f"**{amount}** {amount_of_people} paid celebrated to **{answer}**.")
        
        if react:
            del self.messager[channel.id]
        else:
            del self.messagem[channel.id]
    
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        channel = message.channel

        if user.id == self.bot.user.id:
            return
        if channel.id not in self.messager:
            return    
        if user.id not in self.messager[channel.id]:
            if str(reaction.emoji) == "\U0001f1eb": 
                await channel.send(f"**{user.mention}** has paid celebrated.")
                self.messager[channel.id].append(user.id)

    async def on_message(self, message):
        channel = message.channel
        user = message.author

        if channel.id not in self.messagem:
            return    
        if user.id not in self.messagem[channel.id]:
            if message.content.lower() == "f":
                await ctx.send("**{user.mention}** has paid celebrated.")
                self.messagem[channel.id].append(user.id)
                
