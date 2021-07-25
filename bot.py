import os
import random
import youtube_dl
import discord
from discord.ext import commands
from dotenv import load_dotenv

from main_webscrape import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
activity = discord.Game(name="?help")
bot = commands.Bot(command_prefix='?', intents=intents, activity=activity, help_command=None)
players = {}

# Basic Event Handling
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    print(f"{member.name} has joined.")
    await member.send(f'Welcome {member.name} to the server!\nUse ?help for more info!')


# Custom Help Command
@bot.command()
async def help(ctx, cmd=None):
    commands = [command.name for command in bot.commands]
    if not cmd:
        embed = discord.Embed(title="MALBOT'S COMMANDS!", color=discord.Color.blue())
        embed.add_field(name="Anime Commands", value="?watch\n?ranime\n?details\n?user\n?astats\n?mstats\n?guess")
        embed.add_field(name="Basic Commands", value="?ping\n?clear")
        embed.add_field(name="Music Commands", value="?play\n?leave\n?pause\n?resume\n?stop")
        embed.add_field(name="For More Details", value="?help <command name>", inline=False)
    elif cmd in commands:
        embed = discord.Embed(color=discord.Color.blue())
        embed.add_field(name=cmd, value=bot.get_command(cmd).help)
    else:
        embed = discord.Embed(color=discord.Color.red())
        embed.add_field(name="Error", value="No such command!")

    await ctx.send(embed=embed)


# Basic Commands
@bot.command(help="Get bot's latency in milliseconds.")
async def ping(ctx):
    ms = round(bot.latency*1000)
    if ms < 51:
        embed = discord.Embed(title="Pong", description = str(ms) + 'ms', color=discord.Color.green())
    elif 51 < ms < 150:
        embed = discord.Embed(title="Pong", description = str(ms) + 'ms', color=discord.Color.from_rgb(255, 255, 0))
    else:
        embed = discord.Embed(title="Pong", description = str(ms) + 'ms', color=discord.Color.red())
    await ctx.send(embed=embed)


@bot.command(help="Clear chat (can pass in optional value for # of messages).")
# @commands.has_role("dj")
async def clear(ctx, amt=5):
    await ctx.channel.purge(limit=amt)


# Music Commands
@bot.command(help="Play a video from youtube.")
async def play(ctx, url: str):
    if url == 'duck':
        url = "https://www.youtube.com/watch?v=3flILVgNIi0&ab_channel=Kiddopedia"
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@bot.command(help="Disconnect bot from voice channel.")
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(help="Pause the current video playing.")
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@bot.command(help="Resume the current video playing.")
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@bot.command(help="Stop the video.")
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


# Anime Commands
@bot.command(help="8ball for whether or not you should watch a show!")
async def watch(ctx, *question):
    responses = ['Yes', 'Definetly', 'No', 'NO!', 'Perhaps', 'Go for it!', 'Nah', 'In a week', 'NEVER!', 'WATCH IT RIGHT NOW!']
    embed = embed = discord.Embed(title="8ball", color=discord.Color.blue())
    embed.add_field(name="Answer", value=random.choice(responses))
    await ctx.send(embed=embed)


@bot.command(help="Recommends a random show (can pass in one genre).")
async def ranime(ctx, genre=None):
    reply = random.choice(list(name_id.keys())).replace("!", "").replace("/", '').replace("(", '').replace(")", '')
    if not genre:
        stats = get_anime_stats(reply)
        embed = discord.Embed(title=f"Anime: {stats[0]}", color=discord.Color.blue())
        embed.set_thumbnail(url=stats[7])
        embed.add_field(name="Link", value=stats[9], inline=False)
        await ctx.send(embed=embed)
    else:
        if genre.lower() in all_genres:
            reply = random.choice(get_genre_list(genre.lower())).replace("!", "").replace("/", '').replace("(", '').replace(")", '')
            stats = get_anime_stats(reply)
            embed = discord.Embed(title=f"Anime: {stats[0]}", color=discord.Color.blue())
            embed.set_author(name=f"Genre: {genre.capitalize()}")
            embed.set_thumbnail(url=stats[7])
            embed.add_field(name="Link", value=stats[9], inline=False)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Not a valid genre!", color=discord.Color.red())
            await ctx.send(embed=embed)


