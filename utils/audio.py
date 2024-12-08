import os
import io
from gtts import gTTS
import streamlit as st

class AudioService:
    def __init__(self):
        """Initialize audio service with gTTS"""
        print("Initialized AudioService with gTTS")

    def text_to_speech(self, text, language_code='en-US'):
        """Convert text to speech using gTTS"""
        try:
            # Use the base language code (e.g., 'en' from 'en-US')
            base_lang = language_code.split('-')[0]
            tts = gTTS(text=text, lang=base_lang)
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            return audio_bytes.read()
        except Exception as e:
            st.error(f"Text-to-speech failed: {str(e)}")
            return None

    def save_audio_file(self, audio_content, filename):
        """Save audio content to a file"""
        try:
            with open(filename, 'wb') as out:
                out.write(audio_content)
            return True
        except Exception as e:
            st.error(f"Error saving audio file: {str(e)}")
            return False
