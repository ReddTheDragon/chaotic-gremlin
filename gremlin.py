#Copyright 2022 Thomas D. Streiff
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
import os
#import discord.py, aiohttp (async http, basically), and asyncio (async functionality)
import discord,aiohttp,asyncio
from discord.ext import commands
try:
    import colorama
    from colorama import Fore,Back,Style
    RED = Fore.RED + Style.BRIGHT
    GREEN = Fore.GREEN + Style.BRIGHT
    RESET = Style.RESET_ALL
    YELLOW = Fore.YELLOW + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    colorama.init()
except:
    RED = ""
    GREEN = ""
    RESET = ""
    YELLOW = ""
    WHITE = ""
###VARIABLE DECLARATIONS###
#is this a development version?
IS_DEVELOPMENT_VERSION = 0
#declare the version
VERS = "0.1 beta"

#function to load tokens
def get_token(isdev=0):
    #NOT DEVELOPMENT
    if isdev==0:
        myFile = open(os.path.join(".","tokens","default.txt"),"r")
        for line in myFile:
            myTokenToReturn = line
        #return the token we got from the file
        return myTokenToReturn
    #IS DEVELOPMENT
    elif isdev==1:
        myFile = open(os.path.join('.','tokens','dev.txt'))
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'{RED} Logged on as {self.user}{RESET}!')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

get_token()
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
#client.run(token)
