from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

def add_album_artwork(audio_file, image_file, image_type):
    audio = MP3(audio_file, ID3=ID3)

    if not audio.tags:
        audio.add_tags()

    with open(image_file, 'rb') as f:
        artwork = APIC(encoding=3, mime='image/png', type=image_type, desc=u'Cover', data=f.read())
        audio.tags.add(artwork)
    audio.save()

add_album_artwork(r'C:\Users\Ilya\Documents\GitHub\YTD\Good Life (HGHTS Remix).mp3', r'C:\Users\Ilya\Documents\GitHub\YTD\thumbnail.png', 9)
add_album_artwork(r'C:\Users\Ilya\Documents\GitHub\YTD\Good Life (HGHTS Remix).mp3', r'C:\Users\Ilya\Documents\GitHub\YTD\thumbnail.png', 10)