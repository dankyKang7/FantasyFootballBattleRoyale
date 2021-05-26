# -*- coding: utf-8 -*-
"""
Created on Sun May 23 14:56:03 2021

@author: travm
"""

#Goal of this script is the connect to the yahoo sports API
#This is to get historical fantasy data by week

import os
import requests as req
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import pandas as pd

os.chdir('C:/Blog_Data/FantasyFootball')
#Connect to API
authenticate = OAuth2(None,None, from_file="C:/Blog_Data/FantasyFootball/YahooData_API/apiParams.json")

#Reconnect if not true
if not authenticate.token_is_valid():
    authenticate.refresh_access_token()
    
#Find the leagues you're apart of
leagues = yfa.Game(authenticate,'nfl')


years = ['2015','2016','2017','2018','2019','2020']
LeagueID = [leagues.league_ids(x) for x in years]

yearLeag = [*zip(years,LeagueID)]

yearLeagDF = pd.DataFrame(yearLeag,columns=['year','leagues'])
yearLeagDF_1 = pd.DataFrame(yearLeagDF['leagues'].to_list(),index=yearLeagDF.index,columns=['league_1','league_2'])

#Join them together
years_leagues = yearLeagDF.merge(yearLeagDF_1,on=yearLeagDF.index).drop(\
                                                                        columns=['key_0','leagues'])

#League Name
#Create list of league ID's
leaglist = (years_leagues['league_1'].to_list()+years_leagues['league_2'].to_list())[:-2]

leagName = [yfa.league.League(authenticate,x).settings()['name']\
            for x in leaglist]
    
leagTeams = [yfa.league.League(authenticate,x).settings()['num_teams']\
            for x in leaglist]
leagURL = [yfa.league.League(authenticate,x).settings()['url']\
            for x in leaglist]
leagYear = [yfa.league.League(authenticate,x).settings()['season']\
            for x in leaglist]
    
leagMetaData = zip(leagYear,leagName,leagTeams,leagURL)

leagMetaDF = pd.DataFrame(leagMetaData,columns=['Year','Name','NumTeams','URL'])
