from .tttsuggest import tttsuggest

def setup(bot):
    bot.add_cog(tttsuggest(bot))
