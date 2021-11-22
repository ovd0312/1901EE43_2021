import os
import shutil
import re


def get_se (old_name, season_padding):
	se = re.findall(r"\d+",old_name)[0]
	while len(se)<season_padding:
			se = "0"+se
	return se

def get_ep (old_name, episode_padding):
	ep = re.findall(r"\d+",old_name)[1]
	while len(ep)<episode_padding:
		ep = "0"+ep
	return ep

def get_ep_name(old_name,series):
	episode = ""
	if series != 1:
		episode = re.findall(r"[\w\s]+",old_name)[2]
		episode = episode.strip()
		episode = " "+episode
	return episode

def regex_renamer():

	print("1. Breaking Bad")
	print("2. Game of Thrones")
	print("3. Lucifer")

	series = int(input("Enter the number of the web series that you wish to rename. 1/2/3: "))
	season_padding = int(input("Enter the se Number Padding: "))
	episode_padding = int(input("Enter the ep Number Padding: "))

	series_name = ""
	if series == 1 :
		series_name = "Breaking Bad"
	elif series == 2:
		series_name = "Game of Thrones"
	else:
		series_name = "Lucifer"

	#Create correct directory
	if not os.path.isdir(r"corrected_srt\\" + series_name):
		os.makedirs(r"corrected_srt\\" + series_name)
	
	#Iterate over all files
	for old_name in os.listdir(r"wrong_srt\\" + series_name):		
		#Copy file in correct directory
		shutil.copyfile("wrong_srt\\"+series_name+"\\"+old_name,"corrected_srt\\"+series_name+"\\"+old_name)
		#Get correct name by parts of old name
		new_name = series_name	
		se = " season "+get_se(old_name,season_padding)
		ep = " episode "+get_ep(old_name,episode_padding)
		new_name += get_ep_name(old_name,series)
		new_name += se
		new_name += ep
		ext = re.findall(r"\..{3}$",old_name)[0]
		new_name += ext

		#Rename
		os.rename("corrected_srt"+"\\"+series_name+"\\"+old_name, "corrected_srt"+"\\"+series_name+"\\"+new_name)

regex_renamer()