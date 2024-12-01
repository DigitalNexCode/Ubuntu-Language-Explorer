import streamlit as st
from utils.languages import LANGUAGES
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime, timedelta

# Initialize session state for admin data
if 'content_data' not in st.session_state:
    st.session_state.content_data = {
        'stories': [],
        'videos': [],
        'audio': [],
        'games': []
    }

def generate_sample_data():
    """Generate sample data for visualization"""
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    languages = list(LANGUAGES.keys())
    
    data = []
    for date in dates:
        for lang in languages:
            users = random.randint(50, 500)
            engagement = random.uniform(1, 5)
            content_views = random.randint(100, 1000)
            data.append({
                'date': date,
                'language': lang,
                'users': users,
                'engagement': engagement,
                'content_views': content_views
            })
    
    return pd.DataFrame(data)

def plot_language_engagement(df):
    """Create language engagement visualization"""
    fig = px.bar(
        df.groupby('language').agg({
            'users': 'sum',
            'engagement': 'mean',
            'content_views': 'sum'
        }).reset_index(),
        x='language',
        y='engagement',
        color='users',
        title='Language Engagement Overview'
    )
    return fig

def plot_content_trends(df):
    """Create content trends visualization"""
    daily_trends = df.groupby('date').agg({
        'content_views': 'sum',
        'users': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_trends['date'],
        y=daily_trends['content_views'],
        name='Content Views',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=daily_trends['date'],
        y=daily_trends['users'],
        name='Active Users',
        line=dict(color='green')
    ))
    fig.update_layout(title='Daily Content and User Trends')
    return fig

def content_management():
    st.subheader("📚 Content Management")
    
    content_type = st.selectbox(
        "Select Content Type",
        ["Stories", "Videos", "Audio", "Games"]
    )
    
    # Add new content
    with st.expander("Add New Content"):
        language = st.selectbox(
            "Language",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x]["native_name"]
        )
        
        title = st.text_input("Title")
        description = st.text_area("Description")
        
        if content_type in ["Videos", "Audio"]:
            file = st.file_uploader(
                f"Upload {content_type.lower()[:-1]} file",
                type=['mp4', 'mp3'] if content_type == "Videos" else ['mp3', 'wav']
            )
        elif content_type == "Stories":
            content = st.text_area("Story Content")
            translation = st.text_area("English Translation")
            audio = st.file_uploader("Upload Audio Narration", type=['mp3', 'wav'])
        else:  # Games
            instructions = st.text_area("Game Instructions")
            difficulty = st.select_slider(
                "Difficulty Level",
                options=["Easy", "Medium", "Hard"]
            )
        
        if st.button("Add Content"):
            st.success(f"Added new {content_type.lower()[:-1]} content: {title}")
            # Here you would typically save to a database

def user_analytics():
    st.subheader("📊 Analytics Dashboard")
    
    # Generate sample data
    df = generate_sample_data()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", f"{df['users'].sum():,}")
    with col2:
        st.metric("Active Languages", len(df['language'].unique()))
    with col3:
        st.metric("Avg. Engagement", f"{df['engagement'].mean():.2f}")
    with col4:
        st.metric("Content Views", f"{df['content_views'].sum():,}")
    
    # Language engagement chart
    st.plotly_chart(plot_language_engagement(df))
    
    # Content trends
    st.plotly_chart(plot_content_trends(df))
    
    # Detailed analytics
    with st.expander("View Detailed Analytics"):
        st.dataframe(
            df.groupby('language').agg({
                'users': 'sum',
                'engagement': 'mean',
                'content_views': 'sum'
            }).round(2)
        )

def leaderboard_management():
    st.subheader("🏆 Leaderboard Management")
    
    # Sample leaderboard data
    leaderboard_data = pd.DataFrame({
        'User': ['Themba', 'Sipho', 'Nomvula', 'Zanele', 'Thabo'],
        'Points': [1200, 1100, 1000, 900, 800],
        'Language': ['Zulu', 'Xhosa', 'Sotho', 'Tswana', 'Venda'],
        'Last Active': ['2024-01-31', '2024-01-30', '2024-01-31', '2024-01-29', '2024-01-31']
    })
    
    st.dataframe(leaderboard_data)
    
    with st.expander("Manage Points"):
        user = st.selectbox("Select User", leaderboard_data['User'])
        points = st.number_input("Adjust Points", min_value=0, value=100)
        if st.button("Update Points"):
            st.success(f"Updated points for {user}")

def display_admin_dashboard():
    st.title("👨‍💼 Admin Dashboard")
    
    # Check admin authentication (implement proper auth in production)
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "password":  # Replace with proper auth
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
        return
    
    # Admin navigation
    tab1, tab2, tab3 = st.tabs([
        "Content Management",
        "Analytics",
        "Leaderboard"
    ])
    
    with tab1:
        content_management()
    
    with tab2:
        user_analytics()
    
    with tab3:
        leaderboard_management()

if __name__ == "__main__":
    display_admin_dashboard()
