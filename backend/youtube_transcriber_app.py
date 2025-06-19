import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable, NoTranscriptFound
from pytube import YouTube
import whisper
import os
import tempfile

# Helper function to extract video ID
def get_video_id(url):
    import re
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

# Transcribe audio using Whisper
def transcribe_with_whisper(audio_path):
    model = whisper.load_model("base")  # You can use "small", "medium", "large"
    result = model.transcribe(audio_path)
    return result["text"]

# Download audio from YouTube
def download_audio(youtube_url):
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).first()
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "audio.mp4")
    stream.download(filename=audio_path)
    return audio_path

# Streamlit UI
st.set_page_config(page_title="YouTube Transcript Generator", layout="centered")
st.title("🎬 YouTube Video Transcript Generator")

youtube_url = st.text_input("Enter YouTube Video URL")

if st.button("Generate Transcript"):
    if not youtube_url:
        st.warning("Please enter a YouTube URL.")
    else:
        video_id = get_video_id(youtube_url)
        if not video_id:
            st.error("Invalid YouTube URL format.")
        else:
            try:
                st.info("🔍 Trying to fetch transcript using YouTubeTranscriptApi...")
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                full_text = " ".join([seg["text"] for seg in transcript])
                st.success("✅ Transcript fetched from subtitles!")
                st.text_area("Transcript", full_text, height=400)
            except (TranscriptsDisabled, NoTranscriptFound):
                st.warning("❌ Subtitles unavailable. Falling back to Whisper...")
                try:
                    with st.spinner("Downloading audio and transcribing with Whisper..."):
                        audio_path = download_audio(youtube_url)
                        transcript_text = transcribe_with_whisper(audio_path)
                        st.success("✅ Transcript generated with Whisper!")
                        st.text_area("Transcript", transcript_text, height=400)
                except Exception as e:
                    st.error(f"Whisper transcription failed: {e}")
            except VideoUnavailable:
                st.error("❌ Video is unavailable.")
            except Exception as e:
                st.error(f"Error: {e}")
