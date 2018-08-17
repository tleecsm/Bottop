# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 15:58:05 2018

@author: Tanner Lee
https://github.com/tleecsm

queue.py
Script that contains logic to print the current voice players queue to the chat log
"""

import os

async def queue(client, message, voicePlayerList):
    """
    queue
    Simply prints the current queue to the chat
    """
    #Check current voicePlayerList to ensure something is in it
    if len(voicePlayerList) < 1:
        #Theres nothing currently in the queue
        emptyQueue = 'I don\'t current have anything in the queue!'
        emptyQueue += '\nUse either the play command or the youtube '
        emptyQueue += 'command to put something in the queue!'
        await client.send_message(message.channel, emptyQueue)
    else:
        #There's something in the queue
        #First entry will be currently playing
        queue = 'Currently playing: '
        queue += '\n\n'
        queue += 'Current queue:\n'
        for entry in voicePlayerList:
            queue += entry[1]
            queue += '\n'
        await client.send_message(message.channel, queue)
