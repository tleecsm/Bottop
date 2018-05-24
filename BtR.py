# -*- coding: utf-8 -*-
"""
Created on Fri May 18 17:18:51 2018

@author: Tanner Lee
https://github.com/tleecsm

BtR.py
Entry point for the program
Creates the discord client
Handles the recieving discord event signals
"""

import discord
from initializeBtR import initializeData
from commands.handleCommand import handleCommand
from commands.karma import initializeKarma, karmaUpdate

#Display launching message and initialize version number
print('!Launching BtR!')
versionBtR = '0.2'

#Create an instance of initialization data 
#Then call initialize() to generate data based on the preferences file
initData = initializeData()
initData.initialize()

#Initialize Karma emojis
initKarma = initializeKarma()
initKarma.initialize()

#Create an instance of command data
#Then call initialize() to generatedata based on the current commands 

#Extract the data given by the initialization
botToken = initData.botToken
commandCharacter = initData.commandCharacter
enabledCommands = initData.enabledCommands

#Create the client that will serve as the program's core
client = discord.Client()

@client.event
async def on_message(message):
    """
    on_message
    asynchronous function
    Acts as a listener for the "on_message" event
    The function executes when a message is sent to a channel the bot can see
    """
    #Before doing anything
    #Check to see if the message started with the command character
    if not message.content.startswith(commandCharacter):
        #If it didn't, return
        return
    
    #Ensure the bot wasn't the one who sent the message
    if message.author == client.user:
        #If it was, return
        return
    
    #Kill is checked by default (cannot be disabled)
    if message.content.startswith(commandCharacter+'kill'):
        await client.send_message(message.channel, 'Goodbye Forever...')
        exit(0)
    
    #Parse through the list of all enabled commands
    for command in enabledCommands:
        #We want to ignore case when comparing the message content
        messageContent = message.content.lower()
        #If the message matches one of our commands, we will handle it
        #Requires whitespace after command name
        if messageContent.startswith(commandCharacter+command):
            await handleCommand(client, message)


@client.event
async def on_ready():
    """
    on_ready
    asynchronous function
    Acts as a listener for the "on_ready" event
    The function executes when a message is sent to a channel the bot can see
    """
    print('Launching Complete')
    print('BtR Version: ' + versionBtR)
    print('Discord Username: ' + client.user.name)
    print('Application ID: ' + client.user.id)
    print('------')

@client.event
async def on_reaction_add(reaction, user):
    """
    on_reaction_remove
    asynchronous function
    Acts as a listener for the "on_reaction_remove" event
    The function executes when a reaction is removed
    This only triggers for messages that the bot has in its message cache
    """
    #Before doing anything
    #Check to see if the reaction was a karma emoji
    if reaction.emoji == initKarma.goodKarma:
        consoleMessage = 'Writing to karmaData file :: Increasing '
        consoleMessage += reaction.message.author.name
        consoleMessage += '\'s karma by 1!'
        print(consoleMessage)
        await karmaUpdate(client, reaction.message, '+1')
    if reaction.emoji == initKarma.badKarma:
        consoleMessage = 'Writing to karmaData file :: Decreasing '
        consoleMessage += reaction.message.author.name
        consoleMessage += '\'s karma by 1!'
        print(consoleMessage)
        await karmaUpdate(client, reaction.message, '-1')

@client.event
async def on_reaction_remove(reaction, user):
    """
    on_reaction_remove
    asynchronous function
    Acts as a listener for the "on_reaction_remove" event
    The function executes when a reaction is removed
    This only triggers for messages that the bot has in its message cache
    """
    #Before doing anything
    #Check to see if the reaction was a karma emoji
    if reaction.emoji == initKarma.goodKarma:
        consoleMessage = 'Writing to karmaData file :: Decreasing '
        consoleMessage += reaction.message.author.name
        consoleMessage += '\'s karma by 1!'
        print(consoleMessage)
        await karmaUpdate(client, reaction.message, '-1')
    if reaction.emoji == initKarma.badKarma:
        consoleMessage = 'Writing to karmaData file :: Increasing '
        consoleMessage += reaction.message.author.name
        consoleMessage += '\'s karma by 1!'
        print(consoleMessage)
        await karmaUpdate(client, reaction.message, '+1')



#client.run must be the last line of the main script
client.run(botToken)