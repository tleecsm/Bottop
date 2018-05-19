# -*- coding: utf-8 -*-
"""
Created on Sat May 19 14:23:51 2018

@author: Tanner Lee
https://github.com/tleecsm

hello.py
Script that contains the logic to handle the "hello.py" command
Command mostly used for proof of concept and bot testing
"""

async def hello(client, message):
    """
    hello
    Greets the user
    Mentions their discord username and says hello
    """
    reply = 'Hello, {0.author.mention}!'.format(message)
    await client.send_message(message.channel, reply)