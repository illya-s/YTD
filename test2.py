from pytube import YouTube
import requests
from PIL import Image
from io import BytesIO

video_url = "https://music.youtube.com/watch?v=zWU_9szkSdY&si=v8wNMtA6hHjUoU7U"

yt = YouTube(video_url)

thumbnail_url = yt.thumbnail_url

response = requests.get(thumbnail_url)
img = Image.open(BytesIO(response.content))

img.save("thumbnail.png", "PNG")

print("Thumbnail saved as 'thumbnail.png'")