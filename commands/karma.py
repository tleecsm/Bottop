# -*- coding: utf-8 -*-
"""
Created on Wed May 23 08:46:25 2018

@author: Tanner Lee
https://github.com/tleecsm

karma.py
Script that contains the logic to handle the "karma" command
"""

import configparser

async def karma(client, message):
    """
    karma
    Reports a measure of how often a user has recieved good and bad karma
    Karma is measured via Discord's reaction system
    Each server will have a "good react" and a "bad react"
    Reads a reference file of configuration settings and karma history
    """
    #Strip off the command tag with the command character
    messageContent = message.content[7:]
    #Convert the name to a member
    userSpecified = message.server.get_member_named(messageContent)
    if userSpecified == None:
        #User was not found
        userError = 'User with the name '
        userError += messageContent
        userError += ' was not found!'
        await client.send_message(message.channel, userError)
        return
    #Else the user was found and we can pull their ID
    userId = userSpecified.id
    parser = configparser.RawConfigParser()
    #Try to pull the users data
    parser.read('commands/karmaData')
    try:    
        karmaValue = parser.get('userDataKarma', userId)
        karmaMessage = messageContent
        karmaMessage += '\'s karma:\n'
        karmaMessage += '```\n'
        karmaMessage += karmaValue
        karmaMessage += '\n```'
    except configparser.NoOptionError:
        #The karma data for this user doesnt exist
        karmaMessage = messageContent
        karmaMessage += ' doesn\'t have any karma yet!'

    await client.send_message(message.channel, karmaMessage)

async def karmaself(client, message):
    """
    karma
    A version of karma that has no parameter
    By default this will search for the user who sent the message
    """
    #Get the ID of the user who sent the message
    user = message.author
    #Else the user was found and we can pull their ID
    userId = user.id
    parser = configparser.RawConfigParser()
    #Try to pull the users data
    parser.read('commands/karmaData')
    try:    
        karmaValue = parser.get('userDataKarma', userId)
        karmaMessage = user.name
        karmaMessage += '\'s karma:\n'
        karmaMessage += '```\n'
        karmaMessage += karmaValue
        karmaMessage += '\n```'
    except configparser.NoOptionError:
        #The karma data for this user doesnt exist
        karmaMessage = user.name
        karmaMessage += ' doesn\'t have any karma yet!'

    await client.send_message(message.channel, karmaMessage)