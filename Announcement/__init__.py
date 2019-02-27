from announcement.announce import announcement


async def setup(bot):
    c = announcement(bot)
    await c.init()
    bot.add_cog(c)
