import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import requests
from googletrans import Translator
import qrcode, random
import wikiquote
from bs4 import BeautifulSoup

charlist = [
    "https://jojo.fandom.com/wiki/Jonathan_Joestar",
    "https://jojo.fandom.com/wiki/Will_Anthonio_Zeppeli",
    "https://jojo.fandom.com/wiki/Robert_E._O._Speedwagon",
    "https://jojo.fandom.com/wiki/Erina_Pendleton",
    "https://jojo.fandom.com/wiki/Poco",
    "https://jojo.fandom.com/wiki/George_Joestar_I",
    "https://jojo.fandom.com/wiki/Tonpetty",
    "https://jojo.fandom.com/wiki/Straizo",
    "https://jojo.fandom.com/wiki/Dire",
    "https://jojo.fandom.com/wiki/Dio_Brando",
    "https://jojo.fandom.com/wiki/Wang_Chan",
    "https://jojo.fandom.com/wiki/Jack_the_Ripper",
    "https://jojo.fandom.com/wiki/Tarkus",
    "https://jojo.fandom.com/wiki/Bruford",
    "https://jojo.fandom.com/wiki/Dario_Brando",
    "https://jojo.fandom.com/wiki/Joseph_Joestar",
    "https://jojo.fandom.com/wiki/Caesar_Anthonio_Zeppeli",
    "https://jojo.fandom.com/wiki/Lisa_Lisa",
    "https://jojo.fandom.com/wiki/Rudol_von_Stroheim",
    "https://jojo.fandom.com/wiki/Robert_E._O._Speedwagon",
    "https://jojo.fandom.com/wiki/Messina",
    "https://jojo.fandom.com/wiki/Loggins",
    "https://jojo.fandom.com/wiki/Erina_Pendleton",
    "https://jojo.fandom.com/wiki/Smokey_Brown",
    "https://jojo.fandom.com/wiki/Suzi_Q",
    "https://jojo.fandom.com/wiki/Kars",
    "https://jojo.fandom.com/wiki/Esidisi",
    "https://jojo.fandom.com/wiki/Wamuu",
    "https://jojo.fandom.com/wiki/Santana",
    "https://jojo.fandom.com/wiki/Straizo",
    "https://jojo.fandom.com/wiki/Donovan",
    "https://jojo.fandom.com/wiki/Wired_Beck",
    "https://jojo.fandom.com/wiki/Mark",
    "https://jojo.fandom.com/wiki/Mario_Zeppeli",
    "https://jojo.fandom.com/wiki/George_Joestar_II",
    "https://jojo.fandom.com/wiki/Jotaro_Kujo",
    "https://jojo.fandom.com/wiki/Muhammad_Avdol",
    "https://jojo.fandom.com/wiki/Noriaki_Kakyoin",
    "https://jojo.fandom.com/wiki/Jean_Pierre_Polnareff",
    "https://jojo.fandom.com/wiki/Iggy",
    "https://jojo.fandom.com/wiki/Holy_Kujo",
    "https://jojo.fandom.com/wiki/Enya_the_Hag",
    "https://jojo.fandom.com/wiki/Vanilla_Ice",
    "https://jojo.fandom.com/wiki/Hol_Horse",
    "https://jojo.fandom.com/wiki/Daniel_J._D%27Arby",
    "https://jojo.fandom.com/wiki/Pet_Shop",
    "https://jojo.fandom.com/wiki/N%27Doul",
    "https://jojo.fandom.com/wiki/Alessi",
    "https://jojo.fandom.com/wiki/Oingo",
    "https://jojo.fandom.com/wiki/Boingo",
    "https://jojo.fandom.com/wiki/Anubis",
    "https://jojo.fandom.com/wiki/Telence_T._D%27Arby",
    "https://jojo.fandom.com/wiki/Gray_Fly",
    "https://jojo.fandom.com/wiki/Forever",
    "https://jojo.fandom.com/wiki/Josuke_Higashikata",
    "https://jojo.fandom.com/wiki/Okuyasu Testing_Nijimura",
    "https://jojo.fandom.com/wiki/Koichi_Hirose",
    "https://jojo.fandom.com/wiki/Rohan_Kishibe",
    "https://jojo.fandom.com/wiki/Hayato_Kawajiri",
    "https://jojo.fandom.com/wiki/Reimi_Sugimoto",
    "https://jojo.fandom.com/wiki/Shigekiyo_Yangu",
    "https://jojo.fandom.com/wiki/Mikitaka_Hazekura",
    "https://jojo.fandom.com/wiki/Yukako_Yamagishi",
    "https://jojo.fandom.com/wiki/Toshikazu_Hazamada",
    "https://jojo.fandom.com/wiki/Tamami_Kobayashi",
    "https://jojo.fandom.com/wiki/Tonio_Trussardi",
    "https://jojo.fandom.com/wiki/Nijimura%27s_Father",
    "https://jojo.fandom.com/wiki/Giorno_Giovanna",
    "https://jojo.fandom.com/wiki/Bruno_Bucciarati",
    "https://jojo.fandom.com/wiki/Leone_Abbacchio",
    "https://jojo.fandom.com/wiki/Guido_Mista",
    "https://jojo.fandom.com/wiki/Narancia_Ghirga",
    "https://jojo.fandom.com/wiki/Pannacotta_Fugo",
    "https://jojo.fandom.com/wiki/Trish_Una",
    "https://jojo.fandom.com/wiki/Coco_Jumbo",
    "https://jojo.fandom.com/wiki/Pericolo",
    "https://jojo.fandom.com/wiki/Diavolo",
    "https://jojo.fandom.com/wiki/Vinegar_Doppio",
    "https://jojo.fandom.com/wiki/Carne",
    "https://jojo.fandom.com/wiki/Cioccolata",
    "https://jojo.fandom.com/wiki/Secco",
    "https://jojo.fandom.com/wiki/Pesci",
]

class JoJo(commands.Cog):
    
    def __init__(self, client, trans=Translator()):
        self.client = client
        self.trans = trans
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('JoJo cog ready.')

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def quote(self,ctx):
        embed = discord.Embed(
            title = "Random JoJo\'s quote (spoilers)",
            description=wikiquote.quotes('JoJo\'s Bizarre Adventure', max_quotes=1)[0],
            colour = discord.Colour.blue()
        )
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
        await ctx.send(embed=embed)
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        url = f'https://meme-api.herokuapp.com/gimme/jojomemes'
        response = requests.request("GET", url)
        response_json  = response.json()
        embed = discord.Embed(
            title = response_json["title"],
            colour = discord.Colour.blue()
        )
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
        print(response_json["url"])
        embed.set_image(url=response_json["url"])
        print(response_json)
        await ctx.send(embed=embed)
        
    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def character(self, ctx):
        url = random.choice(charlist)
        response = requests.get(url)
        content = response.content
        soup = BeautifulSoup(content)
        person = soup.find("h1", { "class" : "page-header__title" })
        image_tag = soup.findAll('img')[2]
        embed = discord.Embed(title=person.text,color=discord.Colour.blue())
        embed.set_image(url=image_tag.get('src'))
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
        await ctx.send(embed=embed)
        
    @commands.command(pass_context=True)
    async def truth(self, ctx):
        choices = [
            'the stone ocean adaption will release.'
            'the stone ocean adaption will never release.',
            'the stone ocean adaption might release.'
        ]
        choice = random.choice(choices)
        if choice == 'the stone ocean adaption will release.the stone ocean adaption will never release.':
            choice = 'the stone ocean adaption will never release.'
        await ctx.send(choice)
    

def setup(client):
    client.add_cog(JoJo(client))