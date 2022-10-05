# #Copyright 2022 Thomas D. Streiff
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
import discord,math
from discord.ext import commands
import asyncio,random,traceback
import aiohttp,logging
from pymal.client import Client, BadRequestException
from io import BytesIO
import os

class Anime(commands.Cog):
    def __init__(self,bot):
        self.client = ""
        self.bot = bot
        self.token = ""
        token = ""
        print(os.getcwd())
        with open(os.path.join(".", "tokens","mal-client-id.txt")) as myd:
            token = myd.readlines()
            token = token[0].strip("\r").strip("\n")
            print(token)
        self.client = Client(token)
        print(self.client)

    @discord.app_commands.command(name="anime")
    async def AniGrab(self,ctx,id: str):
        await ctx.response.send_message("One moment...")
        mymsg = await ctx.original_response()
        em = discord.Embed(color=ctx.user.accent_color,title="Anime Query",description="**ID: " + str(id) + "**")
        myAnime = ""
        try:
            myAnime = self.client.get_anime(id,fields="alternative_titles,rating,media_type,start_season,status,synopsis,mean,num_list_users,num_scoring_users,genres,num_episodes,studios,genres")
        except BadRequestException:
            logging.error("Logged a bad request!")
            await mymsg.edit(contents="Sorry, your search returned as a bad request.")
        em.description = em.description + f"\n**Name:** {myAnime.title}\n**Media Type:** {myAnime.media_type}\n**Mean Rating:** {myAnime.mean}\n**Number of Episodes:** {myAnime.num_episodes}\n**Status:** {myAnime.status.readable_status.capitalize()}\n**Start Season:** {myAnime.start_season.season.capitalize()} {myAnime.start_season.year}"
        akaData = ""
        studiosData = ""
        if myAnime.alternative_titles.synonyms is not None:
            for i in myAnime.alternative_titles.synonyms:
                akaData = akaData + f"{i}\n"
            em.add_field(name=f"Also Known As",value=f"{akaData}")
        if myAnime.alternative_titles.en != None:
            em.add_field(name=f"English Name",value=f"{myAnime.alternative_titles.en}")
        if myAnime.alternative_titles.ja != None:
            em.add_field(name=f"Japanese Name",value=f"{myAnime.alternative_titles.ja}")
        if myAnime.studios != "":
            studiosData = ""
            for i in myAnime.studios.studios:
                studiosData = studiosData + f"{i.name}\n"
            em.add_field(name=f"Studios",value=f"{studiosData}")
        if myAnime.genres is not None:
            genresData = ""
            for i in myAnime.genres.genres:
                genresData = genresData + f"{i.name}\n"
            em.add_field(name=f"Genres",value=f"{genresData}")
        em.set_image(url=myAnime.main_picture)
        em.set_author(name="Requested by: " + str(ctx.user.name + "#" + ctx.user.discriminator),icon_url=ctx.user.avatar.url)
        em.set_footer(text="Chaotic Gremlin by TheReddDragon")
        await mymsg.edit(content="I found your anime!",embed=em)

    @discord.app_commands.command(name="search")
    async def AniSearch(self,ctx,name: str):
        await ctx.response.send_message("One moment... Searching...")
        mymsg = await ctx.original_response()
        em = discord.Embed(color=ctx.user.accent_color,title="Anime Search",description="**Query: " + name + "**")
        em.set_author(name="Requested by: " + str(ctx.user.name + "#" + ctx.user.discriminator),icon_url=ctx.user.avatar.url)
        myAnimes = self.client.searchAnime(name,5,fields="alternative_titles,source,rating,media_type,start_season")
        em.set_thumbnail(url=myAnimes[0].main_picture)
        for myAnime in myAnimes:
            myReturnText = "**Also Known As: **\n"
            if myAnime.alternative_titles.synonyms is not None:
                for entry in myAnime.alternative_titles.synonyms:
                    myReturnText = myReturnText + entry + "\n"
                myReturnText = myReturnText + "\n"
            if myAnime.alternative_titles.en != None:
                myReturnText = myReturnText + "**English Name:** " + myAnime.alternative_titles.en + "\n"
            if myAnime.alternative_titles.ja != None:
                myReturnText = myReturnText + "**Japanese Name:** " + myAnime.alternative_titles.ja + "\n"
            myReturnText = myReturnText + f"\n**Rating:** {myAnime.rating.human_rating} - {myAnime.rating.rating_desc}\n\n**Season: **{myAnime.start_season.season.capitalize()} {myAnime.start_season.year}"
            if myAnime.media_type != "":
                em.add_field(name=f"{myAnime.media_type.capitalize()}: {myAnime.title}",value=f"ID: {myAnime.id}\n{myReturnText}",inline=True)
            else:
                em.add_field(name=f"Entry: {myAnime.title}",value=f"ID: {myAnime.id}\n{myReturnText}",inline=True)
        logging.info(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) anime-searched for {name}")
        em.set_footer(text="Chaotic Gremlin by TheReddDragon")
        await mymsg.edit(content="Search Complete!",embed=em)
        
async def setup(bot):
    bot = bot
    logging.info("Anime module activated.")
    await bot.add_cog(Anime(bot))