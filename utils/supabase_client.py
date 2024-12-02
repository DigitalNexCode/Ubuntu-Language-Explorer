# -*- coding: utf-8 -*-
import os
import socket
from dotenv import load_dotenv
import time
from supabase import Client, create_client
from typing import Optional, Dict, Any, List
import httpx
import streamlit as st
from datetime import datetime

class SupabaseClient:
    _instance: Optional['SupabaseClient'] = None
    _initialized: bool = False
    supabase: Optional[Client] = None
    
    def __new__(cls) -> 'SupabaseClient':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Load environment variables
        load_dotenv()
        
        # Get Supabase credentials
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.development_mode = os.getenv("DEVELOPMENT_MODE", "true").lower() == "true"
        
        # Validate credentials
        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file.\n"
                f"Current values - URL: {self.supabase_url}, KEY: {'[hidden]' if self.supabase_key else 'None'}"
            )
        
        # Initialize with retry logic
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                print(f"\nInitializing Supabase client (attempt {attempt + 1}/{max_retries})...")
                
                # Initialize with timeout settings
                options = {
                    'headers': {
                        'Authorization': f"Bearer {self.supabase_key}",
                        'X-Client-Info': 'ubuntu-language-learning'
                    },
                    'timeout': {
                        'connect': 10,  # connection timeout in seconds
                        'read': 30,     # read timeout in seconds
                        'write': 30,    # write timeout in seconds
                        'pool': 5       # connection pool timeout in seconds
                    },
                    'retries': 3,       # Number of retries for failed requests
                }
                
                # Initialize with custom options
                self.supabase = create_client(
                    supabase_url=self.supabase_url,
                    supabase_key=self.supabase_key,
                    options=options
                )
                
                # Test connection with a simple query
                try:
                    self.supabase.table('app_users').select('id').limit(1).execute()
                    print("[SUCCESS] Supabase client initialized successfully")
                    self._initialized = True
                    break
                except Exception as e:
                    if "relation" in str(e) and "does not exist" in str(e):
                        # This is actually a successful connection, the table just doesn't exist yet
                        print("[SUCCESS] Supabase client initialized successfully (no tables yet)")
                        self._initialized = True
                        break
                    raise
                
            except (httpx.ConnectError, socket.gaierror, socket.timeout) as e:
                print(f"[ERROR] Network error (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("[WARNING] Could not connect to Supabase. Running in offline mode.")
                    self.supabase = None
                    return
                    
            except Exception as e:
                print(f"[ERROR] Failed to initialize Supabase client: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("[WARNING] Could not initialize Supabase client. Running in offline mode.")
                    self.supabase = None
                    return

    def ensure_connection(self) -> bool:
        """Ensure we have a valid Supabase connection."""
        if not self.supabase:
            try:
                self.__init__()
            except Exception as e:
                print(f"[ERROR] Failed to initialize Supabase connection: {str(e)}")
                return False
        
        if not self.supabase:
            return False
            
        # Test the connection with a simple query
        try:
            self.supabase.table('app_users').select('id').limit(1).execute()
            return True
        except Exception as e:
            if "relation" in str(e) and "does not exist" in str(e):
                # This is actually a successful connection, the table just doesn't exist yet
                return True
            print(f"[ERROR] Error in ensure_connection: {str(e)}")
            return False

    def sign_up(self, email: str, password: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Sign up a new user."""
        if not self.ensure_connection():
            return {
                'success': False,
                'error': 'No internet connection. Please check your network and try again.'
            }

        try:
            # Check if email exists
            if self.check_email_exists(email):
                return {
                    'success': False,
                    'error': 'Email already exists'
                }

            # Check if username exists
            if self.check_username_exists(metadata.get('username')):
                return {
                    'success': False,
                    'error': 'Username already exists'
                }

            # Create user with redirect URL
            site_url = "http://localhost:8501"  # Streamlit default port
            
            try:
                response = self.supabase.auth.sign_up({
                    'email': email,
                    'password': password,
                    'options': {
                        'data': metadata,
                        'email_redirect_to': f"{site_url}?confirmation=true"
                    }
                })
            except (httpx.ConnectError, socket.gaierror, socket.timeout) as e:
                return {
                    'success': False,
                    'error': 'Network error. Please check your internet connection and try again.'
                }

            if not response.user:
                return {
                    'success': False,
                    'error': 'Failed to create user'
                }

            # In development mode, auto-confirm email
            if self.development_mode:
                print("Development mode: Auto-confirming email")
                try:
                    self.supabase.auth.admin.update_user(
                        response.user.id,
                        {'email_confirmed': True}
                    )
                except Exception as e:
                    print(f"Warning: Could not auto-confirm email: {str(e)}")

            return {
                'success': True,
                'user': response.user,
                'session': response.session,
                'message': 'User created successfully'
            }

        except Exception as e:
            error_msg = str(e)
            if 'User already registered' in error_msg:
                error_msg = 'Email already registered'
            return {
                'success': False,
                'error': error_msg
            }

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in an existing user."""
        if not self.ensure_connection():
            return {
                'success': False,
                'error': 'No internet connection. Please check your network and try again.'
            }

        try:
            try:
                response = self.supabase.auth.sign_in_with_password({
                    'email': email,
                    'password': password
                })
            except (httpx.ConnectError, socket.gaierror, socket.timeout) as e:
                return {
                    'success': False,
                    'error': 'Network error. Please check your internet connection and try again.'
                }

            if not response.user:
                return {
                    'success': False,
                    'error': 'Invalid credentials'
                }

            print("[SUCCESS] User signed in successfully")
            return {
                'success': True,
                'user': response.user,
                'session': response.session,
                'message': 'Signed in successfully'
            }

        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Sign in failed: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }

    def check_email_exists(self, email: str) -> bool:
        """Check if an email already exists."""
        if not self.ensure_connection():
            print("[WARNING] No connection available for email check")
            return False

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                result = self.supabase.table('app_users').select('email').eq('email', email).execute()
                return len(result.data) > 0
            except Exception as e:
                print(f"[ERROR] Error checking email (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("[WARNING] Could not check email existence")
                    return False

    def check_username_exists(self, username: str) -> bool:
        """Check if a username already exists."""
        if not self.ensure_connection():
            print("[WARNING] No connection available for username check")
            return False

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                result = self.supabase.table('app_users').select('username').eq('username', username).execute()
                return len(result.data) > 0
            except Exception as e:
                print(f"[ERROR] Error checking username (attempt {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("[WARNING] Could not check username existence")
                    return False

    def resend_confirmation_email(self, email: str) -> Dict[str, Any]:
        """Resend confirmation email."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            self.supabase.auth.resend_confirmation_email({
                'email': email
            })
            return {
                'success': True,
                'message': 'Confirmation email sent successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def sign_out(self) -> Dict[str, Any]:
        """Sign out the current user."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            self.supabase.auth.sign_out()
            print("[SUCCESS] User signed out successfully")
            return {
                'success': True,
                'message': 'Signed out successfully'
            }
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Sign out failed: {error_msg}")
            return {
                'success': False,
                'error': error_msg
            }

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user data by ID."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            result = self.supabase.table('app_users').select('*').eq('id', user_id).single().execute()
            return result.data if result else None
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

    def update_user(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user data."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            result = self.supabase.table('app_users').update(data).eq('id', user_id).execute()
            return result.data if result else None
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return None

    def save_translation(self, user_id: str, source_text: str, translated_text: str, source_lang: str, target_lang: str) -> bool:
        """Save translation."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            data = {
                'user_id': user_id,
                'source_text': source_text,
                'translated_text': translated_text,
                'source_lang': source_lang,
                'target_lang': target_lang,
                'created_at': datetime.now().isoformat()
            }
            self.supabase.table('translations').insert(data).execute()
            return True
        except Exception as e:
            print(f"Error saving translation: {e}")
            return False

    def get_user_translations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user translations."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            response = self.supabase.table('translations').select("*").eq('user_id', user_id).order('created_at', desc=True).limit(10).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching translations: {e}")
            return []

    def update_user_stats(self, user_id: str, stats: Dict[str, Any]) -> bool:
        """Update user stats."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            self.supabase.table('user_stats').upsert({
                'user_id': user_id,
                **stats,
                'updated_at': datetime.now().isoformat()
            }).execute()
            return True
        except Exception as e:
            print(f"Error updating user stats: {e}")
            return False

    def list_all_users(self) -> Dict[str, Any]:
        """List all users."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            result = self.supabase.table('app_users').select("*").execute()
            return {
                'app_users': result.data if result else []
            }
        except Exception as e:
            print(f"Error listing users: {e}")
            return {'error': str(e)}

    def clear_all_users(self) -> bool:
        """Clear all users."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            result = self.supabase.table('app_users').delete().execute()
            return True
        except Exception as e:
            print(f"Error clearing users: {e}")
            return False

    def set_session(self, access_token: str, refresh_token: Optional[str] = None) -> Dict[str, Any]:
        """Set the session with provided tokens."""
        if not self.ensure_connection():
            raise ConnectionError("No Supabase connection available")

        try:
            # Set the session in the Supabase client
            session = self.supabase.auth.set_session({
                'access_token': access_token,
                'refresh_token': refresh_token
            })
            
            return {
                'success': True,
                'user': session.user,
                'session': session,
                'message': 'Session set successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
