#!/usr/bin/python
# Copyright 2022 TDS (TheReddDragon)
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
import logging, pycurl, json
from pymal.anidefinitions import AnimeBroadcast, AnimeFields, AnimeNsfw, AnimeRating, PaginationTracker, AnimeSeason, AnimeStatus, AnimeAltTitles, AnimeGenres, AnimeGenre, AnimeStudio, AnimeStudios
from pymal.mangadefs import MangaStatus, MangaFields, MangaNsfw, MangaGenres, MangaGenre, MangaAuthors, MangaAuthor, MangaAltTitles
from urllib.parse import quote
from io import BytesIO

class NetworkError(Exception):
    def __init__(self, message, objec: object=None):
        self.message = message
        if isinstance(objec,pycurl.Curl):
            logging.warning("Closed pycurl object")
            objec.close()
        super().__init__(self.message)

class BadRequestException(Exception):
    def __init__(self, message, objec: object=None):
        self.message = message
        if isinstance(objec,pycurl.Curl):
            logging.warning("Closed pycurl object")
            objec.close()


class Client(object):
    def __init__(self,token):
        logging.info(f"Client object created with token {token}")
        self.__token = token
        self.endpoints = {
            "anime":"/anime",
            "manga":"/manga"
        }

    def __mangaEndpoint(self, mangaid):
        return self.endpoints["manga"] + "/" + str(mangaid)

    def __animeEndpoint(self, animeid):
        return self.endpoints["anime"] + "/" + str(animeid)


    def __sanitizeUrl(self,data):
        myData = quote(data,safe="/&,")
        return myData


    def __access_endpoint(self,endpoint,options=None):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(pycurl.HTTPHEADER, [f"X-MAL-CLIENT-ID: {self.__token}"])
        # if options aren't set, just access the endpoint url
        if options is None:
            c.setopt(c.URL, "https://api.myanimelist.net/v2" + str(endpoint) + "?nsfw=true")
            logging.info("Retrieving https://api.myanimelist.net/v2" + str(endpoint) + "...")
        # if options ARE set, access endpoint url with the options
        else:
            c.setopt(c.URL, "https://api.myanimelist.net/v2" + str(endpoint) + "?" + str(options) + "&nsfw=true")
            logging.info("Retrieving https://api.myanimelist.net/v2" + str(endpoint) + "?" + str(options) + "...")
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        if c.getinfo(c.RESPONSE_CODE) != 200:
            if c.getinfo(c.RESPONSE_CODE) == 400:
                logging.warning("Retrieving url failed, bad request")
                return 400
                # raise BadRequestException("Bad Request",c)
            else:
                temp = c.getinfo(c.RESPONSE_CODE)
                logging.warning(f"Retrieving url failed, code {temp}")
                return c.getinfo(c.RESPONSE_CODE)
                # raise NetworkError("Retrieving the url failed with error code " + str(c.getinfo(c.RESPONSE_CODE)),c)
        c.close()
        body = buffer.getvalue()
        body = body.decode("utf-8")
        return body

    def doMangaKeyProcessing(self,myData):
        myManga = []
        myPagination = PaginationTracker("")
        # set pagination data
        if "next" in myData["paging"].keys():
            myPagination.updatePagination(nextURL = myData["paging"]["next"])
        else:
            myPagination.updatePagination(nextURL = "")
        if "previous" in myData["paging"].keys():
            myPagination.updatePagination(previousURL = myData["paging"]["previous"])
        else:
            myPagination.updatePagination(previousURL = "")
        # key processing
        for key in myData["data"]:
            for i in key:
                c = None
                mid = ""
                mtitle = ""
                startdate = ""
                enddate = ""
                synop = ""
                meanscore = ""
                mrank = ""
                mpopularity = ""
                mnum_list_users = ""
                mnum_scoring_users = ""
                mnsfw = None
                mcreated_at = ""
                mupdated_at = ""
                # media type
                mmedia = ""
                mstatus = None
                manga_chapters = ""
                manga_volumes = 0
                manga_chapters = 0
                myAuthors = MangaAuthors()
                myGenres = None
                mid = key[i]["id"]
                mtitle = key[i]["title"]
                try:
                    mpic = key[i]["main_picture"]["large"]
                except KeyError:
                    try:
                        mpic = key[i]["main_picture"]["medium"]
                    except KeyError:
                        mpic = ""
                        pass
                    pass
                try:
                    c = MangaAltTitles(key[i]["alternative_titles"])
                except KeyError:
                    pass
                try:
                    startdate = key[i]["start_date"]
                except KeyError:
                    pass
                try:
                    enddate = key[i]["end_date"]
                except KeyError:
                    pass
                try:
                    synop = key[i]["synopsis"]
                except KeyError:
                    pass
                try:
                    meanscore = key[i]["mean"]
                except KeyError:
                    pass
                try:
                    mrank = key[i]["rank"]
                except KeyError:
                    pass
                try:
                    mpopularity = key[i]["popularity"]
                except KeyError:
                    pass
                try:
                    mnum_list_users = key[i]["num_list_users"]
                except KeyError:
                    pass
                try:
                    mnum_scoring_users = key[i]["num_scoring_users"]
                except KeyError:
                    pass
                try:
                    mnsfw = MangaNsfw(key[i]["nsfw"])
                except KeyError:
                    pass
                myGenres = MangaGenres()
                try:
                    for ow in key[i]["genres"]:
                        mytempgenre = MangaGenre(ow["id"],ow["name"])
                        myGenres.add(mytempgenre)
                except KeyError:
                    pass
                try:
                    mcreated_at = key[i]["created_at"]
                except KeyError:
                    pass
                try:
                    mupdated_at = key[i]["updated_at"]
                except KeyError:
                    pass
                try:
                    mmedia = key[i]["media_type"]
                    if mmedia == "one_shot":
                        mmedia = "one shot"
                    if mmedia == "light_novel":
                        mmedia = "light novel"
                except KeyError:
                    pass
                try:
                    mstatus = MangaStatus(key[i]["status"])
                except KeyError:
                    pass
                try:
                    manga_chapters = key[i]["num_chapters"]
                except KeyError:
                    manga_chapters = -1
                    pass
                try:
                    manga_volumes = key[i]["num_volumes"]
                except KeyError:
                    manga_volumes = -1
                    pass
                try:
                    for b in key[i]["authors"]:
                        myAuthors.add(MangaAuthor(b["id"],b["node"]["first_name"],b["node"]["last_name"],b["role"]))
                except KeyError:

                    pass
                myManga.append(MangaFields(mid,mtitle,mpic,c,startdate,enddate,synop,meanscore,mrank,mpopularity,mnum_list_users,mnum_scoring_users,mnsfw,myGenres,mcreated_at,mupdated_at,mmedia,mstatus,manga_chapters,manga_volumes,myAuthors))
        return myPagination, myManga




    def doAnimeKeyProcessing(self,myData):
        myAnime = []
        myPagination = PaginationTracker("")
        # set pagination data
        if "next" in myData["paging"].keys():
            myPagination.updatePagination(nextURL = myData["paging"]["next"])
        else:
            myPagination.updatePagination(nextURL = "")
        if "previous" in myData["paging"].keys():
            myPagination.updatePagination(previousURL = myData["paging"]["previous"])
        else:
            myPagination.updatePagination(previousURL = "")
        for key in myData["data"]:

            for i in key:
                c = None
                mid = ""
                mtitle = ""
                startdate = ""
                enddate = ""
                synop = ""
                meanscore = ""
                mrank = ""
                mpopularity = ""
                mnum_list_users = ""
                mnum_scoring_users = ""
                mnsfw = None
                mcreated_at = ""
                mupdated_at = ""
                mmedia = ""
                mstatus = None
                meps = ""
                mstart = None
                mbrod = None
                msource = ""
                mavgduration = ""
                mrating = ""
                myStudios = ""
                myGenres = None
                mid = key[i]["id"]
                mtitle = key[i]["title"]
                try:
                    mpic = key[i]["main_picture"]["large"]
                except KeyError:
                    try:
                        mpic = key[i]["main_picture"]["medium"]
                    except KeyError:
                        pass
                    pass
                # get the keys for the alt titles
                try:
                    c = AnimeAltTitles(key[i]["alternative_titles"])
                except KeyError:
                    pass
                try:
                    startdate = key[i]["start_date"]
                except KeyError:
                    pass
                try:
                    enddate = key[i]["end_date"]
                except KeyError:
                    pass
                try:
                    synop = key[i]["synopsis"]
                except KeyError:
                    pass
                try:
                    meanscore = key[i]["mean"]
                except KeyError:
                    pass
                try:
                    mrank = key[i]["rank"]
                except KeyError:
                    pass
                try:
                    mpopularity = key[i]["popularity"]
                except KeyError:
                    pass
                try:
                    mnum_list_users = key[i]["num_list_users"]
                except KeyError:
                    pass
                try:
                    mnum_scoring_users = key[i]["num_scoring_users"]
                except KeyError:
                    pass
                try:
                    mnsfw = AnimeNsfw(key[i]["nsfw"])
                except KeyError:
                    pass
                myGenres = AnimeGenres()
                try:
                    for ow in key[i]["genres"]:
                        mytempgenre = AnimeGenre(ow["id"],ow["name"])
                        myGenres.add(mytempgenre)
                except KeyError:
                    pass
                try:
                    mcreated_at = key[i]["created_at"]
                except KeyError:
                    pass
                try:
                    mupdated_at = key[i]["updated_at"]
                except KeyError:
                    pass
                try:
                    mmedia = key[i]["media_type"]
                except KeyError:
                    pass
                try:
                    mstatus = AnimeStatus(key[i]["status"])
                except KeyError:
                    pass
                try:
                    meps = key[i]["num_episodes"]
                except KeyError:
                    pass
                try:
                    mstart = AnimeSeason(key[i]["start_season"]["year"],key[i]["start_season"]["season"])
                except KeyError:
                    pass
                try:
                    mbrod = AnimeBroadcast(key[i]["broadcast"]["day_of_the_week"], key[i]["broadcast"]["start_time"])
                except KeyError:
                    pass
                try:
                    msource = key[i]["source"]
                except KeyError:
                    msource = ""
                    pass
                try:
                    mavgduration = round(float(key[i]["average_episode_duration"] / 60),2)
                except KeyError:
                    pass
                try:
                    mrating = AnimeRating(key[i]["rating"])
                except KeyError:
                    pass
                myStudios = AnimeStudios()
                try:
                    for i in key[i]["studios"]:
                        myStudios.add(AnimeStudio(i["id"],i["name"]))
                except KeyError:
                    pass
                myAnime.append(AnimeFields(mid,mtitle,mpic,c,startdate,enddate,synop,meanscore,mrank,mpopularity,mnum_list_users,mnum_scoring_users,mnsfw,myGenres,mcreated_at,mupdated_at,mmedia,mstatus,meps,mstart,mbrod,msource,mavgduration,mrating,myStudios))
        return myPagination, myAnime

    def get_manga(self,query,fields = None):
        myquery = quote(query,safe="/&")
        myData = ""
        if fields is None:
            myData = self.__access_endpoint(self.__mangaEndpoint(query))
        else:
            fields = quote(fields)
            myData = self.__access_endpoint(self.__mangaEndpoint(query),f"fields={fields}")
        if myData == 404:
            return 404
        myData = json.loads(myData)
        c = None
        mid = ""
        mtitle = ""
        startdate = ""
        enddate = ""
        synop = ""
        meanscore = ""
        mrank = ""
        mpopularity = ""
        mnum_list_users = ""
        mnum_scoring_users = ""
        mnsfw = None
        mcreated_at = ""
        mupdated_at = ""
        # media type
        mmedia = ""
        mstatus = None
        manga_chapters = ""
        manga_volumes = 0
        manga_chapters = 0
        myAuthors = MangaAuthors()
        myGenres = None
        mid = myData["id"]
        mtitle = myData["title"]
        try:
            mpic = myData["main_picture"]["large"]
        except KeyError:
            try:
                mpic = myData["main_picture"]["medium"]
            except KeyError:
                mpic = ""
                pass
            pass
        try:
            c = MangaAltTitles(myData["alternative_titles"])
        except KeyError:
            pass
        try:
            startdate = myData["start_date"]
        except KeyError:
            pass
        try:
            enddate = myData["end_date"]
        except KeyError:
            pass
        try:
            synop = myData["synopsis"]
        except KeyError:
            pass
        try:
            meanscore = myData["mean"]
        except KeyError:
            pass
        try:
            mrank = myData["rank"]
        except KeyError:
            pass
        try:
            mpopularity = myData["popularity"]
        except KeyError:
            pass
        try:
            mnum_list_users = myData["num_list_users"]
        except KeyError:
            pass
        try:
            mnum_scoring_users = myData["num_scoring_users"]
        except KeyError:
            pass
        try:
            mnsfw = MangaNsfw(myData["nsfw"])
        except KeyError:
            pass
        myGenres = MangaGenres()
        try:
            for ow in myData["genres"]:
                mytempgenre = MangaGenre(ow["id"],ow["name"])
                myGenres.add(mytempgenre)
        except KeyError:
            pass
        try:
            mcreated_at = myData["created_at"]
        except KeyError:
            pass
        try:
            mupdated_at = myData["updated_at"]
        except KeyError:
            pass
        try:
            mmedia = myData["media_type"]
            if mmedia == "one_shot":
                mmedia = "one shot"
            if mmedia == "light_novel":
                mmedia = "light novel"
        except KeyError:
            pass
        try:
            mstatus = MangaStatus(myData["status"])
        except KeyError:
            pass
        try:
            manga_chapters = myData["num_chapters"]
        except KeyError:
            manga_chapters = -1
            pass
        try:
            manga_volumes = myData["num_volumes"]
        except KeyError:
            manga_volumes = -1
            pass
        try:
            for i in myData["authors"]:
                myAuthors.add(MangaAuthor(i["id"],i["node"]["first_name"],i["node"]["last_name"],i["role"]))
        except KeyError:
            pass
        return MangaFields(mid,mtitle,mpic,c,startdate,enddate,synop,meanscore,mrank,mpopularity,mnum_list_users,mnum_scoring_users,mnsfw,myGenres,mcreated_at,mupdated_at,mmedia,mstatus,manga_chapters,manga_volumes,myAuthors)
        
    def get_anime(self,query,fields = None):
        myquery = quote(query,safe="/&")
        myData = ""
        if fields is None:
            myData = self.__access_endpoint(self.__animeEndpoint(query))
        else:
            fields = quote(fields)
            myData = self.__access_endpoint(self.__animeEndpoint(query),f"fields={fields}")
        if myData == 404:
            return 404
        myData = json.loads(myData)
        c = None
        mid = ""
        mtitle = ""
        startdate = ""
        enddate = ""
        synop = ""
        meanscore = ""
        mrank = ""
        mpopularity = ""
        mnum_list_users = ""
        mnum_scoring_users = ""
        mnsfw = None
        mcreated_at = ""
        mupdated_at = ""
        mmedia = ""
        mstatus = None
        meps = ""
        mstart = None
        mbrod = None
        msource = ""
        mavgduration = ""
        mrating = ""
        myStudios = ""
        myGenres = None
        mid = myData["id"]
        mtitle = myData["title"]
        try:
            mpic = myData["main_picture"]["large"]
        except KeyError:
            try:
                mpic = myData["main_pciture"]["medium"]
            except KeyError:
                pass
            pass
        # get the keys for the alt titles
        try:
            c = AnimeAltTitles(myData["alternative_titles"])
        except KeyError:
            pass
        try:
            startdate = myData["start_date"]
        except KeyError:
            pass
        try:
            enddate = myData["end_date"]
        except KeyError:
            pass
        try:
            synop = myData["synopsis"]
        except KeyError:
            pass
        try:
            meanscore = myData["mean"]
        except KeyError:
            meanscore = "Unknown"
            pass
        try:
            mrank = myData["rank"]
        except KeyError:
            mrank = "Unknown"
            pass
        try:
            mpopularity = myData["popularity"]
        except KeyError:
            pass
        try:
            mnum_list_users = myData["num_list_users"]
        except KeyError:
            pass
        try:
            mnum_scoring_users = myData["num_scoring_users"]
        except KeyError:
            pass
        try:
            mnsfw = AnimeNsfw(myData["nsfw"])
        except KeyError:
            pass
        myGenres = AnimeGenres()
        try:
            for ow in myData["genres"]:
                mytempgenre = AnimeGenre(ow["id"],ow["name"])
                myGenres.add(mytempgenre)
        except KeyError:
            pass
        try:
            mcreated_at = myData["created_at"]
        except KeyError:
            pass
        try:
            mupdated_at = myData["updated_at"]
        except KeyError:
            pass
        try:
            mmedia = myData["media_type"]
        except KeyError:
            pass
        try:
            mstatus = AnimeStatus(myData["status"])
        except KeyError:
            pass
        try:
            meps = myData["num_episodes"]
        except KeyError:
            pass
        try:
            mstart = AnimeSeason(myData["start_season"]["year"],myData["start_season"]["season"])
        except KeyError:
            pass
        try:
            mbrod = AnimeBroadcast(myData["broadcast"]["day_of_the_week"], myData["broadcast"]["start_time"])
        except KeyError:
            pass
        try:
            msource = myData["source"]
        except KeyError:
            msource = ""
            pass
        try:
            mavgduration = round(float(myData["average_episode_duration"] / 60),2)
        except KeyError:
            pass
        try:
            mrating = AnimeRating(myData["rating"])
        except KeyError:
            pass
        myStudios = AnimeStudios()
        try:
            for aba in myData["studios"]:
                myStudios.add(AnimeStudio(aba["id"],aba["name"]))
        except KeyError:
            pass
        return AnimeFields(mid,mtitle,mpic,c,startdate,enddate,synop,meanscore,mrank,mpopularity,mnum_list_users,mnum_scoring_users,mnsfw,myGenres,mcreated_at,mupdated_at,mmedia,mstatus,meps,mstart,mbrod,msource,mavgduration,mrating,myStudios)

    def handleNewAnimePage(self,nextQuery):
        myData = ""
        myPagination = PaginationTracker("")
        myData = self.__access_endpoint(self.endpoints["anime"],f"{nextQuery}")
        dataReturned = json.loads(myData)
        myPagination, myAnime = self.doAnimeKeyProcessing(dataReturned)
        return myPagination, myAnime
    
    def handleNewMangaPage(self,nextQuery):
        myData = ""
        myPagination = PaginationTracker("")
        myData = self.__access_endpoint(self.endpoints["manga"],f"{nextQuery}")
        dataReturned = json.loads(myData)
        myPagination, myManga = self.doMangaKeyProcessing(dataReturned)
        return myPagination, myManga

    # searches for an anime
    def searchAnime(self,query,limit=10,fields=None):
        myquery = self.__sanitizeUrl(query)
        myData = ""
        myPagination = PaginationTracker("")
        if fields is None:
            myData = self.__access_endpoint(self.endpoints["anime"],f"q={myquery}&limit={limit}")
            print(limit)
        else:
            fields = quote(fields)
            print(limit)
            myData = self.__access_endpoint(self.endpoints["anime"],f"q={myquery}&limit={limit}&fields={fields}")
        if myData == 404:
            return "",404
        elif myData == 400:
            return "",400
        dataReturned = json.loads(myData)
        
        myPagination, myAnime = self.doAnimeKeyProcessing(dataReturned)
        return myPagination, myAnime

    def searchManga(self,query,limit=10,fields=None):
        myquery = self.__sanitizeUrl(query)
        myData = ""
        myPagination = PaginationTracker("")
        if fields is None:
            myData = self.__access_endpoint(self.endpoints["manga"],f"q={myquery}&limit={limit}")
            print(limit)
        else:
            fields = quote(fields)
            print(limit)
            myData = self.__access_endpoint(self.endpoints["manga"],f"q={myquery}&limit={limit}&fields={fields}")
        if isinstance(myData,int):
            return '', myData
        dataReturned = json.loads(myData)
        myPagination, myManga = self.doMangaKeyProcessing(dataReturned)
        return myPagination, myManga