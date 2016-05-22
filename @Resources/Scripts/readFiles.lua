function Initialize()

	--Live file path for reading live matches into ticker
	liveFile = SELF:GetOption("livePath")
	--Upcoming file path for reading upcoming matches into ticker
	upcomingFile = SELF:GetOption("upcomingPath")
	--Notified live file path for determining whether a notification has already been sent
	notifiedFile = SELF:GetOption("notifiedPath")
	--Notification file for the notification message
	notificationFile = SELF:GetOption("notificationPath")

end

function Update()

	--Live reading file in order to read live matches into ticker
	--@Resources\Match Lists\dota2\live.txt
	liveReadingFile = io.open(liveFile)
	if not liveReadingFile then
		print('Unable to open file at ' .. liveFile)
		return
	end

	--Live match info array (starts at index 1 and includes teams, link, and number of matches total)
	--@Resources\Match Lists\dota2\live.txt
 	liveMatchInfo = {}
 	for line in liveReadingFile:lines() do
    	table.insert(liveMatchInfo, line);
 	end
	
	--Calls rainmeter bang to set variables in the skin for the ticker
	SKIN:Bang("!SetVariable", "numLiveMatches", liveMatchInfo[1])
	counter = 1
	for i=2,table.getn(liveMatchInfo),2 do
		SKIN:Bang("!SetVariable", "liveMatchLink" .. counter, liveMatchInfo[i])
		SKIN:Bang("!SetVariable", "liveMatch" .. counter, liveMatchInfo[i+1])
		counter = counter + 1
	end

	--Upcoming reading file in order to read upcoming matches into ticker
	--@Resources\Match Lists\dota2\upcoming.txt
	upcomingReadingFile = io.open(upcomingFile)
	if not upcomingReadingFile then
		print('Unable to open file at ' .. upcomingFile)
		return
	end

	--Upcoming match info array (starts at index 1 includes teams, link, time to match, time of match, and total number of matches)
 	--@Resources\Match Lists\dota2\upcoming.txt
 	upcomingMatchInfo = {}
 	for line in upcomingReadingFile:lines() do
    	table.insert(upcomingMatchInfo, line);
 	end

 	--Calls rainmeter bangs to set variables in the ticker so that the match info displays
 	SKIN:Bang("!SetVariable", "numUpcomingMatches", upcomingMatchInfo[1])
 	counter = 1
 	for i=2,table.getn(upcomingMatchInfo),4 do
 		SKIN:Bang("!SetVariable", "Match" .. counter, upcomingMatchInfo[i])
		SKIN:Bang("!SetVariable", "TimeToMatch" .. counter, upcomingMatchInfo[i+1])
		SKIN:Bang("!SetVariable", "TimeOfMatch" .. counter, upcomingMatchInfo[i+2])
		SKIN:Bang("!SetVariable", "matchLink" .. counter, upcomingMatchInfo[i+3])
		counter = counter + 1
 	end

	--Notified reading file for determining what notifications to send for live matches
	--@Resources\Match Lists\dota2\notifiedLive.txt
	notifiedReadingFile = io.open(notifiedFile)
	if not notifiedReadingFile then
		print('Unable to open file at ' .. notifiedFile)
		return
	end

	--Reads in line from notified file to determine which live matches have been notified
	--@Resources\Match Lists\dota2\notifiedLive.txt
 	notifiedMatches = {}
 	for line in notifiedReadingFile:lines() do
    	table.insert(notifiedMatches, line);
 	end

 	for i=2,table.getn(liveMatchInfo),2 do
 		--Opens the notified file first in write mode (to remove previous) and then in append mode after writing a match
 		if (i == 2) then
			notifiedWritingFile = io.open(notifiedFile, "w")
		else
			notifiedWritingFile = io.open(notifiedFile, "a")
		end
		--Writes the live match (and link) to the notified file for later reference
	 	io.output(notifiedWritingFile)
	 	io.write(liveMatchInfo[i] .. "\n")
	 	io.write(liveMatchInfo[i+1] .. "\n")
	 	io.close(notifiedWritingFile)

	 	--Checks to see whether a notification has already been sent for the live match
	 	if (notifiedMatches[i] == liveMatchInfo[i+1] or liveMatchInfo[i+1] == "" or liveMatchInfo[i+1] == nil) then
	 	else
	 		--Writes the match name and link to the notification file to display
	 		notificationWritingFile = io.open(notificationFile, "w")
	 		io.output(notificationWritingFile)
	 		io.write(liveMatchInfo[i+1] .. "\n")
	 		io.write(liveMatchInfo[i])
	 		io.close(notificationWritingFile)
	 		--Activates the notification which displays based upon the file written to above
	 		SKIN:Bang("!ActivateConfig MatchTicker\\Notifications Notification.ini") --"!ActivateConfig", SELF:GetOption("notificationPath"), "Notification.ini"
	 	end
 	end
 	
end