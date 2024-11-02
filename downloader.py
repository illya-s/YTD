from PySide6.QtCore import QRunnable

from pytube import Playlist, YouTube
import yt_dlp

import json, requests
from bs4 import BeautifulSoup

from pathlib import Path
from pydub import AudioSegment
from pydub.utils import make_chunks
from additionary import *
from convert import WAV

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


    def get_vid_title(self, link):
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return str(soup.find("title").text).replace("- YouTube", "").strip()
        else:
            return "None"
    def get_vid_author(self, link):
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            author_tag = soup.find("a", {"class": "yt-simple-endpoint style-scope yt-formatted-string"})
            return author_tag.text.strip() if author_tag else "Author not found"
        else:
            return "None"


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
                title = clearFileName(self.get_vid_title(li))

                if self.file_in_list(self.path, f"{title}{".mp4" if not self.mp else ".wav"}"):
                    self.signals.messege.emit(f'{n+1}/{len(link)} --skepped-- {title}', "#ff7000")
                    continue

                if not self.mp:
                    self.download_video(li, self.path)
                else:
                    self.download_audio(li, self.path)

                self.signals.progress.emit(int(((n + 1) * 100) / len(link)))
                self.signals.messege.emit(f'{n+1}/{len(link)} {title}', "#0F0")
            except Exception as e:
                self.signals.messege.emit(f"Error: {e}", "#F00")
                self.signals.progress.emit(100)
                continue


    def download_pytube(self, link, path):
        try:
            yt = YouTube(link, on_progress_callback=self.progress_func)
            video = yt.streams.get_highest_resolution()
            out_file_path = video.download(output_path=path, filename=f"{clearFileName(yt.title)}.mp4")
            return out_file_path
        except Exception as e:
            return False
    def download_yt_dlp(self, link, path):
        def print_progress(d):
            if 'download' in d:
                if d['status'] == 'downloading':
                    self.signals.progress.emit(d['downloaded_bytes'] / d['total_bytes'] * 100)

        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'progress_hooks': [print_progress],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                filename = ydl.prepare_filename(info_dict)
            return filename
        except Exception as e:
            return False


    def download_video(self, link, path):
        ptd = self.download_pytube(link, path)
        if ptd:
            return ptd
        else:
            return self.download_yt_dlp(link, path)


    def download_audio(self, link, path):
        vid = self.download_video(link, path)

        wav = WAV(vid)
        wav.convert(remove=True)
        wav.add_metadata(self.get_vid_author(link))