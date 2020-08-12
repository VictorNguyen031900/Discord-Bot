import discord
import random
import time
import asyncio
import datetime
import math
import os
from time import *
from discord.ext import commands, tasks
from itertools import cycle

#Gets bot token from token.txt
global token
file = open('token.txt','r')
for line in file:
    token = str(line)
file.close()

#Starts discord bot connection
client = commands.Bot(command_prefix = '+')
client.remove_command('help')

#Used to cycle through bot statuses
status = cycle(['Bot is online!', 'Ready to work!', 'Do \'+help\'!'])

#Bot Wakes Up
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd,activity=discord.Game('Waking Up!'))
    sleep(1.5)
    await client.change_presence(status=discord.Status.dnd,activity=discord.Game('I Am Awake Now!'))
    sleep(1.5)
    await client.change_presence(status=discord.Status.dnd,activity=discord.Game(''))
    #change status function
    change_status.start()
    print('We have logged in as {0.user}'.format(client))

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(status=discord.Status.dnd,activity=discord.Game(next(status)))

#Commands
@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx):
    checkEmoji = '\U00002705'
    okhandEmoji = '\U0001F44C'
    okEmoji = '\U0001F197'
    await ctx.message.add_reaction(okEmoji)
    #Log to console
    commandTimeExecuted = datetime.datetime.now()
    print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted} on server \'{ctx.guild.name}\'({ctx.guild.id})')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            print(f'Unloaded {filename}!')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename} at {datetime.datetime.now()}')
            currentDir = os.getcwd()
            #Embed
            LoadedEmbed = discord.Embed(colour=discord.Colour.purple(), title=f'Loaded {filename} at {datetime.datetime.now()}')
            file = [discord.File(fp=f'{currentDir}\\Assets\\PythonLogo.png')]
            LoadedEmbed.set_author(name='Extension Loader', icon_url='attachment://PythonLogo.png')
            await ctx.channel.send(embed=LoadedEmbed, files=file)

@client.command()
async def help(ctx):
    #Indicates that command was accepted
    checkEmoji = '\U00002705'
    okhandEmoji = '\U0001F44C'
    okEmoji = '\U0001F197'
    await ctx.message.add_reaction(okEmoji)
    #Log to console
    commandTimeExecuted = datetime.datetime.now()
    print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted} on server \'{ctx.guild.name}\'({ctx.guild.id})')
    #Setup embed with all commands
    HelpEmbed = discord.Embed(colour=discord.Colour.red(), title='Typing Bot', description='By Victor Nguyen (VecturNewwin)')
    HelpEmbed.set_author(name='Help')
    HelpEmbed.add_field(name='1. +about', value='Information about Typing Bot!\n', inline=False)
    HelpEmbed.add_field(name='2. +clear [EMPTY/NUMBER]', value='Clears line(s) in current text channel!\n', inline=False)
    HelpEmbed.add_field(name='3. +start', value='Starts a typing test!\n', inline=False)
    HelpEmbed.add_field(name='4. +reload', value='ADMIN ONLY\n', inline=False)
    #Sends embed back to channel
    await ctx.channel.send(embed=HelpEmbed)

@client.command()
async def about(ctx):
    #Indicates that command was accepted
    checkEmoji = '\U00002705'
    okhandEmoji = '\U0001F44C'
    okEmoji = '\U0001F197'
    await ctx.message.add_reaction(okEmoji)
    #Log to console
    commandTimeExecuted = datetime.datetime.now()
    print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted} on server \'{ctx.guild.name}\'({ctx.guild.id})')
    #Sends message to channel
    await ctx.channel.send('Take a look at my github for more information! https://github.com/VictorNguyen031900/Discord-Bot')

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, *args):
    #Indicates that command was accepted
    checkEmoji = '\U00002705'
    okhandEmoji = '\U0001F44C'
    okEmoji = '\U0001F197'
    await ctx.message.add_reaction(okEmoji)
    sleep(0.5)
    if not args:
        #Delete an amount of messages
        await ctx.channel.purge(limit=int(2))
        commandTimeExecuted = datetime.datetime.now()
        print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted} on server \'{ctx.guild.name}\'({ctx.guild.id})')
        print(f'{ctx.message.author} cleared 2 line(s)!')
    elif args[0]:
        #Delete an amount of messages
        await ctx.channel.purge(limit=(int(args[0]) + 1))
        commandTimeExecuted = datetime.datetime.now()
        print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted} on server \'{ctx.guild.name}\'({ctx.guild.id})')
        print(f'{ctx.message.author} cleared {int(args[0]) + 1} line(s)!')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}!')

client.run(f'{token}')
