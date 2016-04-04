import pandas as pd
import numpy as np
import requests
import time
import re
import json

import spotipy
import tweepy

from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from collections import defaultdict

def musicbrainz_scrape(ID) :
    musicbrainz = {}
    
    URL = "https://musicbrainz.org/artist/" + ID
    var = requests.get(URL)
    soup = BeautifulSoup(var.text, "html.parser")
    
    sidebar = soup.find_all("dd")
    for entry in sidebar :
        try :
            info_class = entry.get('class','')[0]
        except IndexError:
            info_class =  u"started"
        musicbrainz[info_class] = entry.get_text()
    
    try :
        musicbrainz[u'genres'] = soup.find("div", {"id": "sidebar-tags"}).text.replace("\n","").replace(" ","").replace("...","").split(",")
    except :
        pass
    
    try :
        musicbrainz[u'wikiurl'] = soup.find("li", {"class" : "wikipedia-favicon"}).find("a").get("href").replace("//","http://")
    except :
        pass 
    
    try :
        musicbrainz[u'rateurl'] = soup.find("li", {"class" : "rateyourmusic-favicon"}).find("a").get("href")
    except :
        pass
    
    try :
        musicbrainz[u'twitterurl'] = soup.find("li", {"class" : "twitter-favicon"}).find("a").get("href")
    except :
        pass
    
    try :
        musicbrainz[u'youtubeurl'] = soup.find("li", {"class" : "youtube-favicon"}).find("a").get("href").replace("//","http://")
    except :
        pass

    return musicbrainz

def musicbrainz_scrape2(ID) :
    var = requests.get('https://musicbrainz.org/artist/'+ID)
    soup = BeautifulSoup(var.text, "html.parser")

    album_type = []
    album_type_n = []

    disco = soup.find("form", {"action" : "https://musicbrainz.org/release_group/merge_queue"})
    for el in disco.findAll("h3") :
        album_type.append("n_" + str(el.get_text()).lower().replace(" ","_"))
    for el in disco.findAll("table") :
        album_type_n.append(len(el.find("tbody").findAll("a", {"title" : ""})))

    return dict(zip(album_type, album_type_n))

def spotify_api(artist_name) :
    spotify_tool = spotipy.Spotify()
    spotify = {}

    if pd.isnull(artist_name) == False :
        try :
            results = spotify_tool.search(q='artist:' + artist_name, type='artist')
        except :
            results = []
            
        if len(results) > 0 :
            if len(results['artists']['items']) != 0 :
                spotify['popularity'] = results['artists']['items'][0]['popularity']
                spotify['sp_followers'] = results['artists']['items'][0]['followers']['total']
    
    return spotify

def wiki_search(URL) :
    var = requests.get(URL)
    soup = BeautifulSoup(var.text, "html.parser")
    wiki = {}
    
    wiki['labels'] = [el.get_text() for el in soup.find("a", {"href" : "/wiki/Record_label"}).find_next().findAll("a")]
    if len(wiki['labels']) == 0 :
        wiki['labels'] = soup.find("a", {"href" : "/wiki/Record_label"}).find_next().get_text().replace(" ","").split(",")
    
    return wiki

def youtube_sub(URL) :
    var = requests.get(URL)
    soup = BeautifulSoup(var.text, "html.parser")
    youtube = {'youtube_subs' : int(soup.find("span", {"class" : "yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip"}).get_text().replace(",",""))}
    
    return youtube

def twitter_info(twitter_api, URL) :
    handle = URL.split("/")[-1]
    user = twitter_api.get_user(handle)
    twitter = {'ntweets' : user['statuses_count'], 'tw_followers' : user['followers_count']}
    return twitter

def findInt(string) :
    return [int(s) for s in string.split() if s.isdigit()]

def ratemusic_scrape(URL) :
    rate = {}
    var = requests.get(URL)
    soup = BeautifulSoup(var.text, "html.parser")
    
    for el in soup.find_all("div", {"class" : "disco_header_top"}) :
        rate["n_" + el.find("h3").get_text().strip().lower().replace(" ","_").replace("/","")] = findInt(el.find("span").get_text().strip().replace("(","").replace(")",""))[-1]
        
    return rate