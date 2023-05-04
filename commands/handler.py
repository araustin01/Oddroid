import discord
from discord import app_commands
from .odds_cmd import OddsCmd

def setup(client: discord.Client, tree: app_commands.CommandTree[discord.Client]):
    _odds = OddsCmd(client, tree)
    _odds.register()