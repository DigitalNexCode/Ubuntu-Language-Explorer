import os
import json
import base64
from google.cloud import texttospeech
from google.cloud import speech
from google.oauth2 import service_account
from dotenv import load_dotenv
from gtts import gTTS
import io

class AudioService:
    def __init__(self):
        load_dotenv()
        self.tts_client = None
        self.stt_client = None
        self.use_fallback = False
        
        # Try to initialize Google Cloud clients
        try:
            # Check for credentials in environment variable
            creds_json = os.getenv('GOOGLE_CLOUD_CREDENTIALS')
            if creds_json:
                # If credentials are provided as a JSON string
                creds_dict = json.loads(creds_json)
                credentials = service_account.Credentials.from_service_account_info(creds_dict)
            else:
                # If credentials are provided as a file path
                creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
                if creds_path and os.path.exists(creds_path):
                    credentials = service_account.Credentials.from_service_account_file(creds_path)
                else:
                    raise ValueError("No valid Google Cloud credentials found")
            
            self.tts_client = texttospeech.TextToSpeechClient(credentials=credentials)
            self.stt_client = speech.SpeechClient(credentials=credentials)
            print("Successfully initialized Google Cloud clients")
        except Exception as e:
            print(f"Warning: Failed to initialize Google Cloud clients: {e}")
            print("Falling back to gTTS for text-to-speech")
            self.use_fallback = True

    def text_to_speech(self, text, language_code):
        try:
            if not self.use_fallback and self.tts_client:
                # Use Google Cloud Text-to-Speech
                synthesis_input = texttospeech.SynthesisInput(text=text)
                
                # Clean up language code (e.g., 'zulu-ZA' -> 'zu-ZA')
                lang_code = language_code.lower()
                if 'zulu' in lang_code:
                    lang_code = 'zu-ZA'
                elif 'xhosa' in lang_code:
                    lang_code = 'xh-ZA'
                elif 'sotho' in lang_code:
                    lang_code = 'st-ZA'
                elif 'tswana' in lang_code:
                    lang_code = 'tn-ZA'
                elif 'english' in lang_code:
                    lang_code = 'en-ZA'

                voice = texttospeech.VoiceSelectionParams(
                    language_code=lang_code,
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
            else:
                # Fallback to gTTS
                print(f"Using gTTS fallback for language: {language_code}")
                # Convert language code to gTTS format
                lang_code = language_code.split('-')[0].lower()
                if lang_code == 'zulu':
                    lang_code = 'zu'
                elif lang_code == 'xhosa':
                    lang_code = 'xh'
                elif lang_code == 'sotho':
                    lang_code = 'st'
                elif lang_code == 'tswana':
                    lang_code = 'tn'
                
                tts = gTTS(text=text, lang=lang_code)
                audio_bytes = io.BytesIO()
                tts.write_to_fp(audio_bytes)
                return audio_bytes.getvalue()

        except Exception as e:
            print(f"Error in text_to_speech: {e}")
            return None

    def speech_to_text(self, audio_content, language_code):
        if not self.stt_client:
            print("Speech-to-text is not available in fallback mode")
            return None
            
        try:
            audio = speech.RecognitionAudio(content=audio_content)
            
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code,
            )

            response = self.stt_client.recognize(config=config, audio=audio)

            return response.results[0].alternatives[0].transcript if response.results else None
        except Exception as e:
            print(f"Error in speech_to_text: {e}")
            return None

    def get_supported_voices(self, language_code=None):
        try:
            response = self.tts_client.list_voices()
            voices = []
            
            for voice in response.voices:
                if language_code is None or language_code in voice.language_codes:
                    voices.append({
                        'name': voice.name,
                        'language_codes': voice.language_codes,
                        'gender': voice.ssml_gender.name
                    })
            
            return voices
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []

    def save_audio_file(self, audio_content, filename):
        try:
            with open(filename, 'wb') as out:
                out.write(audio_content)
            return True
        except Exception as e:
            print(f"Error saving audio file: {e}")
            return False
