from .tttsuggestrot import TTTSuggest
from .tttsuggestmc import TTTSuggestMC


def setup(bot):
    bot.add_cog(TTTSuggest(bot))
    bot.add_cog(TTTSuggestMC(bot))
