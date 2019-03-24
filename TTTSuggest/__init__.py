from .tttsuggest import TTTSuggest

def setup(bot):
    bot.add_cog(TTTSuggest(bot))
