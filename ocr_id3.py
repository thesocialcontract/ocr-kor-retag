from mutagen.easyid3 import EasyID3
import tag_processor
import sys
import os
import logging

#	TODO:
#			Add affected mp3s log
#			Accept console commands
#				Accept different directories

current_path = "C:\Users\Koriantor\Desktop\TEST"

def isProcessed(audiofile):
	'''
	Checks to see if the given mp3 file is an OC ReMix, and whether or not
	the OC ReMix has the new tag or default tag.
	'''
	artist = audiofile["artist"]
	if audiofile["artist"] == [u'OC ReMix']:	# An already processed OC ReMix MP3 will have OC ReMix as the artist
		return True									# If OC ReMix is already the artist, it's already processed, so we skip processing
	else:										# If the artist isn't "OC ReMix", we need to figure out if it's a remix that needs processed
		title = audiofile["title"]				# 	or if it's some other type of MP3.
		title_split = title[0].split()				#	Split the title into separate words for easy checking
		for n in title_split:						# The default remix labeling has "OC ReMix" at the end of every title
			if n == "ReMix":						# We scan the title to see if it contains "OC ReMix" at the end
				return False						# If it does, we need to process this remix
		return True								# If OC ReMix isn't in the title, it's not a remix and can be skipped
				
def main():
	''' TODO: Write Documenation '''
	#logging.basicConfig(filename='modified.log',level=logging.DEBUG)	# Set up logfile for keeping track of modified files
	#logging.info("Modified Files:\n")
	
	for root, dirs, files in os.walk(current_path):						# Scan for MP3 files in given directory and subdirectories
		for n in files:													# Scans files in the directory for mp3s
			if n.endswith('.mp3'):										# If it finds an mp3,
				filepath = root + "\\" + n								# Grab the filepath
				audiofile = EasyID3(filepath)							# Make ID3 tag object
				if !isProcessed(audiofile):								# If the MP3 isn't already processed,
					tag_processor.processMP3(audiofile, filepath)			# Process it and save adjustments
					#logging.info(filepath)									# Add Filename to logfile
	return
	
if __name__ == "__main__":
	sys.exit(main())