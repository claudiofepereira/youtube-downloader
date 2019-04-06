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

def my_hook(d):
    if d['status'] == 'finished':
        print("Done downloading -> {}".format(d['filename']))

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'musics/%(title)s.%(ext)s',
    'quiet': True,
    'download_archive': 'info/downloaded_songs.txt',
    'progress_hooks': [my_hook],
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


def printUrlFound(clipboard_content):
    print()
    print("Found url: %s" % str(clipboard_content))


def downloadMusic(url, delay):
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except youtube_dl.DownloadError:
        return youtube_dl.DownloadError


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
