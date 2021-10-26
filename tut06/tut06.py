import os
import shutil
import re

def regex_renamer():

	# Taking input from the user
	print("1. Breaking Bad")
	print("2. Game of Thrones")
	print("3. Lucifer")

	series_id = int(input("Enter the number of the web series that you wish to rename. 1/2/3: "))
	season_padding = int(input("Enter the Season Number Padding: "))
	episode_padding = int(input("Enter the Episode Number Padding: "))

	#Check input validity
	if series_id>3 or series_id<1 or season_padding<1 or episode_padding<1:
		return

	#Series ID -> Series Name
	series_name = {1:"Breaking Bad", 2:"Game of Thrones", 3:"Lucifer"}

	wrong_path = r"wrong_srt\\" + series_name[series_id]
	correct_path = r"corrected_srt\\" + series_name[series_id]

	#Create corrected folder if doesn't exist
	if not os.path.isdir(correct_path):
		os.makedirs(correct_path)

	#Get the list of all file names to be changed
	all_files = os.listdir(wrong_path)

	for file in all_files:		
		#Copy files into corrected_srt folder
		shutil.copyfile(wrong_path+"\\"+file,correct_path+"\\"+file)

		#Get seperate components of the file-name
		ep_name = ""
		if series_id != 1:
			ep_name = re.findall(r"[\w\s]+",file)[2]
			ep_name = ep_name.strip()
			ep_name = " - "+ep_name

		season = re.findall(r"\d+",file)[0]
		episode = re.findall(r"\d+",file)[1]
		extension = re.findall(r"\..{3}$",file)[0]

		#Insert episode and season padding
		while len(season)<season_padding:
			season = "0"+season
		while len(episode)<episode_padding:
			episode = "0"+episode

		#Create new file name from components
		new_file_name = series_name[series_id]+" - Season "+season+" Episode "+episode+ep_name+extension
		
		#Rename the file
		os.rename(correct_path+"\\"+file, correct_path+"\\"+new_file_name)

regex_renamer()