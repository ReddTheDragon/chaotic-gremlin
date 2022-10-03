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

#HERE WE HAVE OUR DEFAULT MODULES
defaultmods = ['modules.image']
import os
#import discord.py, aiohttp (async http, basically), sys module for exit, traceback for better error handling, asyncio for discord.py, atexit to do shit upon exit (I don't think breadbot does shit upon exiting), and asyncio (async functionality)
import discord,aiohttp,asyncio,logging, sys, traceback, atexit
from discord.ext import commands
class Bot(commands.Bot):
    #handle close
    async def async_clean(self):
        print(f"{RED}Logging off!{RESET}")
        logging.info("Bot Logoff Event")

    async def close(self):
        await self.async_clean()
        await super().close()
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
IS_DEVELOPMENT_VERSION = 1
#declare the version
VERS = "0.1 beta"
###END VARIABLE DECLARATIONS###

#setup logging
#setup exception logging
FORMAT = 'T: %(asctime)s | FILE: %(filename)s | FUNC: %(funcName)s | LINE: %(lineno)d | %(name)s, %(levelname)s: %(message)s'
logging.basicConfig(filename='chaoticgremlin.log',filemode="w", level=logging.INFO,format=FORMAT)
#setup function to handle exceptions (50/50, sometimes it works sometimes it doesn't)
def HandleException(exctype, value, tb):
    tbf1 = traceback.format_tb(tb)
    tbf2 = ""
    for line in tbf1:
        tbf2 = tbf2 + line
    logging.critical(f"AN EXCEPTION HAS OCCURRED!\nException Type: {exctype}\nValue: {value}\nTraceback: \n{tbf2}")
    traceback.print_tb(tb)
#set the python exception handler to use function 'HandleException'
sys.excepthook = HandleException


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
        for line in myFile:
            myTokenToReturn = line
        #return the token we got from the file
        return myTokenToReturn

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/",intents=intents)

@bot.event
async def on_ready():
    print(f'{RED}Logged on as {bot.user}{RESET}!')

@bot.hybrid_command(name='test')
async def test(ctx):
    print("A")
    await ctx.send("Test")
token = get_token(IS_DEVELOPMENT_VERSION)
print(token)
logging.info("Bot Login Event")
try:
    bot.run(token)
except Exception as e:
    HandleException(sys.exc_info[0],sys.exc_info[1],sys.exc_info[2])