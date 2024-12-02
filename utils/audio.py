import os
import json
import base64
from google.cloud import texttospeech
from google.cloud import speech_v1 as speech
from google.oauth2 import service_account
from dotenv import load_dotenv
from gtts import gTTS
import streamlit as st
import io

load_dotenv()

class AudioService:
    def __init__(self):
        try:
            # Try to initialize Google Cloud clients
            credentials = service_account.Credentials.from_service_account_info(
                st.secrets["google_credentials"]
            )
            self.tts_client = texttospeech.TextToSpeechClient(credentials=credentials)
            self.speech_client = speech.SpeechClient(credentials=credentials)
            self.using_google_cloud = True
        except Exception as e:
            st.warning("Failed to initialize Google Cloud clients: " + str(e))
            st.info("Falling back to gTTS for text-to-speech")
            self.using_google_cloud = False

    def text_to_speech(self, text, language_code='en-US'):
        if self.using_google_cloud:
            try:
                synthesis_input = texttospeech.SynthesisInput(text=text)
                voice = texttospeech.VoiceSelectionParams(
                    language_code=language_code,
                    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3
                )
                response = self.tts_client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice,
                    audio_config=audio_config
                )
                return response.audio_content
            except Exception as e:
                st.warning(f"Google Cloud TTS failed: {str(e)}. Falling back to gTTS.")
                return self._fallback_tts(text, language_code)
        else:
            return self._fallback_tts(text, language_code)

    def _fallback_tts(self, text, language_code):
        try:
            tts = gTTS(text=text, lang=language_code.split('-')[0])
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            return audio_bytes.read()
        except Exception as e:
            st.error(f"Text-to-speech failed: {str(e)}")
            return None

    def transcribe_audio(self, audio_bytes, language_code='en-US'):
        if self.using_google_cloud:
            try:
                audio = speech.RecognitionAudio(content=audio_bytes)
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000,
                    language_code=language_code,
                )
                response = self.speech_client.recognize(config=config, audio=audio)
                return response.results[0].alternatives[0].transcript if response.results else ""
            except Exception as e:
                st.error(f"Speech recognition failed: {str(e)}")
                return ""
        else:
            st.error("Speech recognition requires Google Cloud Speech-to-Text API")
            return ""

    def save_audio_file(self, audio_content, filename):
        try:
            with open(filename, 'wb') as out:
                out.write(audio_content)
            return True
        except Exception as e:
            st.error(f"Error saving audio file: {str(e)}")
            return False
