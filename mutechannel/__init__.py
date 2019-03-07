from .mutechannel import ChannelMute

def setup(bot):
    bot.add_cog(ChannelMute(bot))
