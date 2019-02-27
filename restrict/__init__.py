from .restrict import restrict

def setup(bot):
    bot.add_cog(restrict(bot))
