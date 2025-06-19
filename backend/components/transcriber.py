from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from components.downloader import download_audio
import whisper
import re

def get_video_id(url: str):
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

async def generate_transcript(url: str):
    video_id = get_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([seg["text"] for seg in transcript])
    except (TranscriptsDisabled, NoTranscriptFound):
        audio_path = await download_audio(url)
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
