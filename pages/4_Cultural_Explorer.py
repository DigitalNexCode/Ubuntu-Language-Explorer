import streamlit as st
from utils.languages import LANGUAGES
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import random
from datetime import datetime
import plotly.express as px
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize Gemini AI
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.warning("AI services not available. Using fallback content.")
    model = None

# Cultural content database
CULTURAL_CONTENT = {
    "traditions": {
        "title": "Traditional Practices & Customs",
        "description": "Explore the rich traditions that define our cultural heritage",
        "categories": {
            "ceremonies": {
                "title": "Ceremonies & Rituals",
                "items": [
                    "Coming of age ceremonies",
                    "Wedding traditions",
                    "Harvest celebrations",
                    "Spiritual ceremonies"
                ]
            },
            "daily_life": {
                "title": "Daily Life & Customs",
                "items": [
                    "Family structures",
                    "Social etiquette",
                    "Traditional dress",
                    "Food customs"
                ]
            }
        }
    },
    "art_crafts": {
        "title": "Art & Crafts",
        "description": "Discover traditional artistic expressions and craftsmanship",
        "categories": {
            "visual_arts": {
                "title": "Visual Arts",
                "items": [
                    "Beadwork",
                    "Pottery",
                    "Painting",
                    "Sculpture"
                ]
            },
            "crafts": {
                "title": "Traditional Crafts",
                "items": [
                    "Basket weaving",
                    "Wood carving",
                    "Textile making",
                    "Jewelry crafting"
                ]
            }
        }
    },
    "music_dance": {
        "title": "Music & Dance",
        "description": "Experience the rhythm and movement of cultural expression",
        "categories": {
            "music": {
                "title": "Traditional Music",
                "items": [
                    "Musical instruments",
                    "Folk songs",
                    "Ceremonial music",
                    "Modern adaptations"
                ]
            },
            "dance": {
                "title": "Traditional Dance",
                "items": [
                    "Ceremonial dances",
                    "Social dances",
                    "Dance costumes",
                    "Dance meanings"
                ]
            }
        }
    },
    "stories": {
        "title": "Oral Traditions & Stories",
        "description": "Listen to the wisdom passed down through generations",
        "categories": {
            "folktales": {
                "title": "Folktales",
                "items": [
                    "Creation stories",
                    "Moral tales",
                    "Animal stories",
                    "Hero tales"
                ]
            },
            "proverbs": {
                "title": "Proverbs & Sayings",
                "items": [
                    "Wisdom sayings",
                    "Life lessons",
                    "Cultural values",
                    "Traditional knowledge"
                ]
            }
        }
    }
}

def get_cultural_response(language, topic, subtopic, question):
    """Get a detailed response about cultural aspects using available AI services."""
    try:
        if model:
            prompt = f"""
            As a cultural expert in {LANGUAGES[language]['name']} ({LANGUAGES[language]['native_name']}), 
            provide detailed information about {topic} - {subtopic}.
            
            Question: {question}
            
            Please provide:
            1. A clear explanation
            2. Cultural significance
            3. Modern relevance
            4. Examples or stories if applicable
            
            Format the response in a clear, engaging way suitable for learning.
            """
            
            response = model.generate_content(prompt)
            return response.text
        else:
            return get_fallback_response(topic, subtopic)
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return get_fallback_response(topic, subtopic)

def get_fallback_response(topic, subtopic):
    """Get a response from fallback content when AI services are unavailable."""
    fallback_responses = [
        f"Learn about the rich traditions of {topic} - {subtopic}.",
        f"Discover the cultural significance of {topic} in {subtopic}.",
        f"Explore the historical importance of {topic} through {subtopic}.",
        f"Understanding {topic} helps us appreciate our cultural heritage in {subtopic}."
    ]
    return random.choice(fallback_responses)

