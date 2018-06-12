# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:58:05 2018

@author: Tanner Lee
https://github.com/tleecsm

play.py
Script that contains the logic to handle the "play" command
"""

async def play(client, message):
    #Check to ensure that a valid voice client was passed
    voiceConnectionExists = False
    voice = None
    for connection in client.voice_clients:
        if connection.server == message.server:
            voiceConnectionExists = True
            voice = connection
    if voiceConnectionExists:
        mp3Player = voice.create_ffmpeg_player('audio/cool.mp3',
                options='-loglevel panic -hide_banner')
        mp3Player.start()
    else:
        playError = 'I have to be connected to a voice channel to do that!\n'
        playError += 'Use the \'connect\' command to summon me!'
        await client.send_message(message.channel, playError)
