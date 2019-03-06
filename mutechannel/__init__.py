from .mutechannel import channelmute

def setup(bot):
    bot.add_cog(channelmute(bot))
