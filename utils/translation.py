"""Translation service with fallback mechanisms for South African languages."""
import os
from typing import Optional
from google.cloud.translate_v3 import TranslationServiceClient
from retry_requests import retry
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TranslationService:
    def __init__(self):
        # Set Google Cloud credentials path
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(credentials_path)
        
        # Initialize Google Cloud Translation if credentials are available
        try:
            self.google_translate_client = TranslationServiceClient()
            self.has_google_translate = True
        except Exception as e:
            print(f"Google Cloud Translation initialization failed: {str(e)}")
            self.google_translate_client = None
            self.has_google_translate = False
            print("Using fallback translation mechanisms.")
            
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = "global"
        
        # Initialize Lelapa AI (Vulavula)
        self.vulavula_token = os.getenv("LELAPA_API_KEY")
        self.vulavula_translation_url = "https://vulavula-services.lelapa.ai/api/v1/translate/process"
        
        # Initialize Google Gemini if API key is available
        self.gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
            self.has_gemini = True
        else:
            self.gemini_model = None
            self.has_gemini = False
            print("Google Gemini not available. Using fallback mechanisms.")
        
        # Cultural features by language
        self.cultural_features = {
            "zu": {
                "greetings": {
                    "morning": "Sawubona ekuseni",
                    "afternoon": "Sawubona emini",
                    "evening": "Sawubona kusihlwa",
                    "respect_elder": "Sanibonani",
                },
                "honorifics": {
                    "elder": "Baba/Mama",
                    "chief": "iNkosi",
                    "respected": "Mnumzane/Nkosikazi",
                },
                "proverbs": [
                    ("Umuntu ngumuntu ngabantu", "A person is a person through other people"),
                    ("Izandla ziyagezana", "Hands wash each other (mutual help)"),
                ],
            },
            "xh": {
                "greetings": {
                    "morning": "Molo ngale ntsasa",
                    "afternoon": "Molo emini",
                    "evening": "Molo ngokuhlwa",
                    "respect_elder": "Molweni",
                },
                "honorifics": {
                    "elder": "Tata/Mama",
                    "chief": "iNkosi",
                    "respected": "Mnumzana/Nkosikazi",
                },
                "proverbs": [
                    ("Umntu ngumntu ngabantu", "A person is a person through other people"),
                    ("Isandla sihlamba esinye", "One hand washes the other"),
                ],
            },
            "af": {
                "greetings": {
                    "morning": "Goeie môre",
                    "afternoon": "Goeie middag",
                    "evening": "Goeie naand",
                    "respect_elder": "Goeie dag",
                },
                "honorifics": {
                    "elder": "Oom/Tannie",
                    "respected": "Meneer/Mevrou",
                },
                "proverbs": [
                    ("'n Boer maak 'n plan", "A farmer makes a plan (resourcefulness)"),
                    ("Alle baat help", "Every little bit helps"),
                ],
            },
            # Add more languages with their cultural features
        }
        
        # Language code mappings
        self.google_codes = {
            "af": "af-ZA",  # Afrikaans
            "en": "en-ZA",  # English
            "nr": "nr-ZA",  # Ndebele
            "nso": "nso-ZA",  # Northern Sotho
            "st": "st-ZA",  # Southern Sotho
            "ss": "ss-ZA",  # Swati
            "ts": "ts-ZA",  # Tsonga
            "tn": "tn-ZA",  # Tswana
            "ve": "ve-ZA",  # Venda
            "xh": "xh-ZA",  # Xhosa
            "zu": "zu-ZA",  # Zulu
        }
        
        self.vulavula_codes = {
            "af": "afr_Latn",  # Afrikaans
            "zu": "zul_Latn",  # isiZulu
            "st": "sot_Latn",  # Sesotho
            "ss": "ssw_Latn",  # Swati
            "ts": "tso_Latn",  # Tsonga
            "en": "eng_Latn",  # English
            "xh": "xho_Latn",  # isiXhosa
            "tn": "tsn_Latn",  # Setswana
            "nr": "nbl_Latn",  # isiNdebele
            "ve": "ven_Latn",  # Tshivenda
            "nso": "nso_Latn", # Sepedi
        }

    def get_cultural_features(self, language_code: str) -> dict:
        """Get cultural features for a specific language."""
        code = language_code.split('-')[0]
        return self.cultural_features.get(code, {})

    def get_appropriate_greeting(self, language_code: str, time_of_day: str, is_elder: bool = False) -> str:
        """Get culturally appropriate greeting based on context."""
        code = language_code.split('-')[0]
        features = self.cultural_features.get(code, {})
        greetings = features.get("greetings", {})
        
        if is_elder and "respect_elder" in greetings:
            return greetings["respect_elder"]
        
        return greetings.get(time_of_day, greetings.get("morning", ""))

    def get_honorific(self, language_code: str, context: str) -> str:
        """Get appropriate honorific for the given context."""
        code = language_code.split('-')[0]
        features = self.cultural_features.get(code, {})
        honorifics = features.get("honorifics", {})
        return honorifics.get(context, "")

    def get_proverbs(self, language_code: str) -> list:
        """Get proverbs for a specific language."""
        code = language_code.split('-')[0]
        features = self.cultural_features.get(code, {})
        return features.get("proverbs", [])

    def translate_text(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """Translate text using available translation services with fallback mechanisms."""
        # Try Google Cloud Translation first if available
        if self.has_google_translate and self.project_id:
            try:
                parent = f"projects/{self.project_id}/locations/{self.location}"
                response = self.google_translate_client.translate_text(
                    request={
                        "parent": parent,
                        "contents": [text],
                        "target_language_code": target_language,
                        "source_language_code": source_language,
                    }
                )
                return response.translations[0].translated_text
            except Exception as e:
                print(f"Google Cloud Translation failed: {str(e)}")
                # Continue to fallback mechanisms
        
        # Try Vulavula API if available
        if self.vulavula_token:
            try:
                headers = {"Authorization": f"Bearer {self.vulavula_token}"}
                data = {
                    "text": text,
                    "source_language": source_language or "en",
                    "target_language": target_language
                }
                response = requests.post(self.vulavula_translation_url, headers=headers, json=data)
                if response.status_code == 200:
                    return response.json()["translation"]
            except Exception as e:
                print(f"Vulavula translation failed: {str(e)}")
                # Continue to fallback mechanisms
        
        # Try Gemini as last resort if available
        if self.has_gemini:
            try:
                prompt = f"Translate the following text from {source_language or 'English'} to {target_language}:\n{text}"
                response = self.gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Gemini translation failed: {str(e)}")
        
        # If all translation services fail, return original text
        print("All translation services failed. Returning original text.")
        return text

    def is_language_supported(self, language_code: str) -> bool:
        """Check if a language is supported by any translation service."""
        code = language_code.split('-')[0]
        return (code in self.google_codes or 
                code in self.vulavula_codes)

    def _google_translate(self, text: str, target_language: str) -> Optional[str]:
        """Translate using Google Cloud Translation."""
        try:
            parent = f"projects/{self.project_id}/locations/{self.location}"
            response = self.google_translate_client.translate_text(
                request={
                    "parent": parent,
                    "contents": [text],
                    "mime_type": "text/plain",
                    "target_language_code": target_language,
                }
            )
            return response.translations[0].translated_text
        except Exception as e:
            print(f"Google Translate error: {e}")
            return None

    def _vulavula_translate(self, text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """Translate using Lelapa AI's Vulavula API."""
        try:
            response = requests.post(
                self.vulavula_translation_url,
                json={
                    "input_text": text,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                },
                headers={"X-CLIENT-TOKEN": self.vulavula_token},
            )
            return response.json().get("translated_text")
        except Exception as e:
            print(f"Vulavula translation error: {e}")
            return None

    def _gemini_translate(self, text: str, target_language: str, context: Optional[str] = None) -> Optional[str]:
        """Use Google Gemini for complex translations and cultural context."""
        try:
            context_prompt = f"\nContext: {context}" if context else ""
            prompt = f"""
            Translate the following text to {target_language}, 
            maintaining cultural context and nuances specific to South African languages.
            {context_prompt}
            
            Text: {text}
            
            Consider:
            1. Cultural context and idioms
            2. Local expressions and colloquialisms
            3. Formal vs informal tone
            4. Traditional references
            5. Appropriate honorifics and respect levels
            6. Regional variations
            """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini translation error: {e}")
            return None

    def translate(self, text: str, source_lang: str, target_lang: str, context: Optional[str] = None) -> str:
        """
        Multi-layered translation approach:
        1. Try Google Translate for common phrases
        2. Use Vulavula for South African language specifics
        3. Fall back to Gemini for complex cases
        """
        # Convert language codes
        google_target = self.google_codes.get(target_lang.split('-')[0], target_lang)
        vulavula_source = self.vulavula_codes.get(source_lang.split('-')[0], None)
        vulavula_target = self.vulavula_codes.get(target_lang.split('-')[0], None)
        
        # Try Google Translate first for simple phrases
        result = self._google_translate(text, google_target)
        
        # If available and needed, try Vulavula for South African languages
        if (not result or len(text.split()) > 3) and vulavula_source and vulavula_target:
            vulavula_result = self._vulavula_translate(text, vulavula_source, vulavula_target)
            if vulavula_result:
                result = vulavula_result
        
        # For complex phrases or when context is provided, use Gemini
        if (not result or len(text.split()) > 5 or context):
            gemini_result = self._gemini_translate(text, target_lang, context)
            if gemini_result:
                result = gemini_result
        
        return result or text
