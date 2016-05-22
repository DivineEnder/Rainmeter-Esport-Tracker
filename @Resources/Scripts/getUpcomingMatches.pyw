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
#Imports os library for path parsing
import os

#Reads and adds all upcoming dota matches from GosuGamers website
def get_GosuGamer_matches(game, numMatches):
    print("Loading matches...")

    #Gets the websites html to parse
    r = requests.get("http://www.gosugamers.net/" + game + "/gosubet")

    updateTime = datetime.now()
    print(updateTime)

    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    #Finds the table that lists the matches
    box = soup.findAll("div", class_ = "box")[1]
    table = box.find("table", class_ = "simple matches")
    #Finds the elements within the table
    elements = table.findAll("tr")

    #Creates a list of matches to return
    matches = []

    if (numMatches == -1 or numMatches > len(elements)):
        numMatches = len(elements)

    #Iterates through the table elements for matches (stops at certain number because only certain number are displayed)
    for i in range(0, numMatches):

        #Local variable to hold currently being iterated across item in the table
        element = elements[i]

        #Creates a match list [teams][league][dateTime][endDateTime]
        match = []

        #Gets the html for the page dedicated to the match
        site = "http://www.gosugamers.net" + element.a["href"]
        r = requests.get(site)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")

        #Saves the website link for this match
        match.append(site)
        
        #Gets the team names from an element in the table
        team1 = soup.find("div", class_ = "opponent opponent1").find("h3").text
        team2 = soup.find("div", class_ = "opponent opponent2").find("h3").text
        # team1 = element.find("span", class_ = "opp opp1").text.replace("\n", "")
        # team2 = element.find("span", class_ = "opp opp2").text.replace("\n", "")
        summary = team1 + " Vs. " + team2

        #Adds the teams to the match
        match.append(summary)
        
        #Gets the league that the match is being played in to add at end of summary
        heading = soup.find("div", class_ = "match-heading-overlay")
        league = heading.a.text

        #Adds the league to the match
        match.append(league)
        
        #Gets the date and time of the match
        date = soup.find("p", class_ = "datetime is-upcomming")
        date = date.text.replace("CEST", "+0200").replace("\n", "").replace(" ", "")

        #Gets the year of the match
        year = soup.find("label", class_ = "stage-name").text.replace(" ", "")
        year = year[len(year) - 4:len(year)]
        date = date + " " + year

        #Parses the date time from the text on the website
        date = datetime.strptime(date, "%B%d,%A,%H:%M%z %Y")
        #Converts to the local time zone
        date = date.astimezone(get_localzone())
        #Converts the datetime object to a string formated for google calendar
        dateTime = date.strftime("%Y-%m-%dT%H:%M:%S%z")

        # #Time to match from match list instead of match page
        # dateTime = element.find("span", class_ = "live-in").text.replace(" ", "").replace("\n", "")

        # #Adds space between the times (2h3m -> 2h 3m) (nice formating of time to match)
        # indicies = {dateTimeStr.find("w"):"w", dateTimeStr.find("d"):"d", dateTimeStr.find("h"):"h", dateTimeStr.find("m"):"m"}
        # for key in indicies:
        #     if (key != -1):
        #         dateTime = dateTime[0:key + 1] + " " + dateTime[key + 1:len(dateTime)])
        #         break

        #Adds the formated dateTime to the match
        match.append(dateTime)

        #Adds the match to the list of matches
        matches.append(match)

    matches.append(len(elements))
    #Returns a list of all the matches on the GosuGamer website
    return matches

game = str(sys.argv[1])
maxMatches = int(sys.argv[2])

#Gets upcoming matches
upcomingMatches = get_GosuGamer_matches(game, maxMatches)

#Finds the path to the resource directory from the path of the script
path = os.path.dirname(os.path.realpath(__file__))
path = path.split("\\")
path = path[0:len(path) - 1]
filePath = ""
for directory in path:
    filePath = filePath + directory + "\\"
filePath = filePath + "Match Lists\\" + game + "\\"

#Opens file for writing
file = open(filePath + "upcoming.txt", "w")
#Writes variable header in file for Rainmeter
#file.write("[Variables]\n")

#file.write("numUpcomingMatches = " + str(len(upcomingMatches)) + "\n")
file.write(str(upcomingMatches[len(upcomingMatches) - 1]) + "\n")

#Iterates through and writes matches to file
for i in range(0, maxMatches):
    if (i >= len(upcomingMatches) - 1):
        file.write("\n\n\n")
    else:
        match = upcomingMatches[i]
        date = datetime.strptime(match[3], "%Y-%m-%dT%H:%M:%S%z")
        now = datetime.now(get_localzone())
        diffDays = (date - now).days
        diffHours = date.hour - now.hour
        diffMinutes = date.minute - now.minute
        strDays = str(diffDays)
        if (diffMinutes < 0):
            diffMinutes = diffMinutes + 60
            diffHours = diffHours - 1
        if (diffHours < 0):
            diffHours = diffHours + 24
        strHours = str(diffHours)
        strMinutes = str(diffMinutes)
        #line = "Match" + str(i + 1) + " = " + match[1] + "\n"
        line = match[1] + "\n"
        file.write(line)
        
        #line = "TimeToMatch" + str(i + 1) + " = "
        line = ""
        if (diffDays > 0):
            if (diffDays > 1):
                line = line + strDays + " days "
            else:
                line = line + strDays + " day"
        if (diffHours > 0):
            line = line + strHours + "h "
        if (diffMinutes > 0):
            line = line + strMinutes + "m"
        line = line + "\n"
        # line = match[2] + "\n"
        file.write(line)

        #line = "TimeOfMatch" + str(i + 1) + " = "
        line = date.strftime("%I:%M %p") + "\n"#"%b %d, %H:%M") + "\n"
        file.write(line)

        #line = "matchLink" + str(i + 1) + " = " + match[0] + "\n"
        line = match[0] + "\n"
        file.write(line)