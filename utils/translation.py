"""Translation service with fallback mechanisms for South African languages."""
import os
from typing import Optional
from googletrans import Translator

class TranslationService:
    def __init__(self):
        """Initialize the translation service with fallback to googletrans"""
        self.translator = Translator()
        self.use_fallback = True
        print("Using googletrans as translation service")

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

    def translate(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """Translate text to target language"""
        try:
            if source_language:
                result = self.translator.translate(text, dest=target_language, src=source_language)
            else:
                result = self.translator.translate(text, dest=target_language)
            return result.text
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return text  # Return original text if translation fails

    def detect_language(self, text: str) -> str:
        """Detect the language of the text"""
        try:
            result = self.translator.detect(text)
            return result.lang
        except Exception as e:
            print(f"Language detection error: {str(e)}")
            return "en"  # Default to English if detection fails

    def is_language_supported(self, language_code: str) -> bool:
        """Check if a language is supported by any translation service."""
        code = language_code.split('-')[0]
        return (code in self.google_codes or 
                code in self.vulavula_codes)
