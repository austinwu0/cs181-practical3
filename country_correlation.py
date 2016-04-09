# -*- coding: utf-8 -*-
"""
Created on Sat Apr 09 15:58:03 2016

@author: Vincent Lan
"""

import pandas as pd
import numpy as np
import pickle
import datetime
print datetime.datetime.now()


user_artist_plays=pickle.load(open( "user_artist_plays.pkl", "rb" ) )
user_medians=pickle.load(open( "user_medians.pkl", "rb" ) )
user_dic=pickle.load(open( "user.pkl", "rb" ) )
artist_dic=pickle.load(open( "artist.pkl", "rb" ) )


user_size=len(user_dic)
artist_size=len(artist_dic)
print(user_size)
print(artist_size)
print(len(user_artist_plays))
print(len(user_medians))
print(len(user_artist_plays))

profiles=pd.read_csv('profiles.csv', index_col=0, parse_dates=True)

country_musician_play={}

for user in list(profiles.index):
    country=str(profiles.loc[user]["country"])
    no_musician=len(user_artist_plays[user])
    for i in range(no_musician):
        country_musician=country+str(user_artist_plays[user][i][0])
        play=user_artist_plays[user][i][1]/user_medians[user]
        if country_musician in country_musician_play:
            country_musician_play[country_musician].append(play)
        else:
            country_musician_play[country_musician]=[play]
            
import csv

train_file = 'train.csv'
test_file  = 'test.csv'
soln_file  = 'pred.csv'

with open(test_file, 'r') as test_fh:
    test_csv = csv.reader(test_fh, delimiter=',', quotechar='"')
    next(test_csv, None)

    with open(soln_file, 'w') as soln_fh:
        soln_csv = csv.writer(soln_fh,
                              delimiter=',',
                              quotechar='"',
                              quoting=csv.QUOTE_MINIMAL)
        soln_csv.writerow(['Id', 'plays'])
        
        for row in test_csv:
                count+=1
                id     = row[0]
                user   = row[1]
                musician = row[2]
            
                country_musician=str(profiles.loc[user]["country"])+musician
                if country_musician in country_musician_play:
                    if len(country_musician_play[country_musician])>5:
                        median_play=np.median(country_musician_play[country_musician])
                        if median_play>1.15:
                            soln_csv.writerow([id, user_medians[user]*median_play])
                        if median_play<0.85:
                            soln_csv.writerow([id, user_medians[user]*median_play])
                elif user in user_medians:
                    soln_csv.writerow([id, user_medians[user]])
                else:
                    print "User", id, "not in training data."
                    soln_csv.writerow([id, global_median])