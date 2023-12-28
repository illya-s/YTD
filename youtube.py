from pytube import Playlist, YouTube
from progress.bar import IncrementalBar
from clearFileName import clearFileName

s = input('Выберите плей лист(1) / одно видео(0): ')
m = input('Выберите аудио(1) / видео(0): ')
IUrl = input('Укажите ссылку: ')
ISrc = input('Укажите папку, наприсер C:/video: ')

# def progress_func(stream, chunk, bytes_remaining):
#     size = stream.filesize
#     progress = int(((size - bytes_remaining) / size) * 100)
#     bar.next(progress)


if s == "0" or s == "False" or s == False:
    # bar1 = IncrementalBar('Progress', max = 100, suffix='%(percent)d%%')
    youtube = YouTube(IUrl)
    title = clearFileName(youtube.title)
    if m == 0:
        stream = youtube.streams.get_highest_resolution()
        stream.download(output_path=ISrc, filename=f"{title}.mp4")
    else:
        stream = youtube.streams.filter(only_audio=True).first()
        stream.download(output_path=ISrc, filename=f"{title}.mp3")
    print(f'1/1 {title} ')
    print('Download completed successfully!')
elif s == "1" or s == "True" or s == True:
    link = Playlist(IUrl)
    bar = IncrementalBar('Progress', max = len(link), suffix='%(percent)d%%')
    for n, i in link.video_urls:
        youtube = YouTube(i)
        title = clearFileName(youtube.title)
        if m == 0:
            stream = youtube.streams.get_highest_resolution()
            stream.download(output_path=ISrc, filename=f"{title}.mp4")
        else:
            stream = youtube.streams.filter(only_audio=True).first()
            stream.download(output_path=ISrc, filename=f"{title}.mp3")
        bar.next()
        print(f'{n}/{len(link)} {title}')
    print('Download completed successfully!')
else:
    print("Error")