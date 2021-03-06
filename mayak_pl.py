#!/usr/bin/env python3
# Title: mayak-podcast-library
# License: MIT
# Created: Jan 2017

import requests
import arrow
from pathlib import Path
from pyPodcastParser.Podcast import Podcast
from mutagenx.id3 import ID3, TIT2, TALB, TPE1, TRCK, COMM, TDAT, TYER, WOAR, APIC
import win_unicode_console

win_unicode_console.enable()
STR_URL = 'http://radiomayak.ru/podcasts/rss/podcast/2001/brand/59986/type/audio/'
OBJ_PODCAST = Podcast(requests.get(STR_URL).content)        # Get podcast object
INT_COUNT = len(OBJ_PODCAST.items)                          # Calculate items quantity
STR_PODCAST_TITLE = OBJ_PODCAST.title
STR_PODCAST_LINK = OBJ_PODCAST.link
STR_PODCAST_LANG = OBJ_PODCAST.language
STR_PODCAST_DESC = OBJ_PODCAST.description
STR_PODCAST_AUTH = OBJ_PODCAST.itunes_author_name
STR_PODCAST_CAT = OBJ_PODCAST.itunes_categories
STR_PODCAST_IMG = OBJ_PODCAST.itune_image
BIN_PODCAST_IMG = requests.get(STR_PODCAST_IMG).content     # Get front cover

# Print podcast description
print(40 * '=', '\n\n', 'Title: ', STR_PODCAST_TITLE, '\n', 'Link: ', STR_PODCAST_LINK, '\n', \
    'Language: ', STR_PODCAST_LANG, '\n', 'Description: ', STR_PODCAST_DESC, '\n', \
    'Author: ', STR_PODCAST_AUTH, '\n', 'Category: ', STR_PODCAST_CAT, '\n', 'Items: ', INT_COUNT)

INT_TRACK = 1
while INT_TRACK <= INT_COUNT:
    STR_TRACK_TITLE = OBJ_PODCAST.items[-INT_TRACK].title
    STR_FILE_NAME = 'D:\\temp\\' + '{0:03}'.format(INT_TRACK) + ' - ' + STR_TRACK_TITLE + ' - ' \
        + STR_PODCAST_TITLE + '.mp3'
    OBJ_FILE_PATH = Path(STR_FILE_NAME)
    if OBJ_FILE_PATH.is_file():     # If file already exists, continue from next
        INT_TRACK += 1
        continue
    STR_TRACK_SUM = OBJ_PODCAST.items[-INT_TRACK].itunes_summary
    STR_TRACK_DATE = OBJ_PODCAST.items[-INT_TRACK].published_date
    STR_TRACK_DUR = OBJ_PODCAST.items[-INT_TRACK].itunes_duration
    STR_TRACK_URL = OBJ_PODCAST.items[-INT_TRACK].enclosure_url
    # Print track description
    print('\n', 40 * '-', '\n\n', 'Track: ', INT_TRACK, '\n', 'Title: ', STR_TRACK_TITLE, '\n', \
        'Summary: ', STR_TRACK_SUM, '\n', 'Date: ', STR_TRACK_DATE, '\n', 'Duration: ', \
        STR_TRACK_DUR, '\n', 'URL: ', STR_TRACK_URL, '\n', 'File name: ', STR_FILE_NAME)
    # Calculate issue date of track to record in ID3 tag
    OBJ_TRACK_DATE = arrow.get(STR_TRACK_DATE, 'ddd, DD MMM YYYY HH:mm:ss ZZZ')
    STR_TRACK_DAY = '{0:02}'.format(OBJ_TRACK_DATE.date().day)
    STR_TRACK_MONTH = '{0:02}'.format(OBJ_TRACK_DATE.date().month)
    STR_TRACK_YEAR = str(OBJ_TRACK_DATE.date().year)
    STR_TRACK_DDMM = STR_TRACK_DAY + STR_TRACK_MONTH
    # Download file, write it to storage with correct name
    FILE_WB_TRACK = open(STR_FILE_NAME, 'wb')
    FILE_WB_TRACK.write(requests.get(STR_TRACK_URL).content)
    FILE_WB_TRACK.close()
    # Imprint data to the ID3 tag of file
    OBJ_TRACK_ID3 = ID3(STR_FILE_NAME)                                  # Open ID3 of file
    OBJ_TRACK_ID3.delete()                                              # Delete all tags
    OBJ_TRACK_ID3.add(TIT2(encoding=1, text=STR_TRACK_TITLE))           # Add track title
    OBJ_TRACK_ID3.add(TALB(encoding=1, text=STR_PODCAST_TITLE))         # Add album title
    OBJ_TRACK_ID3.add(TPE1(encoding=1, text='Радио "Маяк"'))            # Add author
    OBJ_TRACK_ID3.add(TRCK(encoding=1, text=str(INT_TRACK)))            # Add track number
    OBJ_TRACK_ID3.add(COMM(encoding=1, lang='rus', desc='', \
        text=STR_TRACK_SUM))                                            # Add comment to track
    OBJ_TRACK_ID3.add(TDAT(encoding=1, text=STR_TRACK_DDMM))            # Add track date
    OBJ_TRACK_ID3.add(TYER(encoding=1, text=STR_TRACK_YEAR))            # Add track year
    OBJ_TRACK_ID3.add(WOAR(url='http://radiomayak.ru/'))                # Add URL to radiostation
    OBJ_TRACK_ID3.add(APIC(encoding=1, mime='image/jpeg', type=3, \
        desc=STR_PODCAST_TITLE, data=BIN_PODCAST_IMG))                  # Add front cover to track
    OBJ_TRACK_ID3.save(v1=2, v2_version=3)                              # Save ID3 to track

    INT_TRACK += 1

print('\n', 40 * '=', '\n\n')
