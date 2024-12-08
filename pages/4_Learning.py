import streamlit as st
from utils.database import Database
from utils.translation import TranslationService
from utils.audio import AudioService
from utils.learning_content import LearningContent

# Initialize services
db = Database()
translator = TranslationService()
audio = AudioService()
learning_content = LearningContent()

# Page config
st.set_page_config(
    page_title="Learning - Ubuntu Language",
    page_icon="📚",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = None
    if 'selected_topic' not in st.session_state:
        st.session_state.selected_topic = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'conversation_mode' not in st.session_state:
        st.session_state.conversation_mode = False

def get_available_languages():
    return {
        "zulu": "isiZulu",
        "xhosa": "isiXhosa",
        "sotho": "Sesotho",
        "tswana": "Setswana",
        "venda": "Tshivenda",
        "tsonga": "Xitsonga",
        "swati": "Siswati",
        "ndebele": "isiNdebele",
        "pedi": "Sepedi"
    }

def get_available_topics():
    return {
        "basics": {
            "title": "Basic Phrases",
            "description": "Learn essential greetings and everyday phrases."
        },
        "vocabulary": {
            "title": "Common Words",
            "description": "Build your vocabulary with commonly used words."
        },
        "grammar": {
            "title": "Grammar Rules",
            "description": "Understand the structure of the language."
        },
        "culture": {
            "title": "Cultural Context",
            "description": "Learn about cultural aspects and proper language usage."
        }
    }

def format_response(response_data):
    """Format the response for display"""
    formatted_text = response_data["text"]
    if response_data.get("context"):
        formatted_text += "\n\nContext:\n" + "\n".join(response_data["context"])
    if response_data.get("examples"):
        formatted_text += "\n\nExamples:\n" + "\n".join(response_data["examples"])
    if response_data.get("cultural_notes"):
        formatted_text += "\n\nCultural Notes:\n" + "\n".join(response_data["cultural_notes"])
    if response_data.get("usage_notes"):
        formatted_text += "\n\nUsage Notes:\n" + "\n".join(response_data["usage_notes"])
    return formatted_text

def display_language_selection():
    st.sidebar.header("Choose Language")
    languages = get_available_languages()
    
    selected = st.sidebar.selectbox(
        "Select a language to learn",
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        key="language_selector"
    )
    
    if selected != st.session_state.selected_language:
        st.session_state.selected_language = selected
        st.session_state.selected_topic = None
        st.session_state.chat_history = []
        st.rerun()

def display_topic_selection():
    if st.session_state.selected_language:
        st.sidebar.header("Choose Topic")
        topics = get_available_topics()
        
        selected = st.sidebar.selectbox(
            "Select a topic to learn",
            options=list(topics.keys()),
            format_func=lambda x: topics[x]["title"],
            key="topic_selector"
        )
        
        if selected != st.session_state.selected_topic:
            st.session_state.selected_topic = selected
            st.session_state.chat_history = []
            st.rerun()

def display_learning_interface():
    if not st.session_state.user:
        st.warning("Please sign in to access the learning interface.")
        return
        
    if not st.session_state.selected_language:
        st.info("👈 Please select a language from the sidebar to start learning.")
        return
        
    if not st.session_state.selected_topic:
        st.info("👈 Please select a topic from the sidebar to continue.")
        return
        
    languages = get_available_languages()
    topics = get_available_topics()
    
    # Load previous conversation if available
    if not st.session_state.chat_history:
        conversation = db.load_conversation(
            st.session_state.user['id'],
            st.session_state.selected_language,
            st.session_state.selected_topic
        )
        if conversation:
            st.session_state.chat_history = conversation["messages"]
            if conversation.get("context"):
                learning_content.set_conversation_context(
                    st.session_state.selected_language,
                    eval(conversation["context"])
                )
    
    # Display current selection
    st.header(f"Learning {languages[st.session_state.selected_language]}")
    
    # Add conversation mode toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"Topic: {topics[st.session_state.selected_topic]['title']}")
        st.write(topics[st.session_state.selected_topic]['description'])
    with col2:
        if st.button("Practice Speaking" if not st.session_state.conversation_mode else "Exit Practice"):
            st.session_state.conversation_mode = not st.session_state.conversation_mode
            if st.session_state.conversation_mode:
                # Initialize conversation context
                learning_content.initialize_conversation(st.session_state.selected_language)
                response_data = learning_content.get_conversation_response(
                    st.session_state.selected_language,
                    "start_conversation"
                )
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response_data["text"]
                })
            else:
                learning_content.end_practice_mode(st.session_state.selected_language)
            
            # Save conversation state
            context = learning_content.get_conversation_context(st.session_state.selected_language)
            if context:
                db.save_conversation_state(
                    st.session_state.user['id'],
                    st.session_state.selected_language,
                    st.session_state.selected_topic,
                    str(context),
                    st.session_state.chat_history
                )
            st.rerun()
    
    # Chat interface
    st.markdown("---")
    
    if st.session_state.conversation_mode:
        st.markdown("### Practice Speaking")
        st.write("Have a conversation with me in your selected language. I'll help you practice!")
    else:
        st.markdown("### Ask anything about this topic")
        # Show example questions based on selected topic
        st.write("Example questions you can ask:")
        if st.session_state.selected_topic == "basics":
            st.write("- How do I say hello in this language?")
            st.write("- What are the common greetings?")
            st.write("- How do I respond to a greeting?")
        elif st.session_state.selected_topic == "grammar":
            st.write("- What are the noun classes?")
            st.write("- How do I form present tense?")
            st.write("- How do verbs work in this language?")
        elif st.session_state.selected_topic == "vocabulary":
            st.write("- What are the words for family members?")
            st.write("- How do I count in this language?")
            st.write("- What are essential everyday words?")
        elif st.session_state.selected_topic == "culture":
            st.write("- What are important cultural customs?")
            st.write("- How do I show respect when speaking?")
            st.write("- What are traditional greetings?")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message.get("audio"):
                st.audio(message["audio"])
    
    # Chat input
    if prompt := st.chat_input("Type your message..." if st.session_state.conversation_mode else f"Ask about {topics[st.session_state.selected_topic]['title']}..."):
        # Add user message to chat
        st.session_state.chat_history.append({
            "role": "user", 
            "content": prompt
        })
        
        try:
            # Get response based on mode
            response_data = learning_content.get_conversation_response(
                st.session_state.selected_language,
                prompt,
                st.session_state.selected_topic
            )
            
            # Format the response
            formatted_response = format_response(response_data)
            
            # Create response message
            response_message = {
                "role": "assistant",
                "content": formatted_response
            }
            
            # Add audio if available
            if response_data["audio_text"]:
                audio_content = audio.text_to_speech(
                    response_data["audio_text"],
                    st.session_state.selected_language
                )
                if audio_content:
                    response_message["audio"] = audio_content
            
            # Add response to chat history
            st.session_state.chat_history.append(response_message)
            
            # Save conversation state
            context = learning_content.get_conversation_context(st.session_state.selected_language)
            if context:
                db.save_conversation_state(
                    st.session_state.user['id'],
                    st.session_state.selected_language,
                    st.session_state.selected_topic,
                    str(context),
                    st.session_state.chat_history
                )
            
            # Save learning progress
            db.update_learning_progress(
                user_id=st.session_state.user['id'],
                resource_type=st.session_state.selected_topic,
                resource_id=st.session_state.selected_language,
                progress=0.5  # Update this based on actual progress
            )
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error processing request: {str(e)}")

def main():
    initialize_session_state()
    
    # Display sidebar elements
    display_language_selection()
    display_topic_selection()
    
    # Main content
    display_learning_interface()

if __name__ == "__main__":
    main()
