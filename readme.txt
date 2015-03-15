#############################################
#Author: Alex Ross                          #
#Date: 09/03/2015                           #
#Version 1.0                                #
#############################################

Python script to return player fixture history and season history from web service:
http://fantasy.premierleague.com/web/api/elements/10/

base url for player photos:
http://cdn.ismfg.net/static/plfpl/img/shirts/photos

FantasyFootball_tde.py generates 3 .TDE files for Tableau
1) fixture_history.tde - contains detailed information for every player performance in every match this season
2) fixtures.tde - contains information on upcoming fixtures for each player
3) season_history.tde - contains summary player information for previous seasons
