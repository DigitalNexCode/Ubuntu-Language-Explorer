import os
import time
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit.runtime.scriptrunner import get_script_run_ctx, add_script_run_ctx
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
from utils.auth import sign_up, sign_in, sign_out, get_current_user
from utils.database import Database
from utils.audio import AudioService
from utils.translation import TranslationService
from gtts import gTTS
import io
from utils.session import init_session_state, set_current_user, clear_current_user
import bcrypt

# Must be the first Streamlit command
st.set_page_config(
    page_title="Ubuntu Language Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables first
load_dotenv()

# Initialize services with better error handling
db = None
translator = None
audio = None

def init_services():
    """Initialize all required services with proper error handling."""
    global db  # Add this line to make db global
    services = {
        'supabase': None,
        'translation': None,
        'tts': None,
        'ai': None
    }
    
    # Initialize Database
    try:
        db = Database()  # Assign the database instance
        services['supabase'] = db
        print("✅ Database initialized successfully")
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        st.stop()
    
    # Set fallback mode for other services
    services['translation'] = None  # Will use fallback translation
    services['tts'] = gTTS  # Using gTTS for text-to-speech
    services['ai'] = None  # Will use fallback AI features
    
    return services

# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    # Authentication state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Navigation state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # User progress state
    if 'xp' not in st.session_state:
        st.session_state.xp = 0
    
    if 'level' not in st.session_state:
        st.session_state.level = 1
    
    if 'achievements' not in st.session_state:
        st.session_state.achievements = []
    
    # Daily activity tracking
    if 'translations_today' not in st.session_state:
        st.session_state.translations_today = 0
    
    if 'words_learned_today' not in st.session_state:
        st.session_state.words_learned_today = 0
    
    if 'practice_sessions_today' not in st.session_state:
        st.session_state.practice_sessions_today = 0
    
    if 'last_activity_date' not in st.session_state:
        st.session_state.last_activity_date = None
    
    if 'daily_streak' not in st.session_state:
        st.session_state.daily_streak = 0
    
    # Daily challenges
    if 'daily_challenges' not in st.session_state:
        st.session_state.daily_challenges = {
            'learning': {'total': 5, 'current': 0},
            'speaking': {'total': 3, 'current': 0},
            'cultural': {'total': 2, 'current': 0},
            'translation': {'target': 10, 'current': 0}
        }
    
    # Learning state
    if 'learn_page_tab' not in st.session_state:
        st.session_state.learn_page_tab = "Lessons"
    
    if 'learned_words' not in st.session_state:
        st.session_state.learned_words = set()
    
    if 'practice_history' not in st.session_state:
        st.session_state.practice_history = []
    
    if 'skill_levels' not in st.session_state:
        st.session_state.skill_levels = {
            'vocabulary': 1,
            'grammar': 1,
            'pronunciation': 1,
            'comprehension': 1,
            'cultural': 1
        }
    
    # Authentication UI state
    if 'show_resend_signup' not in st.session_state:
        st.session_state.show_resend_signup = False
    
    if 'show_resend_signin' not in st.session_state:
        st.session_state.show_resend_signin = False
    
    if 'resend_email' not in st.session_state:
        st.session_state.resend_email = ""
    
    # User information
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if 'email' not in st.session_state:
        st.session_state.email = None
    
    # Language settings
    if 'current_language' not in st.session_state:
        st.session_state.current_language = 'Zulu'
    
    if 'interface_language' not in st.session_state:
        st.session_state.interface_language = 'English'
    
    # Feature flags
    if 'use_fallback' not in st.session_state:
        st.session_state.use_fallback = True
    
    if 'features' not in st.session_state:
        st.session_state.features = {
            'database': True,  # Database connectivity
            'translation': True,  # Translation service
            'tts': True,  # Text-to-speech
            'ai': True,  # AI features
            'offline_mode': False  # Offline functionality
        }
    
    # User activity tracking
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = None
    
    # Progress tracking
    if 'progress' not in st.session_state:
        st.session_state.progress = {
            'learning_points': 0,
            'daily_streak': 0,
            'translations_today': 0,
            'lessons_completed': 0,
            'current_level': 1,
            'xp': 0
        }
    
    # Achievements and challenges
    if 'daily_challenges' not in st.session_state:
        st.session_state.daily_challenges = {
            'translation': {'target': 10, 'current': 0},
            'learning': {'target': 3, 'current': 0},
            'cultural': {'target': 1, 'current': 0}
        }
    
    # UI state
    if 'learn_page_tab' not in st.session_state:
        st.session_state.learn_page_tab = "Lessons"
    
    # Add new session state variables for resend confirmation
    if 'show_resend_signup' not in st.session_state:
        st.session_state.show_resend_signup = False
    
    if 'show_resend_signin' not in st.session_state:
        st.session_state.show_resend_signin = False
    
    if 'resend_email' not in st.session_state:
        st.session_state.resend_email = ""

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def show_login():
    """Show login form"""
    st.header("Sign In")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")
        
        if submitted and email and password:
            user = db.get_user(email)
            if user and verify_password(password, user['password_hash']):
                set_current_user(user)
                st.success("Successfully signed in!")
                st.rerun()
            else:
                st.error("Invalid email or password")

def show_register():
    """Show registration form"""
    st.header("Create Account")
    
    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            if not email or not password or not confirm_password:
                st.error("Please fill in all required fields")
                return
                
            if password != confirm_password:
                st.error("Passwords do not match")
                return
                
            try:
                # Create user
                result = db.create_user(
                    email=email,
                    password_hash=hash_password(password)
                )
                
                if result.get('success'):
                    st.success("Account created successfully! Please sign in.")
                    st.session_state.show_login = True
                    st.rerun()
                else:
                    st.error(f"Error creating account: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error creating account: {str(e)}")

def show_welcome():
    """Show welcome message for authenticated users"""
    user = st.session_state.user
    st.header(f"Welcome, {user.get('first_name', 'User')}! 👋")
    
    st.write("""
    Welcome to Ubuntu Language! Here's what you can do:
    
    1. 📚 **Learn**: Start learning a new language with interactive lessons
    2. 🎮 **Games**: Practice through fun language games
    3. 🎭 **Culture**: Explore the rich cultural heritage
    4. 👥 **Community**: Connect with other learners
    5. 👤 **Profile**: Track your progress and manage settings
    """)
    
    if st.button("Sign Out"):
        clear_current_user()
        st.rerun()

def show_auth_section():
    """Display authentication section with improved error handling."""
    if not st.session_state.authenticated:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Sign Up")
            with st.form("signup_form"):
                username = st.text_input("Username (min 3 characters)", key="signup_username")
                email = st.text_input("Email", key="signup_email")
                password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
                signup_button = st.form_submit_button("Sign Up")
                
                if signup_button:
                    if len(username) < 3:
                        st.error("Username must be at least 3 characters long")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif not email or '@' not in email:
                        st.error("Please enter a valid email address")
                    else:
                        with st.spinner("Creating your account..."):
                            result = db.sign_up(
                                email=email,
                                password=password,
                                metadata={'username': username}
                            )
                            
                            if result.get('error'):
                                st.error(result['error'])
                            elif result.get('message'):
                                st.success(result['message'])
                                st.info("Please check your email to confirm your account.")
                                st.rerun()  
                            else:
                                st.success("Account created successfully! You can now sign in.")
                                st.rerun()  

        with col2:
            st.write("### Sign In")
            with st.form("signin_form"):
                email = st.text_input("Email", key="signin_email")
                password = st.text_input("Password", type="password", key="signin_password")
                signin_button = st.form_submit_button("Sign In")
                
                if signin_button:
                    if not email or not password:
                        st.error("Please enter both email and password")
                    else:
                        with st.spinner("Signing in..."):
                            result = db.sign_in(email, password)
                            if result.get('error'):
                                st.error(result['error'])
                            else:
                                st.session_state.authenticated = True
                                st.session_state.user = result['user']
                                st.success("Signed in successfully!")
                                st.rerun()  

    else:
        st.write(f"### Welcome back!")
        if st.button("Sign Out"):
            st.session_state.clear()
            st.rerun()

def update_user_activity():
    """Update user activity timestamp and related metrics."""
    if st.session_state.authenticated and st.session_state.user_id:
        current_time = datetime.now()
        
        # Only update if we have a previous activity time
        if st.session_state.last_activity:
            time_diff = current_time - st.session_state.last_activity
            
            # Check for new day
            if time_diff.days > 0:
                # Reset daily counters
                st.session_state.progress['translations_today'] = 0
                st.session_state.daily_challenges = {
                    'translation': {'target': 10, 'current': 0},
                    'learning': {'target': 3, 'current': 0},
                    'cultural': {'target': 1, 'current': 0}
                }
                
                # Update streak
                if time_diff.days == 1:
                    st.session_state.progress['daily_streak'] += 1
                else:
                    st.session_state.progress['daily_streak'] = 0
        
        # Update last activity time
        st.session_state.last_activity = current_time
        
        # Try to save to database if available
        if st.session_state.features['database'] and db and hasattr(db, 'supabase'):
            try:
                db.supabase.table('user_activity').upsert({
                    'user_id': st.session_state.user_id,
                    'last_activity': current_time.isoformat(),
                    'daily_streak': st.session_state.progress['daily_streak'],
                    'learning_points': st.session_state.progress['learning_points']
                }).execute()
            except Exception as e:
                print(f"Failed to update user activity: {str(e)}")

def update_feature_status():
    """Update feature availability status based on service health."""
    st.session_state.features['database'] = db is not None and hasattr(db, 'supabase')
    st.session_state.features['translation'] = translator is not None
    st.session_state.features['tts'] = audio is not None
    st.session_state.features['ai'] = None
    st.session_state.features['offline_mode'] = not st.session_state.features['database']

def show_progress_chart():
    # Sample data - in real app, this would come from the database
    dates = [datetime.now() - timedelta(days=x) for x in range(7)]
    activity = np.random.randint(0, 100, size=7)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=activity,
        mode='lines+markers',
        name='Activity',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Your Learning Activity",
        xaxis_title="Date",
        yaxis_title="Activity Points",
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def calculate_level(xp):
    return int(1 + (xp / 100))

def check_achievements():
    achievements = []
    if st.session_state.translations_today >= 10:
        achievements.append({
            'title': 'Translation Master',
            'description': 'Complete 10 translations in one day',
            'icon': '🎯'
        })
    if st.session_state.daily_streak >= 7:
        achievements.append({
            'title': 'Weekly Warrior',
            'description': 'Maintain a 7-day learning streak',
            'icon': '🔥'
        })
    if st.session_state.learning_points >= 100:
        achievements.append({
            'title': 'Century Club',
            'description': 'Earn 100 learning points',
            'icon': '💯'
        })
    return achievements

def show_achievements_popup():
    new_achievements = check_achievements()
    for achievement in new_achievements:
        if achievement not in st.session_state.achievements:
            st.session_state.achievements.append(achievement)
            st.balloons()
            st.success(f"🏆 New Achievement Unlocked: {achievement['title']}!")

def show_level_progress():
    current_level = st.session_state.level
    current_xp = st.session_state.xp
    xp_for_next_level = (current_level + 1) * 100
    progress = (current_xp % 100) / 100

    st.markdown(f"### Level {current_level}")
    st.progress(progress)
    st.caption(f"XP: {current_xp % 100}/{100} to Level {current_level + 1}")

def show_daily_challenges():
    st.markdown("### 🎯 Daily Challenges")
    
    challenges = {
        'translation': ('Translations', '🔤'),
        'learning': ('Lessons Completed', '📚'),
        'cultural': ('Cultural Activities', '🌍')
    }
    
    cols = st.columns(len(challenges))
    for i, (key, (label, icon)) in enumerate(challenges.items()):
        with cols[i]:
            challenge = st.session_state.daily_challenges[key]
            progress = min(challenge['current'] / challenge['target'], 1)
            st.markdown(f"**{icon} {label}**")
            st.progress(progress)
            st.caption(f"{challenge['current']}/{challenge['target']}")
            
            if challenge['current'] >= challenge['target']:
                st.success("Completed! 🌟")

def show_skill_radar():
    categories = ['Grammar', 'Vocabulary', 'Pronunciation', 'Culture', 'Writing']
    # Sample data - in real app, would come from database
    values = np.random.randint(30, 100, size=len(categories))
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title="Skills Overview",
        height=300
    )
    
    return fig

