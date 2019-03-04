from .announce import announce

def setup(bot):
    bot.add_cog(announce(bot))
