import pathlib
import os
import time

aquanox_basepath = "C:/Games/AquaNox 2 Revelation/Aquanox-2-Dialog-Editor"#Attention windows path but used/ instead of \
locale = "de"
export_basepath = "C:/Games/AquaNox 2 Revelation/Aquanox-2-Dialog-Editor/export"

class Mood_List:
	filepath_des = pathlib.Path(aquanox_basepath, "dat/sty/mood.des")
	table = {}

	def Export(self):
		currenttimepath = time.strftime("%Y-%m-%d-%H-%M")
		outputpath_des = pathlib.Path(export_basepath, currenttimepath, "dat/sty/mood.des")

		outputpath_des.parent.mkdir(exist_ok=True, parents=True)

		output_des = "[Table]\n"
		output_des += "{\n"
		output_des += "\n"

		for entry in self.table.keys():
			char = self.table[entry]
			output_des += f"    [{entry}]\n"
			output_des += "    {\n"
			if char.Comment_des != "NO .DES COMMENT":
				output_des += f"        //{char.Comment_des}\n"
			output_des += f'        Key = {char.Key}\n'
			output_des += "    }\n"
			output_des += "\n"
		output_des += "}\n"
		#print(output_des)
		outputpath_des.write_text(output_des, encoding = 'cp1252')

class Mood:
	Key = -1
	Comment_des = "NO .DES COMMENT"

	def Print(self):
		print(f"Key: {self.Key}")
		print(f"Comment_des: {self.Comment_des}")

def ParseMoods(listobj):
	if hasattr(listobj, "filepath_des"):
		file_des = open(listobj.filepath_des, 'r')

	Lines = file_des.readlines()
	readstate = "TableStart"
	tempchar = Mood()
	entryname = ""
	for line in Lines:
		line = line.lstrip()
		line = line.rstrip()
		if len(line) == 0: #Empty Line
			continue
		if readstate == "TableStart":#Search for [Table]
			if "[Table]" in line:
				readstate = "TableOpen"
				continue
		if readstate == "TableOpen":#Search for { after [Table]
			if line == "{":
				readstate = "SearchTableEntry"
				continue
		if readstate == "SearchTableEntry":#Search for [
			if line[0] == "[":
				line = line.split("[")[1]
				line = line.split("]")[0]
				entryname = line
				readstate = "TableEntryOpen"
				continue
		if readstate == "SearchTableEntry":#Search for last }
			if line[0] == "}":
				readstate = "TableClosed"
				break#End
		if readstate == "TableEntryOpen":
			if line == "{":
				readstate = "TableEntryData"
				continue
		if readstate == "TableEntryData":
			if "//" in line:
				tempchar.Comment_des = line.split("/")[2]
			if "Key = " in line:
				tempchar.Key = line.split(" ")[2]
			if line == "}":
				listobj.table[entryname] = tempchar
				tempchar = Character()
				entryname = ""
				readstate = "SearchTableEntry"
				continue

	if entryname != "":
		print("Current TableEntry was not closed")
		exit()
	if readstate != "TableClosed":
		print("Search did not find closing bracket")
		exit()
	file_des.close()

class Ship_List:
	filepath_loc = pathlib.Path(aquanox_basepath, "dat/sty/", locale, "ship.loc")

	table = {}

	def Export(self):
		currenttimepath = time.strftime("%Y-%m-%d-%H-%M")
		outputpath_loc = pathlib.Path(export_basepath, currenttimepath, "dat/sty/", locale, "ship.loc")

		outputpath_loc.parent.mkdir(exist_ok=True, parents=True)

		output_loc = "[Table]\n"
		output_loc += "{\n"
		output_loc += "\n"

		for entry in self.table.keys():
			char = self.table[entry]
			output_loc += f"    [{entry}]\n"
			output_loc += "    {\n"
			if char.Comment_loc != "NO .LOC COMMENT":
				output_loc += f"        //{char.Comment_loc}\n"
			output_loc += f'        Key = {char.Key}\n'
			output_loc += f'        Name = "{char.Name}"\n'
			output_loc += f'        RewardName = "{char.RewardName}"\n'
			output_loc += f'        ShortDescription = "{char.ShortDescription}"\n'
			output_loc += f'        Info = "{char.Info}"\n'
			output_loc += "    }\n"
			output_loc += "\n"
		output_loc += "}\n"
		#print(output_loc)
		outputpath_loc.write_text(output_loc, encoding = 'cp1252')

