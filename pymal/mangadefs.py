#!/usr/bin/python
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



# VERY HEAVILY TODO: add related anime, manga, and serialization
class MangaStatus(object):
    def __init__(self, stat):
        self.status = stat
        if self.status == "finished":
            self.readable_status = "concluded"
            self.status_id = 0
        elif self.status == "currently_publishing":
            self.readable_status = "currently publishing"
            self.status_id = 1
        elif self.status == "not_yet_published":
            self.readable_status = "not yet published"
            self.status_id = 2
        else:
            self.readable_status = "unknown"
            self.status_id = 3

class MangaAuthor(object):
    def __init__(self,id,FirstName,LastName,role):
        self.id = id
        self.FirstName = FirstName
        self.LastName = LastName
        self.FullName = FirstName + LastName
        self.role = role

class MangaAuthors(object):
    def __init__(self):
        self.authors = []

    def add(self,studio: MangaAuthor):
        self.authors.append(studio)

    def delauthor(self, name: str):
        i = 0
        for z in self.authors:
            if z.FullName == name:
                self.authors.pop(i)
                break
            i = i + 1


#2 = sfw, 1 = questionable, 0 = nsfw
class MangaNsfw(object):
    def __init__(self,nsfw=None):
        self.nsfw = nsfw
        if nsfw == "white":
            self.isnsfw = "Safe For Work"
            self.nsfw_id = 2
        elif nsfw == "gray":
            self.isnsfw = "May Not Be Safe For Work"
            self.nsfw_id = 1
        elif nsfw == "black":
            self.isnsfw = "Not Safe For Work"
            self.nsfw_id = 0
        else:
            self.isnsfw = ""
            self.nsfw_id = 3


class PaginationTracker(object):
    def __init__(self, nextURL, previousURL = None):
        self.nextURL = nextURL
        self.previousURL = previousURL
        if self.nextURL is not None:
            mySplit = self.nextURL.split("?")
            if len(mySplit) > 1:
                self.paginationDevNext = mySplit[1]
        if self.previousURL is not None:
            mySplit = self.previousURL.split("?")
            if len(mySplit) > 1:
                self.paginationDevPrevious = mySplit[1]



    def updatePagination(self,nextURL = None, previousURL = None):
        if nextURL is not None:
            self.nextURL = nextURL
            self.paginationDevNext = self.nextURL.split("?")[1]
        if self.previousURL is not None:
            self.previousURL = previousURL
            self.paginationDevPrevious = self.previousURL.split("?"[1])

class MangaAltTitles(object):
    def __init__(self, data):
        if data["synonyms"] == []:
            self.synonyms = None
        else:
            self.synonyms = data["synonyms"]
        if data["en"] != '':
            self.en = data["en"]
        else:
            self.en = ""
        if data["ja"] != '':
            self.ja = data["ja"]
        else:
            self.ja = ""

class MangaGenre(object):
    def __init__(self, id, genre):
        self.id = id
        self.name = genre

class MangaGenres(object):
    def __init__(self):
        self.genres = []

    def add(self,genre: MangaGenre):
        self.genres.append(genre)

    def delgenre(self, name: str):
        i = 0
        for z in self.genres:
            if z.name == name:
                self.genres.pop(i)
                break
            i = i + 1


class MangaFields(object):
    def __init__(self, id:int = None, title: str = None, main_picture=None, alternative_titles=None, start_date=None, end_date=None, synopsis=None, mean=None, rank=None, popularity=None, num_list_users=None,
    num_scoring_users=None, nsfw=None, genres: MangaGenres = None, created_at=None, updated_at=None, media_type=None, status=None, num_chapters=None, num_volumes=None, authors=None, paging=None):
        self.id: int = id
        self.title: str = title
        self.main_picture = main_picture
        self.alternative_titles = alternative_titles
        self.start_date = start_date
        self.end_date = end_date
        if end_date == "":
            end_date = "n/a"
        else:
            self.end_date = end_date
        self.synopsis = synopsis
        self.mean = mean
        self.rank = rank
        self.popularity = popularity
        self.num_list_users: int = num_list_users
        self.num_scoring_users: int = num_scoring_users
        self.nsfw: MangaNsfw = nsfw
        self.genres = genres
        self.created_at: str = created_at
        self.updated_at: str = updated_at
        self.media_type = media_type
        self.status: MangaStatus = status
        self.num_volumes: int = num_volumes
        self.num_chapters: int = num_chapters
        self.authors: MangaAuthors = authors
        self.paging: PaginationTracker = paging


    def set_id(self,val: int = None):
        self.id = val
        return True

    def set_title(self,val: str = None):
        self.title = val
        return True

    def set_main_picture(self,val = None):
        self.main_picture = val
        return True

    def set_alternative_titles(self,val = None):
        self.alternative_titles = val
        return True

    def set_start_date(self,val = None):
        self.start_date = val
        return True

    def set_end_date(self,val = None):
        self.end_date = val
        return True

    def set_synopsis(self,val = None):
        self.synopsis = val
        return True

    # mean score
    def set_mean(self, val = None):
        self.mean = val
        return True

    def set_rank(self, val = None):
        self.rank = val
        return True

    def set_popularity(self, val = None):
        self.popularity = val
        return True

    # list of users that have it in their list
    def set_num_list_users(self, val = None):
        self.num_list_users = val
        return True

    def set_num_scoring_users(self, val = None):
        self.num_scoring_users = val
        return True

    def set_nsfw(self,val = None):
        self.nsfw = val
        return True

    def set_genres(self, val = None):
        self.genres = val
        return True

    def set_created_at(self, val = None):
        self.created_at = val
        return True

    def set_updated_at(self, val = None):
        self.updated_at = val
        return True

    def set_media_type(self, val = None):
        self.media_type = val
        return True

    def set_status(self, val = None):
        self.status = val
        return True

    def set_num_chapters(self, val = None):
        self.num_chapters = val
        return True

    def set_authors(self, val = None):
        self.authors = val

    def set_paging(self, val = None):
        self.paging = val