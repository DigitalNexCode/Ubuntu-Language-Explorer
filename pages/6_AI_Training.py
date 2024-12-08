import streamlit as st
import google.generativeai as genai
from utils.database import db
from utils.languages import LANGUAGES
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import plotly.express as px
import pandas as pd

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AI Training - Ubuntu Language",
    page_icon="🤖",
    layout="wide"
)

# Initialize Gemini AI
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("Unable to initialize AI model. Please check your API key.")
    model = None

# Training categories
TRAINING_CATEGORIES = {
    "daily_phrases": "Daily Conversations",
    "cultural": "Cultural Expressions",
    "idioms": "Idioms & Proverbs",
    "formal": "Formal Language",
    "slang": "Modern Slang",
    "storytelling": "Traditional Stories"
}

def get_ai_feedback(phrase: str, translation: str, language: str, context: str) -> dict:
    """Get AI feedback on the translation quality and cultural relevance"""
    if not model:
        return {"status": "error", "message": "AI model not available"}
    
    try:
        prompt = f"""
        As a South African language expert, analyze this translation:
        
        English: {phrase}
        {LANGUAGES[language]['name']}: {translation}
        Context: {context}
        
        Please provide:
        1. Translation accuracy (0-100%)
        2. Cultural relevance (0-100%)
        3. Specific feedback
        4. Suggested improvements
        5. Cultural context notes
        
        Format response as JSON:
        {{
            "accuracy": number,
            "cultural_relevance": number,
            "feedback": "string",
            "suggestions": "string",
            "cultural_notes": "string"
        }}
        """
        
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {"status": "error", "message": str(e)}

def calculate_user_level(contributions: int) -> tuple:
    """Calculate user's training level and progress"""
    levels = [
        (0, "Novice", 10),
        (10, "Helper", 25),
        (25, "Contributor", 50),
        (50, "Expert", 100),
        (100, "Master", 200),
        (200, "Elder", float('inf'))
    ]
    
    for i, (min_contrib, title, next_level) in enumerate(levels):
        if contributions < next_level:
            progress = (contributions - min_contrib) / (next_level - min_contrib)
            return title, progress, next_level - contributions
    
    return "Elder", 1.0, 0

def show_training_dashboard():
    """Display user's training dashboard"""
    st.subheader("🎯 Your Training Dashboard")
    
    # Get user stats
    stats = db.get_user_stats(st.session_state.user['id'])
    contributions = stats.get('contributions', 0) if stats else 0
    
    # Calculate level and progress
    level, progress, remaining = calculate_user_level(contributions)
    
    # Display level and progress
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Training Level", level)
    with col2:
        st.progress(progress, f"Progress to Next Level: {int(progress * 100)}%")
    with col3:
        st.metric("Contributions Needed", remaining, f"Total: {contributions}")
    
    # Show achievements
    achievements = db.get_achievements(st.session_state.user['id'])
    if achievements:
        st.write("🏆 Recent Achievements")
        for achievement in achievements:
            st.success(f"🌟 {achievement['title']}: {achievement['description']}")

def save_training_data(language: str, phrase: str, translation: str, context: str, category: str, difficulty: str, formality: str):
    """Save the training data to the database"""
    try:
        with db._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO language_training (
                    user_id, language, phrase, translation, context, category, difficulty, formality, submitted_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (st.session_state.user['id'], language, phrase, translation, context, category, difficulty, formality))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Error saving training data: {e}")
        return False

