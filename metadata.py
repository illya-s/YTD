from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from music_tag import load_file


def get_title(src):
    tag = load_file(src)
    if tag.get('title'):
        title = tag.get('title')
    else:
        title = src.split("\\")[-1]
    return title

def get_artist(src):
    tag = load_file(src)
    if tag.get('artist'):
        artist = tag.get('artist')
    else:
        artist = "Unknown Artist"
    return artist


def get_cover(src):
    audio = MP3(src, ID3=ID3)

    if 'APIC:' in audio:
        artwork = audio['APIC:'].data
        return artwork
    else:
        return None