def get_daily_cultural_fact(language, topic):
    """Generate a cultural fact using available AI services or fallback content."""
    try:
        if model:
            prompt = f"""
            Share an interesting cultural fact about {LANGUAGES[language]['name']} culture,
            specifically about {topic}. Make it engaging and educational.
            Keep it concise (2-3 sentences).
            """
            
            response = model.generate_content(prompt)
            return response.text
        else:
            return get_fallback_response(topic, "general")
    except Exception as e:
        return get_fallback_response(topic, "general")

def display_cultural_explorer():
    st.title("🌍 Cultural Explorer")
    st.write("Discover and learn about the rich cultural heritage of South African languages and traditions.")
    
    # Initialize session state for favorites and points
    if 'favorites' not in st.session_state:
        st.session_state.favorites = set()
    if 'cultural_points' not in st.session_state:
        st.session_state.cultural_points = 0
    
    # Sidebar
    with st.sidebar:
        st.subheader("👤 Your Cultural Journey")
        st.metric("Cultural Points", st.session_state.cultural_points)
        st.write(f"Favorites: {len(st.session_state.favorites)} items")
        
        # Daily cultural fact
        st.subheader("🌟 Daily Cultural Fact")
        if 'daily_fact' not in st.session_state:
            st.session_state.daily_fact = get_daily_cultural_fact("zulu", "general")
        st.info(st.session_state.daily_fact)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Language selection
        selected_language = st.selectbox(
            "Choose a culture to explore:",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: f"{LANGUAGES[x]['native_name']} ({LANGUAGES[x]['name']})"
        )
        
        # Topic selection
        selected_topic = st.selectbox(
            "Select a cultural aspect:",
            options=list(CULTURAL_CONTENT.keys()),
            format_func=lambda x: CULTURAL_CONTENT[x]['title']
        )
        
        # Display topic content
        topic_data = CULTURAL_CONTENT[selected_topic]
        st.subheader(topic_data['title'])
        st.write(topic_data['description'])
        
        # Display categories
        for category_key, category in topic_data['categories'].items():
            with st.expander(f"📚 {category['title']}"):
                for item in category['items']:
                    col_a, col_b = st.columns([3, 1])
                    with col_a:
                        st.write(f"• {item}")
                    with col_b:
                        favorite_key = f"{selected_topic}_{category_key}_{item}"
                        if st.button("❤️", key=f"fav_{favorite_key}"):
                            if favorite_key not in st.session_state.favorites:
                                st.session_state.favorites.add(favorite_key)
                                st.session_state.cultural_points += 10
                                st.success("Added to favorites! +10 points")
                                st.rerun()
                
                # Interactive learning section
                st.write("---")
                st.write("🤔 Ask a question about this topic:")
                user_question = st.text_input("Your question:", key=f"q_{category_key}")
                if user_question:
                    response = get_cultural_response(
                        selected_language,
                        topic_data['title'],
                        category['title'],
                        user_question
                    )
                    st.write("Answer:")
                    st.write(response)
                    st.session_state.cultural_points += 5
                    st.info("You earned 5 points for engaging with the content!")
    
    with col2:
        # Cultural insights and statistics
        st.subheader("📊 Cultural Insights")
        
        # Sample engagement data
        engagement_data = pd.DataFrame({
            'Category': list(CULTURAL_CONTENT.keys()),
            'Engagement': [random.randint(50, 100) for _ in CULTURAL_CONTENT]
        })
        
        fig = px.bar(
            engagement_data,
            x='Category',
            y='Engagement',
            title='Community Engagement by Category'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Your favorites
        st.subheader("❤️ Your Favorites")
        if st.session_state.favorites:
            for fav in st.session_state.favorites:
                topic, category, item = fav.split('_')
                st.write(f"• {item} ({CULTURAL_CONTENT[topic]['categories'][category]['title']})")
        else:
            st.info("Add items to your favorites by clicking the ❤️ button!")

if __name__ == "__main__":
    display_cultural_explorer()
