from PyQt6.QtCore import QRunnable, QObject, pyqtSignal as Signal
from pytube import Playlist, YouTube
import os

from pathlib import Path
from pydub import AudioSegment
from taglib import File

from additionary import is_playlist, clearFileName


class DownloadWorkerSignals(QObject):
    progress = Signal(int)
    messege = Signal(str, str)

class Download(QRunnable):
    def __init__(self, link, path, mp):
        super(Download, self).__init__()
        self.link = link
        self.path = path
        self.mp = mp
        self.signals = DownloadWorkerSignals()
        self.l = 0

    def progress_func(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = int(((size - bytes_remaining) / size) * 100)
        self.signals.progress.emit(progress)

    def run(self):
        if is_playlist(self.link):
            link = Playlist(self.link)
        else:
            link = [self.link]

        self.signals.progress.emit(0)
        for n, li in enumerate(link):
            try:
                youtube = YouTube(li, on_progress_callback=self.progress_func)
                if self.mp == 0:
                    self.download_video(youtube, self.path)
                else:
                    self.download_audio(youtube, self.path)
                self.signals.progress.emit(int(((n + 1) * 100) / len(link)))
                self.signals.messege.emit(f'{n+1}/{len(link)} {clearFileName(youtube.title)}', "#FFF")
                self.signals.messege.emit("Download sucsessful!", "#0F0")
            except Exception as e:
                self.signals.messege.emit(f"Error: {e}", "#F00")
                continue


    def download_video(self, yt, path):
        video = yt.streams.get_highest_resolution()
        out_file_path = video.download(output_path=path, filename=f"{clearFileName(yt.title)}.mp4")
        return out_file_path

    def download_audio(self, yt, path):
        path = Path(path)
        audio_file_path = self.download_youtube_audio(yt, path)
        audio_file_path = self.convert_to_wav(audio_file_path)
        self.add_metadata(yt, audio_file_path)

    def download_youtube_audio(self, yt, output_path):
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file_path = audio_stream.download(output_path=output_path, filename=f"{clearFileName(yt.title)}.mp4")
        return audio_file_path

    def convert_to_wav(self, video_file_path):
        audio = AudioSegment.from_file(Path(video_file_path), format="mp4")
        audio.export(f"{video_file_path.split('.')[0]}.wav", format="wav")
        os.remove(video_file_path)
        return f"{video_file_path.split('.')[0]}.wav"

    def add_metadata(self, yt, file_path):
        with File(file_path, save_on_exit=True) as song:
            song.tags["ALBUM"] = [yt.author]
            song.tags["PERFORMER:HARPSICHORD"] = [yt.author]

## --- add image from video url! ---
# from pytube import YouTube
# import requests
# from PIL import Image
# from io import BytesIO

# video_url = "https://music.youtube.com/watch?v=WUbYKe2DQgU&si=fRcmT7rAMHWDIuSV"

# yt = YouTube(video_url)

# thumbnail_url = yt.thumbnail_url

# response = requests.get(thumbnail_url)
# img = Image.open(BytesIO(response.content))

# img.save("thumbnail.png", "PNG")

# print("Thumbnail saved as 'thumbnail.png'")