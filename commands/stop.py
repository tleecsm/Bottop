# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:58:05 2018

@author: Tanner Lee
https://github.com/tleecsm

stop.py
Script that contains the logic to handle the "stop" and "skip" commands
They were included in the same file due to how similar their logic is.
These may be reworked in a future release.
"""

import os

async def stop(client, message, voicePlayerList):
    """
    stop
    Allows the user to stop the currently playing song
    """
    #First ensure there is something in the voicePlayerList
    if len(voicePlayerList) > 0:
        #Then attempt to stop the currently playing song
        #Current player should be stored in 0 index
        player = voicePlayerList[0]
        #Before stopping the player, clear the queue
        #There is possiblity of race conditions otherwise
        del voicePlayerList[:]
        player.stop()
        #Player has been stopped
        #Give control back to the terminal
        os.system('stty sane')

async def skip(client, message, voicePlayerList):
    """
    skip
    Allows the user to skip the current song
    Then the next player is automatically created
    """
    #Ensure there is something in the voicePlayerList
    if len(voicePlayerList) > 0:
        #Attempt to stop the currently playing song
        player = voicePlayerList[0]
        player.stop()
        #Player has been stopped
        #Next song will AUTOMATICALLY start
        #This is due to the player's after clause
