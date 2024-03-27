# from taglib import File

# def set_wav_metadata(file_path, title, artist, album):
#     with File(file_path, save_on_exit=True) as song:
#         song.tags["ALBUM"] = [album]
#         song.tags["GENRE"] = ["Vocal", "Classical"]
#         song.tags["PERFORMER"] = ["Ton Koopman"]
# # {'ARTIST': ['piman', 'jzig'], 'ALBUM': ['Quod Libet Test Data'], 'TITLE': ['Silence'], 'GENRE': ['Silence'], 'TRACKNUMBER': ['02/10'], 'DATE': ['2004']}


# # Example usage
# file = r"C:\Users\Ilya\Desktop\test\За Тебя.wav"
# set_wav_metadata(file, 'My Song', 'Artist Name', 'Album Name')

from pytube import YouTube

def get_video_metadata(url):
    try:
        yt = YouTube(url)
        metadata = {
            'title': yt.title,
            'author': yt.author,
            'description': yt.description,
            'views': yt.views,
            'length': yt.length,
            'rating': yt.rating,
            'thumbnail_url': yt.thumbnail_url,
            'keywords': yt.keywords,
            'streams': yt.streams
        }
        return metadata
    except Exception as e:
        print("Error:", e)
        return None

# Example usage
video_url = "https://music.youtube.com/watch?v=4ebBW-gzSNw&si=_Kkj3Te0l18uFkIy"  # Rick Astley - Never Gonna Give You Up
metadata = get_video_metadata(video_url)
if metadata:
    print("Title:", metadata['title'])
    print("Author:", metadata['author'])
    print("Description:", metadata['description'])
    print("Views:", metadata['views'])
    print("Length:", metadata['length'])
    print("Rating:", metadata['rating'])
    print("Thumbnail URL:", metadata['thumbnail_url'])
    print("Keywords:", metadata['keywords'])
    print("Streams:", metadata['streams'])