class Ship:
	Key = -1
	Name = "-1"
	RewardName = "-1"
	ShortDescription = "-1"
	Info = "-1"
	Comment_loc = "NO .LOC COMMENT"

	def Print(self):
		print(f"Key: {self.Key}")
		print(f"Name: {self.Name}")
		print(f"RewardName: {self.RewardName}")
		print(f"ShortDescription: {self.ShortDescription}")
		print(f"Info: {self.Info}")
		print(f"Comment_des: {self.Comment_des}")

def ParseShips(listobj):
	if hasattr(listobj, "filepath_loc"):
		file_loc = open(listobj.filepath_loc, 'r')

	Lines = file_loc.readlines()
	readstate = "TableStart"
	tempchar = Ship()
	entryname = ""
	for line in Lines:
		line = line.lstrip()
		line = line.rstrip()
		if len(line) == 0: #Empty Line
			continue
		if readstate == "TableStart":#Search for [Table]
			if "[Table]" in line:
				readstate = "TableOpen"
				continue
		if readstate == "TableOpen":#Search for { after [Table]
			if line == "{":
				readstate = "SearchTableEntry"
				continue
		if readstate == "SearchTableEntry":#Search for [
			if line[0] == "[":
				line = line.split("[")[1]
				line = line.split("]")[0]
				entryname = line
				readstate = "TableEntryOpen"
				continue
		if readstate == "SearchTableEntry":#Search for last }
			if line[0] == "}":
				readstate = "TableClosed"
				break#End
		if readstate == "TableEntryOpen":
			if line == "{":
				readstate = "TableEntryData"
				continue
		if readstate == "TableEntryData":
			if "//" in line:
				tempchar.Comment_des = line.split("/")[2]
			if "Key = " in line:
				tempchar.Key = line.split(" ")[2]
			if "Name = " in line and "RewardName = " not in line:
				tempchar.Name = line.split("\"")[1]
			if "RewardName = " in line:
				tempchar.RewardName = line.split("\"")[1]
			if "ShortDescription = " in line:
				tempchar.ShortDescription = line.split("\"")[1]
			if "Info = " in line:
				tempchar.Info = line.split("\"")[1]
			if line == "}":
				listobj.table[entryname] = tempchar
				tempchar = Character()
				entryname = ""
				readstate = "SearchTableEntry"
				continue

	if entryname != "":
		print("Current TableEntry was not closed")
		exit()
	if readstate != "TableClosed":
		print("Search did not find closing bracket")
		exit()
	file_loc.close()

class Room_List:
	filepath_des = pathlib.Path(aquanox_basepath, "dat/sty/room.des")
	table = {}

	def Export(self):
		currenttimepath = time.strftime("%Y-%m-%d-%H-%M")
		outputpath_des = pathlib.Path(export_basepath, currenttimepath, "dat/sty/room.des")

		outputpath_des.parent.mkdir(exist_ok=True, parents=True)

		output_des = "[Table]\n"
		output_des += "{\n"
		output_des += "\n"

		for entry in self.table.keys():
			char = self.table[entry]
			output_des += f"    [{entry}]\n"
			output_des += "    {\n"
			if char.Comment_des != "NO .DES COMMENT":
				output_des += f"        //{char.Comment_des}\n"
			output_des += f'        Key = {char.Key}\n'
			output_des += f'        Station = {char.Station}\n'
			output_des += f'        Sound = "{char.Sound}"\n'
			output_des += "    }\n"
			output_des += "\n"
		output_des += "}\n"
		#print(output_des)
		outputpath_des.write_text(output_des, encoding = 'cp1252')

class Room:
	Key = -1
	Station = -1
	Sound = "-1"
	Comment_des = "NO .DES COMMENT"

	def Print(self):
		print(f"Key: {self.Key}")
		print(f"Station: {self.Station}")
		print(f"Sound: {self.Sound}")
		print(f"Comment_des: {self.Comment_des}")

