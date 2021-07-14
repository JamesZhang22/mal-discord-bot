import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from main_webscrape import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# intents = discord.Intents(members=True, messages=True, guilds=True)
intents = discord.Intents().all()
activity = discord.Game(name="?help")
bot = commands.Bot(command_prefix='?', intents=intents, activity=activity)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    print(f"{member.name} has joined.")
    await member.send(f'Welcome {member.name} to the server!\nUse ?help for more info!')

@bot.command(help="Get bot's latency in milliseconds.")
async def ping(ctx):
    await ctx.send(f"Pong!\n{round(bot.latency*1000)}ms")

@bot.command(help="Clear chat")
# @commands.has_role("dj")
async def clear(ctx, amt=5):
    await ctx.channel.purge(limit=amt)

@bot.command(help="Anime show 8 ball.")
async def watch(ctx, *question):
    responses = ['Yes', 'Definetly', 'No', 'NO!', 'Perhaps', 'Go for it!', 'Nah', 'In a week', 'NEVER!', 'WATCH IT RIGHT NOW!']
    await ctx.send(f"Show: {''.join(question)}\nAnswer: {random.choice(responses)}")

@bot.command(help="Recommends a random show.")
async def ranime(ctx, genre=None):
    reply = random.choice(list(name_id.keys()))
    if not genre:
        await ctx.send(f"{reply}: https://myanimelist.net/anime/{name_id[reply]}")
    else:
        if genre.lower() in all_genres:
            reply = random.choice(get_genre_list(genre.lower())).replace("!", "")
            await ctx.send(f"Genre: {genre.capitalize()}\nAnime: {reply}\nLink: https://myanimelist.net/anime/{name_id[reply.lower()]}")
        else:
            await ctx.send("Not a valid genre!")

@bot.command(help="Display show stats on myanimelist.")
async def details(ctx, *show: str):
    show = str(show)
    show_name = show.replace(', ', ' ').replace("'", '').replace('(', '').replace(')', '').lower()
    print(show_name)
    reply = get_anime_stats(show_name)
    await ctx.send(reply)

bot.run(TOKEN)