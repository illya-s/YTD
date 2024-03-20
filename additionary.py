from pytube import YouTube

def is_playlist(url):
    try:
        YouTube(url).video_id
        return False
    except:
        return True

def clearFileName(name):
    chars_to_remove = ["|", "<", ">", ":", "\"", "\\", "/", "?", ".", "*"]
    for char in chars_to_remove:
        name  = name.replace(char, "").replace("  ", " ")
    return name