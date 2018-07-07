# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 12:07:55 2018

@author: Tanner Lee
https://github.com/tleecsm

youtube.py
Script that contains the logic to handle the "youtube" command
"""

async def youtube(client, message, voicePlayerList):
    """
    play
    Allows a user to specify the name of a song in the audio folder
    The bot then creates an ffmpeg player for the file
    Then plays the song in a voice channel that it is connected to
    """
    #Check to ensure that a valid voice client was passed
    voiceConnectionExists = False
    voice = None
    for connection in client.voice_clients:
        if connection.server == message.server:
            voiceConnectionExists = True
            voice = connection
    # If there is a valid voice client, try to create an audio player
    if voiceConnectionExists:
        #Create a message content with the users input
        messageContentList = message.content.split(' ')
        if not len(messageContentList) > 1:
            # This is not a valid command, notify the user
            playError = 'I\'m not sure what you want me to do.  '
            playError += 'Please use the format:\n```\n'
            playError += 'youtube {url}\n```'
            await client.send_message(message.channel, playError)
            return
        playFileUrl = messageContentList[1]   # Index 1 contains the song
        youtubePlayer = await voice.create_ytdl_player(playFileUrl, 
                                                       ytdl_options='-i --no-playlist'
													   after= lambda: songFinished(voicePlayerList))
		if len(voicePlayerList) > 0:
			#Theres something in the queue
			voicePlayerList.append(youtubePlayer)
		else:
			youtubePlayer.start()
    else:
        playError = 'I have to be connected to a voice channel to do that!\n'
        playError += 'Use the \'connect\' command to summon me!'
        await client.send_message(message.channel, playError)
        return

async def songFinished(voicePlayerList):
	"""
	songFinished
	A youtube song has just finished
	Pop the queue and start the next song
	"""
	voicePlayerList.pop(0)
	voicePlayerList[0].start()