import streamlit as st

# Must be the first Streamlit command
st.set_page_config(
    page_title="Profile - Ubuntu Language Explorer",
    page_icon="👤",
    layout="wide"
)

from utils.database import db
from utils.translation import TranslationService
from datetime import datetime

# Initialize services
translator = TranslationService()

def initialize_session_state():
    if 'profile_tab' not in st.session_state:
        st.session_state.profile_tab = "Overview"
    if 'learning_history' not in st.session_state:
        st.session_state.learning_history = []

def get_user_stats():
    """Get user's learning statistics"""
    if not st.session_state.user:
        return None
    
    user_id = st.session_state.user['id']
    return db.get_user_stats(user_id)

def display_profile_navigation():
    """Display profile navigation tabs"""
    tabs = ["Overview", "Progress", "Achievements", "Settings"]
    st.sidebar.title("Profile Navigation")
    
    for tab in tabs:
        if st.sidebar.button(tab):
            st.session_state.profile_tab = tab

def display_profile_overview():
    """Display user profile overview"""
    if not st.session_state.user:
        st.warning("Please sign in to view your profile")
        return

    st.header("Profile Overview")
    
    # User info
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("User Information")
        st.write(f"Email: {st.session_state.user['email']}")
        st.write(f"Member since: {st.session_state.user['created_at']}")
    
    # Learning stats
    with col2:
        st.subheader("Learning Statistics")
        stats = get_user_stats()
        if stats:
            st.metric("Stories Read", stats.get('stories_read', 0))
            st.metric("Lessons Completed", stats.get('lessons_completed', 0))
            st.metric("Practice Sessions", stats.get('practice_sessions', 0))

def display_progress_tracking():
    """Display user's learning progress."""
    progress = db.get_learning_progress(st.session_state.user['id'])
    
    if not progress:
        st.info("No learning progress recorded yet. Start learning to see your progress!")
        return
        
    st.subheader("Learning Progress")
    
    # Group progress by language
    progress_by_language = {}
    for entry in progress:
        lang = entry['language']
        if lang not in progress_by_language:
            progress_by_language[lang] = []
        progress_by_language[lang].append(entry)
    
    # Display progress for each language
    for language, entries in progress_by_language.items():
        with st.expander(f"{language} Progress"):
            for entry in entries:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**{entry['resource_type']}**")
                with col2:
                    st.progress(entry['progress'])
                with col3:
                    status = "Completed" if entry['completed'] else f"{int(entry['progress']*100)}% Complete"
                    st.write(status)

def display_achievements():
    """Display user achievements"""
    if not st.session_state.user:
        st.warning("Please sign in to view your achievements")
        return

    st.header("Achievements")
    
    # Get achievements from database
    achievements = db.get_achievements(st.session_state.user['id'])
    
    if not achievements:
        st.info("Complete lessons and stories to earn achievements!")
        return
    
    # Display achievements in a grid
    col1, col2 = st.columns(2)
    
    for i, achievement in enumerate(achievements):
        with col1 if i % 2 == 0 else col2:
            with st.expander(f"🏆 {achievement['title']}", expanded=True):
                st.write(achievement['description'])
                st.caption(f"Earned on: {achievement['earned_date']}")
                if achievement.get('progress'):
                    st.progress(achievement['progress'])

def display_settings():
    """Display user settings"""
    if not st.session_state.user:
        st.warning("Please sign in to access settings")
        return

    st.header("Settings")
    
    # Get current settings from database with default values
    settings = db.get_user_settings(st.session_state.user['id'])
    
    # Language preferences
    st.subheader("Language Preferences")
    preferred_language = st.selectbox(
        "Preferred Learning Language",
        options=["Zulu", "Xhosa", "Sotho", "Tswana", "Venda", "Tsonga", "Swati", "Ndebele", "Pedi"],
        index=["Zulu", "Xhosa", "Sotho", "Tswana", "Venda", "Tsonga", "Swati", "Ndebele", "Pedi"].index(settings['preferred_language'])
    )
    
    # Notification settings
    st.subheader("Notifications")
    email_notifications = st.checkbox("Email Notifications", value=settings['email_notifications'])
    progress_reminders = st.checkbox("Progress Reminders", value=settings['progress_reminders'])
    
    # Save settings
    if st.button("Save Settings"):
        new_settings = {
            'preferred_language': preferred_language,
            'email_notifications': email_notifications,
            'progress_reminders': progress_reminders
        }
        if db.update_user_settings(st.session_state.user['id'], new_settings):
            st.success("Settings saved successfully!")
            st.rerun()
        else:
            st.error("Failed to save settings. Please try again.")

def main():
    initialize_session_state()
    
    if not st.session_state.get('user'):
        st.warning("Please sign in to access your profile")
        return
    
    display_profile_navigation()
    
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
