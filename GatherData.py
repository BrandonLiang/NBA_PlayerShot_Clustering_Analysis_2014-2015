import csv
import os
from sets import Set

directory = "/Users/brandonliang/Desktop/*5. NBA Stats Data/2014-2015 Player Shots Data/Data"
newDirectory = "/Users/brandonliang/Desktop/*5. NBA Stats Data/2014-2015 Player Shots Data"
writingDirectory = "/Users/brandonliang/Desktop/*5. NBA Stats Data/2014-2015 Player Shots Data/Player Cluster Features 2014-2015.csv"
player = []
playerToID = {}
IDToPlayer = {}
avgData = {} #for leagues_NBA_2015_per_game_per_game.csv data
playerShotInfo = {}
def getAllData():
	for root,dirs,files in os.walk(directory):
		for file in files:
			os.chdir(directory)
			if file.endswith(".csv") and file != "leagues_NBA_2015_per_game_per_game.csv" and file != "Player To PlayerID.csv":
				filename = file.split('-')
				if (len(filename)==2): 
					playerName = filename[0]
					ids = filename[1][:-4]
					player.append(playerName)
				if (len(filename)>2): # If a player has "-" in his name
					playerName = filename[0]+"-"+filename[1]
					ids = filename[2][:-4]

				playerToID[playerName] = ids
				IDToPlayer[ids] = playerName
				player.append(playerName)
				ifile  = open(file, "rb")
				reader = csv.reader(ifile)
				tempPlayerInfo = []
				for row in reader:
					if (len(row)==14):
						temp = []
						time = row[0]+"-"+row[1]+":"+row[2]
						temp.append(time)
						temp.append(row[4])
						temp.append(row[5])
						temp.append(row[8])
						temp.append(row[9])
						temp.append(row[10])
						temp.append(row[11])
						temp.append(row[13]) # 1: shot made; 0: shot missed;
						tempPlayerInfo.append(temp)
				playerShotInfo[playerName] = tempPlayerInfo

			ifile = open("/Users/brandonliang/Desktop/*5. NBA Stats Data/2014-2015 Player Shots Data/Data/leagues_NBA_2015_per_game_per_game.csv","rb")
			reader = csv.reader(ifile)
			reader.next()
			for row in reader:
				if (row[0] != "Rk"):
					playerName = row[1]
					position = row[2]
					if (playerName not in avgData.keys()):
						gamesPlayed = int(row[5])
						minutesPlayedAvg = float(row[7])
						team = []
						if (row[4] != "'TOT'"):
							team.append(row[4])
						newValue = []
						newValue.append(gamesPlayed)
						newValue.append(minutesPlayedAvg)
						newValue.append(position)
						newValue.append(team)
						avgData[playerName] = newValue
					else:
						newValue = avgData[playerName]
						team = newValue[-1]
						del newValue[-1]
						team.append(row[4])
						newValue.append(team)
						avgData[playerName] = newValue
	return playerShotInfo, avgData

def cluster1(player, shotInfo, suppData): # For shooting style analysis
	tempEntry = []
	#print len(shotInfo),player
	del shotInfo[0]
	totalShots = len(shotInfo) # total number of rows is the total number of shots taken
	zone1 = 0
	zone2 = 0
	zone3 = 0
	#zone4 = 0
	gamesPlayed = suppData[0]
	minutesPlayedAvg = suppData[1]
	team = suppData[3]
	position = suppData[2]
	for row in shotInfo:
		distance = int(row[4])
		#locX = int(row[5])
		#locY = int(row[6])
		#made = int(row[7])
		if (distance <= 12):
			zone1 = zone1 +1
		if (12 < distance <= 24):
			zone2 = zone2 +1
		if (distance > 24):
			zone3 = zone3 +1
	playerString = player + " " + str(position)
	tempEntry.append(playerString)
	tempEntry.append(list(Set(team)))
	zone1P = zone1 * 1.0 / totalShots
	zone1P = float("{0:.4f}".format(zone1P))
	tempEntry.append(zone1P)
	zone2P = zone2 * 1.0 / totalShots
	zone2P = float("{0:.4f}".format(zone2P))
	tempEntry.append(zone2P)
	zone3P = zone3 * 1.0 / totalShots
	zone3P = float("{0:.4f}".format(zone3P))
	tempEntry.append(zone3P)
	#zone4P = zone4 * 1.0 / totalShots
	#zone4P = float("{0:.4f}".format(zone4P))
	#tempEntry.append(zone4P)
	totalP = totalShots*1.0/gamesPlayed/minutesPlayedAvg
	totalP = float("{0:4f}".format(totalP))
	tempEntry.append(totalP)
	tempEntry.append(minutesPlayedAvg)
	return tempEntry

