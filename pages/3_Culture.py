import streamlit as st
from utils.database import Database
from utils.translation import TranslationService
from utils.audio import AudioService
import json

st.set_page_config(
    page_title="Ubuntu Language - Culture",
    page_icon="🎭",
    layout="wide"
)

# Initialize services
db = Database()
translator = TranslationService()
audio = AudioService()

def main():
    st.title("🎭 Cultural Corner")
    
    if "user" not in st.session_state:
        st.warning("Please sign in to access the Cultural Corner.")
        return
        
    # Get user's preferred language
    user = st.session_state.user
    preferred_language = user.get('preferred_language', 'en')
    
    # Cultural content for South African languages
    cultural_content = {
        'zu': {
            'name': 'Zulu',
            'proverbs': [
                "Umuntu ngumuntu ngabantu - A person is a person through other people",
                "Isandla siyageza esinye - One hand washes the other",
                "Inkosi yinkosi ngabantu - A chief is a chief through his people"
            ],
            'traditions': [
                "Reed Dance (Umkhosi woMhlanga)",
                "Lobola (Marriage customs)",
                "Ancestral ceremonies (Amadlozi)"
            ],
            'festivals': [
                "Umkhosi Womhlanga (Reed Dance Festival)",
                "Umkhosi wokweshwama (First Fruits Festival)",
                "Umgcagco (Traditional Wedding)"
            ]
        },
        'xh': {
            'name': 'Xhosa',
            'proverbs': [
                "Umntu ngumntu ngabantu - A person is a person through others",
                "Inkomo ingazala umniniya - The cow can give birth to its owner",
                "Ubuntu ngumuntu ngabanye abantu - Humanity is a person through other people"
            ],
            'traditions': [
                "Ulwaluko (Male initiation)",
                "Intonjane (Female initiation)",
                "Imbeleko (Child naming ceremony)"
            ],
            'festivals': [
                "Abakwetha (Initiation ceremonies)",
                "Umgidi (Homecoming celebration)",
                "Umthombo (Spring festival)"
            ]
        },
        'af': {
            'name': 'Afrikaans',
            'proverbs': [
                "'n Boer maak 'n plan - A farmer makes a plan",
                "Al dra 'n aap 'n goue ring, bly hy 'n lelike ding - Even if a monkey wears a gold ring, it remains an ugly thing",
                "Die een se dood is die ander se brood - One's death is another's bread"
            ],
            'traditions': [
                "Braai (Barbecue culture)",
                "Volkspele (Folk games)",
                "Boeremusiek (Traditional music)"
            ],
            'festivals': [
                "KKNK (Klein Karoo National Arts Festival)",
                "Aardklop Arts Festival",
                "Innibos Arts Festival"
            ]
        }
    }
    
    # Language selection
    languages = [(code, content['name']) for code, content in cultural_content.items()]
    selected_language = st.selectbox(
        "Choose a language to explore its culture:",
        [code for code, _ in languages],
        format_func=lambda x: next(name for code, name in languages if code == x)
    )
    
    if selected_language:
        content = cultural_content[selected_language]
        
        # Proverbs section
        st.header("📜 Traditional Proverbs")
        for proverb in content['proverbs']:
            with st.expander(f"🔍 {proverb}"):
                if selected_language != 'en':
                    translation = translator.translate(proverb, 'en', selected_language)
                    if translation:
                        st.write(f"Translation: {translation}")
                # Add audio button
                if st.button(f"🔊 Listen", key=f"listen_proverb_{proverb}"):
                    audio_content = audio.text_to_speech(proverb, selected_language)
                    if audio_content:
                        st.audio(audio_content, format='audio/mp3')
        
        # Traditions section
        st.header("🏺 Cultural Traditions")
        for tradition in content['traditions']:
            with st.expander(f"🎯 {tradition}"):
                if selected_language != 'en':
                    translation = translator.translate(tradition, 'en', selected_language)
                    if translation:
                        st.write(f"Translation: {translation}")
                # Add audio button
                if st.button(f"🔊 Listen", key=f"listen_tradition_{tradition}"):
                    audio_content = audio.text_to_speech(tradition, selected_language)
                    if audio_content:
                        st.audio(audio_content, format='audio/mp3')
        
        # Festivals section
        st.header("🎉 Cultural Festivals")
        for festival in content['festivals']:
            with st.expander(f"🎪 {festival}"):
                if selected_language != 'en':
                    translation = translator.translate(festival, 'en', selected_language)
                    if translation:
                        st.write(f"Translation: {translation}")
                # Add audio button
                if st.button(f"🔊 Listen", key=f"listen_festival_{festival}"):
                    audio_content = audio.text_to_speech(festival, selected_language)
                    if audio_content:
                        st.audio(audio_content, format='audio/mp3')

if __name__ == "__main__":
    main()
