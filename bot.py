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
bot = commands.Bot(command_prefix='?', intents=intents, activity=activity)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    print(f"{member.name} has joined.")
    await member.send(f'Welcome {member.name} to the server!\nUse ?help for more info!')

@bot.command()
async def displayembed(ctx):
    embed = discord.Embed(title="Title", description="Test", color=discord.Color.blue())
    embed.set_footer(text="footer")
    embed.set_image(url="https://hatrabbits.com/wp-content/uploads/2017/01/random.jpg")
    embed.set_thumbnail(url="https://i.pinimg.com/originals/5b/b4/8b/5bb48b07fa6e3840bb3afa2bc821b882.jpg")
    embed.set_author(name="Bot", icon_url="https://hatrabbits.com/wp-content/uploads/2017/01/random.jpg")
    embed.add_field(name="Field", value="val", inline=False)
    embed.add_field(name="Field", value="val", inline=True)
    embed.add_field(name="Field", value="val", inline=True)

    await ctx.send(embed=embed)

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
        await ctx.send(f"https://myanimelist.net/anime/{name_id[reply]}")
    else:
        if genre.lower() in all_genres:
            reply = random.choice(get_genre_list(genre.lower())).replace("!", "")
            embed = discord.Embed(title=f"Anime: {reply.capitalize()}", color=discord.Color.blue())
            embed.set_author(name=f"Genre: {genre.capitalize()}")
            embed.set_thumbnail(url="https://i.pinimg.com/originals/5b/b4/8b/5bb48b07fa6e3840bb3afa2bc821b882.jpg")
            embed.add_field(name="Link", value=f"https://myanimelist.net/anime/{name_id[reply.lower()]}", inline=False)

            await ctx.send(embed=embed)
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