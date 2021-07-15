import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from main_webscrape import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
activity = discord.Game(name="?help")
bot = commands.Bot(command_prefix='?', intents=intents, activity=activity, help_command=None)

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
        embed.add_field(name="Anime Commands", value="?watch\n?ranime\n?details")
        embed.add_field(name="Basic Commands", value="?ping\n?clear")
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
    await ctx.send(f"Pong!\n{round(bot.latency*1000)}ms")

@bot.command(help="Clear chat")
# @commands.has_role("dj")
async def clear(ctx, amt=5):
    await ctx.channel.purge(limit=amt)

# Anime Commands
@bot.command(help="8ball for whether or not you should watch a show!")
async def watch(ctx, *question):
    responses = ['Yes', 'Definetly', 'No', 'NO!', 'Perhaps', 'Go for it!', 'Nah', 'In a week', 'NEVER!', 'WATCH IT RIGHT NOW!']
    await ctx.send(f"Show: {''.join(question)}\nAnswer: {random.choice(responses)}")

@bot.command(help="Recommends a random show(can pass in one genre).")
async def ranime(ctx, genre=None):
    reply = random.choice(list(name_id.keys())).replace("!", "").replace("/", '').replace("(", '').replace(")", '')
    if not genre:
        embed = discord.Embed(title=f"Anime: {get_anime_stats(reply)[0]}", color=discord.Color.blue())
        embed.set_thumbnail(url=get_anime_stats(reply)[7])
        embed.add_field(name="Link", value=f"https://myanimelist.net/anime/{name_id[reply]}", inline=False)
        await ctx.send(embed=embed)
    else:
        if genre.lower() in all_genres:
            reply = random.choice(get_genre_list(genre.lower())).replace("!", "").replace("/", '').replace("(", '').replace(")", '')
            embed = discord.Embed(title=f"Anime: {get_anime_stats(reply)[0]}", color=discord.Color.blue())
            embed.set_author(name=f"Genre: {genre.capitalize()}")
            embed.set_thumbnail(url=get_anime_stats(reply.lower())[7])
            embed.add_field(name="Link", value=f"https://myanimelist.net/anime/{name_id[reply.lower()]}", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Not a valid genre!")

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




bot.run(TOKEN)