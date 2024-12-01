import streamlit as st
from utils.supabase_client import SupabaseClient
from utils.translation import TranslationService
from datetime import datetime

# Initialize services
db = SupabaseClient()
translator = TranslationService()

# Page config
st.set_page_config(
    page_title="Community Hub - Ubuntu Language Explorer",
    page_icon="👥",
    layout="wide"
)

def initialize_session_state():
    if 'current_forum' not in st.session_state:
        st.session_state.current_forum = "General"
    if 'user_posts' not in st.session_state:
        st.session_state.user_posts = []

def get_forum_categories():
    return {
        "General": {
            "title": "General Discussion",
            "description": "General discussions about language learning and cultural exchange"
        },
        "Language": {
            "title": "Language Exchange",
            "description": "Find language partners and practice together"
        },
        "Culture": {
            "title": "Cultural Exchange",
            "description": "Share and learn about different South African cultures"
        },
        "Events": {
            "title": "Community Events",
            "description": "Upcoming events and meetups"
        }
    }

def display_forum_selection():
    st.sidebar.header("Forum Categories")
    forums = get_forum_categories()
    
    for forum_id, forum_data in forums.items():
        if st.sidebar.button(
            f"💬 {forum_data['title']}", 
            key=f"forum_{forum_id}",
            help=forum_data['description']
        ):
            st.session_state.current_forum = forum_id
            st.rerun()

def display_user_stats():
    st.sidebar.header("Your Activity")
    
    # Get user stats from database
    user_id = st.session_state.get('user_id')
    if user_id:
        stats = {
            "Posts": len(st.session_state.user_posts),
            "Replies": 0,  # To be implemented
            "Helpful Marks": 0  # To be implemented
        }
        
        for stat, value in stats.items():
            st.sidebar.metric(stat, value)

def create_new_post():
    st.subheader("Create New Post")
    
    title = st.text_input("Post Title")
    content = st.text_area("Post Content")
    language = st.selectbox(
        "Post Language",
        ["English", "Zulu", "Xhosa", "Sotho", "Tswana"]
    )
    
    if st.button("Submit Post"):
        if title and content:
            # Verify cultural sensitivity
            context_check = translator.verify_cultural_context(content, language)
            if context_check:
                st.info(f"Cultural Context Check: {context_check}")
            
            # Add post to session state (in real app, would save to database)
            new_post = {
                'title': title,
                'content': content,
                'language': language,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'author': st.session_state.get('user_id', 'Anonymous')
            }
            st.session_state.user_posts.append(new_post)
            st.success("Post created successfully!")
            st.rerun()
        else:
            st.error("Please fill in both title and content")

def display_posts():
    st.header(f"{get_forum_categories()[st.session_state.current_forum]['title']}")
    st.write(get_forum_categories()[st.session_state.current_forum]['description'])
    
    # Create new post button
    if st.button("➕ Create New Post"):
        create_new_post()
    
    # Display existing posts
    st.subheader("Recent Posts")
    if st.session_state.user_posts:
        for post in reversed(st.session_state.user_posts):
            with st.expander(f"📝 {post['title']} - {post['language']}"):
                st.write(f"**Posted by:** {post['author']}")
                st.write(f"**Date:** {post['timestamp']}")
                st.write("---")
                st.write(post['content'])
                
                # Post actions
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👍 Helpful", key=f"helpful_{post['timestamp']}"):
                        st.success("Marked as helpful!")
                with col2:
                    if st.button("💬 Reply", key=f"reply_{post['timestamp']}"):
                        st.text_area("Your Reply", key=f"reply_text_{post['timestamp']}")
                        if st.button("Submit Reply", key=f"submit_reply_{post['timestamp']}"):
                            st.success("Reply posted!")
                with col3:
                    if st.button("🔄 Translate", key=f"translate_{post['timestamp']}"):
                        translated = translator.translate_text(
                            post['content'],
                            post['language'],
                            "English"
                        )
                        if translated:
                            st.info(f"Translation: {translated}")
    else:
        st.info("No posts yet. Be the first to start a discussion!")

def display_community_guidelines():
    with st.expander("📋 Community Guidelines"):
        st.write("""
        **Ubuntu Language Explorer Community Guidelines**
        
        1. **Respect and Ubuntu**: Treat all members with respect and dignity
        2. **Cultural Sensitivity**: Be mindful and respectful of cultural differences
        3. **Language Learning**: Support and encourage fellow learners
        4. **Constructive Communication**: Keep discussions constructive and helpful
        5. **Privacy**: Respect others' privacy and personal information
        
        Remember: "I am because we are" - Ubuntu philosophy
        """)

def main():
    initialize_session_state()
    
    # Sidebar
    display_forum_selection()
    display_user_stats()
    
    # Main content
    display_community_guidelines()
    display_posts()
    
    # Additional features
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Language Exchange")
        st.info("Coming soon: Find language exchange partners!")
    
    with col2:
        st.subheader("📅 Upcoming Events")
        st.info("Coming soon: Community events and meetups!")

if __name__ == "__main__":
    main()
