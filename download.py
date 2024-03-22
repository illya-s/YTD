import os
from pathlib import Path
from music_tag import load_file
from additionary import clearFileName
from pydub import AudioSegment


def download_video(yt, path):
    video = yt.streams.get_highest_resolution()
    out_file_path = video.download(output_path=path, filename=f"{clearFileName(yt.title)}.mp4")
    return out_file_path

def download_audio(yt, path):
    path = Path(path)
    audio_file_path = download_youtube_audio(yt, path)
    audio_file_path = convert_to_wav(audio_file_path)
    add_metadata(yt, audio_file_path)

def download_youtube_audio(yt, output_path):
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file_path = audio_stream.download(output_path=output_path, filename=f"{clearFileName(yt.title)}.mp4")
    return audio_file_path

def convert_to_wav(video_file_path):
    audio = AudioSegment.from_file(Path(video_file_path), format="mp4")
    audio.export(f"{video_file_path.split('.')[0]}.wav", format="wav")
    os.remove(video_file_path)
    return f"{video_file_path.split('.')[0]}.wav"

def add_metadata(yt, file_path):
    audio = load_file(Path(file_path))
    audio['title'] = yt.title
    audio['artist'] = yt.author
    audio.save()