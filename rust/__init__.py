from .rustsuggestvanilla import RustSuggestVanilla
from .rustsuggestmodded import RustSuggest


def setup(bot):
    bot.add_cog(RustSuggestVanilla(bot))
    bot.add_cog(RustSuggest(bot))
