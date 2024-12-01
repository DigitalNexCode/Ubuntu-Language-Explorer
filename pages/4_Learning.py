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
    page_title="Learning Resources - Ubuntu Language Explorer",
    page_icon="📖",
    layout="wide"
)

def initialize_session_state():
    if 'current_resource' not in st.session_state:
        st.session_state.current_resource = "Grammar"
    if 'saved_resources' not in st.session_state:
        st.session_state.saved_resources = []

def get_learning_resources():
    return {
        "Grammar": {
            "title": "Grammar Guides",
            "content": {
                "overview": """
                Comprehensive grammar guides for South African languages.
                Learn the structure and rules of each language.
                """,
                "resources": [
                    {
                        "title": "Noun Classes",
                        "description": "Understanding noun classes in Bantu languages",
                        "examples": {
                            "Zulu": [
                                ("umuntu", "person - Class 1"),
                                ("abantu", "people - Class 2"),
                                ("umfula", "river - Class 3")
                            ],
                            "Xhosa": [
                                ("umntu", "person - Class 1"),
                                ("abantu", "people - Class 2"),
                                ("umlambo", "river - Class 3")
                            ]
                        }
                    },
                    {
                        "title": "Verb Conjugation",
                        "description": "Learn how verbs change based on tense and subject",
                        "examples": {
                            "Zulu": [
                                ("ngihamba", "I go"),
                                ("ngihambile", "I went"),
                                ("ngizohamba", "I will go")
                            ],
                            "Xhosa": [
                                ("ndihamba", "I go"),
                                ("ndihambile", "I went"),
                                ("ndizahamba", "I will go")
                            ]
                        }
                    }
                ]
            }
        },
        "Vocabulary": {
            "title": "Vocabulary Lists",
            "content": {
                "overview": """
                Themed vocabulary lists with audio pronunciation and cultural context.
                """,
                "resources": [
                    {
                        "title": "Basic Phrases",
                        "description": "Essential everyday phrases",
                        "examples": {
                            "Zulu": [
                                ("Ngiyabonga", "Thank you"),
                                ("Unjani?", "How are you?"),
                                ("Sala kahle", "Stay well/Goodbye")
                            ],
                            "Xhosa": [
                                ("Enkosi", "Thank you"),
                                ("Unjani?", "How are you?"),
                                ("Sala kakuhle", "Stay well/Goodbye")
                            ]
                        }
                    }
                ]
            }
        },
        "Practice": {
            "title": "Practice Exercises",
            "content": {
                "overview": """
                Interactive exercises to practice what you've learned.
                """,
                "resources": [
                    {
                        "title": "Grammar Drills",
                        "description": "Practice exercises for grammar concepts",
                        "exercises": [
                            {
                                "type": "fill-in-blank",
                                "question": "Complete the sentence: Umuntu ___ kahle (The person ___ well)",
                                "options": ["uhamba", "bahamba", "lihamba"],
                                "correct": "uhamba",
                                "explanation": "Class 1 nouns use 'u-' prefix for subject concord"
                            }
                        ]
                    }
                ]
            }
        }
    }

def display_resource_selection():
    st.sidebar.header("Learning Resources")
    resources = get_learning_resources()
    
    for resource_id, resource_data in resources.items():
        if st.sidebar.button(f"📚 {resource_data['title']}", key=f"resource_{resource_id}"):
            st.session_state.current_resource = resource_id
            st.rerun()

def display_saved_resources():
    st.sidebar.header("Saved Resources")
    if st.session_state.saved_resources:
        for resource in st.session_state.saved_resources:
            st.sidebar.write(f"📌 {resource}")
    else:
        st.sidebar.info("No saved resources yet")

def display_resource_content():
    resources = get_learning_resources()
    current_resource = resources[st.session_state.current_resource]
    
    st.header(current_resource['title'])
    st.write(current_resource['content']['overview'])
    
    for resource in current_resource['content']['resources']:
        with st.expander(resource['title']):
            st.write(resource['description'])
            
            if 'examples' in resource:
                st.subheader("Examples")
                tabs = st.tabs(list(resource['examples'].keys()))
                
                for i, (lang, examples) in enumerate(resource['examples'].items()):
                    with tabs[i]:
                        for example in examples:
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.write(f"**{example[0]}**")
                            with col2:
                                st.write(example[1])
                            with col3:
                                if st.button("🔊", key=f"listen_{lang}_{example[0]}"):
                                    audio_content = audio.text_to_speech(
                                        example[0],
                                        f"{lang.lower()}-ZA"
                                    )
                                    if audio_content:
                                        st.audio(audio_content)
            
            if 'exercises' in resource:
                st.subheader("Practice Exercises")
                for exercise in resource['exercises']:
                    st.write(f"**{exercise['question']}**")
                    answer = st.radio(
                        "Select your answer:",
                        exercise['options'],
                        key=f"exercise_{exercise['question']}"
                    )
                    
                    if st.button("Check", key=f"check_{exercise['question']}"):
                        if answer == exercise['correct']:
                            st.success(f"Correct! {exercise['explanation']}")
                        else:
                            st.error(f"Try again. {exercise['explanation']}")
            
            # Save resource button
            if st.button("📌 Save Resource", key=f"save_{resource['title']}"):
                if resource['title'] not in st.session_state.saved_resources:
                    st.session_state.saved_resources.append(resource['title'])
                    st.success("Resource saved!")

def display_download_section():
    st.markdown("---")
    st.header("📥 Downloadable Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Study Materials")
        st.info("Coming soon: Downloadable PDF guides and worksheets")
    
    with col2:
        st.subheader("Audio Lessons")
        st.info("Coming soon: Downloadable audio lessons for offline learning")

def main():
    initialize_session_state()
    
    # Sidebar
    display_resource_selection()
    display_saved_resources()
    
    # Main content
    display_resource_content()
    display_download_section()

if __name__ == "__main__":
    main()