def ParseRooms(listobj):
	if hasattr(listobj, "filepath_des"):
		file_des = open(listobj.filepath_des, 'r')

	Lines = file_des.readlines()
	readstate = "TableStart"
	tempchar = Room()
	entryname = ""
	for line in Lines:
		line = line.lstrip()
		line = line.rstrip()
		if len(line) == 0: #Empty Line
			continue
		if readstate == "TableStart":#Search for [Table]
			if "[Table]" in line:
				readstate = "TableOpen"
				continue
		if readstate == "TableOpen":#Search for { after [Table]
			if line == "{":
				readstate = "SearchTableEntry"
				continue
		if readstate == "SearchTableEntry":#Search for [
			if line[0] == "[":
				line = line.split("[")[1]
				line = line.split("]")[0]
				entryname = line
				readstate = "TableEntryOpen"
				continue
		if readstate == "SearchTableEntry":#Search for last }
			if line[0] == "}":
				readstate = "TableClosed"
				break#End
		if readstate == "TableEntryOpen":
			if line == "{":
				readstate = "TableEntryData"
				continue
		if readstate == "TableEntryData":
			if "//" in line:
				tempchar.Comment_des = line.split("/")[2]
			if "Key = " in line:
				tempchar.Key = line.split(" ")[2]
			if "Station = " in line:
				tempchar.Station = line.split(" ")[2]
			if "Sound = " in line:
				tempchar.Sound = line.split("\"")[1]
			if line == "}":
				listobj.table[entryname] = tempchar
				tempchar = Character()
				entryname = ""
				readstate = "SearchTableEntry"
				continue

	if entryname != "":
		print("Current TableEntry was not closed")
		exit()
	if readstate != "TableClosed":
		print("Search did not find closing bracket")
		exit()
	file_des.close()

class Character_List:
	filepath_des = pathlib.Path(aquanox_basepath, "dat/sty/person.des")
	filepath_loc = pathlib.Path(aquanox_basepath, "dat/sty/", locale, "person.loc")
	table = {}

	def Export(self):
		currenttimepath = time.strftime("%Y-%m-%d-%H-%M")
		outputpath_des = pathlib.Path(export_basepath, currenttimepath, "dat/sty/person.des")
		outputpath_loc = pathlib.Path(export_basepath, currenttimepath, "dat/sty/", locale, "person.loc")

		outputpath_des.parent.mkdir(exist_ok=True, parents=True)

		output_des = "[Table]\n"
		output_des += "{\n"
		output_des += "\n"

		for entry in self.table.keys():
			char = self.table[entry]
			output_des += f"    [{entry}]\n"
			output_des += "    {\n"
			if char.Comment_des != "NO .DES COMMENT":
				output_des += f"        //{char.Comment_des}\n"
			output_des += f'        Key = {char.Key}\n'
			output_des += f'        ImageElf = "{char.ImageElf}"\n'
			output_des += f'        ImageMood0 = "{char.ImageMood0}"\n'
			output_des += f'        Sex = "{char.Sex}"\n'
			output_des += "    }\n"
			output_des += "\n"
		output_des += "}\n"
		#print(output_des)
		outputpath_des.write_text(output_des, encoding = 'cp1252')

		outputpath_loc.parent.mkdir(exist_ok=True, parents=True)

		output_loc = "[Table]\n"
		output_loc += "{\n"
		output_loc += "\n"

		for entry in self.table.keys():
			char = self.table[entry]
			output_loc += f"    [{entry}]\n"
			output_loc += "    {\n"
			if char.Comment_loc != "NO .LOC COMMENT":
				output_loc += f"        //{char.Comment_des}\n"
			output_loc += f'        Key = {char.Key}\n'
			output_loc += f'        Name = "{char.Name}"\n'
			output_loc += f'        ShortName = "{char.ShortName}"\n'
			output_loc += "    }\n"
			output_loc += "\n"
		output_loc += "}\n"
		#print(output_loc)
		outputpath_loc.write_text(output_loc, encoding = 'cp1252')


class Character:
	Key = -1
	ImageElf = "-1"
	ImageElfPath = "-1"
	ImageMood0 = "-1"
	ImageMood0Path = "-1"
	Sex = "-1"
	Name = "-1"
	ShortName = "-1"
	Comment_des = "NO .DES COMMENT"
	Comment_loc = "NO .LOC COMMENT"

	#subpath = ""

	def Print(self):
		print(f"Key: {self.Key}")
		print(f"ImageElf: {self.ImageElf}")
		print(f"ImageElfPath: {self.ImageElfPath}")
		print(f"ImageMood0: {self.ImageMood0}")
		print(f"ImageMood0Path: {self.ImageMood0Path}")
		print(f"Sex: {self.Sex}")
		print(f"Name: {self.Name}")
		print(f"ShortName: {self.ShortName}")
		print(f"Comment_des: {self.Comment_des}")
		print(f"Comment_loc: {self.Comment_loc}")

