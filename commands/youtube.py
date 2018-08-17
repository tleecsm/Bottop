# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 12:07:55 2018

@author: Tanner Lee
https://github.com/tleecsm

youtube.py
Script that contains the logic to handle the "youtube" command
"""

import asyncio

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
        playerListAppend = []
        playerListAppend.append('youtube')
        playerListAppend.append(playFileUrl)
        voicePlayerList.append(playerListAppend)
        if len(voicePlayerList) == 1:
            youtubePlayer = await voice.create_ytdl_player(playFileUrl,
                     ytdl_options='-i --no-playlist',
                     after=lambda: songFinished(client, message, voice, voicePlayerList))
            voicePlayerList[0] = youtubePlayer
            #Print name of the current song before starting it
            nowPlaying = 'Now Playing:```prolog\n'
            nowPlaying += youtubePlayer.title
            nowPlaying += ' ('
            nowPlaying += str(youtubePlayer.duration)
            nowPlaying += ' seconds)\n```'
            await client.send_message(message.channel, nowPlaying)
            youtubePlayer.start()
        else:
            #This has been pushed to the queue
            #Send a confirmation message
            confirmation = 'I\'ve added '
            confirmation += playFileUrl
            confirmation += ' to the queue!'
            await client.send_message(message.channel, confirmation)
    
    else:
        playError = 'I have to be connected to a voice channel to do that!\n'
        playError += 'Use the \'connect\' command to summon me!'
        await client.send_message(message.channel, playError)
        return

def songFinished(client, message, voice, voicePlayerList):
    """
    songFinished
    A youtube song has just finished
    Pop the queue and start the next song
    """
    if len(voicePlayerList) > 0:
        #Pop the current player and begin the next
        voicePlayerList.pop(0)
        nextSong = voicePlayerList[0]
        #Check if it is a local song or youtube
        if nextSong[0] == 'local':
            #Before starting the player
            #Send a currently playing message to chat
            playFilePath = nextSong[1]
            nowPlaying = 'Now Playing:```prolog\n'
            nowPlaying += playFilePath
            nowPlaying += '\n```'
            mroutine = client.send_message(message.channel, nowPlaying)
            mfuture = asyncio.run_coroutine_threadsafe(mroutine, client.loop)
            try:
                mfuture.result()
            except:
                print('Error printing Currently Playing message.')

            #Start the FFMPEG player
            coroutine = voice.create_ffmpeg_player(nextSong[1],
                    options='-loglevel panic -hide_banner',
                    after=lambda: songFinished(client, message, voice, voicePlayerList))
            #Replace the 0 index with the current player so it can be stopped
            voicePlayerList[0] = coroutine
            coroutine.start()
        else:
            #Start a youtube player
            coroutine = voice.create_ytdl_player(nextSong[1],
                    ytdl_options='-i --no-playlist',
                    after=lambda: songFinished(client, message, voice, voicePlayerList))
            future = asyncio.run_coroutine_threadsafe(coroutine, client.loop)
            try:
                #Replace the 0 index with the current player so it can be stopped
                voicePlayerList[0] = future.result()
                future.result().start()
            except:
                print('Error starting next song')

            #Print name of the current song to chat
            nowPlaying = 'Now Playing:```prolog\n'
            nowPlaying += future.result().title
            nowPlaying += ' ('
            nowPlaying += str(future.result().duration)
            nowPlaying += ' seconds)\n```'
            mroutine = client.send_message(message.channel, nowPlaying)
            mfuture = asyncio.run_coroutine_threadsafe(mroutine, client.loop)
            try:
                mfuture.result()
            except:
                print('Error displaying Currently Playing message')

    else:
        return
