import eyed3

#filename = 'C:\Projects\PyID3ocr\EarthBound_Practicing_Retrocognition_OC_ReMix.mp3'
filename = 'C:\Projects\PyID3ocr\Metal_Gear_Uh_Oh_The_Beat_Have_Started_to_Move_OC_ReMix.mp3'

audiofile = eyed3.load(filename)
album_artist = audiofile.tag.artist
old_title = audiofile.tag.title

old_title_list = old_title.split() #Convert old_title to list for easy word access (as opposed to character)

new_title = ''
new_album = ''

done = False
title_started = False

# vvvvv  Thank you stack overflow  vvvvv
def kill_char(string, n): # n = position of which character you want to remove 
    begin = string[:n]    # from beginning to n (n not included)
    end = string[n+1:]    # n+1 through end of string
    return begin + end

for word in old_title_list:
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
audiofile.tag.title = new_title
audiofile.tag.artist = u"OC ReMix"
audiofile.tag.album = new_album
audiofile.tag.albumartist = album_artist
print "New Title: ", new_title
print "New Album: ", new_album
print "New Album Artist: ", audiofile.tag.albumartist
#remixed_game
#audiofile.tag.album

audiofile.tag.save()