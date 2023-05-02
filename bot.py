# bot.py
import os

import discord
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print("Received message: ", message.content)
    await message.channel.send(message.content)

token = os.environ['ODDROID_TOKEN']
print("Running bot with token = ", token)
bot.run(token)
