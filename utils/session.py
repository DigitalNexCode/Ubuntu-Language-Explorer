import streamlit as st
from typing import Optional, Dict, Any
import extra_streamlit_components as stx
import json
from datetime import datetime, timedelta
from utils.database import db

# Cookie configuration
COOKIE_NAME = "ubuntu_language_session"
COOKIE_EXPIRY_DAYS = 30

def get_cookie_manager():
    """Get or create a cookie manager"""
    if 'cookie_manager' not in st.session_state:
        st.session_state.cookie_manager = stx.CookieManager()
    return st.session_state.cookie_manager

def init_session_state():
    """Initialize session state variables and check for existing session"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        
    # Try to restore session from cookie
    if not st.session_state.authenticated:
        restore_session()

def restore_session():
    """Attempt to restore user session from cookie"""
    try:
        cookie_manager = get_cookie_manager()
        session_data = cookie_manager.get(COOKIE_NAME)
        
        if session_data:
            session_info = json.loads(session_data)
            
            # Verify session is not expired
            expiry = datetime.fromisoformat(session_info['expiry'])
            if expiry > datetime.now():
                # Get fresh user data from database
                user = db.get_user_by_id(session_info['user_id'])
                if user:
                    set_current_user(user)
                    return True
            
            # If session is expired or invalid, clear it
            cookie_manager.delete(COOKIE_NAME)
    except Exception as e:
        print(f"Error restoring session: {e}")
    
    return False

def get_current_user() -> Optional[Dict[str, Any]]:
    """Get the current logged-in user from session state"""
    init_session_state()
    return st.session_state.user

def set_current_user(user: Dict[str, Any]):
    """Set the current user in session state and create session cookie"""
    st.session_state.user = user
    st.session_state.authenticated = True
    
    try:
        # Create session data
        session_data = {
            'user_id': user['id'],
            'expiry': (datetime.now() + timedelta(days=COOKIE_EXPIRY_DAYS)).isoformat()
        }
        
        # Save to cookie
        cookie_manager = get_cookie_manager()
        cookie_manager.set(
            COOKIE_NAME,
            json.dumps(session_data),
            expires_at=datetime.now() + timedelta(days=COOKIE_EXPIRY_DAYS)
        )
    except Exception as e:
        print(f"Error setting session cookie: {e}")

def clear_current_user():
    """Clear the current user from session state and remove session cookie"""
    st.session_state.user = None
    st.session_state.authenticated = False
    
    try:
        cookie_manager = get_cookie_manager()
        cookie_manager.delete(COOKIE_NAME)
    except Exception as e:
        print(f"Error clearing session cookie: {e}")

def is_authenticated() -> bool:
    """Check if a user is currently authenticated"""
    init_session_state()
    return st.session_state.authenticated
