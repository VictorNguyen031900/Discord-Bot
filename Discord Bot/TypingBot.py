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

#TO DO list
#1. Implement a leveling system
#2. Implement intergration with google sheet API


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
    #loads words from text file
    global wordCount
    global listWords
    wordCount = 0
    listWords = []
    file = open('words.txt','r')
    for line in file:
        line = line.strip('\n')
        listWords.append(line)
        wordCount += 1
    file.close()
    print(str(wordCount) + ' words were added... from words.txt')

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(status=discord.Status.dnd,activity=discord.Game(next(status)))

#Seperated Commands
@client.command()
async def help(ctx):
    #Indicates that command was accepted
    checkEmoji = '\U00002705'
    okhandEmoji = '\U0001F44C'
    await ctx.message.add_reaction(okhandEmoji)
    #Log to console
    commandTimeExecuted = datetime.datetime.now()
    print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted}')
    #Setup embed with all commands
    testembed = discord.Embed(colour=discord.Colour.red(), title='Typing Bot', description='By Victor Nguyen (VecturNewwin)')
    testembed.set_author(name='Help')
    testembed.add_field(name='1. +about', value='Information about Typing Bot!\n', inline=False)
    testembed.add_field(name='2. +clear', value='Clears line(s) in current text channel!\n', inline=False)
    testembed.add_field(name='3. +start', value='Starts a typing test!\n', inline=False)
    #Sends embed back to channel
    await ctx.channel.send(embed=testembed)

@client.command()
async def about(ctx):
    #Indicates that command was accepted
    checkEmoji = '\U00002705'
    okhandEmoji = '\U0001F44C'
    await ctx.message.add_reaction(okhandEmoji)
    #Log to console
    commandTimeExecuted = datetime.datetime.now()
    print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted}')
    #Sends message to channel
    await ctx.channel.send('```yaml\n' + 'Hello, I\'m Typing Bot! My creator was bored because of COVID-19 and made me KEKW. My main function is determine your WPM(Words per minute).  All you have to do is type the command \'+start\' and type the 50 randomized words I give you as fast as you can. After you type the 50 words BOOM you have your WPM and some nice stats.' + '\n```')

@client.command()
async def clear(ctx, *args):
    #Indicates that command was accepted
    checkEmoji = '\U00002705'
    okhandEmoji = '\U0001F44C'
    await ctx.message.add_reaction(okhandEmoji)
    sleep(0.5)
    if not args:
        #Delete an amount of messages
        await ctx.channel.purge(limit=int(2))
        commandTimeExecuted = datetime.datetime.now()
        print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted}')
        print(f'{ctx.message.author} cleared 2 line(s)!')
    elif args[0]:
        #Delete an amount of messages
        await ctx.channel.purge(limit=(int(args[0]) + 1))
        commandTimeExecuted = datetime.datetime.now()
        print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted}')
        print(f'{ctx.message.author} cleared {int(args[0]) + 1} line(s)!')

