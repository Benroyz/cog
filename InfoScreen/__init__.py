from InfoScreen.rules import InfoScreen


async def setup(bot):
    c = InfoScreen(bot)
    await c.init()
    bot.add_cog(c)
