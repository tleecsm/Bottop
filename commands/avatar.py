# -*- coding: utf-8 -*-
"""
Created on Sun May 20 15:45:10 2018

@author: Tanner Lee
https://github.com/tleecsm
avatar.py
Script that contains the logic to handle the "bee" command
"""

async def avatar(client, message):
    """
    avatar
    Updates the bot's avatar
    Uses the image named avatar.png in the main BtR Directory
    """
    avatar = open('avatar.png', 'rb')
    reply = 'Updating my avatar to this!'
    await client.send_file(message.channel, 'avatar.png', content=reply)
    await client.edit_profile(avatar=avatar.read())
    avatar.close()

