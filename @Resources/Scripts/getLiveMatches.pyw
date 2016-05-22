#Used to log errors to a text file
# import sys
# sys.stderr = open("errlog.txt", "w")

#Imports some libraries for html parsing
import requests
from bs4 import BeautifulSoup

#Imports a datetime libary to get the current date time
from datetime import datetime, timedelta, timezone
#Imports extra library that gets local time zone
from tzlocal import get_localzone

import sys
import os

def get_current_GosuGamer_matches(game):
    print("Loading matches...")

    #Gets the websites html to parse
    r = requests.get("http://www.gosugamers.net/" + game + "/gosubet")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    #Finds the table that lists the matches
    box = soup.findAll("div", class_ = "box")[0]
    table = box.find("table", class_ = "simple matches")
    if (table != None):
        #Finds the elements within the table
        elements = table.findAll("tr")
    else:
        print("No live matches")
        elements = []

    #Creates a list of matches to return
    matches = []

    #Iterates through the table elements for matches
    for element in elements:
        match = []

        #Gets the html for the page dedicated to the match
        site = "http://www.gosugamers.net" + element.a["href"]
        r = requests.get(site)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        
        #Gets the team names from an element in the table
        team1 = soup.find("div", class_ = "opponent opponent1").find("h3").text
        team2 = soup.find("div", class_ = "opponent opponent2").find("h3").text
        summary = team1 + " Vs. " + team2

        #Adds the match to the list of matches
        match.append(summary)

        #Gets live link for the matches twitch stream
        liveLink = soup.find("textarea", id = "stream-media0")

        if (liveLink != None):
            #Adds the match link to the list of matches
            match.append(liveLink.iframe.attrs["src"])
        else:
            print("No stream link was found for the match " + summary)
            match.append(site)

        #Adds the match info to the full list
        matches.append(match)

    #Returns a list of all the matches on the GosuGamer website
    return matches

game = str(sys.argv[1])

#Gets the live matches frome the gosugamer website
liveMatches = get_current_GosuGamer_matches(game)

#Finds the path to the resource directory from the path of the script
path = os.path.dirname(os.path.realpath(__file__))
path = path.split("\\")
path = path[0:len(path) - 1]
filePath = ""
for directory in path:
    filePath = filePath + directory + "\\"
filePath = filePath + "Match Lists\\" + game + "\\"

# lastFile = open(filePath + "storedLive.txt", "r")
# storedMatches = []
# data = []
# for line in lastFile:
#     data.append(line)
# for i in range(0, len(data), 2):
#     if (i + 1 < len(data)):
#         storedMatches.append([data[i].replace("\n", ""), data[i + 1].replace("\n", "")])

#Opens the file for writing
file = open(filePath + "live.txt", "w")

#Writes variable header and live match number
#file.write("[Variables]\n")
#file.write("numLiveMatches = " + str(len(liveMatches)) + "\n")
file.write(str(len(liveMatches)) + "\n")

# storeFile = open(filePath + "storedLive.txt", "w")
#Iterates through and adds first three live matches and writes them to the files
for i in range(0, 3):
    if (i < len(liveMatches)):
        match = liveMatches[i]
    else:
        match = ["", ""]

    # if (i < len(storedMatches)):
    #     storedMatch = storedMatches[i]
    # else:
    #     storedMatch = ["", ""]

    #line = "liveMatchLink" + str(i + 1) + " = " + match[1] + "\n"
    line = match[1] + "\n"
    file.write(line)

    #line = "liveMatch" + str(i + 1) + " = " + match[0] + "\n"
    line = match[0] + "\n"
    file.write(line)

    # if (storedMatch[0] != match[0]):
    #     file.write("1\n")
    # elif (match[0] != ""):
    #     file.write("0\n")

    # for matchItem in match:
    #     storeFile.write(matchItem + "\n")


#Would include more than the assinged 3 matches
#Currently only 3 matches are avaliable for display
# for i in range(3, len(liveMatches)):
#     match = liveMatches[i]
#     line = "liveMatch" + str(i + 1) + " = " + match + "\n"
#     file.write(line)