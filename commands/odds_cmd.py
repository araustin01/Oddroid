import discord
import random
from discord import app_commands
from config import prefix
from game import OddsGame, start_match, get_match

async def respond(interaction: discord.Interaction, message: str, color: int, ephemeral: bool):
    # create a new embed object and set its color to red
    embed = discord.Embed(description=prefix + message, color=color)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

async def message(recepient: discord.User, message: str, color: int, ephemeral: bool):
    # create a new embed object and set its color to red
    embed = discord.Embed(description=prefix + message, color=color)
    await recepient.send(embed=embed, ephemeral=ephemeral)

class OddsCmd:
    def __init__(self, client: discord.Client, tree: app_commands.CommandTree[discord.Client]):
        self.client = client
        self.tree = tree

    def register(self):
        self.client.slash = self.tree.command(name = "odds", description = "Start a round of odds.")(self.odds_command)

    async def odds_command(self, interaction: discord.Interaction, member: discord.Member, maximum: int):
        _max = maximum
        if(member == interaction.user):
            await respond(interaction, "**You can't begin odds with yourself!**", discord.Color.red(), True)
        elif(member == self.client.user):
            start_match(interaction.user, member, maximum)

            rnd_pick = random.randint(1, maximum)
            get_match(member).set(member, rnd_pick)

            # Get the length of the longest display name
            max_length = max(len(interaction.user.display_name), len(member.display_name))

            # Calculate the spacing needed for each name
            user_padding = ((max_length - len(interaction.user.display_name)) + 10) * " "
            member_padding = ((max_length - len(member.display_name)) + 7) * " "
                    
            embed = discord.Embed(title=prefix + f"**{interaction.user.display_name} vs. {member.display_name}**")
            embed.add_field(name=f"\t\t1 to {_max} odds started by {interaction.user.display_name}", value="\u200b", inline=False)
            embed.add_field(name=f"> {interaction.user.display_name}:{user_padding} ❌", value="\u200b", inline=False)
            embed.add_field(name=f"> {member.display_name}:{member_padding} ✅", value="\u200b", inline=False)
            embed.set_thumbnail(url="https://thumbs.gfycat.com/FlamboyantFickleIrishwolfhound-size_restricted.gif") # countdown timer for testing purposes only (not my own)
            msg = await interaction.channel.send(embed=embed)

            class NumInputModal(discord.ui.Modal, title=f'Pick Your Number From 1 to {_max}.'):
                def __init__(self):
                    super().__init__()
                    self.value_input = discord.ui.TextInput(label="Pick A Number (Expires in 30s)", placeholder=f"{_max}", min_length=1, max_length=len(str(_max)))
                    self.add_item(self.value_input)

                async def on_submit(self, interaction: discord.Interaction):
                    choice: int = int(self.value_input.value)
                    game: OddsGame = get_match(interaction.user)
                    if(game.set(interaction.user, choice)):
                        winner: discord.Member = game.get_winner()
                        loser: discord.Member = game.get_loser()

                        embed.set_field_at(1, name=f"> {interaction.user.display_name}:{user_padding} **{game.get_number(interaction.user)}**", value="\u200b", inline=False)
                        embed.set_field_at(2, name=f"> {member.display_name}:{member_padding} **{game.get_number(member)}**", value="\u200b", inline=False)

                        if(winner is not None and loser is not None):
                            embed.add_field(name=f"\n🎉 {winner.name} won!", value="\u200b", inline=False)
                            embed.color = discord.Color.green()
   
                            if(interaction.user == winner):
                                await respond(interaction, f"You guessed {interaction.user.display_name} and won!", discord.Color.green(), True)
                                await message(loser, f"{member.display_name} guessed your number and won!", discord.Color.red(), True)
                            else:
                                await message(winner, f"You guessed {interaction.user.display_name} and won!", discord.Color.green(), True)
                                await respond(interaction, f"{member.display_name} guessed your number and won!", discord.Color.red(), True)

                            await msg.edit(embed=embed)
                        else:
                            embed.color = discord.Color.yellow()
                            await respond(interaction, f"{member.display_name} did not guess your number!", discord.Color.green(), True)
                            embed.add_field(name=f"\nNo winner! {member.display_name} did not guess {interaction.user.display_name}'s number.", value="\u200b", inline=False)
                            await msg.edit(embed=embed)
                    else:                        
                        await respond(interaction, f"Your pick was **{choice}**! Waiting on others...", discord.Color.blue(), True)
                        embed.set_field_at(1, name=f"> {interaction.user.display_name}:{user_padding} ✅\n", value="\u200b", inline=False)
                        await msg.edit(embed=embed)

            modal = NumInputModal()
            await interaction.response.send_modal(modal)

