from announcescreen.announce import announceScreen


async def setup(bot):
    c = announceScreen(bot)
    await c.init()
    bot.add_cog(c)
