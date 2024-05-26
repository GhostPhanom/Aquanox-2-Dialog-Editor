import pathlib
import os
import time
import pygame

aquanox_basepath = "C:/Games/AquaNox 2 Revelation/Aquanox-2-Dialog-Editor"#Attention windows path but used/ instead of \
locale = "de"
export_basepath = "C:/Games/AquaNox 2 Revelation/Aquanox-2-Dialog-Editor/export"

class Sdialog_List:
	filepath_des = pathlib.Path(aquanox_basepath, "dat/sty/sdialog.des")
	table = {}

	def GetObjectwithKey(self, key: int):
		#print(f"ProvidedKey:{key}")
		for table_entry in self.table:
			if self.table[table_entry].Key == key:
				return self.table[table_entry]
		else:
			return Room()

	def Export(self):
		currenttimepath = time.strftime("%Y-%m-%d-%H-%M")
		outputpath_des = pathlib.Path(export_basepath, currenttimepath, "dat/sty/sdialog.des")

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
			output_des += f'        Type = "{char.Type}"\n'
			output_des += f'        Room = {char.Room}\n'
			output_des += "    }\n"
			output_des += "\n"
		output_des += "}\n"
		#print(output_des)
		outputpath_des.write_text(output_des, encoding = 'cp1252')

class Sdialog:
	Key = -1
	Type = "-1"
	Room = -1
	Comment_des = "NO .DES COMMENT"

	def Print(self):
		print(f"Key: {self.Key}")
		print(f"Type: {self.Type}")
		print(f"Room: {self.Room}")
		print(f"Comment_des: {self.Comment_des}")

def ParseSdialogs(listobj):
	if hasattr(listobj, "filepath_des"):
		file_des = open(listobj.filepath_des, 'r')

	Lines = file_des.readlines()
	readstate = "TableStart"
	tempchar = Sdialog()
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
				tempchar.Key = int(line.split(" ")[2])
			if "Type = " in line:
				tempchar.Type = line.split("\"")[1]
			if "Room = " in line:
				tempchar.Room = int(line.split(" ")[2])
			if line == "}":
				listobj.table[entryname] = tempchar
				tempchar = Sdialog()
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

class Stake_List:
	filepath_des = pathlib.Path(aquanox_basepath, "dat/sty/stake.des")
	filepath_loc = pathlib.Path(aquanox_basepath, "dat/sty/", locale, "stake.loc")
	table = {}
	last_key = -1

	def GetObjectwithKey(self, key: int):
		#print(f"ProvidedKey:{key}")
		for table_entry in self.table:
			if self.table[table_entry].Key == key:
				return self.table[table_entry]
		else:
			return Stake()

	def GetDialogeStakeEntrys(self, key: int):
		stake_list = []
		#print(f"ProvidedKey:{key}")
		for table_entry in self.table:
			if self.table[table_entry].Dialog == key:
				stake_list.append(self.table[table_entry])
		return stake_list

	def Export(self):
		currenttimepath = time.strftime("%Y-%m-%d-%H-%M")
		outputpath_des = pathlib.Path(export_basepath, currenttimepath, "dat/sty/stake.des")
		outputpath_loc = pathlib.Path(export_basepath, currenttimepath, "dat/sty/", locale, "stake.loc")

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
			output_des += f'        Dialog = {char.Dialog}\n'
			output_des += f'        Person = {char.Person}\n'
			output_des += f'        Wav = "{char.Wav}"\n'
			output_des += f'        Mood = {char.Mood}\n'
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
			output_loc += f'        Text = "{char.Text}"\n'
			output_loc += "    }\n"
			output_loc += "\n"
		output_loc += "}\n"
		#print(output_loc)
		outputpath_loc.write_text(output_loc, encoding = 'cp1252')

class Stake:
	Key = -1
	Dialog = -1
	Person = -1
	Wav = "-1"
	WavPath = "-1"
	Mood = -1
	Comment_des = "NO .DES COMMENT"
	Comment_loc = "NO .LOC COMMENT"

	def Print(self):
		print(f"Key: {self.Key}")
		print(f"Dialog: {self.Dialog}")
		print(f"Person: {self.Person}")
		print(f"Wav: {self.Wav}")
		print(f"WavPath: {self.WavPath}")
		print(f"Mood: {self.Mood}")
		print(f"Comment_des: {self.Comment_des}")
		print(f"Comment_loc: {self.Comment_loc}")

