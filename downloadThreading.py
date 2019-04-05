#!/bin/env python

import win32clipboard
import pyperclip
import _thread
import time
import youtube_dl
import sys
import os

sys.path.append(os.path.abspath("SO_site-packages"))


def cleanClipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloaded-musics/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def printUrlFound(clipboard_content):
    print("Found url: %s" % str(clipboard_content))


def downloadMusic(url, delay):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == '__main__':
    recent_value = ""
    try:
        cleanClipboard()
        while True:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                printUrlFound(recent_value)
                _thread.start_new_thread(downloadMusic, (recent_value, 5))
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
