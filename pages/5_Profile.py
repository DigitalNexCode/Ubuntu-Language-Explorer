import streamlit as st
from utils.supabase_client import SupabaseClient
from utils.translation import TranslationService
from datetime import datetime

# Initialize services
db = SupabaseClient()
translator = TranslationService()

# Page config
st.set_page_config(
    page_title="User Profile - Ubuntu Language Explorer",
    page_icon="👤",
    layout="wide"
)

def initialize_session_state():
    if 'profile_tab' not in st.session_state:
        st.session_state.profile_tab = "Overview"
    if 'learning_history' not in st.session_state:
        st.session_state.learning_history = []
    if 'achievements' not in st.session_state:
        st.session_state.achievements = []
    if 'preferences' not in st.session_state:
        st.session_state.preferences = {
            "primary_language": "English",
            "learning_languages": ["Zulu"],
            "difficulty_level": "Beginner",
            "daily_goal": 30,  # minutes
            "preferred_topics": ["Culture", "Grammar"]
        }

def get_user_stats():
    # In a real app, these would come from the database
    return {
        "total_lessons": len(st.session_state.learning_history),
        "languages_learning": len(st.session_state.preferences["learning_languages"]),
        "achievements_earned": len(st.session_state.achievements),
        "streak_days": 5  # Placeholder
    }

def display_profile_navigation():
    st.sidebar.header("Profile Sections")
    sections = ["Overview", "Progress", "Achievements", "Settings"]
    
    for section in sections:
        if st.sidebar.button(f"👉 {section}", key=f"nav_{section}"):
            st.session_state.profile_tab = section
            st.rerun()

def display_profile_overview():
    st.header("Profile Overview")
    
    # User info
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/150", caption="Profile Picture")
    with col2:
        st.subheader("Welcome back!")
        st.write("Member since: January 2024")
        st.write(f"Primary Language: {st.session_state.preferences['primary_language']}")
        st.write("Learning: " + ", ".join(st.session_state.preferences["learning_languages"]))
    
    # Quick stats
    st.subheader("Your Learning Journey")
    stats = get_user_stats()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Lessons", stats["total_lessons"])
    with col2:
        st.metric("Languages Learning", stats["languages_learning"])
    with col3:
        st.metric("Achievements", stats["achievements_earned"])
    with col4:
        st.metric("Day Streak", stats["streak_days"])

def display_progress_tracking():
    st.header("Learning Progress")
    
    # Language progress
    for language in st.session_state.preferences["learning_languages"]:
        with st.expander(f"{language} Progress"):
            # Progress bars for different skills
            st.subheader("Skills Progress")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("Grammar")
                st.progress(0.7)
                st.write("Vocabulary")
                st.progress(0.5)
            
            with col2:
                st.write("Pronunciation")
                st.progress(0.3)
                st.write("Cultural Knowledge")
                st.progress(0.6)
            
            # Recent activity
            st.subheader("Recent Activity")
            if st.session_state.learning_history:
                for activity in st.session_state.learning_history[-5:]:
                    st.write(f"📝 {activity}")
            else:
                st.info("No learning activity recorded yet")

def display_achievements():
    st.header("Achievements")
    
    # Achievement categories
    categories = {
        "Language Mastery": [
            {
                "title": "First Steps",
                "description": "Complete your first lesson",
                "icon": "🎯",
                "earned": True
            },
            {
                "title": "Grammar Guru",
                "description": "Master 10 grammar concepts",
                "icon": "📚",
                "earned": False
            }
        ],
        "Cultural Explorer": [
            {
                "title": "Cultural Pioneer",
                "description": "Learn about 5 cultural traditions",
                "icon": "🌍",
                "earned": True
            },
            {
                "title": "Story Collector",
                "description": "Read 10 traditional stories",
                "icon": "📖",
                "earned": False
            }
        ]
    }
    
    for category, achievements in categories.items():
        st.subheader(category)
        cols = st.columns(len(achievements))
        
        for i, achievement in enumerate(achievements):
            with cols[i]:
                st.write(f"{achievement['icon']} **{achievement['title']}**")
                st.write(achievement['description'])
                if achievement['earned']:
                    st.success("Earned! 🏆")
                else:
                    st.info("In Progress...")

def display_settings():
    st.header("Profile Settings")
    
    with st.form("profile_settings"):
        # Language preferences
        st.subheader("Language Settings")
        primary_language = st.selectbox(
            "Primary Language",
            ["English", "Zulu", "Xhosa", "Sotho"],
            index=["English", "Zulu", "Xhosa", "Sotho"].index(
                st.session_state.preferences["primary_language"]
            )
        )
        
        learning_languages = st.multiselect(
            "Languages I'm Learning",
            ["Zulu", "Xhosa", "Sotho", "Tswana"],
            default=st.session_state.preferences["learning_languages"]
        )
        
        # Learning preferences
        st.subheader("Learning Preferences")
        difficulty = st.select_slider(
            "Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"],
            value=st.session_state.preferences["difficulty_level"]
        )
        
        daily_goal = st.number_input(
            "Daily Learning Goal (minutes)",
            min_value=5,
            max_value=240,
            value=st.session_state.preferences["daily_goal"],
            step=5
        )
        
        preferred_topics = st.multiselect(
            "Preferred Learning Topics",
            ["Grammar", "Vocabulary", "Culture", "Conversation", "Reading", "Writing"],
            default=st.session_state.preferences["preferred_topics"]
        )
        
        # Save button
        if st.form_submit_button("Save Changes"):
            st.session_state.preferences.update({
                "primary_language": primary_language,
                "learning_languages": learning_languages,
                "difficulty_level": difficulty,
                "daily_goal": daily_goal,
                "preferred_topics": preferred_topics
            })
            st.success("Settings saved successfully!")

def main():
    initialize_session_state()
    
    # Sidebar navigation
    display_profile_navigation()
    
    # Main content based on selected tab
    if st.session_state.profile_tab == "Overview":
        display_profile_overview()
    elif st.session_state.profile_tab == "Progress":
        display_progress_tracking()
    elif st.session_state.profile_tab == "Achievements":
        display_achievements()
    elif st.session_state.profile_tab == "Settings":
        display_settings()

if __name__ == "__main__":
    main()