def show_home():
    st.title("Ubuntu Language Explorer")
    
    # Welcome message and stats
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
            Welcome to Ubuntu Language Explorer - your gateway to South African languages and culture.
            Explore, learn, and preserve our rich linguistic heritage.
        """)
        
        if st.session_state.user_id:
            # Show level and XP progress
            show_level_progress()
            
            # Activity chart
            st.plotly_chart(show_progress_chart(), use_container_width=True)
            
            # Skills radar
            st.plotly_chart(show_skill_radar(), use_container_width=True)
    
    with col2:
        if st.session_state.user_id:
            # Daily challenges
            show_daily_challenges()
            
            # Recent achievements
            st.markdown("### 🏆 Recent Achievements")
            for achievement in st.session_state.achievements[-3:]:
                st.success(f"{achievement['icon']} {achievement['title']}")
    
    # Quick start guide
    st.header("Quick Start Guide")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔤 Start Learning")
        st.write("Begin your language learning journey with interactive lessons and exercises.")
        if st.button("Go to Lessons", key="home_lessons"):
            # Set the page and tab to navigate to
            st.session_state.learn_page_tab = "Lessons"
            st.session_state.current_page = "Learn"
    
    with col2:
        st.markdown("### 🗣️ Practice Speaking")
        st.write("Practice pronunciation with our audio tools and get instant feedback.")
        if st.button("Try Translation", key="home_translation"):
            selected = "Translation"
            st.rerun()
    
    with col3:
        st.markdown("### 🤝 Join Community")
        st.write("Connect with other learners and native speakers.")
        if st.button("Visit Community", key="home_community"):
            st.session_state.daily_challenges['cultural']['current'] += 1
            show_achievements_popup()
            st.session_state.current_page = "Community"
            st.rerun()
    
    # Featured content with gamification
    st.markdown("---")
    st.header("Featured Content")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📚 Word of the Day")
        word = {
            'word': 'Ubuntu',
            'language': 'Zulu/Xhosa',
            'meaning': 'Humanity towards others',
            'points': 5
        }
        st.info(f"{word['word']} ({word['language']})\n\n*{word['meaning']}*")
        if st.button("Learn Word (+5 XP)"):
            st.session_state.xp += word['points']
            st.session_state.level = calculate_level(st.session_state.xp)
            st.success(f"Word learned! +{word['points']} XP")
            show_achievements_popup()
        
    with col2:
        st.markdown("### 🎯 Daily Challenge")
        challenge = {
            'title': 'Cultural Explorer',
            'task': 'Learn about a new tradition',
            'points': 10
        }
        st.info(f"Today's Challenge: {challenge['task']}")
        if st.button(f"Complete (+{challenge['points']} XP)"):
            st.session_state.xp += challenge['points']
            st.session_state.level = calculate_level(st.session_state.xp)
            st.session_state.daily_challenges['cultural']['current'] += 1
            st.success(f"Challenge completed! +{challenge['points']} XP")
            show_achievements_popup()
            
    with col3:
        st.markdown("### 👥 Community")
        st.metric("Active Learners", "42")
        if st.session_state.user_id:
            st.metric("Your Rank", f"#{np.random.randint(1, 100)}")

def show_learn():
    st.title("Learn")
    st.write("Welcome to the learning section! Here you can:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📚 Lessons")
        st.write("Start with structured lessons")
        if st.button("Start Learning"):
            # Set the page and tab to navigate to
            st.session_state.learn_page_tab = "Lessons"
            st.session_state.current_page = "Learn"
    
    with col2:
        st.subheader("🎯 Practice")
        st.write("Practice what you've learned")
        if st.button("Practice Now"):
            # Set the page and tab to navigate to
            st.session_state.learn_page_tab = "Practice"
            st.session_state.current_page = "Learn"

def show_games():
    st.title("Language Games")
    st.write("Learn while having fun!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🎮 Word Match")
        st.write("Match words with their meanings")
        if st.button("Play Word Match"):
            st.session_state.xp += 2
    
    with col2:
        st.subheader("🎲 Language Quiz")
        st.write("Test your knowledge")
        if st.button("Start Quiz"):
            st.session_state.xp += 2
    
    with col3:
        st.subheader("🏆 Leaderboard")
        st.write("See how you rank")

def show_culture():
    st.title("Cultural Exploration")
    st.write("Discover the rich cultural heritage of South Africa")
    
    tab1, tab2, tab3 = st.tabs(["Stories", "Traditions", "History"])
    
    with tab1:
        st.subheader("📖 Traditional Stories")
        st.write("Explore traditional stories and folklore")
    
    with tab2:
        st.subheader("🎭 Cultural Traditions")
        st.write("Learn about customs and traditions")
    
    with tab3:
        st.subheader("📜 Historical Context")
        st.write("Understand the historical context of languages")

def show_community():
    st.title("Community Hub")
    st.write("Connect with fellow language learners")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👥 Discussion Forum")
        st.write("Join conversations about language and culture")
    
    with col2:
        st.subheader("🤝 Language Exchange")
        st.write("Find language exchange partners")

def show_learning():
    st.title("My Learning Journey")
    st.write("Track your progress and achievements")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Progress")
        st.progress(st.session_state.xp % 100 / 100)
        st.write(f"Level: {st.session_state.level}")
        st.write(f"XP: {st.session_state.xp}")
    
    with col2:
        st.subheader("🏆 Achievements")
        for achievement in st.session_state.achievements:
            st.write(f"- {achievement}")

def show_profile():
    st.title("My Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👤 User Info")
        st.write(f"Username: {st.session_state.username}")
        st.write(f"Level: {st.session_state.level}")
        st.write(f"XP: {st.session_state.xp}")
    
    with col2:
        st.subheader("⚙️ Settings")
        language = st.selectbox("Interface Language", ["English", "isiZulu", "isiXhosa", "Sesotho", "Setswana"])
        theme = st.selectbox("Theme", ["Light", "Dark"])
        notifications = st.checkbox("Enable Notifications")

def main():
    """Main application"""
    st.title("🌍 Ubuntu Language")
    
    # Initialize session state
    init_session_state()
    
    # Show appropriate view based on authentication state
    if st.session_state.user:
        show_welcome()
    else:
        # Toggle between login and register
        if 'show_login' not in st.session_state:
            st.session_state.show_login = True
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sign In", type="primary" if st.session_state.show_login else "secondary"):
                st.session_state.show_login = True
                st.rerun()
        with col2:
            if st.button("Create Account", type="primary" if not st.session_state.show_login else "secondary"):
                st.session_state.show_login = False
                st.rerun()
                
        if st.session_state.show_login:
            show_login()
        else:
            show_register()

if __name__ == "__main__":
    db = Database()
    main()
