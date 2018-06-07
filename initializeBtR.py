# -*- coding: utf-8 -*-
"""
Created on Fri May 18 19:20:36 2018

@author: Tanner Lee
https://github.com/tleecsm

initializeBtR.py
Small script used to parse the preferences file
Stores preference data in a class called initializeData
"""

import configparser

class initializeData:
    """
    initializeData
    Class responsible for storing the data recieved from the config file
    Will be read by BtR.py
    """
    def initialize(self):
        """
        initialize
        Function responsible for initialize the bot
        Stores parameters from the preferences file to class variables
        """
        #Create a ConfigParser to do the dirty work
        self.parser = configparser.RawConfigParser()
        self.parser.read('preferences')
        self.botToken = self.parser.get('configBtR', 'botToken')
        self.commandCharacter = self.parser.get('configBtR', 
                                                'commandCharacter')
        #enabledCommands parses in as a comma delimited string
        #split the string and place it in a list to make it more usable
        self.enabledCommands = self.parser.get('configBtR', 'enabledCommands')
        self.enabledCommands = self.enabledCommands.split(',')
