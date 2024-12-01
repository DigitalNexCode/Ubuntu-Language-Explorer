import streamlit as st
from utils.languages import LANGUAGES
from utils.audio import AudioService
from gtts import gTTS
import os
import tempfile
from datetime import datetime
import json
import random

# Initialize audio service
audio_service = AudioService()

# Story database
STORIES = {
    "zulu": [
        {
            "title": "UMvelo noMntwana",
            "english_title": "Nature and the Child",
            "content": "Kwesukasukela, kwakukhona umntwana omncane owayethanda kakhulu imvelo...",
            "english_content": "Once upon a time, there was a small child who loved nature very much...",
            "moral": "Respect and protect nature",
            "age_group": "5-8",
            "difficulty": "easy"
        },
        {
            "title": "Umfana Negundane",
            "english_title": "The Boy and the Mouse",
            "content": """
            Kwesukasukela, kwakukhona umfana ogama lakhe kunguThemba. 
            UThemba wayehlala nomndeni wakhe emzini omkhulu.
            Ngelinye ilanga, wabona igundane elincane ekhishini.
            Igundane lalibukeka lilambe kakhulu.
            UThemba walinike iqhezu lesinkwa.
            Kusukela ngalelo langa, igundane laba umngani kaThemba.
            """,
            "english_content": """
            Once upon a time, there was a boy named Themba.
            Themba lived with his family in a big house.
            One day, he saw a small mouse in the kitchen.
            The mouse looked very hungry.
            Themba gave it a piece of bread.
            From that day, the mouse became Themba's friend.
            """,
            "moral": "Help others and they will help you",
            "age_group": "4-7",
            "difficulty": "easy"
        },
        # Add more Zulu stories
    ],
    "xhosa": [
        {
            "title": "UMvundla noNkawu",
            "english_title": "The Rabbit and the Monkey",
            "content": "Kwathi ke kaloku ngantsomi, kwakukho umvundla onobuhlobo nonkawu...",
            "english_content": "Once upon a time, there was a rabbit who was friends with a monkey...",
            "moral": "True friendship overcomes all obstacles",
            "age_group": "6-9",
            "difficulty": "medium"
        },
        {
            "title": "UThabo noMvula",
            "english_title": "Thabo and the Rain",
            "content": """
            Kwathi ke kaloku ngantsomi, kwakukho inkwenkwe egama linguThabo.
            UThabo wayethanda ukudlala emvuleni.
            Ngenye imini kweza imvula enkulu.
            UThabo waphuma waya kudlala.
            Umama wakhe wamxelela ukuba angadlali emvuleni.
            UThabo wamamela umama wakhe waza wangena endlwini.
            """,
            "english_content": """
            Once upon a time, there was a boy named Thabo.
            Thabo loved playing in the rain.
            One day, there was heavy rain.
            Thabo went out to play.
            His mother told him not to play in the rain.
            Thabo listened to his mother and went inside.
            """,
            "moral": "Listen to your parents",
            "age_group": "4-7",
            "difficulty": "easy"
        },
        # Add more Xhosa stories
    ],
    "sotho": [
        {
            "title": "Tau le Tweba",
            "english_title": "The Lion and the Mouse",
            "content": "Ho kile ha eba le tau e matla, e neng e busa naheng...",
            "english_content": "There once was a mighty lion who ruled the land...",
            "moral": "Help others and they will help you",
            "age_group": "4-7",
            "difficulty": "easy"
        },
        {
            "title": "Palesa le Nonyana",
            "english_title": "Palesa and the Bird",
            "content": """
            Ho kile ha eba le ngoanana ea bitsoang Palesa.
            Palesa o ne a rata linonyana haholo.
            Tsatsi le leng a bona nonyana e hlokang thuso.
            A e thusa mme a e fa lijo.
            Nonyana ea fola mme ea bina ea lebohela Palesa.
            Ho tloha tsatsing leo, nonyana ea etela Palesa kamehla.
            """,
            "english_content": """
            There was once a girl named Palesa.
            Palesa loved birds very much.
            One day she saw a bird that needed help.
            She helped it and gave it food.
            The bird healed and sang to thank Palesa.
            From that day, the bird visited Palesa every day.
            """,
            "moral": "Help others and they will help you",
            "age_group": "4-7",
            "difficulty": "easy"
        },
        # Add more Sotho stories
    ]
}

def text_to_speech(text, language):
    """Convert text to speech and return the audio file path"""
    try:
        tts = gTTS(text=text, lang=LANGUAGES[language].get('tts_code', 'en'))
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

def award_points(points):
    """Award points to the user"""
    if 'learning_points' not in st.session_state:
        st.session_state.learning_points = 0
    st.session_state.learning_points += points
    st.success(f"🌟 You earned {points} points!")

def display_story(story, language):
    """Display a story with interactive features"""
    st.subheader(f"📖 {story['title']}")
    st.caption(f"English: {story['english_title']}")
    
    # Story content
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(story['content'])
        st.caption("English translation:")
        st.write(story['english_content'])
    
    with col2:
        # Audio controls
        st.write("🔊 Listen to the story:")
        audio_file = text_to_speech(story['content'], language)
        if audio_file:
            st.audio(audio_file)
            os.unlink(audio_file)  # Clean up temp file
        
        # Story info
        st.info(f"""
        Age Group: {story['age_group']}
        Difficulty: {story['difficulty'].title()}
        Moral: {story['moral']}
        """)
    
    # Interactive elements
    if st.button("Mark as Read ✅"):
        award_points(10)
        if 'read_stories' not in st.session_state:
            st.session_state.read_stories = set()
        st.session_state.read_stories.add(f"{language}_{story['title']}")
        st.success("Great job! Keep reading to earn more points!")

def kids_zone():
    st.title("🎈 Kids Zone")
    st.write("Welcome to the fun and interactive learning zone for kids!")
    
    # Language selection
    selected_language = st.selectbox(
        "Choose your story language:",
        options=[lang for lang in STORIES.keys()],
        format_func=lambda x: f"{LANGUAGES[x]['native_name']} ({LANGUAGES[x]['name']})"
    )
    
    # Story filters
    col1, col2 = st.columns(2)
    with col1:
        age_filter = st.selectbox(
            "Age group:",
            options=["All"] + list(set(story['age_group'] for stories in STORIES.values() for story in stories))
        )
    with col2:
        difficulty_filter = st.selectbox(
            "Difficulty level:",
            options=["All", "easy", "medium", "hard"]
        )
    
    # Display available stories
    if selected_language in STORIES:
        stories = STORIES[selected_language]
        
        # Apply filters
        if age_filter != "All":
            stories = [s for s in stories if s['age_group'] == age_filter]
        if difficulty_filter != "All":
            stories = [s for s in stories if s['difficulty'] == difficulty_filter.lower()]
        
        if stories:
            for story in stories:
                with st.expander(f"📚 {story['title']} ({story['english_title']})"):
                    display_story(story, selected_language)
        else:
            st.info("No stories found matching your filters. Try different filter options!")
    else:
        st.info(f"Stories in {LANGUAGES[selected_language]['name']} coming soon! Check back later.")
    
    # Progress tracking
    if 'read_stories' in st.session_state:
        st.sidebar.subheader("📊 Your Reading Progress")
        st.sidebar.metric("Stories Read", len(st.session_state.read_stories))
        st.sidebar.metric("Points Earned", st.session_state.learning_points)
        
        if len(st.session_state.read_stories) > 0:
            st.sidebar.success("Keep up the great work! 🌟")

if __name__ == "__main__":
    kids_zone()
