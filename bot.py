import os
import discord
from discord import app_commands
from discord.interactions import InteractionResponse
from enum import Enum
from discord.ui import Modal, Button, TextInput, View
from discord.ext import commands
import datetime

from commands.handler import setup

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

prefix = "🎲 "

@tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    await tree.sync()
    print('Command tree synced.')

@client.event
async def on_ready():
    setup(client, tree)
    tree.copy_global_to(guild=discord.Object(id=os.environ['GUILD_ID']))
    await tree.sync(guild=discord.Object(id=os.environ['GUILD_ID']))

# run the bot
token = os.environ['ODDROID_TOKEN']
client.run(token)