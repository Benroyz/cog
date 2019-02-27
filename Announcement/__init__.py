from .Announcement import announcement

def setup(bot):
    bot.add_cog(announcement(bot))
