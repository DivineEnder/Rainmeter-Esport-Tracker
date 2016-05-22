import sys

game = str(sys.argv[1])

settingsFile = open("settings.inc", "r")
settings = settingsFile.readlines()
for i in range(0, len(settings)):
	setting = settings[i]
	if (setting.find("Game = ") != -1):
		settings[i] = setting[0:len("Game = ")] + game + "\n"

with open("settings.inc", "w") as file:
	file.writelines(settings)


