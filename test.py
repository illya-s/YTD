from pytube import YouTube
from taglib import File
from pathlib import Path


video_url = "https://music.youtube.com/watch?v=4ebBW-gzSNw&si=_Kkj3Te0l18uFkIy"
yt = YouTube(video_url)


def set_wav_metadata(file_path):
    with File(file_path, save_on_exit=True) as audio:
        audio.tags["TITLE"] = [yt.title.encode(encoding='utf_8', errors="ignore")]
        audio.tags["ALBUM"] = [yt.author.encode(encoding='utf_8', errors="ignore")]
        audio.tags["PERFORMER:HARPSICHORD"] = [yt.author.encode(encoding='utf-8', errors="ignore")]


def get_audio_metadata(file_path):
    audio_file = File(file_path)
    metadata = {
        "title": audio_file.tags.get("TITLE", [""])[0],
        "artist": audio_file.tags.get("ARTIST", [""])[0],
        "album": audio_file.tags.get("ALBUM", [""])[0],
    }
    return metadata


file = Path("C:/Users/Ilya/Desktop/test/За Тебя.wav")
set_wav_metadata(file)
metadata = get_audio_metadata(file)

print("Title:", metadata["title"])
print("Artist:", metadata["artist"])
print("Album:", metadata["album"])