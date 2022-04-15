from __future__ import unicode_literals
import yt_dlp
import os

ydl_opts = {
    'outtmpl': os.path.join('C:/Users/TruyenTDM/Desktop', '%(title)s.%(ext)s'),
    'ratelimit': 50000000
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=pEF6mb1jf0w'])