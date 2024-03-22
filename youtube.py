from pytube import Playlist, YouTube
from progress.bar import IncrementalBar
from additionary import clearFileName, is_playlist
from download import download_video, download_audio
from pathlib import Path

import sys

params = sys.argv[1:]

m = params[0]
IUrl = params[1]
ISrc = Path(params[2])


if not is_playlist(IUrl):
    youtube = YouTube(IUrl)
    if m == 0:
        download_video(youtube, ISrc)
    else:
        download_audio(youtube, ISrc)
    print(f'1/1 {clearFileName(youtube.title)} \nDownload completed successfully!')
else:
    link = Playlist(IUrl)
    bar = IncrementalBar('Progress', max = len(link), suffix='%(percent)d%%')
    for n, i in link.video_urls:
        youtube = YouTube(i)
        title = clearFileName(youtube.title)
        if m == 0:
            download_video(youtube, ISrc)
        else:
            download_audio(youtube, ISrc)
        bar.next()
        print(f'{n}/{len(link)} {title} \nDownload completed successfully!')