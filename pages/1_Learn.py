import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Learn - Ubuntu Language Explorer",
    page_icon="📚",
    layout="wide"
)

from utils.audio import AudioService
from utils.translation import TranslationService
from utils.database import db
from utils.auth import get_current_user
from utils.languages import LANGUAGES, get_language_code, get_native_name, is_sign_language
import time

def initialize_services():
    """Initialize translation and text-to-speech services"""
    global audio, translator
    
    # Initialize translation service (using googletrans)
    translator = TranslationService()
    
    # Initialize text-to-speech (using gTTS)
    audio = AudioService()
    print("Services initialized with local services for text-to-speech and translation")

# Initialize services
initialize_services()

# Check if user is authenticated
user = get_current_user()
if not user:
    st.error("Please sign in to access the learning content.")
    st.stop()

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'daily_challenges' not in st.session_state:
    st.session_state.daily_challenges = {
        'translation': {'target': 10, 'current': 0},
        'learning': {'total': 5, 'current': 0},
        'speaking': {'total': 3, 'current': 0},
        'cultural': {'total': 2, 'current': 0}
    }

# Initialize session state for lesson progress
if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = 1
if 'lesson_complete' not in st.session_state:
    st.session_state.lesson_complete = False
if 'current_level' not in st.session_state:
    st.session_state.current_level = "Beginner"

# Initialize widget IDs
if f"$$WIDGET_ID-ca615b65eeaefac8b139b0fc3c8d0031-q_ceremonies" not in st.session_state:
    st.session_state[f"$$WIDGET_ID-ca615b65eeaefac8b139b0fc3c8d0031-q_ceremonies"] = None

# Initialize learning state
if 'learn_page_tab' not in st.session_state:
    st.session_state.learn_page_tab = "Lessons"
if 'learned_words' not in st.session_state:
    st.session_state.learned_words = set()
if 'practice_history' not in st.session_state:
    st.session_state.practice_history = []

# Lesson content for each level
LESSON_CONTENT = {
    "Beginner": {
        1: {
            "title": "Basic Greetings",
            "description": "Learn essential greetings and introductions.",
            "phrases": [
                ("hello", "Hello"),
                ("thank_you", "Thank you"),
                ("how_are_you", "How are you?")
            ]
        },
        2: {
            "title": "Numbers and Counting",
            "description": "Learn to count and use basic numbers.",
            "phrases": [
                ("one", "One"),
                ("two", "Two"),
                ("three", "Three")
            ]
        },
        3: {
            "title": "Days and Time",
            "description": "Learn days of the week and telling time.",
            "phrases": [
                ("today", "Today"),
                ("tomorrow", "Tomorrow"),
                ("yesterday", "Yesterday")
            ]
        },
        4: {
            "title": "Family Members",
            "description": "Learn words for family relationships.",
            "phrases": [
                ("mother", "Mother"),
                ("father", "Father"),
                ("sister", "Sister")
            ]
        },
        5: {
            "title": "Basic Phrases",
            "description": "Learn common everyday phrases.",
            "phrases": [
                ("please", "Please"),
                ("goodbye", "Goodbye"),
                ("good_morning", "Good morning")
            ]
        }
    },
    "Intermediate": {
        1: {
            "title": "Weather and Seasons",
            "description": "Learn to discuss weather and seasons.",
            "phrases": [
                ("sunny", "Sunny"),
                ("rainy", "Rainy"),
                ("cold", "Cold")
            ]
        },
        2: {
            "title": "Food and Drinks",
            "description": "Learn vocabulary for food and drinks.",
            "phrases": [
                ("water", "Water"),
                ("coffee", "Coffee"),
                ("pizza", "Pizza")
            ]
        },
        3: {
            "title": "Travel and Directions",
            "description": "Learn to ask for directions and discuss travel.",
            "phrases": [
                ("where_is", "Where is..."),
                ("how_much", "How much is this?"),
                ("i_am_lost", "I am lost")
            ]
        },
        4: {
            "title": "Shopping and Numbers",
            "description": "Learn to shop and count in the target language.",
            "phrases": [
                ("how_much_is_this", "How much is this?"),
                ("i_want_to_buy", "I want to buy..."),
                ("do_you_have", "Do you have...?")
            ]
        },
        5: {
            "title": "Emergency and Help",
            "description": "Learn to ask for help and discuss emergencies.",
            "phrases": [
                ("help", "Help!"),
                ("call_police", "Call the police!"),
                ("i_need_doctor", "I need a doctor")
            ]
        }
    },
    "Advanced": {
        1: {
            "title": "Complex Conversations",
            "description": "Learn to handle complex dialogues.",
            "phrases": [
                ("can_you_help", "Can you help me?"),
                ("i_understand", "I understand"),
                ("explain", "Please explain")
            ]
        },
        2: {
            "title": "Debates and Discussions",
            "description": "Learn to engage in debates and discussions.",
            "phrases": [
                ("i_agree", "I agree"),
                ("i_disagree", "I disagree"),
                ("what_do_you_think", "What do you think?")
            ]
        },
        3: {
            "title": "Formal and Informal Language",
            "description": "Learn to use formal and informal language.",
            "phrases": [
                ("hello_formal", "Hello (formal)"),
                ("hello_informal", "Hello (informal)"),
                ("goodbye_formal", "Goodbye (formal)")
            ]
        },
        4: {
            "title": "Idioms and Expressions",
            "description": "Learn common idioms and expressions.",
            "phrases": [
                ("break_a_leg", "Break a leg!"),
                ("call_it_a_day", "Call it a day"),
                ("cost_an_arm_and_a_leg", "Cost an arm and a leg")
            ]
        },
        5: {
            "title": "Business and Professional",
            "description": "Learn business and professional vocabulary.",
            "phrases": [
                ("meeting", "Meeting"),
                ("presentation", "Presentation"),
                ("deadline", "Deadline")
            ]
        }
    }
}

