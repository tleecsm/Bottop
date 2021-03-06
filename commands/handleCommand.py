# -*- coding: utf-8 -*-
"""
Created on Fri May 18 22:29:12 2018

@author: Tanner Lee
https://github.com/tleecsm

handleCommand.py
Small script used when a command signal has been recieved from the bot
Runs logic to determine which command was sent
Calls other command handling scripts
"""

from commands.hello import hello
from commands.bee import bee
from commands.avatar import avatar
from commands.purge import purge, purgelast
from commands.karma import karma, karmaself
from commands.imgur import imgurCommand
from commands.connect import connect
from commands.play import play
from commands.youtube import youtube
from commands.stop import stop, skip
from commands.queue import queue

async def handleCommand(client, message, voicePlayerList):
    """
    handleCommand
    Function called when a command is identified by the bot
    Determines which command was called
    Passes client and message to the appropriate function
    @param client The discord client the bot is linked to
    @param message The message containing the command
    """
    #Start by stripping the command character off
    commandName = message.content[1:]
    commandName = commandName.lower()
    
    imgurHandle = imgurCommand()

    #Pass the command to the correct handling function
    if commandName.startswith('hello'):
        await hello(client, message)
    elif commandName.startswith('howdy'):
        await hello(client, message)
    elif commandName.startswith('bee '):
        await bee(client, message)
    elif commandName.startswith('avatar'):
        await avatar(client, message)
    elif commandName.startswith('purge '):
        await purge(client, message)
    elif commandName.startswith('purgelast '):
        await purgelast(client, message)
    elif commandName.startswith('karma '):
        await karma(client, message)
    elif commandName == 'karma':
        await karmaself(client, message)
    elif commandName.startswith('imgur '):
        await imgurHandle.imgur(client, message)
    elif commandName == 'imgur':
        await imgurHandle.imgurRandom(client, message)
    elif commandName.startswith('connect'):
        await connect(client,message)
    elif commandName.startswith('stop'):
        await stop(client,message,voicePlayerList)
    elif commandName.startswith('skip'):
        await skip(client,message,voicePlayerList)
    elif commandName.startswith('play'):
        await play(client,message,voicePlayerList)
    elif commandName.startswith('youtube '):
        await youtube(client,message,voicePlayerList)
    elif commandName.startswith('queue'):
        await queue(client,message,voicePlayerList)
