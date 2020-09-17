import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import requests
from discord.ext.commands import has_permissions, bot_has_permissions

class Admin(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Admin cog ready.')

    @commands.command(pass_context=True)
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True, embed_links=True)
    async def purge(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title="Oi Josuke!",description=f"I used Za Hando to erase {amount} messages. Ain\'t that crazy?!", color=discord.Color.red())
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
        await ctx.send(embed=embed)
        
    @commands.command()
    @has_permissions(administrator=True)
    @bot_has_permissions(administrator=True, embed_links=True)
    async def close(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            embed = discord.Embed(title="Channel closed :lock:", description=f"{ctx.message.author.mention} has closed `{channel.name}`, with the help of Za Hando, of course.", color=discord.Color.red())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
            await ctx.send(embed=embed)
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            embed = discord.Embed(title="Channel closed :lock:", description=f"{ctx.message.author.mention} has closed `{channel.name}`, with the help of Za Hando, of course.", color=discord.Color.red())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
            await ctx.send(embed=embed)
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            embed = discord.Embed(title="Channel opened :unlock:", description=f"{ctx.message.author.mention} has opened `{channel.name}`, with the help of Za Hando, of course.", color=discord.Color.green())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
            await ctx.send(embed=embed)
            
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def slowmode(self, ctx, num:int):
        if not num > 21600: 
            embed=discord.Embed(title="Slowmode set. :watch:", description=f"Slowmode set to {num} seconds.", color=discord.Color.blue())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
            await ctx.channel.edit(slowmode_delay=num)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Slowmode failed.", description="Please keep slowmode under 21600 seconds.", color=discord.Color.red())
            embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
            await ctx.send(embed=embed)
def setup(client):
    client.add_cog(Admin(client))