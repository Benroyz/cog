from .phsuggest import PHSuggestionBox
from .phtodo import PHToDo

def setup(bot):
    bot.add_cog(PHSuggestionBox(bot))
    bot.add_cog(PHToDo(bot))
    