def ParseCharacters(listobj):
	if hasattr(listobj, "filepath_des") and hasattr(listobj, "filepath_loc"):
		file_des = open(listobj.filepath_des, 'r')
		file_loc = open(listobj.filepath_loc, 'r')

	Lines = file_des.readlines()
	readstate = "TableStart"
	tempchar = Character()
	entryname = ""
	for line in Lines:
		line = line.lstrip()
		line = line.rstrip()
		if len(line) == 0: #Empty Line
			continue
		if readstate == "TableStart":#Search for [Table]
			if "[Table]" in line:
				readstate = "TableOpen"
				continue
		if readstate == "TableOpen":#Search for { after [Table]
			if line == "{":
				readstate = "SearchTableEntry"
				continue
		if readstate == "SearchTableEntry":#Search for [
			if line[0] == "[":
				line = line.split("[")[1]
				line = line.split("]")[0]
				entryname = line
				readstate = "TableEntryOpen"
				continue
		if readstate == "SearchTableEntry":#Search for last }
			if line[0] == "}":
				readstate = "TableClosed"
				break#End
		if readstate == "TableEntryOpen":
			if line == "{":
				readstate = "TableEntryData"
				continue
		if readstate == "TableEntryData":
			if "//" in line:
				tempchar.Comment_des = line.split("/")[2]
			if "Key = " in line:
				tempchar.Key = line.split(" ")[2]
			if "ImageElf = " in line:
				tempchar.ImageElf = line.split("\"")[1]
				if len(line.split("\"")[1]) > 0:
					tempchar.ImageElfPath = pathlib.Path(aquanox_basepath, line.split("\"")[1])
			if "ImageMood0 = " in line:
				tempchar.ImageMood0 = line.split("\"")[1]
				if len(line.split("\"")[1]) > 0:
					tempchar.ImageMood0Path = pathlib.Path(aquanox_basepath, line.split("\"")[1])
			if "Sex = " in line:
				tempchar.Sex = line.split("\"")[1]
			if line == "}":
				listobj.table[entryname] = tempchar
				tempchar = Character()
				entryname = ""
				readstate = "SearchTableEntry"
				continue

	if entryname != "":
		print("Current TableEntry was not closed")
		exit()
	if readstate != "TableClosed":
		print("Search did not find closing bracket")
		exit()
	file_des.close()

	Lines = file_loc.readlines()
	readstate = "TableStart"
	tempchar = Character()#Object will not be used
	entryname = ""
	tempcomment = ""
	for line in Lines:
		line = line.lstrip()
		line = line.rstrip()
		if len(line) == 0: #Empty Line
			continue
		if readstate == "TableStart":#Search for [Table]
			if "[Table]" in line:
				readstate = "TableOpen"
				continue
		if readstate == "TableOpen":#Search for { after [Table]
			if line == "{":
				readstate = "SearchTableEntry"
				continue
		if readstate == "SearchTableEntry":#Search for [
			if line[0] == "[":
				line = line.split("[")[1]
				line = line.split("]")[0]
				entryname = line
				tempchar = listobj.table[entryname]
				readstate = "TableEntryOpen"
				continue
		if readstate == "SearchTableEntry":#Search for last }
			if line[0] == "}":
				readstate = "TableClosed"
				break#End
		if readstate == "TableEntryOpen":
			if line == "{":
				readstate = "TableEntryData"
				continue
		if readstate == "TableEntryData":
			if "//" in line:
				if tempchar.Key == -1:
					tempcomment = line.split("/")[2]
				else:
					tempchar.Comment_loc = line.split("/")[2] #Needed if table number is not stable
			if "Key = " in line:
				key = line.split(" ")[2]
				if key != tempchar.Key:
					print("Key in Tablekey in .loc does not match Key in Tablekey in .des")
					print(tempchar)
					print(key)
					exit()
			if "Name = " in line:
				tempchar.Name = line.split("\"")[1]
			if "ShortName = " in line:
				tempchar.ShortName = line.split("\"")[1]
			if line == "}":
				#listobj.table[entryname] = tempchar # Not needed as the object is already in the list
				tempchar = Character()
				entryname = ""
				tempcomment = ""
				readstate = "SearchTableEntry"
				continue
	file_loc.close()
		

charlist = Character_List()

print(charlist.filepath_des)
print(charlist.filepath_loc)

ParseCharacters(charlist)
print(charlist.table.keys())
print(charlist.table)
for char in charlist.table.values():
	char.Print()
charlist.Export()

roomlist = Room_List()
ParseRooms(roomlist)
roomlist.Export()

shiplist = Ship_List()
ParseShips(shiplist)
shiplist.Export()

moodlist = Mood_List()
ParseMoods(moodlist)
moodlist.Export()