def cluster2(player, shotInfo, suppData): # For shooting style + shot performance analysis
	tempEntry = []
	del shotInfo[0]
	totalShots = len(shotInfo) # total number of rows is the total number of shots taken
	zone1 = 0
	zone2 = 0
	zone3 = 0
	#zone4 = 0
	made1 = 0
	made2 = 0
	made3 = 0
	#made4 = 0
	gamesPlayed = suppData[0]
	minutesPlayedAvg = suppData[1]
	team = suppData[3]
	position = suppData[2]
	for row in shotInfo:
		distance = int(row[4])
		#locX = int(row[5])
		#locY = int(row[6])
		made = int(row[7])
		if (distance <= 12):
			zone1 = zone1 +1
			if (made==1):
				made1 = made1 +1
		if (12 < distance <= 24):
			zone2 = zone2 +1
			if (made==1):
				made2 = made2 + 1
		if (24 < distance):
			zone3 = zone3 +1
			if (made==1):
				made3 = made3 + 1
	playerString = player + " " + str(position)
	tempEntry.append(playerString)
	tempEntry.append(list(Set(team)))
	if (totalShots == 0):
		totalShots = 1
	zone1P = zone1 * 1.0 / totalShots
	zone1P = float("{0:.4f}".format(zone1P))
	tempEntry.append(zone1P)
	zone2P = zone2 * 1.0 / totalShots
	zone2P = float("{0:.4f}".format(zone2P))
	tempEntry.append(zone2P)
	zone3P = zone3 * 1.0 / totalShots
	zone3P = float("{0:.4f}".format(zone3P))
	tempEntry.append(zone3P)
	#zone4P = zone4 * 1.0 / totalShots
	#zone4P = float("{0:.4f}".format(zone4P))
	#tempEntry.append(zone4P)
	if (zone1 != 0):
		zone1FG = made1 * 1.0 / zone1
		zone1FG = float("{0:.4f}".format(zone1FG))
	else:
		zone1FG = 0
	tempEntry.append(zone1FG)
	if (zone2 != 0):
		zone2FG = made2 * 1.0 / zone2
		zone2FG = float("{0:.4f}".format(zone2FG))
	else:
		zone2FG = 0
	tempEntry.append(zone2FG)
	if (zone3 != 0):
		zone3FG = made3 * 1.0 / zone3
		zone3FG = float("{0:.4f}".format(zone3FG))
	else:
		zone3FG = 0
	tempEntry.append(zone3FG)
	"""
	if (zone4 != 0):
		zone4FG = made4 * 1.0 / zone4
		zone4FG = float("{0:.4f}".format(zone4FG))
	else:
		zone4FG = 0
	tempEntry.append(zone4FG)
	"""		
	totalMade = made1 + made2 + made3 #+ made4
	totalFG = totalMade * 1.0 / totalShots
	totalFG = float("{0:.4f}".format(totalFG))
	tempEntry.append(totalFG)
	totalP = totalShots*1.0/gamesPlayed/minutesPlayedAvg
	totalP = float("{0:4f}".format(totalP))
	tempEntry.append(totalP)
	FGPerMinute = totalMade * 1.0 / gamesPlayed / minutesPlayedAvg
	FGPerMinute = float("{0:.4f}".format(FGPerMinute))
	tempEntry.append(FGPerMinute)
	return tempEntry

