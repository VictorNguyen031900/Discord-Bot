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

class Typing(commands.Cog):

    def __init__(self, client):
        self.client = client
        global EnglishList
        global EnglishExpandedList
        EnglishList = []
        EnglishExpandedList = []
        print('Loading words from English.txt')
        currentDir = os.getcwd()
        file = open(f'{currentDir}\\cogs\\Words\\English.txt','r')
        for line in file:
            line = line.strip('\n')
            EnglishList.append(line)
        file.close()
        print('Words loaded successfully from English.txt')
        print('Loading words from English_Expanded.txt')
        file = open(f'{currentDir}\\cogs\\Words\\English_Expanded.txt', 'r')
        for line in file:
            line = line.strip('\n')
            EnglishExpandedList.append(line)
        file.close()
        print('Words loaded successfully from English_Expanded.txt')

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print('Bot is online.')
    @commands.command()
    async def test(self, ctx, *args):
        teststring = ''
        for i in range(0,len(args)):
            teststring += str(args[i]) + str(' ')

        await ctx.channel.send(teststring)
        print(type(args[0]))


    @commands.command(aliases=['type','typingtest', 'wpm'])
    async def start(self, ctx):
        checkEmoji = '\U00002705'
        okhandEmoji = '\U0001F44C'
        okEmoji = '\U0001F197'
        await ctx.message.add_reaction(okEmoji)
        #Embed from bot
        TypeThisEmbed = discord.Embed(colour=discord.Colour.blue(), title=f'{ctx.message.author} Type The Text Below As Fast As You Can!')
        await ctx.channel.send(embed=TypeThisEmbed)
        #Get time of when command was executed
        commandTimeExecuted = datetime.datetime.now()
        print(f'{ctx.author} executed command {ctx.message.content} at {commandTimeExecuted} on server \'{ctx.guild.name}\'({ctx.guild.id})')
        commandTimeSecs = ((commandTimeExecuted.minute * 60) + commandTimeExecuted.second) #Convert minutes and seconds to just all seconds
        #Pick random words from wordCount and concatenate in typeThis(String)
        typeThis = ""
        for x in range(0, 50):
            num = random.randint(1, len(EnglishList))
            typeThis += str(EnglishList[num-1]) + str(' ')
        #Formats typeThis(string) in bold
        await ctx.channel.send('**\n' + typeThis + '\n**')
        #Function that checks if the message the bot detects is from the same person that executed the command
        #https://stackoverflow.com/questions/54723139/discord-py-rewrite-how-to-wait-for-author-message
        def check(author):
            def inner_check(message):
                return message.author == author
            return inner_check
        #Waits for 'author' to send back message
        #Changed client to self.client
        userString = await self.client.wait_for('message', check=check(ctx.author))
        #Gets time of when message was received to compare with time of when command was executed
        userTimeResponse = datetime.datetime.now()
        print(f'{ctx.author} responded to {ctx.message.content} at {userTimeResponse} on server \'{ctx.guild.name}\'({ctx.guild.id})')
        userTimeSecs = ((userTimeResponse.minute * 60) + userTimeResponse.second) #Convert minutes and seconds to just all seconds
        #Converts message recieved to string
        userAttempt = str(userString.content)
        #Put strings into list for easier comparing
        typeList = typeThis.split()
        compareList = userAttempt.split()
        #Variables used for comparing
        finalString = ""
        userCorrect = 0
        #Algorithm
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
            #Cheater detected
            currentDir = os.getcwd()
            CheaterEmbed = discord.Embed(colour=discord.Colour.dark_red(), title=f'{ctx.author} is a cheater!', description=f'**{ctx.author}, you\'re lowkey a loser :(**')
            file = [discord.File(fp=f"{currentDir}\\Assets\\forsenCD.png", filename="forsenCD.png"),discord.File(fp=f"{currentDir}\\Assets\\weirdChamp.png", filename="weirdChamp.png"),discord.File(fp=f"{currentDir}\\Assets\\PointAtCheater.png", filename="PointAtCheater.png")]
            CheaterEmbed.set_thumbnail(url=f"attachment://forsenCD.png")
            CheaterEmbed.set_author(name='Weird Champ', icon_url=f"attachment://weirdChamp.png")
            CheaterEmbed.set_image(url=f"attachment://PointAtCheater.png")
            CheaterEmbed.add_field(name=f'**FAKE WPM DETECTED! {wpm}**', value=f'**NO XP FOR YOU!**', inline=False)
            await ctx.channel.send(embed=CheaterEmbed, files=file)
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
            ResultEmbed = discord.Embed(colour=discord.Colour.blue(), title=f'{ctx.author} got {wpm} WPM!')
            file = [discord.File(fp=f"{currentDir}\\Assets\\{picName}", filename=f"{picName}"), discord.File(fp=f"{currentDir}\\Assets\\PepoG.png", filename="PepoG.png"),]
            ResultEmbed.set_thumbnail(url=f"attachment://{picName}")
            ResultEmbed.set_author(name='Statistics', icon_url="attachment://PepoG.png")
            ResultEmbed.add_field(name='**Words Typed**', value=f'{len(compareList)}')
            ResultEmbed.add_field(name='**Incorrect**', value=f'{len(compareList) - userCorrect}')
            ResultEmbed.add_field(name='**Time**', value=f'{minutes} mins {seconds} secs')
            await ctx.channel.send(embed=ResultEmbed, files=file)

def setup(client):
    client.add_cog(Typing(client))
