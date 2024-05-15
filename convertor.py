from PyQt6.QtCore import QRunnable, QThread, QObject, pyqtSignal as Signal
from pathlib import Path
import subprocess, os
from additionary import get_filename

class ConvertorWorkerSignals(QObject):
    progress = Signal(int)
    messege = Signal(str, str)

class Convertor(QRunnable):
    def __init__(self, inFP:str, ext:str):
        super(Convertor, self).__init__()

        self.inFP = inFP
        self.ext = ext
        self.signals = ConvertorWorkerSignals()

    def run(self):
        fn, ext = get_filename(self.inFP)

        outPath = "/".join(self.inFP.split("/")[:-1])
        output_file = f"{outPath}/{fn}.{self.ext}"

        cmd = ['ffmpeg', '-i', self.inFP, output_file]
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        total_duration = None
        self.signals.progress.emit(0)

        while True:
            line = self.process.stderr.readline().strip()
            if not line:
                break

            if line.startswith('Duration:'):
                total_duration = line.split(', ')[0].split(': ')[1]
                total_duration = sum(x * int(t) for x, t in zip([3600, 60, 1], map(float, total_duration.split(':'))))

            if 'time=' in line and total_duration:
                time_position = line.split('time=')[1].split()[0]
                current_time = sum(x * int(t) for x, t in zip([3600, 60, 1], map(float, time_position.split(':'))))
                progress = int((current_time / total_duration) * 100)
                self.signals.progress.emit(progress)
        self.signals.messege.emit("Download sucsessful!", "#0F0")

class FFmpegReader(QObject):
    def __init__(self, process):
        super(FFmpegReader, self).__init__()

        self.signals = ConvertorWorkerSignals()
        self.process = process