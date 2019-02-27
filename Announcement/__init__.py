from Announcement.announce import announcement


async def setup(bot):
    c = Announcement(bot)
    await c.init()
    bot.add_cog(c)
