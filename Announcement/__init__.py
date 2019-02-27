from announce.announce import announce


async def setup(bot):
    c = announce(bot)
    await c.init()
    bot.add_cog(c)
