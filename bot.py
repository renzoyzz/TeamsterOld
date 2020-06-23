from enum import Enum
import discord
import configparser
import random
import math

config = configparser.ConfigParser()
config.read('config.ini')
print('The token is {}'.format(config['DEFAULT']['token']))
token = config['DEFAULT']['token']

client = discord.Client()

class Stage(Enum):
    IDLE = 0
    SETUP_CHANNELS = 1
    REGISTER_PLAYERS = 2
    SPLIT = 3


class Lobby:
    players = []
    stage = Stage.IDLE
    startingChannel = 0 
    teamOneChannel = 0
    teamTwoChannel = 0
    teamOne = []
    teamTwo = []

lobby = Lobby()

@client.event
async def on_message(message):
    # global keyword allows you to modify the variable outside of the current scope. It is used to create a global variable and make changes to the variable in a local context.
    # https://www.programiz.com/python-programming/global-keyword
    global lobby
    if message.content.startswith('!Teamster'):
        lobby = Lobby()
        for c in message.channel.guild.voice_channels:
            for m in c.members:
                if m.id == message.author.id:
                    lobby.startingChannel = c
        print(lobby.startingChannel)
        await message.channel.send('Players register by typing !register')
        lobby.stage = Stage.REGISTER_PLAYERS
    elif lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!register'):
        lobby.players.append(message.author)
        await message.channel.send('{0} has been registered'.format(message.author.name))
        await message.author.move_to(lobby.startingChannel)
    elif lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!list'):
        for p in lobby.players:
            await message.channel.send(p.name)
    elif lobby.stage == Stage.REGISTER_PLAYERS and message.content.startswith('!lockin'):
        await message.channel.send("Moving players to random teams!")
        i = 0
        playerCount = len(lobby.players)
        while i < playerCount:
            player = random.choice(lobby.players)
            lobby.players.remove(player)
            if i % 2 == 0:
                lobby.teamOne.append(player)
            else:
                lobby.teamTwo.append(player)
            i += 1
        for c in message.channel.guild.voice_channels:
           if c.name == 'T-Side':
                for p in lobby.teamOne:
                    await p.move_to(c)
           elif c.name == 'CT-Side':
                for p in lobby.teamTwo:
                    await p.move_to(c)

client.run(token)

