import bcrypt
from typing import Dict, Any, Optional
import streamlit as st
from .database import db

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def sign_up(email: str, password: str) -> Dict[str, Any]:
    """Sign up a new user"""
    # Hash the password before storing
    password_hash = hash_password(password)
    
    # Create user in database
    result = db.create_user(email, password_hash)
    
    if result['success']:
        # Set session state
        st.session_state['user'] = {
            'id': result['user_id'],
            'email': result['email']
        }
        return {'success': True, 'message': 'Account created successfully!'}
    else:
        return {'success': False, 'error': result.get('error', 'Failed to create account')}

def sign_in(email: str, password: str) -> Dict[str, Any]:
    """Sign in an existing user"""
    user = db.get_user(email)
    
    if not user:
        return {'success': False, 'error': 'Invalid email or password'}
    
    if verify_password(password, user['password_hash']):
        # Set session state
        st.session_state['user'] = {
            'id': user['id'],
            'email': user['email']
        }
        return {'success': True, 'message': 'Signed in successfully!'}
    else:
        return {'success': False, 'error': 'Invalid email or password'}

def sign_out():
    """Sign out the current user"""
    if 'user' in st.session_state:
        del st.session_state['user']

def get_current_user() -> Optional[Dict[str, Any]]:
    """Get the currently signed in user"""
    return st.session_state.get('user')

def require_auth():
    """Require authentication to access a page"""
    if 'user' not in st.session_state:
        st.warning('Please sign in to access this page')
        st.stop()
    return st.session_state['user']
