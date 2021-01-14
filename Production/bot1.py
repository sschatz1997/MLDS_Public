#!/usr/bin/python3

"""
File:  [ bot1.py ]
Author: Samuel Schatz
Date: 1/14/2021
Description: The main bot for this project.
"""
# bot1.py
import csv
import sys
import json
import config
import asyncio
import discord
import pprint
import logging
from datetime import date
from time import sleep as s
from datetime import datetime
from collections import Counter
from discord.ext import commands

# User made functions
from functions1 import toJson, counter1, writeSuggestions, getCount
from functions1 import countTEST, copyimg, copy, tolog, getOptedOut
from functions1 import addOptOut, regServer

token = str(config.token)

# intents are a new feature
intents = discord.Intents().all()#members = True, presences = True)

bot = commands.Bot(command_prefix='!!', intents = intents)


def datetimeNow():
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

"""
This gets the info about the bot.
"""
@bot.command()
async def getInfo(ctx):
    text = '```View captured data at http://dadywarbucks.xyz/logs.json \n'
    text += 'View more info at http://dadywarbucks.xyz/botInfo.php \n'
    text += 'View code at https://github.com/sschatz1997/MLDS_Public \n'
    text += 'join the support server here https://discord.gg/cpcGmu5 !\n'
    text += 'join the Subreddit here https://www.reddit.com/r/MLDS_bot/ !\n'
    text += 'View Commands by typing !!commands1\n```'
    await ctx.send(text)

"""
This tells a user the commands.
"""
@bot.command()
async def commands1(ctx):
    text = "```Commands: \n"
    text += "!!commands1 == show the commands. \n"
    text += "!!getInfo == show info about this bot. \n"
    text += "!!suggestions {what you want to say} == suggests a feature for the bot. \n"
    text += "!!count == get the number of entries. \n"
    text += "!!optOut == opt out of your status being logged {work in progress}.\n"
    text += "!!reg == registers the server with the backend. \n"
    text += "!!getInvite == gets the invite for your server!\n```"
    await ctx.send(text)

"""
This adds a users sugestions to a file.
"""
@bot.command()
async def suggestions(ctx, arg):
    formated = str(arg + "\n")
    writeSuggestions(formated)
    await ctx.send("Added, thanks!")

"""
This returns the number of entries.
"""
@bot.command()
async def count(ctx):
    print('count')
    num = getCount()
    await ctx.send("{} || Entries: {}.".format(str(ctx.message.author.mention), str(num)))

"""
This adds a user to the opt out list so their data isn't collected.
"""
@bot.command()
async def optOut(ctx):
    username = str(ctx.message.author)
    addOptOut(username)
    await ctx.send("{} youve opted out!".format(str(ctx.message.author.mention)))

"""
This registers the server with the bot.
"""
@bot.command()
async def reg(ctx):
    serverName = ctx.guild.name
    status = regServer(serverName)
    if status == True:
        await ctx.send("Registered!")
    else:
        await ctx.send("This server is already registered!")

"""
This sends the invite to the bots discord server.
"""
@bot.command()
async def getInvite(ctx):
    invite = "https://discord.com/api/oauth2/authorize?client_id=720440825103777863&permissions=0&scope=bot"
    await ctx.send("click here to add the bot to your server {}".format(invite))

"""
This shuts down the bot, only the owner of the bot can do this.
"""
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("{} is shuting down the bot in 30 seconds!!".format(str(ctx.message.author.mention)))
    s(30)
    await bot.close()

"""
This adds the presence to the bot when it starts.
"""
@bot.event
async def on_ready():
    print("RUNNING YE HAW!!")
    #copy()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!!commands1 to see commands"))

"""
tells the user that the command isnt found
"""
@bot.event
async def on_command_error(ctx, error):
    await ctx.send("{} command not found!".format(str(ctx.message.author.mention)))

"""
This logs the change.
"""
@bot.event
async def on_member_update(before, after):
    username = str(before.name)
    optedOut = getOptedOut()
    #print('entered')
    t = datetime.today().strftime('%M')
    #print('min {}\n'.format(t))
    if int(t)%5 == 0: # only collecting every 5 mins
        #print('5\n')
        if username not in optedOut:
            if str(before.status) == "online":
                if str(after.status) == "offline":
                    temp = [str(after.status), datetimeNow()]
                    tolog(temp)
            if str(before.status) == "offline":
                if str(after.status) == "online":
                    temp = [str(after.status), datetimeNow()]
                    tolog(temp)
    del t

    
bot.run(token)
