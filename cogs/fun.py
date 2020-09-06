import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import requests, json
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from forismatic import *
import time
import random
import giphy_client
from giphy_client.rest import ApiException
from discord.ext.commands import has_permissions, bot_has_permissions

epicquoteman = forismatic.ForismaticPy()

api_instance = giphy_client.DefaultApi()
api_key = 'S01bsQdyZov4iPBDByqu7z2AzHbW3Wqq'
limit = 1
offset = 0
rating = 'g'
lang = 'en'
fmt = 'json'

def get_dolphins():
    with open('dolphins.json','r') as f:
        dolphins = json.load(f)
    dolphins['Dolphins'] += 1
    with open('dolphins.json','w') as f:
        json.dump(dolphins, f, indent=4)
    return dolphins['Dolphins']

class Fun(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun cog ready.')
        
    @commands.command(pass_context=True)
    async def dolphin(self,ctx):
        embed = discord.Embed(title="How many dolphins has Jotaro fucked?",description="Good question, lemme go ahead and check...", colour = discord.Colour.red())
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
        message = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        embed = discord.Embed(title="How many dolphins has Jotaro fucked?",description=f"As of this moment Jotaro has fucked {get_dolphins()} dolphins", colour = discord.Colour.blue())
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
        await message.edit(embed=embed)
        
    @commands.command(pass_context=True)
    async def hentai(self,ctx):
        message = await ctx.send("Okay, I'll use Za Hando to get you some hentai...")
        await asyncio.sleep(3)
        await message.edit(content="Just one more second...")
        await asyncio.sleep(2)
        await message.edit(content="get stickbugged lol")
        await ctx.send("https://media.tenor.com/images/993a1a17a94f88ae98311382eb3306d4/tenor.gif")
        
    @commands.command(pass_context = True)
    async def inspire(self, ctx):
        quote = epicquoteman.get_Quote()
        embed = discord.Embed(
            title = 'Oi Josuke! I used Za Hando to find the meaning of life:',
            description = quote[0],
            colour = discord.Colour.blue()
        )
        author = ctx.message.author.mention
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        await ctx.send(embed=embed)
    @commands.command(pass_context = True)
    async def steppedin(self, ctx, *, args):
        img = Image.open("cogs/images/ewisteppedin.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("cogs/fonts/Roboto-Bold.ttf", int(600/len(args)))
        draw.text((250,825),args,(0,0,0),font=font)
        img.save('cogs/images/output.jpg')
        with open('cogs/images/output.jpg', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file = picture)
    @steppedin.error
    async def steppedin_error(self, ctx, args):
        if isinstance(args, commands.MissingRequiredArgument):
            await ctx.send('Please specify the || shit ||.')
def setup(client):
    client.add_cog(Fun(client))