from music_tag import load_file

# def set_tag(file):
#     f = load_file(file)
#     f['title'] = 'Example Title'
#     f['artist'] = 'Example Artist'
#     f.save()

def get_tag(file):
    tag = load_file(file)
    if tag.get('title'):
        print(tag.get('title'))
    if tag.get('artist'):
        print(tag.get('artist'))

get_tag("НОЭМ Обратный отсчет.wav")