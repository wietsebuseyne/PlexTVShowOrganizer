#!/usr/bin/python

import os
import argparse
from shutil import move

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', default='.')
	parser.add_argument('original', action='store')
	parser.add_argument('replacement', action='store')

	args = parser.parse_args()

	for dirname, dirnames, filenames in os.walk(args.input):
		for filename in filenames:
			original_path = os.path.join(dirname, filename)

			new_filename = filename.replace(args.original, args.replacement)

			if not new_filename == filename:
				print("Renaming \n\t" + filename + " to \n\t" + new_filename)
				move(original_path, os.path.join(dirname, new_filename))

if __name__ == "__main__": main()