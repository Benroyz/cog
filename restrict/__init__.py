from .restrict import Restrict

def setup(bot):
    bot.add_cog(Restrict(bot))
