from .tttchangelogs import TTTChangelogs
from .todoukttt import TTTUKtodo

def setup(bot):
    bot.add_cog(TTTChangelogs(bot))
    bot.add_cog(TTTUKtodo(bot))
