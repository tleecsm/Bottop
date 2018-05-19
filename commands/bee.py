# -*- coding: utf-8 -*-
"""
Created on Sat May 19 14:48:43 2018

@author: Tanner Lee
https://github.com/tleecsm

bee.py
Script that contains the logic to handle the "bee" command
"""

async def bee(client, message):
    """
    bee
    Takes the users message and converts all vowels to the word "bee"
    Replies with the message and uses TTS to broadcast it
    """
    #Create a copy of the message that we can modify
    messageContent = message.content
    
    #Strip off the "bee" tag
    messageContent = messageContent[4:]
    
    #Create a blank string to fill with the reply
    reply = ''
    
    #Create two booleans to identify if 'y' should be considered a vowel
    lastLetterWasVowel = False
    lastLetterWasY = False
    #Initialize dummy variable that will be used to contain the Y's case
    lastLetterCase = 'Y'
    
    for letter in messageContent:

        if letter.lower() in ('a', 'e', 'i', 'o', 'u'):
            #If the current letter is a vowel
            #Change it to bee
            letter = 'bee'
            #Check to see if previous letter was a Y
            if lastLetterWasY:
                #The last y was not a vowel
                #Add Y + bee to the reply
                reply = reply + lastLetterCase + letter
            else:
                #Add the 'bee' to the reply
                reply = reply + letter
            lastLetterWasY = False
        elif letter.lower() == 'y':
            #If the current letter is a Y
            #Check previous letter 
            if lastLetterWasVowel or lastLetterWasY:
                #Then Y is not a vowel
                #Add the Y to the reply
                reply = reply + letter
            else:
                #Y may be a vowel
                #Do not add it to the reply yet
                lastLetterWasY = True
                lastLetterCase = letter
        else:
            #Current letter is not a vowel 
            #Check to see if previous letter was a Y
            if lastLetterWasY:
                #Then Y is a vowel
                #Add 'bee' + letter to the reply
                reply = reply + 'bee' + letter
            else: 
                #Add the letter to the reply
                reply = reply + letter
            lastLetterWasY = False

    #Ensure the last letter was not a Y
    if lastLetterWasY:
        #Add a final y to the reply
        reply = reply + lastLetterCase
        
                
                
    
    #Reply with a TTS message
    await client.send_message(message.channel, reply, tts=True)
            