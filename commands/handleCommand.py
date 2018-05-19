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

async def handleCommand(client, message):
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
    
    #Pass the command to the correct handling function
    if commandName.startswith('hello'):
        await hello(client, message)
    elif commandName.startswith('howdy'):
        await hello(client, message)
    elif commandName.startswith('bee'):
        await bee(client, message)