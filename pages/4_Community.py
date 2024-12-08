import streamlit as st
from utils.database import Database
from utils.translation import TranslationService
from datetime import datetime

# Must be the first Streamlit command
st.set_page_config(
    page_title="Community - Ubuntu Language",
    page_icon="👥",
    layout="wide"
)

# Initialize services
db = Database()
translator = TranslationService()

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
    if st.session_state.user:
        user = st.session_state.user
        st.sidebar.markdown("---")
        st.sidebar.header("Your Stats")
        st.sidebar.write(f"👤 {user['first_name']} {user['last_name']}")
        st.sidebar.write(f"🌍 {user['country']}")
        st.sidebar.write(f"🗣️ {user['preferred_language']}")
        
        # Get user's post count
        post_count = db.get_user_post_count(user['id'])
        st.sidebar.write(f"📝 Posts: {post_count}")

def create_new_post():
    if not st.session_state.user:
        st.warning("Please sign in to create posts.")
        return
        
    st.subheader("Create New Post")
    with st.form("new_post"):
        title = st.text_input("Title")
        content = st.text_area("Content")
        submitted = st.form_submit_button("Post")
        
        if submitted:
            if not title or not content:
                st.error("Please fill in both title and content.")
                return
                
            try:
                result = db.create_post(
                    user_id=st.session_state.user['id'],
                    forum=st.session_state.current_forum,
                    title=title,
                    content=content
                )
                
                if result.get('success'):
                    st.success("Post created successfully!")
                    st.rerun()
                else:
                    st.error(f"Error creating post: {result.get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error creating post: {str(e)}")

def display_posts():
    forum = st.session_state.current_forum
    forum_data = get_forum_categories()[forum]
    
    st.header(f"{forum_data['title']}")
    st.write(forum_data['description'])
    
    # Create new post section
    create_new_post()
    
    st.markdown("---")
    st.subheader("Recent Posts")
    
    try:
        posts = db.get_forum_posts(forum)
        
        if not posts:
            st.info("No posts yet. Be the first to post!")
            return
            
        for post in posts:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {post['title']}")
                    st.write(post['content'])
                with col2:
                    author = db.get_user_by_id(post['user_id'])
                    st.write(f"Posted by: {author['first_name']} {author['last_name']}")
                    st.write(f"Date: {post['created_at']}")
                st.markdown("---")
    except Exception as e:
        st.error(f"Error loading posts: {str(e)}")

def display_community_guidelines():
    with st.expander("Community Guidelines"):
        st.write("""
        🤝 **Be Respectful**: Treat all members with respect and kindness.
        
        🌈 **Celebrate Diversity**: Embrace different cultures and viewpoints.
        
        📚 **Share Knowledge**: Help others learn and grow.
        
        ❌ **No Hate Speech**: Zero tolerance for discrimination or harassment.
        
        🤔 **Stay On Topic**: Keep discussions relevant to language learning and culture.
        """)

def main():
    initialize_session_state()
    
    # Display sidebar elements
    display_forum_selection()
    display_user_stats()
    
    # Main content
    if not st.session_state.user:
        st.warning("Please sign in to participate in the community.")
        st.stop()
    
    display_community_guidelines()
    display_posts()

if __name__ == "__main__":
    main()
