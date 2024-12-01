"""Language configuration and utilities for Ubuntu Language Explorer."""

LANGUAGES = {
    "afrikaans": {
        "name": "Afrikaans",
        "code": "af-ZA",
        "native_name": "Afrikaans",
        "hello": "Hallo",
        "thank_you": "Dankie",
        "how_are_you": "Hoe gaan dit?"
    },
    "english": {
        "name": "English",
        "code": "en-ZA",
        "native_name": "English",
        "hello": "Hello",
        "thank_you": "Thank you",
        "how_are_you": "How are you?"
    },
    "ndebele": {
        "name": "Ndebele",
        "code": "nr-ZA",
        "native_name": "isiNdebele",
        "hello": "Lotjhani",
        "thank_you": "Ngiyathokoza",
        "how_are_you": "Unjani?"
    },
    "pedi": {
        "name": "Northern Sotho (Pedi)",
        "code": "nso-ZA",
        "native_name": "Sepedi",
        "hello": "Dumela",
        "thank_you": "Ke a leboga",
        "how_are_you": "O kae?"
    },
    "sotho": {
        "name": "Southern Sotho",
        "code": "st-ZA",
        "native_name": "Sesotho",
        "hello": "Dumela",
        "thank_you": "Ke a leboha",
        "how_are_you": "O phela joang?"
    },
    "swati": {
        "name": "Swati",
        "code": "ss-ZA",
        "native_name": "SiSwati",
        "hello": "Sawubona",
        "thank_you": "Ngiyabonga",
        "how_are_you": "Unjani?"
    },
    "tsonga": {
        "name": "Tsonga",
        "code": "ts-ZA",
        "native_name": "Xitsonga",
        "hello": "Avuxeni",
        "thank_you": "Ndza khensa",
        "how_are_you": "U njhani?"
    },
    "tswana": {
        "name": "Tswana",
        "code": "tn-ZA",
        "native_name": "Setswana",
        "hello": "Dumela",
        "thank_you": "Ke a leboga",
        "how_are_you": "O kae?"
    },
    "venda": {
        "name": "Venda",
        "code": "ve-ZA",
        "native_name": "Tshivenḓa",
        "hello": "Ndaa",
        "thank_you": "Ndi a livhuwa",
        "how_are_you": "Ni khou ita zwone?"
    },
    "xhosa": {
        "name": "Xhosa",
        "code": "xh-ZA",
        "native_name": "isiXhosa",
        "hello": "Molo",
        "thank_you": "Enkosi",
        "how_are_you": "Unjani?"
    },
    "zulu": {
        "name": "Zulu",
        "code": "zu-ZA",
        "native_name": "isiZulu",
        "hello": "Sawubona",
        "thank_you": "Ngiyabonga",
        "how_are_you": "Unjani?"
    },
    "sasl": {
        "name": "South African Sign Language",
        "code": "sasl",
        "native_name": "SASL",
        "hello": "👋",  # Waving hand sign
        "thank_you": "🙏",  # Folded hands sign
        "how_are_you": "👉❓"  # Pointing to 'you' + question mark
    }
}

# Basic phrases for each language
COMMON_PHRASES = {
    lang_code: {
        "greetings": [
            (lang_info["hello"], "Hello"),
            (lang_info["thank_you"], "Thank you"),
            (lang_info["how_are_you"], "How are you?")
        ],
        "numbers": [
            ("1", "one"),
            ("2", "two"),
            ("3", "three"),
            ("4", "four"),
            ("5", "five")
        ]
    }
    for lang_code, lang_info in LANGUAGES.items()
}

def get_language_code(language_name):
    """Get the language code for a given language name."""
    for code, info in LANGUAGES.items():
        if info["name"].lower() == language_name.lower():
            return info["code"]
    return None

def get_language_name(language_code):
    """Get the language name for a given language code."""
    for code, info in LANGUAGES.items():
        if info["code"] == language_code:
            return info["name"]
    return None

def get_native_name(language_code):
    """Get the native name for a given language code."""
    for code, info in LANGUAGES.items():
        if info["code"] == language_code:
            return info["native_name"]
    return None

def get_all_languages():
    """Get a list of all available languages."""
    return [(info["name"], info["native_name"]) for info in LANGUAGES.values()]

def get_common_phrases(language_code):
    """Get common phrases for a given language code."""
    return COMMON_PHRASES.get(language_code, COMMON_PHRASES["english"])

def is_sign_language(language_code):
    """Check if the given language code is for sign language."""
    return language_code == "sasl"