def ParseStakes(listobj):
	if hasattr(listobj, "filepath_des") and hasattr(listobj, "filepath_loc"):
		file_des = open(listobj.filepath_des, 'r')
		file_loc = open(listobj.filepath_loc, 'r')

	Lines = file_des.readlines()
	readstate = "TableStart"
	tempchar = Stake()
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
				tempchar.Key = int(line.split(" ")[2])
			if "Dialog = " in line:
				tempchar.Dialog = int(line.split(" ")[2])
			if "Person = " in line:
				tempchar.Person = int(line.split(" ")[2])
			if "Wav = " in line:
				tempchar.Wav = line.split("\"")[1]
				if len(line.split("\"")[1]) > 0:
					tempchar.WavPath = pathlib.Path(aquanox_basepath, "sfx/speech/", locale, line.split("\"")[1] + ".ogg")
			if "Mood = " in line:
				tempchar.Mood = int(line.split(" ")[2])
			if line == "}":
				listobj.table[entryname] = tempchar
				tempchar = Stake()
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
	tempchar = Stake()#Object will not be used
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
				key = int(line.split(" ")[2])
				if key != tempchar.Key:
					print("Key in Tablekey in .loc does not match Key in Tablekey in .des")
					print(tempchar)
					print(key)
					exit()
			if "Text = " in line:
				tempchar.Text = line.split("\"")[1]
			if line == "}":
				#listobj.table[entryname] = tempchar # Not needed as the object is already in the list
				tempchar = Stake()
				entryname = ""
				tempcomment = ""
				readstate = "SearchTableEntry"
				continue
	file_loc.close()

class Mood_List:
	filepath_des = pathlib.Path(aquanox_basepath, "dat/sty/mood.des")
	table = {}

	def GetObjectwithKey(self, key: int):
		#print(f"ProvidedKey:{key}")
		for table_entry in self.table:
			if self.table[table_entry].Key == key:
				return self.table[table_entry]
		else:
			return Mood()

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
				tempchar.Key = int(line.split(" ")[2])
			if line == "}":
				listobj.table[entryname] = tempchar
				tempchar = Mood()
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

	def GetObjectwithKey(self, key: int):
		#print(f"ProvidedKey:{key}")
		for table_entry in self.table:
			if self.table[table_entry].Key == key:
				return self.table[table_entry]
		else:
			return Ship()

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
				tempchar.Key = int(line.split(" ")[2])
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
				tempchar = Ship()
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

	def GetObjectwithKey(self, key: int):
		#print(f"ProvidedKey:{key}")
		for table_entry in self.table:
			if self.table[table_entry].Key == key:
				return self.table[table_entry]
		else:
			return Room()

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
	SoundPath = "-1"
	Comment_des = "NO .DES COMMENT"

	def Print(self):
		print(f"Key: {self.Key}")
		print(f"Station: {self.Station}")
		print(f"Sound: {self.Sound}")
		print(f"SoundPath: {self.SoundPath}")
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
				tempchar.Key = int(line.split(" ")[2])
			if "Station = " in line:
				tempchar.Station = int(line.split(" ")[2])
			if "Sound = " in line:
				tempchar.Sound = line.split("\"")[1]
				tempchar.SoundPath = pathlib.Path(aquanox_basepath, line.split("\"")[1][:-4] + ".wav")
			if line == "}":
				listobj.table[entryname] = tempchar
				tempchar = Room()
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

	def GetObjectwithKey(self, key: int):
		#print(f"ProvidedKey:{key}")
		for table_entry in self.table:
			if self.table[table_entry].Key == key:
				return self.table[table_entry]
		else:
			return Character()

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
				tempchar.Key = int(line.split(" ")[2])
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
				key = int(line.split(" ")[2])
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
		
def PlayDialogAudio(dialogid, background=True):
	stake_list = stakelist.GetDialogeStakeEntrys(dialogid)
	room = roomlist.GetObjectwithKey(sdialoglist.GetObjectwithKey(dialogid).Room)
	if len(stake_list) > 0:
		channel_bg = pygame.mixer.Channel(0)

		if background == True:
			channel_dialog = pygame.mixer.Channel(1)
			sound_bg = pygame.mixer.Sound(room.SoundPath)
			sound_bg.set_volume(basevolume_bg)
			channel_bg.play(sound_bg)

		for stake in stake_list:
			sound_stake = pygame.mixer.Sound(stake.WavPath)
			sound_stake.set_volume(basevolume_text)
			channel_dialog.play(sound_stake)
			while channel_dialog.get_busy() == True:
				if background == True and channel_bg.get_busy() == False:
					channel_bg.play(sound_bg)
				time.sleep(0.05)
			time.sleep(0.6)

		if background == True:
			channel_bg.stop()

	else:
		print("stake list empty, no sound played!")

basevolume_text = 10 / 100
basevolume_bg = basevolume_text / 5 * 2
pygame.mixer.init()#Initialize Sound


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

sdialoglist = Sdialog_List()
ParseSdialogs(sdialoglist)
sdialoglist.Export()

stakelist = Stake_List()
ParseStakes(stakelist)
stakelist.Export()
stakelist.GetObjectwithKey(17).Print()


for stake in stakelist.GetDialogeStakeEntrys(18):
	print(f"{charlist.GetObjectwithKey(stake.Person).Name}: {stake.Text}")

PlayDialogAudio(173)
