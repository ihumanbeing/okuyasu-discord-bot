import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import requests
from googletrans import Translator
import qrcode
from jikanpy import Jikan
jikan = Jikan()


class Util(commands.Cog):
    
    def __init__(self, client, trans=Translator()):
        self.client = client
        self.trans = trans
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Util cog ready.')

    @commands.command(pass_context=True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def reddit(self, ctx, arg=""):
        if arg == "":
            url = 'https://meme-api.herokuapp.com/gimme/specifyasubreddit'
        else:
            url = f'https://meme-api.herokuapp.com/gimme/{arg}'
        response = requests.request("GET", url)
        response_json  = response.json()
        if response_json["nsfw"] == True:
            embed = discord.Embed(
                title = "Sorry!",
                description = "NSFW posts are disabled.",
                colour = discord.Colour.red()
            )
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
            await ctx.send(embed=embed)
        else:
            if str(response_json["subreddit"]) == "hentai": 
                response_json["subreddit"] += " ( ͡° ͜ʖ ͡°)"
            embed = discord.Embed(
                title = response_json["title"],
                description = f'posted in r/{response_json["subreddit"]}',
                colour = discord.Colour.blue()
            )
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
            print(response_json["url"])
            embed.set_image(url=response_json["url"])
            print(response_json)
            await ctx.send(embed=embed)
    @reddit.error
    async def reddit_error(self, ctx, args):
        if isinstance(args, commands.CommandOnCooldown):
            embed = discord.Embed(title="This command is on cooldown", description=f"Please try again in `{args.retry_after:,.1f}` seconds.", color=discord.Color.red())
            await ctx.send(embed=embed)
    @commands.command(pass_context = True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def translate(self, ctx, *, args):
        embed = discord.Embed(
            title = 'Translation',
            colour = discord.Colour.blue()
        )
        author = ctx.message.author.mention
        print(author)
        t = self.trans.translate(
            args, dest='en'
        )
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.add_field(name='Input:', value=args, inline=True)
        embed.add_field(name='Output:', value=t.text, inline=True)
        await ctx.send(embed=embed)
    @commands.command(pass_context = True)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def qr(self, ctx, *, query):
        qr = qrcode.QRCode(
            version = 2,
            error_correction = qrcode.constants.ERROR_CORRECT_M,
            box_size = 8,
            border = 4,
        )
        qr.add_data(query)
        qr.make(fit=True)  
        img = qr.make_image()   
        qr.clear()
        img.save('img.png')
        qrimg = discord.File('img.png')
        await ctx.send(file=qrimg)
    @commands.command(pass_context = True)
    async def say(self, ctx, *, query):
        if "@here" in query:
            pass
        elif "@everyone" in query:
            pass
        else:
            await ctx.send(query)
    @commands.command(pass_context = True)
    @commands.cooldown(1,7,commands.BucketType.user)
    async def anime(self, ctx, *, args):
        results = jikan.search('anime', args)
        if len(results["results"]) == 0:
            await ctx.send('Sorry, I tried to use Za Hando but still couldn\'t find you an anime.')
        else:
            results = results["results"]
            results = results[0]
        embed = discord.Embed(
            title = results["title"],
            colour = discord.Colour.blue()
        )
        author = ctx.message.author.mention
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url=results["image_url"])
        embed.add_field(name="Description:", value=results["synopsis"], inline=True)
        embed.add_field(name="Episodes:", value=str(results["episodes"]), inline=True)
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(Util(client))