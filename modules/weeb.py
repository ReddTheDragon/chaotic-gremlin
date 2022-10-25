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
        # TO DO MAINTENANCE
        self.maintenance_mode = False
        print(os.getcwd())
        with open(os.path.join(".", "tokens","mal-client-id.txt")) as myd:
            token = myd.readlines()
            token = token[0].strip("\r").strip("\n")
            print(token)
        self.client = Client(token)
        print(self.client)

    @discord.app_commands.command(name="anime",description="Grab info about a specific anime")
    async def AniGrab(self,ctx,id: str):
        await ctx.response.send_message("One moment...")
        mymsg = await ctx.original_response()
        em = discord.Embed(color=ctx.user.accent_color,title="Anime Query",description="**ID: " + str(id) + "**")
        myAnime = ""
        myAnime = self.client.get_anime(id,fields="alternative_titles,nsfw,rating,media_type,start_season,status,synopsis,mean,num_list_users,num_scoring_users,genres,num_episodes,studios,genres")
        if myAnime == 404:
            await mymsg.edit(content="Your anime couldn't be found 😭")
            return
        if myAnime.nsfw.nsfw_id == 1 or myAnime.nsfw.nsfw_id == 0:
            if ctx.channel.nsfw == False:
                tag = ""
                if myAnime.nsfw.nsfw_id == 1:
                    tag = "potential NSFW"
                elif myAnime.nsfw.nsfw_id == 0:
                    tag = "NSFW"
                else:
                    tag = "<<<THERE HAS BEEN AN ERROR PLEASE CONTACT BOT DEV>>>"
                    logging.critical(f"<<<BUG ALERT>>> Anime {myAnime.title} (id {myAnime.id}) has NSFW ID of {myAnime.nsfw.nsfw_id}.")
                em.description = em.description + f"\nSorry, but I cannot display {tag} anime in this chat. Please try again in an age-restricted channel."
                em.color=discord.Color.red()
                await mymsg.edit(content="Error retrieving anime...",embed=em)
                return
        em.description = em.description + f"\n**Name:** {myAnime.title}\n**Media Type:** {myAnime.media_type}\n**Mean Rating:** {myAnime.mean}\n**Number of Episodes:** {myAnime.num_episodes}\n**Status:** {myAnime.status.readable_status.capitalize()}\n"
        if myAnime.start_season is not None:
            em.description = em.description + f"**Start Season:** {myAnime.start_season.season.capitalize()} {myAnime.start_season.year}\n**Rated {myAnime.rating.human_rating} - {myAnime.rating.rating_desc}**\n"
        em.description = em.description + f"**Safety:** *{myAnime.nsfw.isnsfw.capitalize()}*"
        akaData = ""
        studiosData = ""
        if myAnime.alternative_titles.synonyms is not None:
            for i in myAnime.alternative_titles.synonyms:
                akaData = akaData + f"{i}\n"
            em.add_field(name=f"Also Known As",value=f"{akaData}",inline=False)
        if myAnime.alternative_titles.en != '':
            em.add_field(name=f"English Name",value=f"{myAnime.alternative_titles.en}",inline=False)
        if myAnime.alternative_titles.ja != '':
            em.add_field(name=f"Japanese Name",value=f"{myAnime.alternative_titles.ja}",inline=False)
        if myAnime.studios is not None:
            studiosData = ""
            for i in myAnime.studios.studios:
                studiosData = studiosData + f"{i.name}\n"
            em.add_field(name=f"Studios",value=f"{studiosData}",inline=False)
        if myAnime.genres is not None:
            genresData = ""
            for i in myAnime.genres.genres:
                genresData = genresData + f"{i.name}\n"
            em.add_field(name=f"Genres",value=f"{genresData}",inline=False)
        em.set_image(url=myAnime.main_picture)
        em.set_author(name="Requested by: " + str(ctx.user.name + "#" + ctx.user.discriminator),icon_url=ctx.user.avatar.url)
        em.set_footer(text="Chaotic Gremlin by TheReddDragon")
        if myAnime.synopsis is not None:
            if len(myAnime.synopsis) > 950:
                em.add_field(name="Synopsis",value=f"||{myAnime.synopsis[0:950]}... View the rest on MAL.||",inline=False)
            else:
                em.add_field(name="Synopsis",value=f"||{myAnime.synopsis}||",inline=False)
        logging.info(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) anime-grabbed {myAnime.id} ({myAnime.title}) in guild {ctx.guild_id}")
        await mymsg.edit(content="I found your anime!",embed=em)

    @discord.app_commands.command(name="manga",description="Grab info about a specific manga")
    async def MangaGrab(self,ctx,id: str):
        await ctx.response.send_message("One moment...")
        mymsg = await ctx.original_response()
        em = discord.Embed(color=ctx.user.accent_color,title="Manga Query",description="**ID: " + str(id) + "**")
        mymanga = ""
        mymanga = self.client.get_manga(id,fields="alternative_titles,nsfw,media_type,start_date,end_date,status,synopsis,mean,num_list_users,num_scoring_users,genres,num_chapters,num_volumes,authors,genres,mean")
        if mymanga == 404:
            await mymsg.edit(content="Your manga couldn't be found 😭")
            return
        if mymanga.nsfw.nsfw_id == 1 or mymanga.nsfw.nsfw_id == 0:
            if ctx.channel.nsfw == False:
                tag = ""
                if mymanga.nsfw.nsfw_id == 1:
                    tag = "potential NSFW"
                elif mymanga.nsfw.nsfw_id == 0:
                    tag = "NSFW"
                else:
                    tag = "<<<THERE HAS BEEN AN ERROR PLEASE CONTACT BOT DEV>>>"
                    logging.critical(f"<<<BUG ALERT>>> Manga {mymanga.title} (id {mymanga.id}) has NSFW ID of {mymanga.nsfw.nsfw_id}.")
                em.description = em.description + f"\nSorry, but I cannot display {tag} manga in this chat. Please try again in an age-restricted channel."
                em.color=discord.Color.red()
                await mymsg.edit(content="Error retrieving manga...",embed=em)
                return
        if mymanga.mean == "" or mymanga.mean is None:
            mymanga.set_mean("n/a")
        em.description = em.description + f"\n**Name:** {mymanga.title}\n**Media Type:** {mymanga.media_type}\n**Mean Rating:** {mymanga.mean}\n"
        if mymanga.num_chapters != -1 and mymanga.num_volumes != -1:
            em.description = em.description + f"\n**{mymanga.num_chapters} chapter(s), {mymanga.num_volumes} volume(s)**\n"
        elif mymanga.num_chapters != -1 and mymanga.num_volumes == -1:
            em.description = em.description + f"\n**{mymanga.num_chapters} chapter(s), 0 volume(s)**\n"
        elif mymanga.num_chapters == -1 and mymanga.num_volumes != -1:
            em.description = em.description + f"\n**0 chapter(s), {mymanga.num_volumes} volume(s)**\n"
        elif mymanga.num_chapters == -1 and mymanga.num_volumes == -1:
            em.description = em.description + f"\n**No chapters or volumes**\n"
        em.description = em.description + f"\n**Status:** {mymanga.status.readable_status.capitalize()}\n"
        if mymanga.start_date is not None and mymanga.start_date != "":
            em.description = em.description + f"**Start Date:** {mymanga.start_date}\n"
        if mymanga.end_date is not None and mymanga.end_date != "":
            em.description = em.description + f"**End Date:** {mymanga.end_date}\n\n"
        else:
            em.description = em.description + "\n"
        em.description = em.description + f"**Safety:** *{mymanga.nsfw.isnsfw.capitalize()}*"
        akaData = ""
        studiosData = ""
        if mymanga.alternative_titles.synonyms is not None:
            for i in mymanga.alternative_titles.synonyms:
                akaData = akaData + f"{i}\n"
            em.add_field(name=f"Also Known As",value=f"{akaData}",inline=False)
        if mymanga.alternative_titles.en != '':
            em.add_field(name=f"English Name",value=f"{mymanga.alternative_titles.en}",inline=False)
        if mymanga.alternative_titles.ja != '':
            em.add_field(name=f"Japanese Name",value=f"{mymanga.alternative_titles.ja}",inline=False)
        if mymanga.authors is not None:
            print(mymanga.authors)
            studiosData = ""
            for i in mymanga.authors.authors:
                print(i)
                studiosData = studiosData + f"{i.FullName} - {i.role}\n"
            if studiosData == "":
                studiosData = "N/A"
            em.add_field(name=f"Authors",value=f"{studiosData}",inline=False)
        if mymanga.genres is not None:
            genresData = ""
            for i in mymanga.genres.genres:
                genresData = genresData + f"{i.name}\n"
            em.add_field(name=f"Genres",value=f"{genresData}",inline=False)
        em.set_image(url=mymanga.main_picture)
        em.set_author(name="Requested by: " + str(ctx.user.name + "#" + ctx.user.discriminator),icon_url=ctx.user.avatar.url)
        em.set_footer(text="Chaotic Gremlin by TheReddDragon")
        if mymanga.synopsis is not None:
            if len(mymanga.synopsis) > 950:
                em.add_field(name="Synopsis",value=f"||{mymanga.synopsis[0:950]}... View the rest on MAL.||",inline=False)
            else:
                em.add_field(name="Synopsis",value=f"||{mymanga.synopsis}||",inline=False)
        print(em.fields)
        logging.info(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) manga-grabbed {mymanga.id} ({mymanga.title}) in guild {ctx.guild_id}")
        await mymsg.edit(content="I found your manga!",embed=em)


    def handleAnimeReturnText(self,anime,embed):
        print(anime.rating)
        myReturnText = ""
        if anime.alternative_titles.synonyms is not None and anime.alternative_titles.synonyms != "":
            myReturnText = "**Also Known As: **\n"
            for entry in anime.alternative_titles.synonyms:
                myReturnText = myReturnText + entry + "\n"
            myReturnText = myReturnText + "\n"
        if anime.alternative_titles.en != None and anime.alternative_titles.en != "":
            myReturnText = myReturnText + "**English Name:** " + anime.alternative_titles.en + "\n"
        if anime.alternative_titles.ja != None and anime.alternative_titles.ja != "":
            myReturnText = myReturnText + "**Japanese Name:** " + anime.alternative_titles.ja + "\n"
        if anime.rating != "":
            myReturnText = myReturnText + f"\n**Rating:** {anime.rating.human_rating} - {anime.rating.rating_desc}\n\n"
        if anime.start_season is not None:
            myReturnText = myReturnText + f"**Season: **{anime.start_season.season.capitalize()} {anime.start_season.year}"
        if anime.media_type != "":
            embed.add_field(name=f"{anime.media_type.capitalize()}: {anime.title}",value=f"ID: {anime.id}\n{myReturnText}")
        else:
            embed.add_field(name=f"Entry: {anime.title}",value=f"ID: {anime.id}\n{myReturnText}")
        return anime, embed

    def handleMangaReturnText(self,manga,embed):
        myReturnText = ""
        if manga.status != "":
            myReturnText = f"**Status:** {manga.status.readable_status}\n"
        if manga.alternative_titles.synonyms is not None and manga.alternative_titles.synonyms != "":
            myReturnText = myReturnText + "**Also Known As: **\n"
            for entry in manga.alternative_titles.synonyms:
                myReturnText = myReturnText + entry + "\n"
            myReturnText = myReturnText + "\n"
        if manga.alternative_titles.en != None and manga.alternative_titles.en != "":
            myReturnText = myReturnText + "**English Name:** " + manga.alternative_titles.en + "\n"
        if manga.alternative_titles.ja != None and manga.alternative_titles.ja != "":
            myReturnText = myReturnText + "**Japanese Name:** " + manga.alternative_titles.ja + "\n"
        if manga.start_date is not None and manga.start_date != "":
            myReturnText = myReturnText + f"**Start Date: **{manga.start_date}"
        if manga.end_date is not None and manga.end_date != "":
            myReturnText = myReturnText + f"\n**End Date: **{manga.end_date}\n"
        if manga.media_type != "":
            embed.add_field(name=f"{manga.media_type.capitalize()}: {manga.title}",value=f"ID: {manga.id}\n{myReturnText}")
        else:
            embed.add_field(name=f"Entry: {manga.title}",value=f"ID: {manga.id}\n{myReturnText}")
        return manga, embed

    @discord.app_commands.command(name="anisearch",description="Search for an anime")
    async def AniSearch(self,ctx,name: str):
        await ctx.response.send_message("One moment... Searching...  If this takes more than a few seconds, please try again with a longer search string.")
        mymsg = await ctx.original_response()
        em = discord.Embed(color=ctx.user.accent_color,title="Anime Search",description="**Query: " + name + "**")
        em.set_author(name="Requested by: " + str(ctx.user.name + "#" + ctx.user.discriminator),icon_url=ctx.user.avatar.url)
        # lazy code
        pageData, myAnimes = self.client.searchAnime(name,20,fields="alternative_titles,source,rating,media_type,start_season,nsfw")
        if myAnimes == 400:
            logging.warning(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) tried to search {name}, generating a bad request.")
            await mymsg.edit(content="Bad Request, please try a longer search string")
            return
        if myAnimes == 404:
            logging.warning(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) tried to search {name}, generating a not found error.")
            await mymsg.edit(content="404 Not Found. Please report this to bot developer.")
            return
        isThumbSet = False
        totalAnimesListed = 0
        while totalAnimesListed < 5:
            for myAnime in myAnimes:
                totalAnimesListed = totalAnimesListed + 1
                if totalAnimesListed == 6:
                    break
                if myAnime.nsfw.nsfw_id == 1 or myAnime.nsfw.nsfw_id == 0:
                    if ctx.channel.nsfw == True:
                        if isThumbSet == False:
                            em.set_thumbnail(url=myAnime.main_picture)
                            isThumbSet = True
                        myAnime, em = self.handleAnimeReturnText(myAnime, em)
                    else:
                        totalAnimesListed = totalAnimesListed - 1
                else:
                    if isThumbSet == False:
                        em.set_thumbnail(url=myAnime.main_picture)
                        isThumbSet = True
                    myAnime, em = self.handleAnimeReturnText(myAnime, em)
        logging.info(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) anime-searched for \"{name}\" in guild {ctx.guild_id}")
        em.set_footer(text="Chaotic Gremlin by TheReddDragon")
        await mymsg.edit(content="Search Complete!",embed=em)
    
    @discord.app_commands.command(name="mangasearch",description="Search for a manga")
    async def MangaSearch(self,ctx,name: str):
        await ctx.response.send_message("One moment... Searching...  If this takes more than a few seconds, please try again with a longer search string.")
        mymsg = await ctx.original_response()
        em = discord.Embed(color=ctx.user.accent_color,title="Manga Search",description="**Query: " + name + "**")
        em.set_author(name="Requested by: " + str(ctx.user.name + "#" + ctx.user.discriminator),icon_url=ctx.user.avatar.url)
        pageData, myMangas = self.client.searchManga(name,20,fields="alternative_titles,media_type,start_date,authors,end_date,status,nsfw,mean")
        print(myMangas)
        if myMangas == 400:
            logging.warning(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) tried to search {name}, generating a bad request.")
            await mymsg.edit(content="Bad Request, please try a longer search string")
            return
        if myMangas == 404:
            logging.warning(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) tried to search {name}, generating a not found error.")
            await mymsg.edit(content="404 Not Found. Please report this to bot developer.")
            return
        isThumbSet = False
        totalMangaListed = 0
        while totalMangaListed < 5:
            for myManga in myMangas:
                totalMangaListed = totalMangaListed + 1
                if totalMangaListed == 6:
                    break
                if myManga.nsfw.nsfw_id == 1 or myManga.nsfw.nsfw_id == 0:
                    if ctx.channel.nsfw == True:
                        if isThumbSet == False:
                            em.set_thumbnail(url=myManga.main_picture)
                            isThumbSet = True
                        myManga, em = self.handleMangaReturnText(myManga, em)
                    else:
                        totalMangaListed = totalMangaListed - 1
                else:
                    if isThumbSet == False:
                        em.set_thumbnail(url=myManga.main_picture)
                        isThumbSet = True
                    myManga, em = self.handleMangaReturnText(myManga, em)
        logging.info(f"User {ctx.user.name}#{ctx.user.discriminator} (<@{ctx.user.id}>) manga-searched for \"{name}\" in guild {ctx.guild_id}")
        em.set_footer(text="Chaotic Gremlin by TheReddDragon")
        await mymsg.edit(content="Search Complete!",embed=em)
tree = ""
async def setup(bot):
    bot = bot
    tree = bot.tree
    logging.info("Anime module activated.")
    await bot.add_cog(Anime(bot))