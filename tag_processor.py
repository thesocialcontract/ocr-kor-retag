from mutagen.easyid3 import EasyID3

# TODO: Write logfile
#		Test


#vvvvv  Thank you stack overflow  vvvvv
def killChar(string, n): # n = position of which character you want to remove 
	begin = string[:n]    # from beginning to n (n not included)
	end = string[n+1:]    # n+1 through end of string
	return begin + end

	
def processMP3(audiofile, filepath):
	''' 
	This function takes a file and changes the default tagging to my tagging.

	OCR's default tagging:
	Title: "<Game> '<Remix Title>' OC ReMix"
	Artist: <contributing remixer>, <contributing remixer>, <etc.>
	Album: "http://www.ocremix.org"

	Desired tagging:
	Title: <Remix Title>
	Artist: "OC ReMix"
	Album: <Game>
	Album Artist: <contributing remixer>, <contributing remixer>, <etc.>
	'''

	# Initialize Variables
	album_artist = audiofile["artist"]			# Grab a string version of the artist
	old_title = audiofile["title"]				# Grab a string version of the title
	old_title_split = old_title[0].split() 		# Convert old_title to list for easy word access (as opposed to character)
	
	new_title = ''
	new_album = ''
	found_remix_title = False					# Flag for <remix title>
	done = False
	
	for word in old_title_split:				# Scan the title, and split the parts
		if found_remix_title == False:			# Check if we've hit the remix title (if the word starts with ')
			if word[0] == "'":  				# If the first character of the word is an apostrophe
				found_remix_title = True		# It's part of the title
				new_title += word				# Add the world
				new_album = killChar(new_album, len(new_album) - 1) 	#Remove the extra whitespace at the end of the game
			
				if word.endswith("\'"):			# Check if it's a one word title
					done = True					# If so, we're done, clean up the title
					new_title = killChar(word, len(word) - 1)		# Remove end "'" and add to the new title
					new_title = killChar(new_title, 0)				# Remove Beginning "'"
					
				
			else:								# ELSE
				new_album += word				#	It's part of the game's name.  Add it to the game.
				new_album += ' '				#	Add spaces between word.  
			
		else:									# If we've already hit the title, now we need to finish the title
			if done == False:					# Check if we've reached the end of the title
				new_title += ' '					# Add whitespace between words in the remix title
				
				if word.endswith("\'"):				# Check if this is the last word
					done = True						# (the last word should have an apostrophe at the end)
					new_title += killChar(word, len(word) - 1)		# Remove end "'" and add to the new title
					new_title = killChar(new_title, 0)				# Remove Beginning "'"
				
				else:
					new_title += word			# If it's not the last word in title, add it"
	
	# Reassign ID3 Tag and save everything :D
	audiofile["title"] = new_title
	audiofile["artist"] = u"OC ReMix"
	audiofile["album"] = new_album
	audiofile["performer"] = album_artist
	
	audiofile.save()
	
	return