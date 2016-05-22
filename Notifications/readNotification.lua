function Initialize()

	filePath = SELF:GetOption("path")
	
end

function Update()

	file = io.open(filePath)
	if not file then
		print('Unable to open file at ' .. filePath)
		return
	end

 	--text = file:read("*all")

 	notification = {}
 	for line in file:lines() do
    	table.insert(notification, line);
 	end
	
	SKIN:Bang("!SetVariable", "notificationText", notification[1])
	SKIN:Bang("!SetVariable", "notificationCommand", notification[2])
	
end