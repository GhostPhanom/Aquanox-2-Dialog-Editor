import pathlib
import os
import time
import pygame
import filemanager

aquanox_basepath = "C:/Games/AquaNox 2 Revelation/Aquanox-2-Dialog-Editor"#Attention windows path but used/ instead of \
locale = "de"
export_basepath = "C:/Games/AquaNox 2 Revelation/Aquanox-2-Dialog-Editor/export"
FileOptions = filemanager.FilemanagerOptions()
FileOptions.ConfigureFilemanagerOptions(basepath = aquanox_basepath, game_locale = locale, export_path = export_basepath)

def main():
	basevolume_text = 10 / 100
	basevolume_bg = basevolume_text / 5 * 2
	pygame.mixer.init()#Initialize Sound
	FileOptions = filemanager.FilemanagerOptions()
	FileOptions.ConfigureFilemanagerOptions(basepath = aquanox_basepath, game_locale = locale, export_path = export_basepath)

	charlist = filemanager.Character_List()

	print(charlist.filepath_des)
	print(charlist.filepath_loc)

	filemanager.ParseCharacters(charlist)
	print(charlist.table.keys())
	print(charlist.table)
	for char in charlist.table.values():
		char.Print()
	charlist.Export()

	roomlist = filemanager.Room_List()
	filemanager.ParseRooms(roomlist)
	roomlist.Export()

	shiplist = filemanager.Ship_List()
	filemanager.ParseShips(shiplist)
	shiplist.Export()

	moodlist = filemanager.Mood_List()
	filemanager.ParseMoods(moodlist)
	moodlist.Export()

	sdialoglist = filemanager.Sdialog_List()
	filemanager.ParseSdialogs(sdialoglist)
	sdialoglist.Export()

	stakelist = filemanager.Stake_List()
	filemanager.ParseStakes(stakelist)
	stakelist.Export()
	stakelist.GetObjectwithKey(17).Print()


	for stake in stakelist.GetDialogeStakeEntrys(18):
		print(f"{charlist.GetObjectwithKey(stake.Person).Name}: {stake.Text}")

	filemanager.PlayDialogAudio(173, stakelist, roomlist, sdialoglist)

if __name__ == "__main__":
    main()