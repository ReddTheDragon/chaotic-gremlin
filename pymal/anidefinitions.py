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


#0, finished airing. 1, currently airing. 2, not yet aired. 3, unknown.
class AnimeStatus(object):
    def __init__(self, stat):
        self.status = stat
        if self.status == "finished_airing":
            self.readable_status = "finished airing"
            self.status_id = 0
        elif self.status == "currently_airing":
            self.readable_status = "currently airing"
            self.status_id = 1
        elif self.status == "not_yet_aired":
            self.readable_status = "not yet aired"
            self.status_id = 2
        else:
            self.readable_status = "unknown"
            self.status_id = 3

class AnimeStudio(object):
    def __init__(self,id,name):
        self.id = id
        self.name = name

class AnimeStudios(object):
    def __init__(self):
        self.studios = []

    def add(self,studio: AnimeStudio):
        self.studios.append(studio)

    def delstudio(self, name: str):
        i = 0
        for z in self.studios:
            if z.name == name:
                self.studios.pop(i)
                break
            i = i + 1

class AnimeSeason(object):
    def __init__(self, year: int = 0, season: str = "not set"):
        self.year = year
        self.season = season


class AnimeBroadcast(object):
    def __init__(self, day_of_week, start_time = None):
        self.day_of_the_week = day_of_week
        self.start_time = start_time


#2 = sfw, 1 = questionable, 0 = nsfw
class AnimeNsfw(object):
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


#0 = g, 1 = pg, 2 = pg_13, 3 = r, 4 = r+, 5 = rx
class AnimeRating(object):
    def __init__(self, rating):
        self.rating = rating
        if rating == "g":
            self.human_rating = "G"
            self.rating_id = 0
            self.rating_desc = "All Ages"
        elif rating == "pg":
            self.human_rating = "PG"
            self.rating_id = 1
            self.rating_desc = "Children"
        elif rating == "pg_13":
            self.human_rating = "PG-13"
            self.rating_id = 2
            self.rating_desc = "Teens 13 and Older"
        elif rating == "r":
            self.human_rating = "R"
            self.rating_id = 3
            self.rating_desc = "18+ (Violence and Profanity)"
        elif rating == "r+":
            self.human_rating = "M"
            self.rating_id = 4
            self.rating_desc = "18+ (Violence and Mild Nudity)"
        elif rating == "rx":
            self.human_rating = "AO"
            self.rating_id = 5
            self.rating_desc = "Adults Only"
        else:
            self.human_rating = "Unknown"
            self.rating_id = 6
            self.rating_desc = "No rating was provided"


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

class AnimeAltTitles(object):
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

class AnimeGenre(object):
    def __init__(self, id, genre):
        self.id = id
        self.name = genre

class AnimeGenres(object):
    def __init__(self):
        self.genres = []

    def add(self,genre: AnimeGenre):
        self.genres.append(genre)

    def delgenre(self, name: str):
        i = 0
        for z in self.genres:
            if z.name == name:
                self.genres.pop(i)
                break
            i = i + 1


class AnimeFields(object):
    def __init__(self, id:int = None, title: str = None, main_picture=None, alternative_titles=None, start_date=None, end_date=None, synopsis=None, mean=None, rank=None, popularity=None, num_list_users=None,
    num_scoring_users=None, nsfw=None, genres: AnimeGenres = None, created_at=None, updated_at=None, media_type=None, status=None, num_episodes=None, start_season=None, broadcast=None, source=None, average_episode_duration=None,
    rating=None, studios=None, paging=None):
        self.id: int = id
        self.title: str = title
        self.main_picture = main_picture
        self.alternative_titles = alternative_titles
        self.start_date = start_date
        self.end_date = end_date
        self.synopsis = synopsis
        self.mean = mean
        self.rank = rank
        self.popularity = popularity
        self.num_list_users: int = num_list_users
        self.num_scoring_users: int = num_scoring_users
        self.nsfw: AnimeNsfw = nsfw
        self.genres = genres
        self.created_at: str = created_at
        self.updated_at: str = updated_at
        self.media_type = media_type
        self.status: AnimeStatus = status
        self.num_episodes: int = num_episodes
        self.start_season: AnimeSeason = start_season
        self.broadcast: AnimeBroadcast = broadcast
        self.source = source
        self.average_episode_duration = average_episode_duration
        self.rating: AnimeRating = rating
        self.studios = studios
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

    def set_num_episodes(self, val = None):
        self.num_episodes = val
        return True

    def set_start_season(self, val = None):
        self.start_season = val
        return True

    def set_broadcast(self, val = None):
        self.broadcast = val
        return True

    def set_source(self, val = None):
        self.source = val
        return True

    # note this is measured in seconds
    def set_average_episode_duration(self, val = None):
        self.set_average_episode_duration = val

    def set_rating(self, val = None):
        self.rating = val

    def set_studios(self, val = None):
        self.studios = val

    def set_paging(self, val = None):
        self.paging = val