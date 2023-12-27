from pytube import Playlist, YouTube
from progress.bar import IncrementalBar

s = input('Выберите плей лист(1) / одно видео(0): ')
m = input('Выберите аудио(1) / видео(0): ')
IUrl = input('Укажите ссылку: ')
ISrc = input('Укажите папку, наприсер C:/video: ')


def clearFileName(name):
    chars_to_remove = ["|", "<", ">", ":", "\"", "\\", "/", "?", "*"]
    for char in chars_to_remove:
        name = name.replace(char, "")
    return(name)


if s == "0" or s == "False" or s == False:
    youtube = YouTube(IUrl)
    stream = youtube.streams.filter(only_audio=f"{True if m==1 else False}", file_extension=f"{"mp4" if m==0 else "mp3"}").first()
    title = clearFileName(youtube.title)
    stream.download(output_path=ISrc, filename=title)
    print(f'1/1 {title} ')
    print('Download completed successfully!')
elif s == "1" or s == "True" or s == True:
    link = Playlist(IUrl)
    bar = IncrementalBar('Progress', max = len(link), suffix='%(percent)d%%')
    for n, i in link.video_urls:
        youtube = YouTube(i)
        stream = youtube.streams.filter(only_audio=f"{True if m==1 else False}", file_extension=f"{"mp4" if m==0 else "mp3"}").first()
        title = clearFileName(youtube.title)
        stream.download(output_path=ISrc, filename=title)
        bar.next()
        print(f'{n}/{len(link)} {title}')
    print('Download completed successfully!')
else:
    print("Error")