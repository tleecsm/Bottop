# -*- coding: utf-8 -*-
"""
Created on Fri May 18 17:18:51 2018

@author: Tanner Lee
https://github.com/tleecsm
"""

import discord

TOKEN = 'NDQ3MTc1Mzg5ODE5Njk5MjAy.DeDwLQ.wKoeyn83-c430dziGKGt3_ed6Ww'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)