def show_lesson_content(lesson_number, language_code, level):
    st.subheader(f"Lesson {lesson_number}: {LESSON_CONTENT[level][lesson_number]['title']}")
    
    # Get language info
    language_info = None
    for lang, info in LANGUAGES.items():
        if info["code"] == language_code:
            language_info = info
            break
    
    if not language_info:
        st.error(f"Language not found: {language_code}")
        st.write("Available languages:", [info["code"] for info in LANGUAGES.values()])
        return

    # Show lesson description
    st.write(f"### {LESSON_CONTENT[level][lesson_number]['description']}")

    # Get user's progress from database
    user_progress = db.get_learning_progress(st.session_state.user['id'])
    current_lesson_progress = next(
        (p for p in user_progress if p['language'] == language_code and p['level'] == level and p['lesson_id'] == lesson_number),
        None
    ) if user_progress else None

    # Lesson progress tracker
    progress_placeholder = st.empty()
    progress = current_lesson_progress['progress'] if current_lesson_progress else 0.0
    progress_placeholder.progress(progress)

    # Display phrases with audio support and practice
    phrases = LESSON_CONTENT[level][lesson_number]['phrases']
    
    correct_answers = 0
    total_exercises = len(phrases)
    
    for phrase_key, english in phrases:
        st.write("---")
        native = language_info.get(phrase_key, phrase_key)  # Fallback to key if translation not found
        
        col1, col2, col3 = st.columns([2,2,1])
        with col1:
            if is_sign_language(language_code):
                st.write(f"**{native}** (Sign)")
            else:
                st.write(f"**{native}**")
        with col2:
            st.write(english)
        with col3:
            if not is_sign_language(language_code) and audio:
                if st.button("🔊", key=f"play_{native}"):
                    try:
                        audio_content = audio.text_to_speech(native, language_code)
                        st.audio(audio_content, format="audio/mp3")
                    except Exception as e:
                        st.error("Could not play audio")
            elif is_sign_language(language_code):
                st.write("📹")

        # Practice exercise
        user_answer = st.text_input(
            f"Type the correct translation for '{english}' in {language_info['name']}:",
            key=f"exercise_{native}"
        )
        
        if user_answer:
            if user_answer.lower().strip() == native.lower().strip():
                st.success("Correct! 🎉")
                correct_answers += 1
            else:
                st.error(f"Not quite. The correct answer is: {native}")

        # Update progress (as a value between 0 and 1)
        progress = float(correct_answers) / float(total_exercises)
        progress_placeholder.progress(progress)

        # Update progress in database
        db.update_learning_progress(
            user_id=st.session_state.user['id'],
            language=language_code,
            level=level,
            lesson_id=lesson_number,
            progress=progress,
            completed=(progress >= 1.0)
        )

    # Check if lesson is complete
    if correct_answers == total_exercises:
        st.success("🎉 Congratulations! You've completed this lesson!")
        
        # Award XP and update in database
        xp_gained = 50
        db.update_user_xp(st.session_state.user['id'], xp_gained)
        
        # Update daily challenge progress
        db.update_daily_challenge_progress(
            user_id=st.session_state.user['id'],
            challenge_type='learning',
            progress=1
        )
        
        # Show next lesson button if not at last lesson
        if lesson_number < 5:
            if st.button(f"Continue to Lesson {lesson_number + 1} →"):
                st.session_state.current_lesson = lesson_number + 1
                st.rerun()
        else:
            st.success("🎓 Congratulations! You've completed all lessons in this level!")

