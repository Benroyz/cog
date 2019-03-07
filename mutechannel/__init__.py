from .mutechannel import MuteChannel

def setup(bot):
    bot.add_cog(MuteChannel(bot))
