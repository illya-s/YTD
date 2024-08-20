from pytube import YouTube
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal as Signal

def is_playlist(url):
    try:
        YouTube(url).video_id
        return False
    except:
        return True
def is_channel(url):
    return True if "@" in url else False
def is_file(src):
    return True if Path(src).is_file() else False


def is_audio(ext):
    li = ["mp3", "aac", "wav", "ogg", "flac"]
    return True if ext in li else False
def is_video(ext):
    li = ["avi", "mov", "mp4", "mkv", "wmv", "flv", "webm", "mpeg", "mpg", "3gp", "ogg"]
    return True if ext in li else False


def clearFileName(name):
    chars_to_remove = ["|", "<", ">", ":", "\"", "\\", "/", "?", ".", "*"]
    for char in chars_to_remove:
        name = name.replace(char, "")
    return name.replace("  ", " ")

class DownloadWorkerSignals(QObject):
    progress = Signal(int)
    messege = Signal(str, str)