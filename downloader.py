from PyQt6.QtCore import QRunnable
from pytube import Playlist, YouTube
import os, json

from pathlib import Path
from pydub import AudioSegment
from taglib import File
from youtobe import YouTobe
from additionary import *

class Download(QRunnable):
    def __init__(self, link, path, mp):
        super(Download, self).__init__()
        self.link = link
        self.path = path
        self.mp = mp
        self.signals = DownloadWorkerSignals()

    def progress_func(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = int(((size - bytes_remaining) / size) * 100)
        self.signals.progress.emit(progress)

    def file_in_list(self, directory_path, fileName):
        return True if fileName in [file.name for file in Path(directory_path).iterdir() if file.is_file()] else False

    def run(self):
        if is_file(self.link):
            with open(self.link, 'r') as file:
                link = json.load(file)
        # elif is_channel(self.link):
        #     self.signals.messege.emit("Search video...", "#FFF")
        #     link = YouTobe(self.link).run()
        elif is_playlist(self.link):
            link = Playlist(self.link)
        else:
            link = [self.link]

        self.signals.progress.emit(0)
        for n, li in enumerate(link):
            try:
                youtube = YouTube(li, on_progress_callback=self.progress_func)
                title = clearFileName(youtube.title)

                if self.file_in_list(self.path, f"{title}{".mp4" if self.mp == 0 else ".wav"}"):
                    self.signals.messege.emit(f'{n+1}/{len(link)} --skpped-- {title}', "#ff7000")
                    continue

                self.download_video(youtube, self.path) if self.mp == 0 else self.download_audio(youtube, self.path)

                self.signals.progress.emit(int(((n + 1) * 100) / len(link)))
                self.signals.messege.emit(f'{n+1}/{len(link)} {title}', "#0F0")
            except Exception as e:
                self.signals.messege.emit(f"Error: {e}", "#F00")
                continue

    def download_video(self, yt, path):
        video = yt.streams.get_highest_resolution()
        out_file_path = video.download(output_path=path, filename=f"{clearFileName(yt.title)}.mp4")
        return out_file_path


    def download_audio(self, yt, path):
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(path)

        audio_file_path = self.convert(audio_file)
        self.add_metadata(yt, audio_file_path)

    def convert(self, video_file):
        base, ext = os.path.splitext(video_file)
        audio = AudioSegment.from_file(video_file)
        audio.export(f"{base}.wav", format="wav")
        os.remove(video_file)
        return f"{base}.wav"

    def add_metadata(self, yt, file_path):
        with File(file_path, save_on_exit=True) as song:
            song.tags["ALBUM"] = [yt.author]
            song.tags["PERFORMER:HARPSICHORD"] = [yt.author]