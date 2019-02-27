from .announcement import Announcement

def setup(bot):
    bot.add_cog(Announcement(bot))
