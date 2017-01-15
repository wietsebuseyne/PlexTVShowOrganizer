# PlexTVShowOrganizer
An attempt at a TV Show organizer, compatible with Plex

The scripts are written in python3 and come as a simple command-line tool.

To use these scripts, make sure you have python3 installed. 

#organize.py
This is the main script that will recursively search a given directory, try to recognize all TV Shows and copy or move the files into a new directory structure as required by plex. Next to TV Shows, it will also find subtitles in the same directory or a 'Subs' directory given they start with the same name as the media file.

The options for the script are:

| option | long name | description |
| --- | --- | --- |
| -i <dir> | --input <dir> | Input directory that will be scanned recursively
| -o <dir> | --output <dir> | Output directory that will contain the organized TV Shows. The script will create subdirectories for the different shows and seasons. |
| -m | --move | If set, the script will move all files rather than copying. *Use at own risk:*  the original files will be removed and the renaming might not always be accurate! |
| -n <replacements> | --names <replacements> |  Can be used when certain shows don't have their correct name in their filename. Each replacement has to consist of the name to be replaced and its replacement, separated by a '>' sign |

To clarify the *-n* option: If your 'How I Met Your Mother' media files are named *HIMYM-SxxExx.avi*, it can be automatically replaced by the full name by the following option:
```
- n "HIMYM>How I Met Your Mother"
```
If multiple shows need renaming, they can be added easily:
```
- n "HIMYM>How I Met Your Mother" "akb>Alles Kan Beter"
```

An example of how to run this script:
```
python organize.py -i "C:\Downloads" -o "C:\Series" - n "HIMYM>How I Met Your Mother" -m
```

#prepend_to_all.py

This script will prepend a given name to all files in the input directory recursively. Be careful to select the correct directory! This might come in handy if some of your TV Shows are inside a folder and don't have the show's name in their filename.

Example:

**Before** (Files will not be recognized by the organize script)
```
Band of Brothers
---01 Currahee.mkv
---02 Days of Days.mkv
...
```

```
python prepend_to_all.py -i 'C:\Band of Brothers' 'Band of Brothers - s01e'
```
**After**
```
Band of Brothers
---Band of Brothers - s01e01 Currahee.mkv
---Band of Brothers - s01e02 Days of Days.mkv
...
```
These files will be identified by the organize.py script correctly.

#replace_in_all.py

This script will replace a given set of characters by another set of characters in all files recursively. Can also be used to remove characters if the second argument is left empty. This can be used if certain files have incorrect names.

```
python replace_in_all.py -i 'C:\HIMYM' 'HIMYM' 'How I Met Your Mother'
```
