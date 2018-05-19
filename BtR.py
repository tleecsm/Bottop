# -*- coding: utf-8 -*-
"""
Created on Fri May 18 17:18:51 2018

@author: Tanner Lee
https://github.com/tleecsm
"""

import discord
from initializeBtR import initializeData

#Display launching message
print('!Launching BtR!')

#Create an instance of initialization data 
#Then call initialize() to generate data based on the preferences file
initData = initializeData()
initData.initialize()

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
    
    #Kill is checked by default
    if message.content.startswith(commandCharacter+'kill'):
        await client.send_message(message.channel, 'Goodbye Forever...')
        exit(0)
    
    for command in enabledCommands:
        if message.content.startswith(commandCharacter+command):
            reply = 'Hey there {0.author.mention}!'.format(message)
            await client.send_message(message.channel, reply)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#client.run must be the last line of the main script
client.run(botToken)