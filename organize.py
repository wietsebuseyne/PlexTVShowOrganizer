#!/usr/bin/python

import json
import itertools
import sys
import argparse
import os
import re
import json
import string
import glob
from shutil import copy2, move
#from pymediainfo import MediaInfo


help_string = 'organize.py -o <outputdirectory> [-i <inputdirectory>] [-n <replacement_names>] [-m]'

settings = None

os.environ['PATH'] = sys.path[0] + ';' + os.environ['PATH']

def is_video(filename):
	global settings
	return os.path.splitext(filename)[1] in settings['video_file_extensions']

def filename_to_serie(filename, name_replacements = None):
	global settings
	matchingRegex = ""
	for regex in settings['regexes']:
		p = re.compile(regex, re.IGNORECASE)
		m = p.match(filename)
		if not m is None:
			matchingRegex = regex
			break
	if m is None: 
		return None
	
	season = str(m.group(3)).zfill(2)
	episode = str(m.group(4)).zfill(2)
	name = string.capwords(m.group(1).strip(' ._-').replace('.', ' ').replace('_', ' '))
	extra_info = m.group(5).strip(' ._-')
	if not name_replacements is None:
		for r in name_replacements:
			if r[0].lower() == name.lower():
				name = r[1]
	print("Regex match: " + regex)
	return (name, season, episode, extra_info)

def serie_to_str(serie):
	return serie[0] + " - s" + serie[1] + "e" + serie[2] + " - " + serie[3]

def move_file(serie, original_path, output_directory, copy_files = True):
	global settings

	move_string = 'Copying' if copy_files else 'Moving';

	new_filepath = os.path.join(output_directory, serie[0] + '/Season ' + serie[1])
	if not os.path.exists(new_filepath):
		os.makedirs(new_filepath)
	new_file = new_filepath + '/' + serie_to_str(serie) + os.path.splitext(original_path)[1];
	
	if os.path.isfile(new_file):
		print('Skipping, already exists')
	else:
		print()
		print(move_string + ' \n\t' + original_path + "\nto\n\t" + new_file)

		if copy_files:
			copy2(original_path, new_file)
		else:
			move(original_path, new_file)

		sub_path = os.path.basename(os.path.splitext(original_path)[0])

		sub_regex = re.escape(sub_path.strip(r'.\/')) + '(.*)\.' + settings['subtitle_regex'] + '$'

		sub_pattern = re.compile(sub_regex)

		subs = [f for f in os.listdir(os.path.dirname(original_path)) if re.search(sub_regex, f)]

		subs2 = []
		subsDir = os.path.dirname(original_path) + '/Subs'
		if os.path.exists(subsDir):
			subs2 = [f for f in os.listdir(subsDir) if re.search(sub_regex, f)]

		for sub_file in subs:
			m = sub_pattern.match(sub_file)
			print(move_string + ' subtitle for ' + serie_to_str(serie))
			new_file = new_filepath + '/' + serie_to_str(serie) + '.' + m.group(1).strip('._-[]') + m.group(2)
			old_file = os.path.dirname(original_path) + '/' + sub_file
			if copy_files:
				copy2(old_file, new_file)
			else:
				move(old_file, new_file)

		#Files in subs directory
		for sub_file in subs2:
			m = sub_pattern.match(sub_file)
			print(move_string + ' subtitle for ' + serie_to_str(serie))
			new_file = new_filepath + '/' + serie_to_str(serie) + '.' + m.group(1).strip('._-[]') + m.group(2)
			old_file = os.path.dirname(original_path) + '/Subs/' + sub_file
			if copy_files:
				copy2(old_file, new_file)
			else:
				move(old_file, new_file)

def name_replacement(s):
	try:
		original_name, replace_name = s.split('>')
		return original_name, replace_name
	except:
		raise argparse.ArgumentTypeError('Replacement names must be in the following format: original_name>replacement_name')

def main():
	global settings
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', default='.')
	parser.add_argument('-o', '--output', default='.')
	parser.add_argument('-n', '--names', nargs='*', type=name_replacement)
	parser.add_argument('-m', '--move', action='store_true')

	args = parser.parse_args()
	if args.output == '.':
		args.output = args.input + '/../PlexTVShows'
	print()
	print('All media files in directory ' + args.input + ' will be ' + ('moved' if args.move else 'copied') + ' to their organized folders in ' + args.output)
	print()
	videos_total = 0
	series_found = 0
	movies_found = 0
	unrecognized_files = []

	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	settings_file = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname('settings.json')))
	with open(os.path.join(__location__, 'settings.json')) as json_data:
		settings = json.load(json_data)
		settings['subtitle_regex'] = "(" + '|'.join(settings['subtitle_extensions']) + ")"

	for dirname, dirnames, filenames in os.walk(args.input):
		filenames = [f for f in filenames if not f[0] == '.']
		dirnames[:] = [d for d in dirnames if not d[0] == '.']
		for filename in filenames:
			original_path = os.path.join(dirname, filename)
			print()
			print("Analyzing " + filename)
			if is_video(original_path):
			#fileInfo = MediaInfo.parse(original_path)
			#for track in fileInfo.tracks:
			#	if track.track_type == "Video":
				videos_total += 1
				serie = filename_to_serie(filename, args.names)
				if not serie is None:
					move_file(serie, original_path, args.output, not args.move)
					series_found += 1
				else:
					unrecognized_files.append(filename)
			else:
				print('Skipping, no video file')
	print('\nOrganizing media library finished.')
	print('Total video files encountered:	' + str(videos_total))
	print('TV-show found:					' + str(series_found))
	print('Unrecognized video files:		' + str(unrecognized_files))

if __name__ == "__main__": main()