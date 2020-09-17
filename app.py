import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord.utils import find
import qrcode, os, datetime, json, time, requests, random

prefixes = {}

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix, case_insensitive=True)
client.remove_command('help')

first_time = datetime.datetime.now()

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = 'Oi Josuke! '
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        hello = discord.Embed(
            title = f'Oi {guild.name}!',
            description = 'Please use Oi Josuke! help for a list of commands.',
            colour = discord.Colour.blue()
        )
        
        hello.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        hello.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        hello.set_image(url='https://media1.tenor.com/images/64c94bc74be39aa6bfe2ea42556972f3/tenor.gif?itemid=15525426')
        
        await general.send("If you have any problems, questions or feedback, please join our support server: https://discord.gg/vuYseDR",embed=hello)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)



@client.command()
async def prefix(ctx, * , prefix):
    if ctx.message.author.guild_permissions.administrator:
        if isinstance(prefix, commands.MissingRequiredArgument):
            await ctx.send('Please specify a prefix.')
        if prefix[-2:] == '>>':
            prefix = prefix[:-2]
            prefix += ' '
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f'Oi Josuke! help'))
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f'I used Za Hando to update the prefix! `{prefix}`.')
    else:
        await ctx.send('Sorry, it seems you don\'t have sufficient privileges to execute this command.')
  

@client.command()
async def fun(ctx):
    await ctx.send('Did you mean `help fun`?')

@client.command()
async def config(ctx):
    await ctx.send('Did you mean `help config`?')

@client.command()
async def jojo(ctx):
    await ctx.send('Did you mean `help fun`?')

@client.command()
async def sound(ctx):
    await ctx.send('Did you mean `help sound`?')

@client.command()
async def util(ctx):
    await ctx.send('Did you mean `help util`?')

@client.command()
async def admin(ctx):
    await ctx.send('Did you mean `help admin`?')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Oi Josuke! help'))
    first_time = datetime.datetime.now()
    print('Bot ready.')  

@client.event
async def on_command_error(ctx, error):
    # if command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Oi Josuke!",description="You didn't seem to pass in all the required arguments for this command.",color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="This command is on cooldown", description=f'Please try again in `{error.retry_after:,.1f}` seconds.', color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.TooManyArguments):
        embed = discord.Embed(title="Stop wasting Za Hando's time!",description="You specified too many things!!",color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="nani the fuck",description='Looks like you don\'t have permissions to do that! :think:',color=discord.Color.red())
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        if fmt == "Embed Links":
            await ctx.send(f"I don't seem to have the {fmt} permissions to do this!")
        else:
            embed = discord.Embed(title="You restrain Za Hando's power, why?",description=f"I don't seem to have the {fmt} permissions to do this!",color=discord.Color.red())
            await ctx.send(embed=embed)
        return

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        

@client.command(pass_context = True)
async def help(ctx, args=''):
    author = ctx.message.author.mention
    
    if args == 'sound':
        sound = discord.Embed(
            title = 'Sound Help',
            description = 'Here\'s a list of sound-related commands.',
            colour = discord.Colour.blue()
        
        )
        
        sound.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        sound.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        sound.add_field(name='`join`', value='Joins current voice channel.', inline=False)
        sound.add_field(name='`leave`', value='Leaves current voice channel.', inline=False)
        sound.add_field(name='`play <URL>`', value='Plays specified YouTube URL in current voice channel.', inline=False)
        sound.add_field(name='`stop`', value='Stops playing audio.', inline=False)
        sound.add_field(name='`queue <URL>`', value='Adds specified YouTube URL to queue.', inline=False)
        sound.add_field(name='`next`', value='Plays next song in queue.', inline=False)
        
        await ctx.send(author, embed=sound)

    elif args == 'util':
        util = discord.Embed(
            title = 'Utility Help',
            description = 'Here\'s a list of useful commands.',
            colour = discord.Colour.blue()
            
        )
        
        util.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        util.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        util.add_field(name='`translate <Sentence>`', value='Translates specified message into english.', inline=False) 
        util.add_field(name='`qr <Data>`', value='Returns QR Code with specified data.', inline=False) 
        util.add_field(name='`say <Message>`', value='Returns specified message.', inline=False)
        util.add_field(name='`reddit <Subreddit>`', value='Returns random post from specified subreddit.', inline=False)  
        util.add_field(name='`anime <Anime>`', value='Returns information on requested anime.', inline=False)  
        await ctx.send(author, embed=util)   
    elif args == 'config':
            config = discord.Embed(
                title = 'Configuration Help',
                description = 'Here\'s a list of settings.',
                colour = discord.Colour.blue()
                
            )
            
            config.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            config.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
            config.add_field(name='`ping`', value='Returns current ping.', inline=False)   
            config.add_field(name='`prefix <Prefix>`', value='Changes bot prefix as specified.(use ">>" at the end for a space)', inline=False)
            config.add_field(name='`info`', value='Returns information on this bot.', inline=False) 
            
            await ctx.send(author, embed=config)       
    elif args == 'fun':
        fun = discord.Embed(
            title = 'Fun Help',
            description = 'Here\'s a list of fun commands.',
            colour = discord.Colour.blue()
            
        )
        
        fun.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        fun.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        fun.add_field(name='`inspire`', value='Returns a random inspirational quote.', inline=False) 
        fun.add_field(name='`steppedin <Shit>`', value='Returns "ew i stepped in shit" meme.', inline=False)
        fun.add_field(name='`dolphin`', value='Returns how many dolphins Jotaro has fucked.', inline=False)
        fun.add_field(name='`hentai`', value='Returns hentai. ( ͡° ͜ʖ ͡°)', inline=False)
        fun.add_field(name='`meme`', value='Returns a random JoJo meme.', inline=False) 
        fun.add_field(name='`truth`', value='Returns THE TRUTH.', inline=False) 
        fun.add_field(name='`character`', value='Returns a random JoJo character.', inline=False) 
        await ctx.send(author, embed=fun)
    elif args == 'admin':
        fun = discord.Embed(
            title = 'Admin Help',
            description = 'Here\'s a list of admin commands. **If you invited this bot before 31/08/2020, you will need to enable Administrator privileges to use these commands.**',
            colour = discord.Colour.blue()
            
        )
        
        fun.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        fun.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        fun.add_field(name='`purge <Amount>`', value='Purges specified amount of messages.', inline=False) 
        fun.add_field(name='`slowmode <Time>`', value='Sets slowmode for current channel.', inline=False) 
        fun.add_field(name='`close <Channel>`', value='Closes or opens specified channel for default role. (Defaults to current channel)', inline=False)
        await ctx.send(author, embed=fun)
    else:
        embed = discord.Embed(
            title = 'Help',
            description = 'Here\'s a list of help commands.',
            colour = discord.Colour.blue()
            
        )
        
        embed.set_author(name='Okuyasu', icon_url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/720731150254866553/94ff5f04cc3a5bbe36e70d63a44980a6.png?size=256')
        
        embed.add_field(name='`help fun`', value='Returns help for fun and jojo commands.', inline=True)
        embed.add_field(name='`help sound`', value='Returns help for sound related commands.', inline=True)  
        embed.add_field(name='`help util`', value='Returns information for useful commands.', inline=True)
        embed.add_field(name='`help config`', value='Returns help for configuration commands.', inline=True)
        embed.add_field(name='`help admin`', value='Returns help for administrator commands.', inline=True)        
        embed.add_field(name='Latest commands:',value='`slowmode`', inline=False)
        await ctx.send(author, embed=embed)
        
client.run(TOKEN)