@bot.command(help="Display the anime's stats on myanimelist.")
async def details(ctx, *show: str):
    show = str(show)
    show_name = show.replace(', ', ' ').replace("'", '').replace('(', '').replace(')', '').replace(",", '').lower()
    reply = get_anime_stats(show_name)
    embed = discord.Embed(title=f"Anime: {reply[0]}", color=discord.Color.blue())
    embed.set_author(name=f"Genre(s): {reply[5]}")
    embed.set_thumbnail(url=reply[7])
    embed.add_field(name=f"Rating: {reply[1]}", value='\u200b')
    embed.add_field(name=f"Rank: {reply[2]}", value='\u200b')
    embed.add_field(name=f"Popularity: {reply[3]}", value='\u200b')
    embed.add_field(name=f"Episodes: {reply[4]}", value='\u200b')
    embed.add_field(name="Description", value=reply[8], inline=False)
    embed.add_field(name="Similar Shows", value=reply[6], inline=False)
    embed.add_field(name="Link", value=reply[9], inline=False)
    await ctx.send(embed=embed)


@bot.command(help="Display the user general information.")
async def user(ctx, name: str):
    reply = get_user(name)
    if not reply:
        embed = discord.Embed(title='Invalid User', color=discord.Color.red())
    else:
        embed = discord.Embed(title=reply[0], color=discord.Color.blue())
        embed.set_thumbnail(url=reply[1])
        embed.set_author(name=f"Last Online: {reply[2]}")
        embed.add_field(name="Forum Posts", value=reply[3]["Forum Posts"])
        embed.add_field(name="Reviews", value=reply[3]["Reviews"])
        embed.add_field(name="Recommendations", value=reply[3]["Recommendations"])
        embed.add_field(name="Blog Posts", value=reply[3]["Blog Posts"])
        embed.add_field(name="Clubs", value=reply[3]["Clubs"])
        embed.add_field(name="Friends", value=reply[4])
        embed.add_field(name="\u200b", value=reply[5], inline=False)
    await ctx.send(embed=embed)


@bot.command(help="Display the user anime stats.")
async def astats(ctx, name: str):
    reply = get_user_anime_stats(name)
    if not reply:
        embed = discord.Embed(title='Invalid User', color=discord.Color.red())
    else:
        embed = discord.Embed(title=reply[0], color=discord.Color.blue())
        embed.set_thumbnail(url=reply[5])
        embed.add_field(name=f"Entries", value=reply[1])
        embed.add_field(name=f"Watching", value=reply[2][0])
        embed.add_field(name=f"Completed", value=reply[2][1])
        embed.add_field(name=f"On-Hold", value=reply[2][2])
        embed.add_field(name=f"Dropped", value=reply[2][3])
        embed.add_field(name=f"Plan to Watch", value=reply[2][4])
        if reply[3] != []:
            embed.add_field(name="Favorite Shows", value=reply[3])
        embed.add_field(name="\u200b", value=reply[4], inline=False)
    await ctx.send(embed=embed)


@bot.command(help="Display the user manga stats.")
async def mstats(ctx, name: str):
    reply = get_user_manga_stats(name)
    if not reply:
        embed = discord.Embed(title='Invalid User', color=discord.Color.red())
    else:
        embed = discord.Embed(title=reply[0], color=discord.Color.blue())
        embed.set_thumbnail(url=reply[5])
        embed.add_field(name=f"Entries", value=reply[1])
        embed.add_field(name=f"Reading", value=reply[2][0])
        embed.add_field(name=f"Completed", value=reply[2][1])
        embed.add_field(name=f"On-Hold", value=reply[2][2])
        embed.add_field(name=f"Dropped", value=reply[2][3])
        embed.add_field(name=f"Plan to Read", value=reply[2][4])
        if reply[3] != []:
            embed.add_field(name="Favorite Mangas", value=reply[3])
        embed.add_field(name="\u200b", value=reply[4], inline=False)
    await ctx.send(embed=embed)


@bot.command(help="Guess a random anime character with 3 guesses.")
async def guess(ctx):
    character = get_random_character()
    lower_character = character.lower()
    try:
        first_name = lower_character.split(", ")[1]
        last_name = lower_character.split(", ")[0]
    except:
        first_name = None
    img = get_image_character(character)
    
    embed = discord.Embed(title='Guess', color=discord.Color.blue())
    embed.set_image(url=img)
    await ctx.send(embed=embed)

    response = await bot.wait_for('message')
    guess = str(response.content).lower()

    if guess == lower_character.replace(",", ''):
        embed2 = discord.Embed(title='Correct', color=discord.Color.green())
    elif guess == first_name:
        embed2 = discord.Embed(title='Correct', color=discord.Color.green())
    elif guess == last_name:
        embed2 = discord.Embed(title='Correct', color=discord.Color.green())
    elif guess == f"{first_name} {last_name}":
        embed2 = discord.Embed(title='Correct', color=discord.Color.green())
    else:
        embed2 = discord.Embed(title='Incorrect', color=discord.Color.red())
        embed2.add_field(name=f"Character", value=character.replace(",", ""))

    await ctx.send(embed=embed2)


bot.run(TOKEN)