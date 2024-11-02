from PySide6.QtCore import QRunnable
from pydub import AudioSegment
from pydub.utils import make_chunks
from taglib import File
from additionary import *

import os


class WAV(QRunnable):
    def __init__(self, video_file):
        super(WAV, self).__init__()
        self.chunk_size_ms = 1000
        self.video_file = video_file
        self.signals = DownloadWorkerSignals()
        
        base, ext = os.path.splitext(self.video_file)
        self.name = f"{base}.wav"

    def convert(self, remove=True):
        self.signals.messege.emit(f"Converting to wav", "#FF0")
        audio = AudioSegment.from_file(self.video_file)

        total_duration = len(audio)
        chunks = [audio[i:i + self.chunk_size_ms] for i in range(0, total_duration, self.chunk_size_ms)]
        wav_audio = AudioSegment.empty()

        for i, chunk in enumerate(chunks):
            wav_audio += chunk
            self.signals.progress.emit(round((i + 1) / len(chunks) * 100))

        wav_audio.export(self.name, format="wav")
        if remove:
            os.remove(self.video_file)
        return self.name

    def add_metadata(self, author):
        with File(self.name, save_on_exit=True) as song:
            song.tags["ALBUM"] = [author]
            song.tags["PERFORMER:HARPSICHORD"] = [author]