def get_training_history(language: str = None, categories: list = None, statuses: list = None):
    """Get the training history for a specific language or all languages"""
    try:
        with db._get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT * FROM language_training 
                WHERE user_id = ?
            """
            params = (st.session_state.user['id'],)
            
            if language:
                query += " AND language = ?"
                params += (language,)
            
            if categories:
                query += " AND category IN (%s)" % ','.join('?' for _ in categories)
                params += tuple(categories)
            
            if statuses:
                query += " AND validation_status IN (%s)" % ','.join('?' for _ in statuses)
                params += tuple(statuses)
            
            query += " ORDER BY submitted_at DESC LIMIT 10"
            
            cursor.execute(query, params)
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching training history: {e}")
        return []

def main():
    st.title("🤖 AI Language Training Hub")
    
    if "user" not in st.session_state:
        st.warning("Please sign in to contribute to AI training.")
        return

    # Show training dashboard
    show_training_dashboard()
    
    # Language selection with flag emoji
    selected_language = st.selectbox(
        "Select Language to Train",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: f"{LANGUAGES[x]['flag']} {LANGUAGES[x]['name']}"
    )

    # Create tabs for different training modes
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Contribute", "🔄 Review & Validate", 
        "📊 Analytics", "👥 Community Leaders"
    ])

    with tab1:
        st.subheader("Contribute New Content")
        
        # Category selection
        category = st.selectbox(
            "Select Category",
            options=list(TRAINING_CATEGORIES.keys()),
            format_func=lambda x: TRAINING_CATEGORIES[x]
        )
        
        # Input form with real-time AI feedback
        with st.form("training_form"):
            phrase = st.text_input("Phrase in English")
            translation = st.text_input(f"Translation in {LANGUAGES[selected_language]['name']}")
            context = st.text_area(
                "Cultural Context & Usage Notes",
                help="Provide cultural background, usage examples, or special meanings"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                difficulty = st.select_slider(
                    "Difficulty Level",
                    options=["Beginner", "Intermediate", "Advanced"]
                )
            with col2:
                formality = st.select_slider(
                    "Formality Level",
                    options=["Informal", "Neutral", "Formal"]
                )
            
            submitted = st.form_submit_button("Submit & Get AI Feedback")
            
            if submitted and phrase and translation:
                # Get AI feedback
                feedback = get_ai_feedback(phrase, translation, selected_language, context)
                
                if feedback.get("status") != "error":
                    # Display feedback in an organized way
                    st.write("### AI Feedback")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Translation Accuracy", f"{feedback['accuracy']}%")
                    with col2:
                        st.metric("Cultural Relevance", f"{feedback['cultural_relevance']}%")
                    
                    st.write("#### Detailed Feedback")
                    st.info(feedback['feedback'])
                    
                    if feedback['suggestions']:
                        st.write("#### Suggestions for Improvement")
                        st.warning(feedback['suggestions'])
                    
                    if feedback['cultural_notes']:
                        st.write("#### Cultural Context")
                        st.success(feedback['cultural_notes'])
                    
                    # Save if accuracy is good enough
                    if feedback['accuracy'] >= 70:
                        if save_training_data(
                            selected_language, phrase, translation, 
                            context, category, difficulty, formality
                        ):
                            st.success("Contribution saved! Thank you! 🎉")
                            db.update_user_stats(st.session_state.user['id'], 'contributions')
                    else:
                        st.warning("Please review and improve the translation based on the feedback.")

    with tab2:
        st.subheader("Community Review & Validation")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            filter_category = st.multiselect(
                "Filter by Category",
                options=list(TRAINING_CATEGORIES.keys()),
                format_func=lambda x: TRAINING_CATEGORIES[x]
            )
        with col2:
            filter_status = st.multiselect(
                "Filter by Status",
                options=["Pending", "Verified", "Rejected"]
            )
        
        # Get filtered entries
        entries = get_training_history(
            selected_language, 
            categories=filter_category,
            statuses=filter_status
        )
        
        if not entries:
            st.info("No entries found matching your filters.")
        else:
            for entry in entries:
                with st.expander(
                    f"{entry['category'].title()}: {entry['phrase']} ↔️ {entry['translation']}", 
                    expanded=False
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Context:** {entry['context']}")
                        st.write(f"**Difficulty:** {entry['difficulty']}")
                        st.write(f"**Formality:** {entry['formality']}")
                    with col2:
                        st.write(f"**Submitted by:** {entry['user_email']}")
                        st.write(f"**Status:** {entry['validation_status']}")
                        st.write(f"**Validations:** {entry['validation_count']}")
                    
                    # Validation buttons
                    if entry['validation_status'] == 'pending':
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            if st.button("✅ Correct", key=f"correct_{entry['id']}"):
                                db.update_training_validation(
                                    entry['id'], 'correct', 
                                    st.session_state.user['id']
                                )
                                st.success("Validated as correct!")
                        with col2:
                            if st.button("❌ Incorrect", key=f"incorrect_{entry['id']}"):
                                db.update_training_validation(
                                    entry['id'], 'incorrect', 
                                    st.session_state.user['id']
                                )
                                st.error("Marked as incorrect!")
                        with col3:
                            if st.button("📝 Suggest Edit", key=f"edit_{entry['id']}"):
                                suggestion = st.text_area(
                                    "Your suggestion",
                                    key=f"suggestion_{entry['id']}"
                                )
                                if suggestion:
                                    db.add_training_suggestion(
                                        entry['id'], 
                                        st.session_state.user['id'],
                                        suggestion
                                    )
                                    st.info("Suggestion recorded!")
                        with col4:
                            if st.button("🤔 Need Context", key=f"context_{entry['id']}"):
                                db.request_more_context(
                                    entry['id'],
                                    st.session_state.user['id']
                                )
                                st.warning("Context request sent to contributor!")

    with tab3:
        st.subheader("Training Analytics")
        
        # Get analytics data
        analytics = db.get_training_analytics(selected_language)
        
        if analytics:
            # Contribution trends
            st.write("#### Contribution Trends")
            fig = px.line(
                analytics['trends'], 
                x='date', 
                y='contributions',
                title="Daily Contributions"
            )
            st.plotly_chart(fig)
            
            # Category distribution
            st.write("#### Category Distribution")
            fig = px.pie(
                analytics['categories'],
                values='count',
                names='category',
                title="Contributions by Category"
            )
            st.plotly_chart(fig)
            
            # Validation stats
            st.write("#### Validation Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pending Validation", analytics['stats']['pending'])
            with col2:
                st.metric("Verified Entries", analytics['stats']['verified'])
            with col3:
                st.metric("Rejection Rate", f"{analytics['stats']['rejection_rate']}%")

    with tab4:
        st.subheader("Community Leaders")
        
        # Get leaderboard data
        leaderboard = db.get_training_leaderboard(selected_language)
        
        if leaderboard:
            st.write("#### Top Contributors")
            for i, leader in enumerate(leaderboard[:10], 1):
                st.write(
                    f"{i}. {leader['user_email']} - "
                    f"Level: {calculate_user_level(leader['contributions'])[0]} - "
                    f"Contributions: {leader['contributions']}"
                )
            
            # Show contribution map
            st.write("#### Global Contribution Map")
            fig = px.scatter_mapbox(
                leaderboard,
                lat='latitude',
                lon='longitude',
                size='contributions',
                hover_name='user_email',
                title="Where Contributors Are From"
            )
            st.plotly_chart(fig)

if __name__ == "__main__":
    main()
