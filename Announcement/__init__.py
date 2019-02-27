from announcement.announce import Announcement


async def setup(bot):
    c = Announcement(bot)
    await c.init()
    bot.add_cog(c)
