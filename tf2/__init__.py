from .2fortsuggest import 2FortSuggest
from .hightowersuggest import HighTowerSuggest


def setup(bot):
    bot.add_cog(2FortSuggest(bot))
    bot.add_cog(HighTowerSuggest(bot))
