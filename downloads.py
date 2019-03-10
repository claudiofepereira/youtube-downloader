#!/bin/env python

# Requires: youtube_dl module
# Requires: ffmpeg
# Requires: pyperclip module
# Requires: pywin32 module

import win32clipboard
import pyperclip
import time
import youtube_dl
import sys
import os

sys.path.append(os.path.abspath("SO_site-packages"))

# To clean the first clipboard available - avoid instant download
win32clipboard.OpenClipboard()
win32clipboard.EmptyClipboard()
win32clipboard.CloseClipboard()

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

recent_value = ''


def downloadMusic(value):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([recent_value])


while True:
    tmp_value = pyperclip.paste()
    if tmp_value != recent_value and tmp_value != None:
        recent_value = tmp_value
        downloadMusic(recent_value)
    time.sleep(0.1)
