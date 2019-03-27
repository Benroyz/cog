from .phsuggest import PHSuggestionBox

def setup(bot):
    bot.add_cog(SuggestionBox(bot))
