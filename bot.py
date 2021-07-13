import os

import discord
from dotenv import load_dotenv

intents = discord.Intents(members=True)
client = discord.Client(intents=intents)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    print(member.name)
    await member.send(f'Welcome {member.name} to the server!')

client.run(TOKEN)