import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import datetime


class Config(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print('Config cog ready.')
        
    @commands.command(pass_context = True)
    async def ping(self, ctx):
        author = ctx.message.author.mention
        print(author)
        embed = discord.Embed(
            title = 'Pong! 🏓',
            colour = discord.Colour.blue()
        )
        author = ctx.message.author.mention
        print(author)
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.add_field(name='I used Za Hando to check the ping! ', value=f'{round(self.client.latency * 1000)}ms', inline=True)
        await ctx.send(embed=embed)
    @commands.command(pass_context = True)
    async def info(self, ctx):
        author = ctx.message.author.mention
        servers = list(self.client.guilds)
        print(author)
        embed = discord.Embed(
            title = 'Okuyasu',
            colour = discord.Colour.blue()
        )
        
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.add_field(name='Default prefix:', value='Oi Josuke! ', inline=True)
        embed.add_field(name='Server Count:', value=str(len(servers)), inline=True)
        embed.add_field(name='Ping:', value=f'{round(self.client.latency * 1000)}ms', inline=True)
        embed.add_field(name='discord.py:', value='1.3.4', inline=True)
        embed.add_field(name='Python:', value='3.8', inline=True)
        embed.add_field(name='Support Server:', value='discord.gg/vuYseDR', inline=True)
        embed.add_field(name='Creator:', value='<@511237266589614102>', inline=True)
        embed.add_field(name='Creation Date:', value='12/06/2020', inline=True)
        
        await ctx.send(author, embed=embed)
def setup(client):
    client.add_cog(Config(client))