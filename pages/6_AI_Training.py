import streamlit as st
import google.generativeai as genai
from utils.database import db
from utils.languages import LANGUAGES
import os
from dotenv import load_dotenv
import json
from datetime import datetime

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

def save_training_data(language: str, phrase: str, translation: str, context: str):
    """Save the training data to the database"""
    try:
        with db._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO language_training (
                    user_id, language, phrase, translation, context, submitted_at
                ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (st.session_state.user['id'], language, phrase, translation, context))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Error saving training data: {e}")
        return False

def get_training_history(language: str = None):
    """Get the training history for a specific language or all languages"""
    try:
        with db._get_db_connection() as conn:
            cursor = conn.cursor()
            if language:
                cursor.execute("""
                    SELECT * FROM language_training 
                    WHERE user_id = ? AND language = ?
                    ORDER BY submitted_at DESC LIMIT 10
                """, (st.session_state.user['id'], language))
            else:
                cursor.execute("""
                    SELECT * FROM language_training 
                    WHERE user_id = ?
                    ORDER BY submitted_at DESC LIMIT 10
                """, (st.session_state.user['id'],))
            return cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching training history: {e}")
        return []

def main():
    st.title("🤖 AI Language Training")
    st.write("""
    Help improve our AI's understanding of South African languages! Share your knowledge
    and contribute to making our language learning platform more accurate and comprehensive.
    """)

    if "user" not in st.session_state:
        st.warning("Please sign in to contribute to AI training.")
        return

    # Language selection
    selected_language = st.selectbox(
        "Select Language to Train",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x]['name']
    )

    # Create tabs for different training modes
    tab1, tab2, tab3 = st.tabs(["📝 Add Phrases", "🔄 Review & Validate", "📊 Training History"])

    with tab1:
        st.subheader("Add New Phrases")
        
        # Input form
        with st.form("training_form"):
            phrase = st.text_input("Phrase in English")
            translation = st.text_input(f"Translation in {LANGUAGES[selected_language]['name']}")
            context = st.text_area("Context or Usage Notes", 
                                 help="Provide any cultural context, usage examples, or notes about the phrase")
            
            submitted = st.form_submit_button("Submit Training Data")
            if submitted and phrase and translation:
                if save_training_data(selected_language, phrase, translation, context):
                    st.success("Thank you for your contribution! 🎉")
                    
                    # Update user stats
                    db.update_user_stats(st.session_state.user['id'], 'contributions')
                    
                    # Try to use the AI to validate
                    if model:
                        try:
                            prompt = f"""
                            Please validate this translation:
                            English: {phrase}
                            {LANGUAGES[selected_language]['name']}: {translation}
                            Context: {context}
                            
                            Is this translation accurate? Please explain your reasoning.
                            """
                            response = model.generate_content(prompt)
                            st.info("AI Feedback:\n" + response.text)
                        except Exception as e:
                            st.warning("Could not get AI feedback at this time.")

    with tab2:
        st.subheader("Review & Validate")
        history = get_training_history(selected_language)
        
        if not history:
            st.info("No training data available for review yet.")
        else:
            for entry in history:
                with st.expander(f"{entry['phrase']} ↔️ {entry['translation']}", expanded=False):
                    st.write(f"**Context:** {entry['context']}")
                    st.write(f"**Submitted:** {entry['submitted_at']}")
                    
                    # Add validation buttons
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("👍 Correct", key=f"correct_{entry['id']}"):
                            db.update_training_validation(entry['id'], 'correct')
                            st.success("Marked as correct!")
                    with col2:
                        if st.button("👎 Incorrect", key=f"incorrect_{entry['id']}"):
                            db.update_training_validation(entry['id'], 'incorrect')
                            st.error("Marked as incorrect!")
                    with col3:
                        if st.button("🤔 Not Sure", key=f"unsure_{entry['id']}"):
                            db.update_training_validation(entry['id'], 'unsure')
                            st.info("Marked as unsure!")

    with tab3:
        st.subheader("Your Training History")
        
        # Show statistics
        total_contributions = len(get_training_history())
        st.metric("Total Contributions", total_contributions)
        
        # Show recent contributions
        st.write("Recent Contributions:")
        history = get_training_history()
        if history:
            for entry in history:
                st.write(f"• {entry['phrase']} → {entry['translation']}")
        else:
            st.info("No contributions yet. Start adding phrases to help train the AI!")

if __name__ == "__main__":
    main()
