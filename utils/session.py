import streamlit as st
from typing import Optional, Dict, Any

def init_session_state():
    """Initialize session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

def get_current_user() -> Optional[Dict[str, Any]]:
    """Get the current logged-in user from session state"""
    init_session_state()
    return st.session_state.user

def set_current_user(user: Dict[str, Any]):
    """Set the current user in session state"""
    st.session_state.user = user
    st.session_state.authenticated = True

def clear_current_user():
    """Clear the current user from session state"""
    st.session_state.user = None
    st.session_state.authenticated = False

def is_authenticated() -> bool:
    """Check if a user is currently authenticated"""
    init_session_state()
    return st.session_state.authenticated