def main():
	(playerShotInfo, avgData) = getAllData()

	# Heading column categories for the resulting csv files we will write

	# Only shooting style, we don't take shot performance/result into consideration
	header1 = ["Player","Team","0-12 Attempt%","12-24 Attempt%",">=24 Attempt%","Attempt/Minute","Minute/Game"]
	# For the second file, we are going to take into consideration the shot performance/result, aka shooting percentage broken down into each distance metric
	header2 = ["Player","Team","0-12 Attempt%","12-24 Attempt%",">=24 Attempt%","0-12 FG%","12-24 FG%",">=24 FG%","FG%","Attempt/Minute","FG Made/Minute"]
	resultEntry1 = []
	resultEntry2 = []
	result1PG = []
	result1SG = []
	result1SF = []
	result1PF = []
	result1C = []
	result2PG = []
	result2SG = []
	result2SF = []
	result2PF = []
	result2C = []
	for player in playerShotInfo.keys():
		if (player in avgData.keys()):
			shotInfo = playerShotInfo[player] # List of List of each shot features
			suppData = avgData[player] # Supplementary data of games played, minutes played and team list
			position = suppData[2]

			tempEntry1 = cluster1(player, shotInfo, suppData)
			tempEntry2 = cluster2(player, shotInfo, suppData)
			resultEntry1.append(tempEntry1)
			resultEntry2.append(tempEntry2)

			if (position == "1"):
				result1PG.append(tempEntry1)
				result2PG.append(tempEntry2)
			if (position == "2"):
				result1SG.append(tempEntry1)
				result2SG.append(tempEntry2)
			if (position == "3"):
				result1SF.append(tempEntry1)
				result2SF.append(tempEntry2)
			if (position == "4"):
				result1PF.append(tempEntry1)
				result2PF.append(tempEntry2)	
			if (position == "5"):
				result1C.append(tempEntry1)
				result2C.append(tempEntry2)			

	
	result1 = csv.writer(open(newDirectory+"/Shooting Style/Player Shooting Style Analysis.csv", "wb"))
	result1.writerow(header1)
	for tempEntry in resultEntry1:
		result1.writerow(tempEntry)

	
	result2 = csv.writer(open(newDirectory+"/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis.csv", "wb"))
	result2.writerow(header2)
	for tempEntry in resultEntry2:
		result2.writerow(tempEntry)
	
	result1PGG = csv.writer(open(newDirectory+"/Shooting Style/Player Shooting Style Analysis-PG.csv", "wb"))
	result1PGG.writerow(header1)
	for tempEntry in result1PG:
		result1PGG.writerow(tempEntry)

	
	result2PGG = csv.writer(open(newDirectory+"/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-PG.csv", "wb"))
	result2PGG.writerow(header2)
	for tempEntry in result2PG:
		result2PGG.writerow(tempEntry)

	result1SGG = csv.writer(open(newDirectory+"/Shooting Style/Player Shooting Style Analysis-SG.csv", "wb"))
	result1SGG.writerow(header1)
	for tempEntry in result1SG:
		result1SGG.writerow(tempEntry)

	
	result2SGG = csv.writer(open(newDirectory+"/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-SG.csv", "wb"))
	result2SGG.writerow(header2)
	for tempEntry in result2SG:
		result2SGG.writerow(tempEntry)	

	result1SFF = csv.writer(open(newDirectory+"/Shooting Style/Player Shooting Style Analysis-SF.csv", "wb"))
	result1SFF.writerow(header1)
	for tempEntry in result1SF:
		result1SFF.writerow(tempEntry)

	
	result2SFF = csv.writer(open(newDirectory+"/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-SF.csv", "wb"))
	result2SFF.writerow(header2)
	for tempEntry in result2SF:
		result2SFF.writerow(tempEntry)

	result1PFF = csv.writer(open(newDirectory+"/Shooting Style/Player Shooting Style Analysis-PF.csv", "wb"))
	result1PFF.writerow(header1)
	for tempEntry in result1PF:
		result1PFF.writerow(tempEntry)

	
	result2PFF = csv.writer(open(newDirectory+"/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-PF.csv", "wb"))
	result2PFF.writerow(header2)
	for tempEntry in result2PF:
		result2PFF.writerow(tempEntry)

	result1CC = csv.writer(open(newDirectory+"/Shooting Style/Player Shooting Style Analysis-C.csv", "wb"))
	result1CC.writerow(header1)
	for tempEntry in result1C:
		result1CC.writerow(tempEntry)

	
	result2CC = csv.writer(open(newDirectory+"/Shooting Style + Shot Performance/Player Shooting Style + Shot Performance Analysis-C.csv", "wb"))
	result2CC.writerow(header2)
	for tempEntry in result2C:
		result2CC.writerow(tempEntry)		

if __name__ == "__main__":
	main()
	allPlayer = Set(player)

