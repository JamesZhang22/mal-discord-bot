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
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    print(f"{member.name} has joined.")
    await member.send(f'Welcome {member.name} to the server!\nUse ?help for more info!')

@bot.command(name="ranime", help="Recommends a random show.")
async def ranime(ctx):
    reply = random.choice(list(name_id.keys()))
    await ctx.send(reply)

@bot.command(name="details", help="Display show stats on myanimelist.")
async def details(ctx, *show: str):
    show_name = ''.join(show)
    reply = get_anime_stats(show_name)
    await ctx.send(reply)

bot.run(TOKEN)