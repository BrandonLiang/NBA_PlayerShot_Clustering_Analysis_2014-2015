# -*- coding: utf-8 -*-
import csv
#import requests
import json
from urllib2 import urlopen
import codecs
import urllib


url_fixed = "http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=2014-15&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=201935&PlusMinus=N&Position=&Rank=N&RookieYear=&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0"
# Mimic desktop-type firefox browser
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
NameToShotInfo = {}
PlayerIDToTeamName = {}
parameterList = []
AllPlayerID = []
FullPlayerIDList = []

urlPrefix = "http://stats.nba.com/stats/shotchartdetail?CFID=33&CFPARAMS=2014-15&ContextFilter=&ContextMeasure=FGA&DateFrom=&DateTo=&GameID=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID="
urlEnd = "&PlusMinus=N&Position=&Rank=N&RookieYear=&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&TeamID=0&VsConference=&VsDivision=&mode=Advanced&showDetails=0&showShots=1&showZones=0"

def retrieveShotInfo(url): # Retrieves the JSON object for each player from NBA.com/stats links
	#response = requests.get(url, headers=headers)
	result = urllib.urlopen(url)
	data = json.load(result.fp)
	return data['resultSets']

def retrieveParameters(url_fixed): # Retrieves the list of parameters for each of the player shot data (to write as the header for each resulting csv file)
	#response = requests.get(url_fixed, headers=headers)
	result = urllib.urlopen(url_fixed)
	data = json.load(result.fp)
	return data['resultSets'][0]['headers'][7:]

def processShotInfo(data): # Gets the data we want from each player's JSON object
	shotInfo = data[0]['rowSet']
	header = retrieveParameters(url_fixed) #other info (might be useful)

	# Retrieves basic information for each JSON object: player name, player ID, player team, and add the information to the formats we need later on (dictionary primarily)
	playerID = shotInfo[0][3]
	FullPlayerIDList.append(playerID)
	parameterList = data[0]['headers']
	playerName = shotInfo[0][4]
	teamName = shotInfo[0][6]
	teamID = shotInfo[0][5]
	PlayerIDToTeamName[playerID] = teamName

	#Only want infomation after index = 6
	parameterList = parameterList[7:]

	# The shot info list that stores all shot data for every single player
	shotInfoList = []
	for temp in shotInfo:
		shotInfoList.append(temp[7:]) # Add every single shot datum to the shotInfoList for this very player
	NameToShotInfo[playerName] = shotInfoList # Now associate this whole set of shot data to that specific player


def toCSV(playerID, NameToID, IDToName):
	# Specify where you want to write all your resulting csv files to
	title = "/Users/brandonliang/Desktop/*5. NBA Stats Data/2014-2015 Player Shots Data/Data/" + IDToName[playerID]+ "-" + str(playerID) + ".csv"
	playerName = IDToName[playerID] # Maps from player ID to player name
	allShots = NameToShotInfo[playerName] # Retrieve all relevant shot data for this specific player
	c = csv.writer(open(title, "wb"))
	c.writerow(retrieveParameters(url_fixed))
	for entry in allShots:
		c.writerow(entry)

def getPlayerID(): # This is a helper function that reads in the supplementary csv file that contains all ID's associated to each NBA player for 2014-2015 season -- "Player to PlayerID.csv"
	AllPlayerID = []
	NameToID = {}
	IDToName = {}
	ifile  = open("/Users/brandonliang/Desktop/*5. NBA Stats Data/2014-2015 Player Shots Data/Data/Player To PlayerID.csv", "rb")
	reader = csv.reader(ifile)
	for row in reader:
		AllPlayerID.append(row[1])
		NameToID[row[0]] = row[1]
		IDToName[row[1]] = row[0]
	return AllPlayerID, NameToID, IDToName


def main():

	# Here you put your desired players' ID's
	(AllPlayerID, NameToID, IDToName) = getPlayerID()
	#AllPlayerID = [101108]
	#AllPlayerID={201588}
	for ids in AllPlayerID:
		url_temp = urlPrefix + str(ids) + urlEnd
		print ids
		print retrieveShotInfo(url_temp)[0]['rowSet']
		if (len(retrieveShotInfo(url_temp)[0]['rowSet']) > 0):
			
			processShotInfo(retrieveShotInfo(url_temp))
			#IDToName = {1891:"Jason Terry",101108:"Chris Paul"}
			#IDToName = {201588:"George Hill"}
			toCSV(ids, NameToID, IDToName)


if __name__ == "__main__":
	main() 