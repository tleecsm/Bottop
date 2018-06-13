# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 15:37:14 2018

@author: Tanner Lee
https://github.com/tleecsm

connect.py
Script that contains the logic to handle the "connect" command
"""

import discord

async def connect(client, message):
    """
    connect
    Creates a voice client for the bot and connects it to a channel
    """
    #Ensure the user is in a voice channel
    channel = message.author.voice.voice_channel
    if channel is None:
        connectError = 'You\'re not in a voice channel!  '
        connectError += 'If you want to summon me please join a chat first!'
        await client.send_message(message.channel, connectError)
        return
    #Try to connect to the voice channel
    try:
        await client.join_voice_channel(channel)
    except discord.errors.ClientException:
        #The client is already in a voice channel
        #Move it
        voice = None
        for connection in client.voice_clients:
            if connection.server == message.server:
                voice = connection
        await voice.move_to(channel)