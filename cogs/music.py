import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import youtube_dl
import random

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



class Music(commands.Cog):
    
    def __init__(self, client, songno=0, songs=[], currentsong=''):
        self.client = client
        self.songno = songno
        self.songs = songs
        self.currentsong = currentsong
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music cog ready.')
        
    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                l = [
                    "Stop wasting Za Hando's time.",
                    "Bruh moment.",
                    "It's time to stop."
                ]
                embed = discord.Embed(title="Already in current voice channel",description=random.choice(l), colour = discord.Colour.red())
                embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
                embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
                await voice.move_to(channel)
            else:
                embed = discord.Embed(title="Joining...", colour = discord.Colour.orange())
                embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
                embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
                message = await ctx.send(embed = embed)
                voice = await channel.connect()
                embed = discord.Embed(title="Joined.", colour = discord.Colour.green())
                embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
                embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
                await message.edit(embed=embed)
        except AttributeError:
            l = [
                "Stop wasting Za Hando's time.",
                "Bruh moment.",
                "It's time to stop."
            ]
            embed = discord.Embed(title="You are not connected to a voice channel",description=random.choice(l), colour = discord.Colour.red())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
            await ctx.send(embed = embed)
            return
            
    
    @commands.command()
    async def leave(self, ctx):
        try:
            embed = discord.Embed(title="Leaving...", colour = discord.Colour.orange())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
            message = await ctx.send(embed = embed)
            server = ctx.message.guild.voice_client
            await server.disconnect()
            embed = discord.Embed(title="Left.", colour = discord.Colour.green())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            await message.edit(embed=embed)
        except AttributeError:
            l = [
                "Stop wasting Za Hando's time.",
                "Bruh moment.",
                "It's time to stop."
            ]
            embed = discord.Embed(title="You are not connected to a voice channel",description=random.choice(l), colour = discord.Colour.red())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            await ctx.send(embed = embed)
            return

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():        
            embed = discord.Embed(title="Stopping...", colour = discord.Colour.orange())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            message = await ctx.send(embed = embed)
            voice.stop()
            embed = discord.Embed(title="Stopped.", colour = discord.Colour.green())
            await message.edit(embed=embed)
        else:
            l = [
                "Stop wasting Za Hando's time.",
                "Bruh moment.",
                "It's time to stop.",
                "idiot."
            ]
            embed = discord.Embed(title="No audio is playing",description=random.choice(l), colour = discord.Colour.red())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            await ctx.send(embed = embed)
    
    @commands.command(pass_context=True)
    async def queue(self, ctx, *, query):
        embed = discord.Embed(title='Adding {} to queue.'.format(query), colour = discord.Colour.green())
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        await ctx.send(embed = embed)
        query += '.mp3'
        self.songs.append(query)
        
    @queue.error
    async def queue_error(self, ctx, query):
        if isinstance(query, commands.MissingRequiredArgument):
            l = [
                "Stop wasting Za Hando's time.",
                "Bruh moment.",
                "It's time to stop.",
                "idiot.",
                "It's not that difficult my guy :pensive:"
            ]
            embed = discord.Embed(title="Please specify a song URL",description=random.choice(l), colour = discord.Colour.red())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            await ctx.send(embed = embed)
        
        
    @commands.command(pass_context=True)
    async def next(self, ctx):
        try:
            ctx.voice_client.stop()
            self.currentsong = self.songs[self.songno]
            embed = discord.Embed(title="Skipping to next song", colour = discord.Colour.orange())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            message = await ctx.send(embed=embed)
            async with ctx.typing():
                player = await YTDLSource.from_url(self.currentsong, loop=self.client.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            embed = discord.Embed(title="Now playing:",description=player.title, colour = discord.Colour.green())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')        
            await message.edit(embed=embed)
            self.songno += 1
        except IndexError:
            await ctx.send('No songs currently queued.')

    @commands.command(pass_context=True)
    async def play(self, ctx, *, url):
        ctx.voice_client.stop()
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        embed = discord.Embed(title="Now playing:",description=player.title, colour = discord.Colour.green())
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        await ctx.send(embed=embed)
    @play.error
    async def play_error(self, ctx, query):
        if isinstance(query, commands.MissingRequiredArgument):
            l = [
                "Stop wasting Za Hando's time.",
                "Bruh moment.",
                "It's time to stop.",
                "idiot.",
                "It's not that difficult my guy :pensive:"
            ]
            embed = discord.Embed(title="Please specify a song URL",description=random.choice(l), colour = discord.Colour.red())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            await ctx.send(embed = embed)
def setup(client):
    client.add_cog(Music(client))