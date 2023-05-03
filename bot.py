import os
import discord
from discord import app_commands
from discord.interactions import InteractionResponse
from enum import Enum
from discord.ui import Modal, Button, TextInput, View
from discord.ext import commands
import datetime

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

prefix = "🎲 "

@tree.command(name='sync', description='Owner only')
async def sync(interaction: discord.Interaction):
    await tree.sync()
    print('Command tree synced.')

@tree.command(name = "odds", description = "Start a round of odds.") 
async def odds_command(interaction: discord.Interaction, member: discord.Member, maximum: int):
    _max = maximum
    if(member == interaction.user):
        await message(interaction, "**You can't begin odds with yourself!**", discord.Color.red(), True)
    elif(member == client.user):
        # Get the length of the longest display name
        max_length = max(len(interaction.user.display_name), len(member.display_name))

        # Calculate the spacing needed for each name
        user_padding = ((max_length - len(interaction.user.display_name)) + 10) * " "
        member_padding = ((max_length - len(member.display_name)) + 7) * " "
                
        embed = discord.Embed(title=prefix + f"**{interaction.user.display_name} vs. {member.display_name}**")
        embed.add_field(name=f"\t\t1 to {_max} odds started by {interaction.user.display_name}", value="\u200b", inline=False)
        embed.add_field(name=f"> {interaction.user.display_name}:{user_padding} ❌\n> {member.display_name}:{member_padding} ❌", value="\u200b", inline=False)
        embed.set_thumbnail(url="https://thumbs.gfycat.com/FlamboyantFickleIrishwolfhound-size_restricted.gif") # countdown timer for testing purposes only (not my own)
        await interaction.channel.send(embed=embed)

        class NumInputModal(discord.ui.Modal, title=f'Pick Your Number From 1 to {_max}.'):
            name = discord.ui.TextInput(label="Pick A Number (Expires in 30s)", placeholder=f"{_max}", min_length=1, max_length=len(str(_max)))

            async def on_submit(self, interaction: discord.Interaction):
                print("submit...")
        modal = NumInputModal()
        await interaction.response.send_modal(modal)

        

async def message(interaction: discord.Interaction, message: str, color: int, ephemeral: bool):
    # create a new embed object and set its color to red
    embed = discord.Embed(description=prefix + message, color=color)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


@client.event
async def on_ready():
    await tree.sync()

# run the bot
token = os.environ['ODDROID_TOKEN']
client.run(token)