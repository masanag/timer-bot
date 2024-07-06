import discord
from dotenv import load_dotenv
import os

TOKEN=os.getenv('DISCORD_BOT_TOKEN')
client = discord.Client(intents=discord.Intents.all())
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'hello':
        await message.channel.send('hay')
client.run(TOKEN)