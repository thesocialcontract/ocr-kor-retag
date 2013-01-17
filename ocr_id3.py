import eyed3
from mutagen.easyid3 import EasyID3

#filename = 'C:\Projects\PyID3ocr\EarthBound_Practicing_Retrocognition_OC_ReMix.mp3'
filename = 'C:\Projects\PyID3ocr\Metal_Gear_Uh_Oh_The_Beat_Have_Started_to_Move_OC_ReMix.mp3'

audiofile = EasyID3(filename)
album_artist = audiofile["artist"]
old_title = audiofile["title"]

old_title_split = old_title[0].split() #Convert old_title to list for easy word access (as opposed to character)
new_title = ''
new_album = ''

done = False
title_started = False

#vvvvv  Thank you stack overflow  vvvvv
def kill_char(string, n): # n = position of which character you want to remove 
	begin = string[:n]    # from beginning to n (n not included)
	end = string[n+1:]    # n+1 through end of string
	return begin + end

for word in old_title_split:
	if title_started == False:
		if word[0] == "'":  				#IF the first character is an apostrophe
			title_started = True			#	It's part of the title
			new_title += word
			new_album = kill_char(new_album, len(new_album) - 1) #Remove the extra whitespace at the end of the album
		else:								#ELSE
			new_album += word				#	It's part of the game's name.  Add it to the game.
			new_album += ' '				#	Add spaces between word.  
		
	else:
		if done == False:
			new_title += ' '				#Add whitespace between words
			
			if word[len(word) - 1] == "'":
				done = True
				new_title += kill_char(word, len(word) - 1)		#Remove end "'"
				new_title = kill_char(new_title, 0)				#Remove Beginning "'"
			
			else:
				new_title += word			#If it's not the last word in title, add it"
			
#Reassign ID3 Tag
audiofile["title"] = new_title
audiofile["artist"] = u"OC ReMix"
audiofile["album"] = new_album
audiofile["performer"] = album_artist
print "New Title: ", audiofile["title"]
print "New Artist: ", audiofile["artist"]
print "New Album: ", audiofile["album"]
print "New Album Artist: ", audiofile["performer"]

audiofile.save()