def show_level_progress(level):
    st.sidebar.subheader("Level Progress")
    # Get progress from database
    user_progress = db.get_learning_progress(st.session_state.user['id'])
    completed_lessons = len([
        p for p in user_progress 
        if p['level'] == level and p['completed']
    ]) if user_progress else 0
    
    total_lessons = 5
    progress = completed_lessons / total_lessons
    st.sidebar.progress(progress)
    st.sidebar.write(f"Completed: {completed_lessons}/{total_lessons} lessons")

def show_practice_section(language_code):
    st.subheader("Practice")
    
    # Get language info
    language_info = None
    for lang, info in LANGUAGES.items():
        if info["code"] == language_code:
            language_info = info
            break
    
    if not language_info:
        st.error("Language not found")
        return

    st.write("Practice what you've learned in the lessons!")
    
    # Random phrase practice
    if st.button("Generate Random Phrase"):
        import random
        phrases = [
            (language_info["hello"], "Hello"),
            (language_info["thank_you"], "Thank you"),
            (language_info["how_are_you"], "How are you?")
        ]
        phrase = random.choice(phrases)
        st.session_state.current_practice_phrase = phrase
        st.session_state.show_answer = False

    if 'current_practice_phrase' in st.session_state:
        native, english = st.session_state.current_practice_phrase
        st.write(f"Translate: **{english}**")
        
        user_answer = st.text_input("Your answer:", key="practice_answer")
        
        if st.button("Check Answer"):
            if user_answer.lower().strip() == native.lower().strip():
                st.success("Correct! 🎉")
                # Award XP for practice
                st.session_state.xp += 10
            else:
                st.error(f"Not quite. The correct answer is: {native}")
        
        if st.button("Play Audio") and not is_sign_language(language_code) and audio:
            try:
                audio_content = audio.text_to_speech(native, language_code)
                st.audio(audio_content, format="audio/mp3")
            except Exception as e:
                st.error("Could not play audio")

def main():
    st.title("📚 Learn")
    
    # Language selection
    language_options = [(info["code"], info["name"], info["native_name"]) 
                       for code, info in LANGUAGES.items()]
    
    # Create a formatted display name for each language
    language_display = [f"{name} ({native})" for _, name, native in language_options]
    selected_index = st.selectbox(
        "Choose your language",
        range(len(language_options)),
        format_func=lambda x: language_display[x],
        key="learn_language"
    )
    
    selected_language_code = language_options[selected_index][0]
    
    # Level selection
    level = st.selectbox(
        "Select your level",
        ["Beginner", "Intermediate", "Advanced"],
        key="learn_level"
    )
    st.session_state.current_level = level
    
    # Main content tabs
    if 'learn_page_tab' not in st.session_state:
        st.session_state.learn_page_tab = "Lessons"
    
    tabs = ["Lessons", "Practice"]
    active_tab = tabs.index(st.session_state.learn_page_tab)
    tab1, tab2 = st.tabs(tabs)
    
    with tab1:
        show_lesson_content(st.session_state.current_lesson, selected_language_code, level)
        show_level_progress(level)
    
    with tab2:
        show_practice_section(selected_language_code)
    
    # Progress tracking
    st.sidebar.header("Progress")
    st.sidebar.progress(st.session_state.xp % 100 / 100)
    st.sidebar.write(f"Level: {st.session_state.level}")
    st.sidebar.write(f"XP: {st.session_state.xp}")
    
    # Daily challenges
    st.sidebar.header("Daily Challenges")
    st.sidebar.write(f"🎯 Translations: {st.session_state.daily_challenges['translation']['current']}/{st.session_state.daily_challenges['translation']['target']}")
    st.sidebar.write(f"📚 Lessons: {st.session_state.daily_challenges['learning']['current']}/{st.session_state.daily_challenges['learning']['total']}")
    st.sidebar.write(f"🗣️ Speaking: {st.session_state.daily_challenges['speaking']['current']}/{st.session_state.daily_challenges['speaking']['total']}")
    st.sidebar.write(f"🏺 Cultural: {st.session_state.daily_challenges['cultural']['current']}/{st.session_state.daily_challenges['cultural']['total']}")
    
    # Try to load logo in sidebar, use text if image is not available
    with st.sidebar:
        try:
            st.image("assets/logo.png", use_container_width=True)
        except:
            st.title("Ubuntu Explorer")
            st.markdown("---")

if __name__ == "__main__":
    main()
