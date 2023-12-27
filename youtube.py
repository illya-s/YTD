from pytube import Playlist, YouTube
from progress.bar import IncrementalBar


link = Playlist(f"Укажите ссылку на плей лист{input()}")
path = f"Укажите папку{input()}"

bar = IncrementalBar('Progress', max = len(link), suffix='%(percent)d%%')

for i in link.video_urls:
    yt = YouTube(i)
    stream = yt.streams.filter(only_audio=True).first()
    chars_to_remove = ["|", "<", ">", ":", "\"", "\\", "/", "?", "*"]
    ti = yt.title
    for char in chars_to_remove:
        ti = ti.replace(char, "")
    stream.download(filename=f"{path}{ti}.mp3")
    bar.next()
bar.finish()
print('Loading successful!')