@client.command()
async def start(ctx):
    #Indicates that command was accepted
    checkEmoji = '\U00002705'
    okhandEmoji = '\U0001F44C'
    await ctx.message.add_reaction(okhandEmoji)
    #Embed from bot
    testembed = discord.Embed(colour=discord.Colour.blue(), title=f'{ctx.message.author} Type The Text Below As Fast As You Can!')
    await ctx.channel.send(embed=testembed)
    #Get time of when command was executed
    commandTimeExecuted = datetime.datetime.now()
    print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted}')
    commandTimeSecs = ((commandTimeExecuted.minute * 60) + commandTimeExecuted.second) #Convert minutes and seconds to just all seconds
    #Pick random words from wordCount and concatenate in typeThis(String)
    typeThis = ""
    for x in range(0, 50):
        num = random.randint(0, wordCount)
        typeThis += str(listWords[num]) + str(' ')
    #Sends typeThis(string) in a codeblock
    await ctx.channel.send('```yaml\n' + typeThis + '\n```')
    #Function this checks if the message the bot detects is from the same person that executed the command
    #https://stackoverflow.com/questions/54723139/discord-py-rewrite-how-to-wait-for-author-message
    def check(author):
        def inner_check(message):
            return message.author == author
        return inner_check
    #Waits for 'author' to send back message
    userString = await client.wait_for('message', check=check(ctx.author))
    #Gets time of when message was received to compare with time of when command was executed
    userTimeResponse = datetime.datetime.now()
    print(f'{ctx.author} responded to {ctx.message.content} at {userTimeResponse}')
    userTimeSecs = ((userTimeResponse.minute * 60) + userTimeResponse.second) #Convert minutes and seconds to just all seconds
    #Converts message recieved to string
    userAttempt = str(userString.content)
    #Put strings into list for easier comparing
    typeList = typeThis.split()
    compareList = userAttempt.split()
    #Variables used for comparing
    finalString = ""
    userCorrect = 0
    #Algorithm [Multihexed(Twitch) helped alot of this one] https://pastebin.com/dEDYRNBd
    for x, y in zip(typeList, compareList):
        if x == y:
            finalString += y
            userCorrect += 1
    #Calculates Words Per Minute
    finalStringCount = len(finalString)
    timeCompleted = ((userTimeSecs - commandTimeSecs)/60)
    minutes = math.floor(timeCompleted)
    seconds = int((timeCompleted - minutes) * 60)
    wpm = ((finalStringCount/5)/timeCompleted)
    wpm = round(wpm, 2)
    if wpm >= 220 and timeCompleted <= 10:
        #cheater detected
        #Output CHEATER in an embed
        currentDir = os.getcwd()
        testembed = discord.Embed(colour=discord.Colour.dark_red(), title=f'{ctx.author} is a cheater!', description=f'**{ctx.author}, you\'re lowkey a loser :(**')
        file = [discord.File(fp=f"{currentDir}\\Assets\\forsenCD.png", filename="forsenCD.png"),discord.File(fp=f"{currentDir}\\Assets\\weirdChamp.png", filename="weirdChamp.png"),discord.File(fp=f"{currentDir}\\Assets\\PointAtCheater.png", filename="PointAtCheater.png")]
        testembed.set_thumbnail(url=f"attachment://forsenCD.png")
        testembed.set_author(name='Weird Champ', icon_url=f"attachment://weirdChamp.png")
        testembed.set_image(url=f"attachment://PointAtCheater.png")
        testembed.add_field(name=f'**FAKE WPM DETECTED! {wpm}**', value=f'**NO XP FOR YOU!**', inline=False)
        await ctx.channel.send(embed=testembed, files=file)
    else:
        if wpm >= 0 and wpm <= 10:
            picName = "Pepega.png"
        elif wpm >= 11 and wpm <= 20:
            picName = "peepoSad.png"
        elif wpm >= 21 and wpm <= 30:
            picName = "PepeHands.png"
        elif wpm >= 31 and wpm <= 40:
            picName = "pepeLaugh.png"
        elif wpm >= 41 and wpm <= 50:
            picName = "KEKW.png"
        elif wpm >= 51 and wpm <= 60:
            picName = "POGGERS.png"
        elif wpm >= 61 and wpm <= 70:
            picName = "gachiGASM.png"
        elif wpm >= 71 and wpm <= 80:
            picName = "HACKERMANS.gif"
        elif wpm >= 81:
            picName = "EZ.png"
        #Output stats in an embed
        currentDir = os.getcwd()
        testembed = discord.Embed(colour=discord.Colour.gold(), title=f'{ctx.author} got {wpm} WPM!')
        file = [discord.File(fp=f"{currentDir}\\Assets\\{picName}", filename=f"{picName}"), discord.File(fp=f"{currentDir}\\Assets\\PepoG.png", filename="PepoG.png"),]
        testembed.set_thumbnail(url=f"attachment://{picName}")
        testembed.set_author(name='Statistics', icon_url="attachment://PepoG.png")
        testembed.add_field(name='**Words Typed**', value=f'{len(compareList)}')
        testembed.add_field(name='**Incorrect**', value=f'{len(compareList) - userCorrect}')
        testembed.add_field(name='**Time**', value=f'{minutes} mins {seconds} secs')
        await ctx.channel.send(embed=testembed, files=file)

client.run(f'{token}')
