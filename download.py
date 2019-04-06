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
    'outtmpl': 'musics/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


def printUrlFound(clipboard_content):
    print("Found url: %s" % str(clipboard_content))


def verifyUrlExists(url):
    ies = youtube_dl.extractor.gen_extractors()
    for ie in ies:
        if ie.suitable(url) and ie.IE_NAME != 'generic':
            # Site has dedicated extractor
            return True
    return False


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
