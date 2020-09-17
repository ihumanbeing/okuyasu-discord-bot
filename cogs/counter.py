import dbl, requests
import discord
from discord.ext import commands

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        print('TopGG Cog Ready')
        self.bot = bot
        self.token = TOKEN
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")
def setup(bot):
    bot.add_cog(TopGG(bot))
