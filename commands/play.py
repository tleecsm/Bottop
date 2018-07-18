# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:58:05 2018

@author: Tanner Lee
https://github.com/tleecsm

play.py
Script that contains the logic to handle the "play" command
"""

import os.path
import asyncio

async def play(client, message, voicePlayerList):
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
        #Create a filepath with the users input
        playFilePath = 'audio/'
        messageContentList = message.content.split(' ')
        if not len(messageContentList) > 1:
            # This is not a valid command, notify the user
            playError = 'I\'m not sure what you want me to do.  '
            playError += 'Please use the format:\n```\n'
            playError += 'play {songtitle}\n```'
            await client.send_message(message.channel, playError)
            return
        playFilePath += messageContentList[1]   # Index 1 contains the song
        playFilePath += '.mp3'
        #Check if the file exists
        if os.path.isfile(playFilePath):
            #Create a list to be appended to the queue
            #List will contain ['local', local_mp3_id]
            #Will be used by songFinished to identify the type of player needed
            playerListAppend = []
            playerListAppend.append('local')
            playerListAppend.append(playFilePath)
            voicePlayerList.append(playerListAppend)
            if len(voicePlayerList) == 1:
                #There is nothing currently playing
                #Start a new player
                mp3Player = voice.create_ffmpeg_player(playFilePath,
                        options='-loglevel panic -hide_banner',								              after=lambda: songFinished(client, voice, voicePlayerList))
                #Before starting it, replace the 0 index of the queue
                #With the player so it can be stopped if needed
                voicePlayerList[0] = mp3Player
                mp3Player.start()

        else: 
            #No file was found, notify the user
            playError = 'I can\'t find a song with the name \''
            playError += messageContentList[1]
            playError += '\'!'
            await client.send_message(message.channel, playError)
            return
    else:
        playError = 'I have to be connected to a voice channel to do that!\n'
        playError += 'Use the \'connect\' command to summon me!'
        await client.send_message(message.channel, playError)
        return


def songFinished(client, voice, voicePlayerList):
    """
    songFinished
    A local song has just finished
    Pop the queue and start the next song
    """
    if len(voicePlayerList) > 0:
        #Pop the current player and begin the next
        voicePlayerList.pop(0)
        nextSong = voicePlayerList[0]
        #Check if it is a local song or youtube
        if nextSong[0] == 'local':
            #Start an ffmpeg player
            playFilePath = voicePlayerList[0]
            coroutine = voice.create_ffmpeg_player(nextSong[1],
                    options='-loglevel panic -hide_banner',
                    after=lambda: songFinished(client, voice, voicePlayerList))
            #Replace the 0 index with the current player so it can be stopped
            voicePlayerList[0] = coroutine
            coroutine.start()
        else:
            #Start a youtube player
            coroutine = voice.create_ytdl_player(nextSong[1],
                    ytdl_options='-i --no-playlist',
                    after=lambda: songFinished(client, voice, voicePlayerList))
            future = asyncio.run_coroutine_threadsafe(coroutine, client.loop)
            try:
                #Replace the 0 index with the current player so it can be stopped
                voicePlayerList[0] = future.result()
                future.result().start()
            except:
                print('Error starting next song')
    else:
        return
        
