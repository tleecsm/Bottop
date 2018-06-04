# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 15:37:14 2018

@author: Tanner Lee
https://github.com/tleecsm

connect.py
Script that contains the logic to handle the "connect" command
"""

async def connect(client, message):
    """
    connect
    Creates a voice client for the bot and connects it to a channel
    """
    channel = message.author.voice.voice_channel
    voice = await client.join_voice_channel(channel)
