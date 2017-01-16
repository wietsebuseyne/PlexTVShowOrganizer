#!/usr/bin/python

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

video_file_extensions = [
'.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec', '.aep', '.aepx',
'.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf', '.asx', '.avb',
'.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik', '.bin', '.bix',
'.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine', '.cip',
'.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat', '.dav', '.dce',
'.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm', '.dmsm3d', '.dmss',
'.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms', '.dvx', '.dxr',
'.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp', '.fcproject',
'.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp', '.h264', '.hdmov',
'.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf', '.ivr', '.ivs',
'.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg', '.m1v', '.m21',
'.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv', '.mj2', '.mjp',
'.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie', '.mp21',
'.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex', '.mpl',
'.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb', '.mvc',
'.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv', '.nvc', '.ogm',
'.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist', '.plproj',
'.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr', '.pxv',
'.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd', '.rmd',
'.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk', '.sbt',
'.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi', '.smi',
'.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi', '.swf', '.swi',
'.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts', '.tsp', '.ttxt',
'.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg','.vem', '.vep', '.vf', '.vft',
'.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6', '.vp7', '.vpj',
'.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx', '.wot', '.wp3',
'.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog', '.yuv', '.zeg',
'.zm1', '.zm2', '.zm3', '.zmv'  ]

help_string = 'organize.py -o <outputdirectory> [-i <inputdirectory>] [-n <replacement_names>] [-m]'

sub_extensions_regex = '(srt|sub|sbv|smi|ssa|ass|vtt|pgs|vobsub|idx)'

os.environ['PATH'] = sys.path[0] + ';' + os.environ['PATH']

def is_video(filename):
	return os.path.splitext(filename)[1] in video_file_extensions

def filename_to_serie(filename, name_replacements = None):
	p = re.compile('(.+)(s)(\d\d?)e(\d\d?).*', re.IGNORECASE)
	m = p.match(filename)
	if m is None:
		p = re.compile('(.+)([_\-. ])(\d\d?)(\d\d)[_\-. ].*')
		m = p.match(filename)
		if m is None:
			p = re.compile('(.+)([^0-9])(\d\d?)x(\d\d?).*', re.IGNORECASE)
			m = p.match(filename)
			if m is None:
				return None
		
	season = str(m.group(3)).zfill(2)
	episode = str(m.group(4)).zfill(2)
	name = string.capwords(m.group(1).strip(' ._-').replace('.', ' ').replace('_', ' '))
	if not name_replacements is None:
		for r in name_replacements:
			if r[0].lower() == name.lower():
				name = r[1]
	return (name, season, episode)

def serie_to_str(serie):
	return serie[0] + " - s" + serie[1] + "e" + serie[2]

def move_file(serie, original_path, output_directory, copy_files = True):

	move_string = 'Copying' if copy_files else 'Moving';

	new_filepath = os.path.join(output_directory, serie[0] + '/Season ' + serie[1])
	if not os.path.exists(new_filepath):
		os.makedirs(new_filepath)
	new_file = new_filepath + '/' + serie_to_str(serie) + os.path.splitext(original_path)[1];
	
	print()
	print(move_string + ' \n\t' + original_path + "\nto\n\t" + new_file)

	if copy_files:
		copy2(original_path, new_file)
	else:
		move(original_path, new_file)

	sub_path = os.path.basename(os.path.splitext(original_path)[0])

	sub_regex = re.escape(sub_path.strip(r'.\/')) + '(.*)\.' + sub_extensions_regex + '$'

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

	for dirname, dirnames, filenames in os.walk(args.input):
		for filename in filenames:
			original_path = os.path.join(dirname, filename)
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
				break
	print('\nOrganizing media library finished.')
	print('Total video files encountered:	' + str(videos_total))
	print('TV-shows found and moved:		' + str(series_found))
	print('Unrecognized video files:		' + str(unrecognized_files))

if __name__ == "__main__": main()