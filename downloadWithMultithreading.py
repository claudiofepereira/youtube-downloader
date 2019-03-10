#!/bin/env python

# Requires: youtube_dl module
# Requires: ffmpeg
# Requires: pyperclip module
# Requires: pywin32 module

import win32clipboard
import pyperclip
import threading
import time
import youtube_dl
import sys
import os

sys.path.append(os.path.abspath("SO_site-packages"))

# To clean the first clipboard available - avoid instant download
def cleanClipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'output/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def is_url_but_not_bitly(url):
    if url.startswith("http://") and not "bit.ly" in url:
        return True
    return False


def print_to_stdout(clipboard_content):
    print("Found url: %s" % str(clipboard_content))


def downloadMusic(value):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([value])


class ClipboardWatcher(threading.Thread):
    def __init__(self, predicate, callback, pause=1.):
        super(ClipboardWatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                downloadMusic(recent_value)
                if self._predicate(recent_value):
                    self._callback(recent_value)
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True


def main():
    watcher = ClipboardWatcher(is_url_but_not_bitly,
                               print_to_stdout,
                               1.)
    watcher.start()


if __name__ == '__main__':
    try:
        cleanClipboard()
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
