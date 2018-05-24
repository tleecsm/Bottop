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
    parser.read('commands/karmaData', encoding='utf-8')
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
    karmaself
    A version of karma that has no parameter
    By default this will search for the user who sent the message
    """
    #Get the ID of the user who sent the message
    user = message.author
    userId = user.id
    parser = configparser.RawConfigParser()
    #Try to pull the users data
    parser.read('commands/karmaData', encoding='utf-8')
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
    
async def karmaUpdate(client, message, indicator):
    """
    karmaUpdate
    Not a command function
    Used whenever a user has a message reacted to with a karma emoji
    Increases or decreases karma by one for each react
    """
    #Find the user id of the message author
    user = message.author
    userId = user.id
    parser = configparser.RawConfigParser()
    parser.read('commands/karmaData', encoding='utf-8')
    #Decide whether karma should be increased or decreased
    #Try to fetch the user's current karma
    try:    
        karmaValue = parser.get('userDataKarma', userId)
        #convert to int
        karmaValue = int(karmaValue)
    except configparser.NoOptionError:
        #If they have no karma data, default the value to 0
        karmaValue = 0

    #Parse whether the karma should be increased or decreased
    if indicator == '+1':
        #Increase their karma
        karmaValue += 1        
    elif indicator == '-1':
        #Decrease their karma
        karmaValue -= 1
    else:
        #Something terrible happened
        print('ERROR: Could not update karmaData file!')
        return
    
    #Update the data
    parser.set('userDataKarma', str(userId), str(karmaValue))
    with open('commands/karmaData', 'w', encoding='utf-8') as data:
        parser.write(data)
    consoleMessage = 'Writing to karmaData file :: COMPLETED'
    print(consoleMessage)
    
    
    
class initializeKarma:
    
    def initialize(self):
        """
        initialize
        Function responsible for initializing the karma emojis
        Stores parameters from the karma file to class variables
        """
        #Create a ConfigParser to do the dirty work
        self.parser = configparser.RawConfigParser()
        self.parser.read('commands/karmaData', encoding='utf-8')
        self.goodKarma = self.parser.get('configKarma', 'goodKarmaReact')
        self.badKarma = self.parser.get('configKarma', 'badKarmaReact')

        