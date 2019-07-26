from .fortsuggest import Fort
from .hightowersuggest import HighTowerSuggest


def setup(bot):
    bot.add_cog(Fort(bot))
    bot.add_cog(HighTowerSuggest(bot))
