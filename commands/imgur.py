# -*- coding: utf-8 -*-
"""
Created on Tue May 29 08:36:06 2018

@author: Tanner Lee
https://github.com/tleecsm

imgur.py
Script that contains the logic to handle the "imgur" command

TODO:
    Download images and upload them directly to discord
"""

from imgurpython import ImgurClient
import random

#Create the logic for imgur.py in a class
#This ensures initialization only happens once
class imgurCommand:
    """
    imgurCommand
    Class that contains the initialization and runtime logic for imgur command
    """
    def __init__(self):
        """
        __init__
        Creates the class variables needed for the client
        Additionally stores the client for access in a class variable
        """
        self.clientId = 'ebae683a1f7ca07'
        self.clientSecret = 'c49e4fcb78b0cbe92481c1778a38cb884f9af584'
        self.imgurClient = ImgurClient(self.clientId, self.clientSecret)
    
    async def imgur(self, discordClient, message):
        """
        imgur
        Main execution logic for the imgur command
        Leverages the imgurClient to fetch image requests from the user
        Image request terms fetched from message content
        """
        #Start by stripping the imgur command off the message
        #messageContent will contain the search request from the user
        messageContent = message.content[7:]
        gallery = self.imgurClient.gallery_search(messageContent,
                                                  sort='best',page=0)
        if len(gallery) < 1:
            #There are no images in the gallery 
            #Return an error message
            imgurError = 'I couldn\'t find anything with that tag!'
            await discordClient.send_message(message.channel, imgurError)
            return
        image = random.choice(gallery)
        await discordClient.send_message(message.channel, image.link)
        
    async def imgurRandom(self, discordClient, message):
        """
        imgurRandom
        Fetches a random imgur post
        Returns it in a message to the user's channel
        """
        #Fetch a random gallery and pull a random image from the gallery
        gallery = self.imgurClient.gallery_random()
        await discordClient.send_message(message.channel, gallery[0].link)
        
    