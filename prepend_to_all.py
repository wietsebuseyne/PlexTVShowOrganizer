#!/usr/bin/python

import os
import argparse
from shutil import move

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', default='.')
	parser.add_argument('prepend_string', action='store')

	args = parser.parse_args()

	for dirname, dirnames, filenames in os.walk(args.input):
		for filename in filenames:
			original_path = os.path.join(dirname, filename)
			move(original_path, os.path.join(dirname, args.prepend_string + filename))

if __name__ == "__main__": main()