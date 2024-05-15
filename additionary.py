from pytube import YouTube
from pathlib import Path

def is_playlist(url):
    try:
        YouTube(url).video_id
        return False
    except:
        return True
def is_audio(ext):
    li = ["mp3", "aac", "wav", "ogg", "flac"]
    return True if ext in li else False
def is_video(ext):
    li = ["avi", "mov", "mp4", "mkv", "wmv", "flv", "webm", "mpeg", "mpg", "3gp", "ogg"]
    return True if ext in li else False


def get_filename(path):
    fn = str(Path(path)).split("\\")[-1].split(".")
    return fn[0], fn[-1]
def clearFileName(name):
    chars_to_remove = ["|", "<", ">", ":", "\"", "\\", "/", "?", ".", "*"]
    for char in chars_to_remove:
        name = name.replace(char, "")
    return name.replace("  ", " ")