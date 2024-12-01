import streamlit as st
from utils.supabase_client import SupabaseClient
from utils.translation import TranslationService
from utils.audio import AudioService

# Initialize services
db = SupabaseClient()
translator = TranslationService()
audio = AudioService()

# Page config
st.set_page_config(
    page_title="Cultural Explorer - Ubuntu Language Explorer",
    page_icon="🌍",
    layout="wide"
)

def initialize_session_state():
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = "Greetings"
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

def get_cultural_topics():
    return {
        "Greetings": {
            "title": "Greetings and Respect",
            "content": {
                "overview": """
                In South African cultures, greetings are more than just saying hello. 
                They are a way of showing respect and acknowledging the humanity in others.
                """,
                "practices": [
                    {
                        "title": "The Importance of Greeting",
                        "description": "Taking time to greet properly shows respect and ubuntu.",
                        "examples": {
                            "Zulu": "Sawubona (I see you)",
                            "Xhosa": "Molo (Hello)",
                            "Sotho": "Dumela (Hello)"
                        }
                    },
                    {
                        "title": "Respect in Language",
                        "description": "Using proper honorifics and titles when addressing elders.",
                        "examples": {
                            "Zulu": "Mama/Baba (Mother/Father)",
                            "Xhosa": "Tata/Mama (Father/Mother)",
                            "Sotho": "Ntate/Mme (Father/Mother)"
                        }
                    }
                ]
            }
        },
        "Family": {
            "title": "Family and Relationships",
            "content": {
                "overview": """
                Family in South African cultures extends beyond immediate relatives.
                The concept of ubuntu emphasizes our interconnectedness.
                """,
                "practices": [
                    {
                        "title": "Extended Family",
                        "description": "Understanding the importance of extended family relationships.",
                        "examples": {
                            "Zulu": "Umndeni (Family)",
                            "Xhosa": "Usapho (Family)",
                            "Sotho": "Lelapa (Family)"
                        }
                    }
                ]
            }
        },
        "Celebrations": {
            "title": "Celebrations and Festivals",
            "content": {
                "overview": """
                Traditional celebrations play a vital role in preserving culture and bringing communities together.
                """,
                "practices": [
                    {
                        "title": "Traditional Ceremonies",
                        "description": "Important life events and their cultural significance.",
                        "examples": {
                            "Zulu": "Umemulo (Coming of age)",
                            "Xhosa": "Intonjane (Girl's initiation)",
                            "Sotho": "Lebollo (Initiation)"
                        }
                    }
                ]
            }
        }
    }

def display_topic_selection():
    st.sidebar.header("Cultural Topics")
    topics = get_cultural_topics()
    
    for topic_id, topic_data in topics.items():
        if st.sidebar.button(f"📚 {topic_data['title']}", key=f"topic_{topic_id}"):
            st.session_state.current_topic = topic_id
            st.rerun()

def display_favorites():
    st.sidebar.header("Your Favorites")
    if st.session_state.favorites:
        for favorite in st.session_state.favorites:
            st.sidebar.write(f"⭐ {favorite}")
    else:
        st.sidebar.info("No favorites yet")

def display_cultural_content():
    topics = get_cultural_topics()
    current_topic = topics[st.session_state.current_topic]
    
    st.header(current_topic['title'])
    
    # Overview
    st.subheader("Overview")
    st.write(current_topic['content']['overview'])
    
    # Cultural Practices
    st.subheader("Cultural Practices")
    for practice in current_topic['content']['practices']:
        with st.expander(practice['title']):
            st.write(practice['description'])
            
            # Language Examples
            st.subheader("Examples in Different Languages")
            cols = st.columns(len(practice['examples']))
            
            for i, (lang, example) in enumerate(practice['examples'].items()):
                with cols[i]:
                    st.write(f"**{lang}:**")
                    st.write(example)
                    
                    # Audio playback
                    if st.button(f"🔊 Listen", key=f"listen_{lang}_{example}"):
                        audio_content = audio.text_to_speech(
                            example,
                            f"{lang.lower()}-ZA"
                        )
                        if audio_content:
                            st.audio(audio_content)
            
            # Cultural context verification
            if st.button("🔍 Verify Cultural Context", key=f"verify_{practice['title']}"):
                context = translator.verify_cultural_context(
                    practice['description'],
                    "English"
                )
                if context:
                    st.info(context)
            
            # Add to favorites
            if st.button("⭐ Add to Favorites", key=f"favorite_{practice['title']}"):
                if practice['title'] not in st.session_state.favorites:
                    st.session_state.favorites.append(practice['title'])
                    st.success("Added to favorites!")

def main():
    initialize_session_state()
    
    # Sidebar
    display_topic_selection()
    display_favorites()
    
    # Main content
    display_cultural_content()
    
    # Additional resources
    st.markdown("---")
    st.subheader("Additional Resources")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("📚 **Recommended Reading**")
        st.info("Coming soon: Curated list of books and articles about South African cultures")
    
    with col2:
        st.write("🎥 **Video Resources**")
        st.info("Coming soon: Cultural documentaries and educational videos")

if __name__ == "__main__":
    main()
