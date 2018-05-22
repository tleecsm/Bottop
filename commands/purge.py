# -*- coding: utf-8 -*-
"""
Created on Mon May 21 16:27:44 2018

@author: Tanner Lee
https://github.com/tleecsm

purge.py
Script that contains the logic to handle the "purge" command

#TODO:
    Add override for number of messages that get deleted
    Add ability to purge "last X amount of messages"
    Recursive call maybe?
"""

async def purge(client, message):
    """
    purge
    Deletes a selection of messages
    Will delete all messages posted after a given message id
    >>purge #MESSAGE_ID#
    """
    maximumDelete = 250
    #Start by stripping off the command
    #messageContent will contain the message_id we need for delete
    messageContent = message.content[7:]
    #Get the message you want to delete after
    deleteAfter = await client.get_message(message.channel, messageContent)
    #Purge the messages and store the messages in a list
    deletedList = await client.purge_from(message.channel,
                            limit=maximumDelete,
                            after=deleteAfter)
    purgeMessage = 'Purge Successful!'
    purgeMessage += ' Deleted ' + str(len(deletedList)) + ' messages.'
    if len(deletedList) == maximumDelete:
        purgeMessage += ' This is the maximum number of messages I can delete'
        purgeMessage += ' at one time!'
    await client.send_message(message.channel, purgeMessage)
  
    
async def purgelast(client, message):
    """
    purge
    Deletes a selection of messages
    Will delete a specified number of messages from the last message
    >>purge #NUM_TO_DELETE#
    """
    #Start by stripping off the command
    #messageContent will contain the number of messages we need to delete
    messageContent = message.content[11:]

    try:
        #Try to convert the value passed to an int
        maximumDelete = int(messageContent)
        #Purge the messages and store the messages in a list
        deletedList = await client.purge_from(message.channel,
                            limit=maximumDelete,
                            before=message)
        purgeMessage = 'Purge Successful!'
        purgeMessage += ' Deleted ' + str(len(deletedList)) + ' messages.'
        await client.send_message(message.channel, purgeMessage)
    except ValueError:
        #If the value passed isnt an int display an error message
        errorMessage = 'Error deleting messages!'
        errorMessage += ' Please use the form:\n'
        errorMessage += '```\n purgelast #NUM_TO_DELETE\n```'
        await client.send_message(message.channel, errorMessage)
