import discord
import asyncio

class OddsGame:
    
    def __init__(self, player1: discord.Member, player2: discord.Member, max: int):
        self.author = player1
        self.player = player2

        self.chooser = self.author
        self.guesser = self.player

        self.winner = None
        self.loser = None

        self.max = max

        self.ongoing = True

        self.scores = {}
        self.scores[self.author.name] = 0
        self.scores[self.player.name] = 0
    
    # Returns whoever originally started the Odds Match
    def get_author(self):
        return self.author
    
    # Returns whoever originally joined the Odds Match
    def get_player(self):
        return self.player

    def set(self, player: discord.Member, val: int):
        self.scores[player.name] = val
        print(f"{player.name} set {val}!")  
        print(self.scores)

        if(self.scores[self.chooser.name] > 0 and self.scores[self.guesser.name] > 0):
            self.end_round()
            return True
        
        return False

    def get_max(self):
        return self.max

    async def wait_till_round(self):
        while self.ongoing:
            await asyncio.sleep(1)
        return self.winner

    def get_number(self, player: discord.Member):
        return self.scores[player.name]

    def get_winner(self):
        return self.winner
    
    def get_loser(self):
        return self.loser
    
    def is_ongoing(self):
        return self.ongoing
    
    def next_round(self):
        self.ongoing = True

        self.scores[self.author.name] = 0
        self.scores[self.player.name] = 0

        self.max = self.max - 1

    def end_round(self):
        self.ongoing = False

        if(self.scores[self.guesser.name] == self.scores[self.chooser.name]):
            self.winner = self.guesser
            self.loser = self.chooser
            return(self.winner)

        self.chooser, self.guesser = self.guesser, self.chooser


matches = {}

def start_match(player1: discord.Member, player2: discord.Member, max: int):
    game = OddsGame(player1, player2, max)
    matches[player1.name] = game
    matches[player2.name] = game
    return game

def get_match(player: discord.Member):
    return matches[player.name]