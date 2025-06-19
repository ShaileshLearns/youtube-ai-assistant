from pytube import YouTube
import tempfile
import os

async def download_audio(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "audio.mp4")
    stream.download(filename=audio_path)
    return audio_path
